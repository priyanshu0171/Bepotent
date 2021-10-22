#import libraries
from flask import Flask, render_template,request,redirect, url_for,request,make_response
import requests
import pymongo
import bcrypt
import datetime
#Initialize the flask App
app = Flask(__name__)


app.secret_key = "testing"
client = pymongo.MongoClient("mongodb+srv://Bepotent:12345@cluster0.f8pdb.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.get_database('User')
records = db.register


@app.route("/")
def home():
    if 'email' in request.cookies:
        message = "logged in"
        return redirect(url_for("dashboard"))
    else:
        return render_template("index.html")



@app.route("/dashboard")
def dashboard():
    if 'email' in request.cookies and 'email' != '':
        email = request.cookies.get("email") 
        rec_mail = records.find_one({"email": email})       # fetching Data
        # current Year
        curryear = datetime.datetime.now().strftime("%Y")
        return render_template('dashboard.html', details=rec_mail, year=curryear)
    else:
        return redirect(url_for('home'))


@app.route("/about")
def about():
    return render_template('about.html')



@app.route("/form",methods=['post', 'get'])
def form():
    if 'email' in request.cookies and 'email' != '':
        if request.method == "POST":
            sl=request.form.get("sl")
            height=request.form.get("height")
            weight=request.form.get("weight")
            age=request.form.get("age")
            slList= [{"sl":sl}]
            input={"height":height,"weight":weight,"age":age,"slList":slList}
            email = request.cookies.get('email')
            records.update( {"email":email},{"$set":input},upsert=True)
           
        return render_template('vitals_form.html')
    else:
        return render_template('index.html')        
    



@app.route("/login", methods=["POST", "GET"])
def login():

    message = ''
   
    if 'email' in request.cookies and 'email' != '':
        message = "logged in"
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

       
        email_found = records.find_one({"email": email})
        if email_found:
            email_val = email_found['email']
            passwordcheck = email_found['password']
            
            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                resp = make_response(redirect(url_for("dashboard")))  
                resp.set_cookie('email',email_val, max_age=90 * 60 * 60 * 24) 
                return resp
            else:
                if 'email' in request.cookies and 'email' != '':
                    message = "logged in"
                    return redirect(url_for("dashboard"))
                     
                message = 'Wrong password'
                return render_template('login.html', message=message)
        else:
            message = 'Email not found'
            return render_template('login.html', message=message)
    return render_template('login.html', message=message)
    

@app.route("/signup", methods=['post', 'get'])
def signup():

    message = ''

    if 'email' in request.cookies and 'email' != '':
        return redirect(url_for("home"))
    if request.method == "POST":
        user = request.form.get("name")
        email = request.form.get("email")
        
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        if user=="" and email=="" and password1=="" and password2=="":
            message = 'All feilds required'
            return render_template('signup.html', message=message)
        else:

            email_found = records.find_one({"email": email})

            if  email_found:
                message = 'This email already exists'
                return render_template('signup.html', message=message)
            elif  password1 != password2:
                message = 'Passwords should match!'
                return render_template('signup.html', message=message)
            else:
                hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())
                user_input = {'name': user, 'email': email, 'password': hashed}
                records.insert_one(user_input)
                
                user_data = records.find_one({"email": email})
                new_email = user_data['email']
            
                return render_template('login.html', email=new_email)
    return render_template('signup.html')


@app.route('/excercise')
def excercise():
    if 'email' in request.cookies and 'email' != '':
        return redirect(url_for("home"))
    else:
        return redirect(url_for("dashboard"))
        
@app.route('/dietchart')
def dietchart():
    if 'email' in request.cookies and 'email' != '':
        return redirect(url_for("home"))
    else:
        return redirect(url_for("dashboard"))

@app.route('/reports')
def reports():
    if 'email' in request.cookies and 'email' != '':
        return redirect(url_for("home"))
    else:
        return redirect(url_for("dashboard"))

@app.route('/logout')
def logout():
   resp = make_response(redirect(url_for("dashboard")))  
   resp.set_cookie('email','', expires=0) 
   return resp




if __name__ == "__main__":
    app.run(debug=True)
