#import libraries
import numpy as np
from flask import Flask, render_template,request,redirect, url_for,request,make_response
import pickle
import pymongo
import bcrypt
import time
#Initialize the flask App
app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

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
    if 'email' in request.cookies:
        email = request.cookies.get("email") 
        rec_mail = records.find_one({"email": email})       # fetching Data
    return render_template('dashboard.html', details=rec_mail)


@app.route("/about")
def about():
    return render_template('about.html')



@app.route("/form",methods=['post', 'get'])
def form():
    if 'email' in request.cookies:
        if request.method == "POST":
            sl=request.form.get("sl")
            height=request.form.get("height")
            weight=request.form.get("weight")
            age=request.form.get("age")
            slList= [{"sl":sl}]
            input={"height":height,"weight":weight,"age":age,"slList":slList}
            email = request.cookies.get('email')
            records.update( {"email":email},{"$set":input},upsert=True)
           
        else:
            return render_template('index.html')        
        return render_template('vitals_form.html')
    



@app.route("/login", methods=["POST", "GET"])
def login():

    message = ''
   
    if 'email' in request.cookies:
        message = "logged in"
        # print("Jai ho")
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
                if 'email' in request.cookies:
                    # time.sleep(2)
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

    if 'email' in request.cookies:
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
            # user_found = records.find_one({"name": user})
            email_found = records.find_one({"email": email})
            # if user_found:
            #     message = 'There already is a user by that name'
            #     return render_template('signup.html', message=message)
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


@app.route("/predict-diabetes", methods=["GET","POST"])
def predictor():
    return render_template('predictor.html')

@app.route("/predict", methods=["POST"])
def predict():
# HTML for GUI rendering
   # For rendering results on HTML GUI
    prg = request.form['prg']
    glc = request.form['glc']
    bp = request.form['bp']
    skt = request.form['skt']
    ins = request.form['ins']
    bmi = request.form['bmi']
    dpf = request.form['ped']
    age = request.form['age']

    prg = int(prg)
    glc = int(glc)
    bp = int(bp)
    skt = int(skt)
    ins = int(ins)
    bmi = float(bmi)
    dpf = float(dpf)
    age = int(age)
#   int_features = [int(x) for x in request.form.values()]
    final_features = np.array([(prg, glc, bp, skt, ins, bmi, dpf, age)])
    sc=pickle.load(open('scaler.sav','rb'))
    final_features=sc.transform(final_features)

    prediction = model.predict(final_features)

    if prediction == 1:
        text = 'have diabetes'
    else:
        text = 'does not have diabetes'
    text = f'The patient {text}'
    print(prediction)
    print(text)
    return render_template("predictor.html", prediction_text = text, prediction=prediction)

@app.route('/logout')
def logout():
   resp = make_response(redirect(url_for("dashboard")))  
   resp.set_cookie('email','', expires=0) 
   return resp


if __name__ == "__main__":
    app.run(debug=True)
