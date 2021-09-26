from flask import Flask,redirect,url_for,render_template,request,session
from flask import json


app = Flask(__name__)
app = Flask(__name__)
app.secret_key="MTIS"

from flask_mysqldb import MySQL 
import MySQLdb.cursors 
import re 

app = Flask(__name__) 
  
  
app.secret_key = 'tanya23'
  
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'tanya23'
app.config['MYSQL_DB'] = 'myu'
mysql = MySQL(app)

@app.route("/home",methods=["POST", "GET"])
def home():
    return render_template("home.html")

@app.route("/aboutus",methods=["POST", "GET"])
def aboutus():
    return render_template("aboutus.html")

@app.route("/ourteam", methods=["POST", "GET"])
def ourteam():
    return render_template("ourteam.html")

@app.route("/feedback", methods=["POST", "GET"])
def feedback():
    if request.method=="POST":
        feedname=request.form["fname"]
        feedemail=request.form["feed-email"]
        feedmessage=request.form["message"]
        if feedname=="" or feedemail=="" or feedmessage=="":
            return render_template("feedback.html")
        ##append to a feedback database
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)       
        cursor.execute("INSERT INTO feedback VALUES (%s,%s,%s)", (feedname, feedemail,feedmessage))
        mysql.connection.commit()
        
        return render_template("feedback.html")
    else:
        return render_template("feedback.html")

@app.route("/login", methods=["POST", "GET"])#would contain signup too
def login():
    #print(session)
    if request.method=="POST":
        usertype=request.form["usertype"]
        username=request.form["username"]
        password=request.form["pwd"]

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if usertype=='Musician':
            cursor.execute('SELECT * FROM musician WHERE username = %s', [username])#change table name
        elif usertype=='Non-Musician':
            cursor.execute('SELECT * FROM nonmusician WHERE username = %s', [username])#change table name
            
        result=cursor.fetchone()
        
        if result:
            if password==result['password'] and usertype=='Musician':
                print("confimend mus")
                session["username"]=username
                print("M")
                #print(session)
                return redirect(url_for('musicianprofile'))
            elif password==result['password'] and usertype=='Non-Musician':
                session["username"]=username
                print("NM")
                #print(session)
                return redirect(url_for('nonmusicianprofile'))
            else:
                return render_template("login.html")
        else:
            return render_template("login.html")
        

        
    else:#if nothing is submitted
        return render_template("login.html")
   


    
@app.route("/signupm",methods=["POST","GET"])
def signupm():
    if request.method=="POST":
        name=request.form["name"]
        username=request.form["username"]
        password=request.form["password"]
        dob=request.form["dob"]
        gender=request.form["gender"]
        email=request.form["email"]
        mobile=request.form["mobile"]
        workex=request.form["workex"]
        worklinks=request.form["worklinks"]
        english=request.form.getlist("LangEng")
        hindi=request.form.getlist("LangHindi")
        otherl=request.form.getlist("LangOther")
        vocalist=request.form.getlist("vocalist")
        instru=request.form.getlist("instrumentalist")
        composer=request.form.getlist("composer")
        othert=request.form.getlist("Typeother")
        pop=request.form.getlist("pop")
        rock=request.form.getlist("rock")
        hiphop=request.form.getlist("hiphop")
        jazz=request.form.getlist("jazz")
        otherg=request.form.getlist("Genreother")

        if name=="" or username=="" or password=="" or dob=="" or email=="" or mobile=="":
            return render_template("signupm.html")
        parameters=[english,hindi,otherl,vocalist,instru,composer,othert,pop,rock,hiphop,jazz,otherg]
        temp=[name,username,password,dob,gender,email,mobile,workex,worklinks,english,hindi,otherl,vocalist,instru,composer,othert,pop,rock,hiphop,jazz,otherg]
        for i in range(0,12):
            if parameters[i]==[]:
                parameters[i]='0'
            elif parameters[i]==['1']:
                parameters[i]='1'
            print(parameters[i])
                

            
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)       
        cursor.execute("SELECT * FROM musician where username= %s", [username])
        result=cursor.fetchone()
        if result:
            print("result was positive")                                        
            return render_template("signupm.html")
                
        elif len(password)<5:
            return render_template("signupm.html")
        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("INSERT INTO musician VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (name,username,password,dob,gender,email,mobile,workex,worklinks,parameters[0],parameters[1],parameters[2],parameters[3],parameters[4],parameters[5],parameters[6],parameters[7],parameters[8],parameters[9],parameters[10],parameters[11]))            
            mysql.connection.commit()
            return render_template("login.html")
    else:
        return render_template("signupm.html")
            

        
    

@app.route("/signupnm",methods=["POST","GET"])
def signupnm():
    if request.method=="POST":
        name=request.form["name"]
        username=request.form["username"]
        password=request.form["password"]
        dob=request.form["dob"]
        gender=request.form["gender"]
        email=request.form["email"]
        mobile=request.form["mobile"]
        workex=request.form["workex"]
        worklinks=request.form["worklinks"]
        company=request.form["company"]
  
        if name=="" or username=="" or password=="" or dob=="" or email=="" or mobile=="":
            return render_template("signupnm.html")           
            
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)       
        cursor.execute("SELECT * FROM nonmusician where username= %s", [username])
        result=cursor.fetchone()
        if result:
            print("result was positive")                                        
            return render_template("signupnm.html")
                
        elif len(password)<5:
            return render_template("signupm.html")
        
        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("INSERT INTO nonmusician VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (name,username,password,dob,gender,email,mobile,workex,worklinks,company))            
            mysql.connection.commit()
            return render_template("login.html")
    else:
        return render_template("signupnm.html")


########loginmadness#########


@app.route("/musicianprofile",methods=["POST", "GET"])
def musicianprofile():
   # print(session)
    if "username" in session:
        username=session["username"]
        print("i am in mus profile")
    else:
        return redirect(url_for('login'))
        
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM musician WHERE username = %s', [username])
    result=cursor.fetchone()
    
    fname=result['name']
    fpassword=result['password']
    fdob=result['dob']
    fgender=result['gender']
    femail=result['email']
    fmobile=result['mobile']
    fworkex=result['workex']
    fworklinks=result['worklinks']
    fenglish=result['english']
    fhindi=result['hindi']
    fotherl=result['otherl']
    fvocalist=result['vocalist']
    finstru=result['instru']
    fcomposer=result['composer']
    fothert=result['othert']
    fpop=result['pop']
    frock=result['rock']
    fhiphop=result['hiphop']
    fjazz=result['jazz']
    fotherg=result['otherg']
    parameters=[fenglish,fhindi,fotherl,fvocalist,finstru,fcomposer,fothert,fpop,frock,fhiphop,fjazz,fotherg]
    parametersname=["English","Hindi","Other","Vocalist","Instrumental","Composer","Other","Pop","Rock","Hiphop","Jazz","Other"]
    typel=[]
    langl=[]
    genrel=[]
    for i in range(0,3):
        if parameters[i]=='1':
            typel.append(parametersname[i])
    for i in range(3,7):
        if parameters[i]=='1':
            langl.append(parametersname[i])
    for i in range(7,12):
        if parameters[i]=='1':
            genrel.append(parametersname[i])
    info=[fname,fmobile,femail,fgender,fdob,fworkex,langl,typel,genrel,fworklinks]
    return render_template("musicianprofile.html",username=username,info=json.dumps(info))


@app.route("/nonmusicianprofile",methods=["POST", "GET"])
def nonmusicianprofile():
    if "username" in session:
        username=session["username"]
        
    else:
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM nonmusician WHERE username = %s', [username])
    result=cursor.fetchone()
    
    fname=result['name']
    fpassword=result['password']
    fdob=result['dob']
    fgender=result['gender']
    femail=result['email']
    fmobile=result['mobile']
    fworkex=result['workex']
    fworklinks=result['worklinks']
    fcompany=result['company']
    
    
    info=[fname,fmobile,femail,fgender,fdob,fworkex,fcompany]
    return render_template("nonmusicianprofile.html",username=username,info=json.dumps(info))

@app.route("/searchm",methods=["POST", "GET"])
def searchm():
    if "username" in session:
        username=session["username"]
    else:
        return redirect(url_for('login'))
    
    if request.method=="POST":

        english=request.form.getlist("LangEng")
        hindi=request.form.getlist("LangHindi")
        otherl=request.form.getlist("LangOther")
        vocalist=request.form.getlist("vocalist")
        instru=request.form.getlist("instrumentalist")
        composer=request.form.getlist("composer")
        othert=request.form.getlist("Typeother")
        pop=request.form.getlist("pop")
        rock=request.form.getlist("rock")
        hiphop=request.form.getlist("hiphop")
        jazz=request.form.getlist("jazz")
        otherg=request.form.getlist("Genreother")

        paraofsearch=[english,hindi,otherl,vocalist,instru,composer,othert,pop,rock,hiphop,jazz,otherg]
        print("para of search=",paraofsearch)
        for i in range(0,12):
            if paraofsearch[i]==[]:
                paraofsearch[i]='0'
            elif paraofsearch[i]==['1']:
                paraofsearch[i]='1'
        print("para of search=",paraofsearch)
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)       
        cursor.execute("SELECT * FROM musician")
        result=cursor.fetchall()
        toshow=[]
        for profile in result:
            print("result=",result)
            fname=profile['name']
            fusername=profile['username']
            fdob=profile['dob']
            fgender=profile['gender']
            femail=profile['email']
            fmobile=profile['mobile']
            fworkex=profile['workex']
            fworklinks=profile['worklinks']
            fenglish=profile['english']
            fhindi=profile['hindi']
            fotherl=profile['otherl']
            fvocalist=profile['vocalist']
            finstru=profile['instru']
            fcomposer=profile['composer']
            fothert=profile['othert']
            fpop=profile['pop']
            frock=profile['rock']
            fhiphop=profile['hiphop']
            fjazz=profile['jazz']
            fotherg=profile['otherg']
            
            parameters=[fenglish,fhindi,fotherl,fvocalist,finstru,fcomposer,fothert,fpop,frock,fhiphop,fjazz,fotherg]
            print("parameters=",parameters)
            parametersname=["English","Hindi","Other","Vocalist","Instrumental","Composer","Other","Pop","Rock","Hiphop","Jazz","Other"]
            match=0
            print()
            for i in range(12):
                if paraofsearch[i]==parameters[i]:
                    match+=1
            match=match/12
            match=match*100

            print("match=",match)
            
            typel=[]
            langl=[]
            genrel=[]
            for i in range(0,3):
                if parameters[i]=='1':
                    typel.append(parametersname[i])
            for i in range(3,7):
                if parameters[i]=='1':
                    langl.append(parametersname[i])
            for i in range(7,12):
                if parameters[i]=='1':
                    genrel.append(parametersname[i])

            print("typel=",typel)
            print("langl=",langl)
            print("genrel=",genrel)
            
            temp=[match,fname,fusername,fdob,fgender,femail,fmobile,fworkex,fworklinks,typel,langl,genrel]
            print("temp=",temp)
            toshow.append(temp)
            print("toshowinloop=",toshow)
            
        #bubble sort to show in decending with o in toshow wrt o[0]
        print()
        for i in range(len(toshow)): 
            min_idx = i 
            for j in range(i+1, len(toshow)): 
                if toshow[min_idx][0] > toshow[j][0]: 
                    min_idx = j   
            toshow[i], toshow[min_idx] = toshow[min_idx], toshow[i]
        print("toshowoutloop=",toshow)
        toshow.reverse()#for decending order
        print("toshowoutloop=",toshow)


        return render_template("searchm.html",toshow=json.dumps(toshow))
            
        
    else:
        return render_template("searchm.html",toshow="")

    

@app.route("/lookforajob",methods=["POST", "GET"])
def lookforajob():
    if "username" in session:
        username=session["username"]
        return render_template("lookforajob.html")
    else:
        return redirect(url_for('login'))


@app.route("/searchnm",methods=["POST", "GET"])
def searchnm():
    if "username" in session:
        username=session["username"]
        return render_template("searchnm.html")
    else:
        return redirect(url_for('login'))



@app.route("/editm",methods=["POST","GET"])
def editm():
    if "username" in session:
        username=session["username"]
    else:
        return redirect(url_for('login'))
    

##
##      ##############get all the particulars from username and database
##    fname=request.form["name"]
##    #username=request.form["username"]
##    fpassword=request.form["password"]
##    fdob=request.form["dob"]
##    fgender=request.form["gender"]
##    femail=request.form["email"]
##    fmobile=request.form["mobile"]
##    fworkex=request.form["workex"]
##    fworklinks=request.form["worklinks"]
##    fenglish=request.form.getlist("LangEng")
##    fhindi=request.form.getlist("LangHindi")
##    fotherl=request.form.getlist("LangOther")
##    fvocalist=request.form.getlist("vocalist")
##    finstru=request.form.getlist("instrumentalist")
##    fcomposer=request.form.getlist("composer")
##    fthert=request.form.getlist("Typeother")
##    fpop=request.form.getlist("pop")
##    frock=request.form.getlist("rock")
##    fhiphop=request.form.getlist("hiphop")
##    fjazz=request.form.getlist("jazz")
##    fotherg=request.form.getlist("Genreother")

    if request.method=="POST":
        dob=request.form["dob"]
        gender=request.form["gender"]
        email=request.form["email"]
        mobile=request.form["mobile"]
        workex=request.form["workex"]
        worklinks=request.form["worklinks"]
        english=request.form.getlist("LangEng")
        hindi=request.form.getlist("LangHindi")
        otherl=request.form.getlist("LangOther")
        vocalist=request.form.getlist("vocalist")
        instru=request.form.getlist("instrumentalist")
        composer=request.form.getlist("composer")
        othert=request.form.getlist("Typeother")
        pop=request.form.getlist("pop")
        rock=request.form.getlist("rock")
        hiphop=request.form.getlist("hiphop")
        jazz=request.form.getlist("jazz")
        otherg=request.form.getlist("Genreother")



        parameters=[english,hindi,otherl,vocalist,instru,composer,othert,pop,rock,hiphop,jazz,otherg]
        temp=[dob,gender,email,mobile,workex,worklinks,parameters[0],parameters[1],parameters[2],parameters[3],parameters[4],parameters[5],parameters[6],parameters[7],parameters[8],parameters[9],parameters[10],parameters[11]]
        #temp=[dob,gender,email,mobile,workex,worklinks,english,hindi,otherl,vocalist,instru,composer,othert,pop,rock,hiphop,jazz,otherg]
        for i in range(0,12):
            if parameters[i]==[]:
                parameters[i]='0'
            elif parameters[i]==['1']:
                parameters[i]='1'
            print(parameters[i])

        print("jcccccccccccccccccccccccccccccd")
        for i in range(0,18):
            print(temp[i])


                 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if dob:
            cursor.execute("update musician set dob=%s where username=%s",(dob,username))
            print("dob")
        if gender:
            cursor.execute("update musician set gender=%s where username=%s",(gender,username))
            print("gender")
        if email:
            cursor.execute("update musician set email=%s where username=%s",(email,username))
            print("email")
        if mobile:
            cursor.execute("update musician set mobile=%s where username=%s",(mobile,username))
            print("mobile")
        if workex:
            cursor.execute("update musician set workex=%s where username=%s",(workex,username))
            print("workex")
        if worklinks:
            cursor.execute("update musician set worklinks=%s where username=%s",(worklinks,username))
            print("worklinks")
        
        cursor.execute("update musician set english=%s where username=%s",(parameters[0],username))
        cursor.execute("update musician set hindi=%s where username=%s",(parameters[1],username))
        cursor.execute("update musician set otherl=%s where username=%s",(parameters[2],username))
        cursor.execute("update musician set vocalist=%s where username=%s",(parameters[3],username))
        cursor.execute("update musician set instru=%s where username=%s",(parameters[4],username))
        cursor.execute("update musician set composer=%s where username=%s",(parameters[5],username))
        cursor.execute("update musician set othert=%s where username=%s",(parameters[6],username))
        cursor.execute("update musician set pop=%s where username=%s",(parameters[7],username))
        cursor.execute("update musician set rock=%s where username=%s",(parameters[8],username))
        cursor.execute("update musician set hiphop=%s where username=%s",(parameters[9],username))
        cursor.execute("update musician set jazz=%s where username=%s",(parameters[10],username))
        cursor.execute("update musician set otherg=%s where username=%s",(parameters[11],username))
        
        mysql.connection.commit()
        return render_template("editm.html")
        
    else:
        #return render_template("editm.html",username=username,fdob=fdob,fgender=fgender........)
        return render_template("editm.html")
    


@app.route("/editnm",methods=["POST","GET"])
def editnm():
    if "username" in session:
        username=session["username"]
    else:
        return redirect(url_for('login'))
    
##      ##############get all the particulars from username and database
##        fdob=request.form["dob"]
##        fgender=request.form["gender"]
##        femail=request.form["email"]
##        fmobile=request.form["mobile"]
##        fworkex=request.form["workex"]
##        fworklinks=request.form["worklinks"]
##        fcompany=request.form["company"]

    if request.method=="POST":
        dob=request.form["dob"]
        gender=request.form["gender"]
        email=request.form["email"]
        mobile=request.form["mobile"]
        workex=request.form["workex"]
        worklinks=request.form["worklinks"]
        company=request.form["company"]
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if dob:
            cursor.execute("update nonmusician set dob=%s where username=%s",(dob,username))
            print("dob")
        if gender:
            cursor.execute("update nonmusician set gender=%s where username=%s",(gender,username))
            print("gender")
        if email:
            cursor.execute("update nonmusician set email=%s where username=%s",(email,username))
            print("email")
        if mobile:
            cursor.execute("update nonmusician set mobile=%s where username=%s",(mobile,username))
            print("mobile")
        if workex:
            cursor.execute("update nonmusician set workex=%s where username=%s",(workex,username))
            print("workex")
        if worklinks:
            cursor.execute("update nonmusician set worklinks=%s where username=%s",(worklinks,username))
            print("worklinks")
        if company:
            cursor.execute("update nonmusician set company=%s where username=%s",(worklinks,username))
            print("worklinks")
        
        mysql.connection.commit()
        return render_template("editnm.html")
        
    else:
        #return render_template("editnm.html",username=username,fdob=fdob,fgender=fgender........)
        return render_template("editnm.html")

    

@app.route("/logout",methods=["POST", "GET"])
def logout():
    session.pop("username",None)
    return redirect(url_for('login'))




if __name__=="__main__":
    app.run()
