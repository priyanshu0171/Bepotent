#import libraries
import numpy as np
from flask import Flask, render_template,request,redirect
import pickle
#Initialize the flask App
app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

@app.route("/")
def home():
    return render_template('index.html')


@app.route("/dashboard")
def dashboard():
    return render_template('dashboard.html')


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/login")
def login():
    return render_template('login.html')


@app.route("/signup")
def signup():
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




if __name__ == "__main__":
    app.run(debug=True)
