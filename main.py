

import pyrebase
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
import cv2
import tempfile
from werkzeug import secure_filename
import numpy as np
app = Flask(__name__)       #Initialze flask constructor

#Add your own details
config = {
  "apiKey": "AIzaSyDWlY7WeyehsAphz7oIIPKfsLRsfIzKyuQ",
  "authDomain": "scalevr-a133b.firebaseapp.com",
  "databaseURL": "https://scalevr-a133b.firebaseio.com",
  "storageBucket": "scalevr-a133b.appspot.com"
}

#initialize firebase
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()
storage = firebase.storage()
#Initialze person as dictionary
person = {"is_logged_in": False, "name": "", "email": "", "uid": ""}

#Login
@app.route("/")
def login():
    return render_template("login.html")

#Sign up/ Register
@app.route("/signup")
def signup():
    return render_template("signup.html")

#Welcome page
@app.route("/welcome")
def welcome():
    if person["is_logged_in"] == True:
        return render_template("welcome.html", email = person["email"], name = person["name"])
    else:
        return redirect(url_for('login'))

#If someone clicks on login, they are redirected to /result
@app.route("/result", methods = ["POST", "GET"])
def result():
    if request.method == "POST":        #Only if data has been posted
        result = request.form           #Get the data
        email = result["email"]
        password = result["pass"]
        try:
            #Try signing in the user with the given information
            user = auth.sign_in_with_email_and_password(email, password)
            #Insert the user data in the global person
            global person
            person["is_logged_in"] = True
            person["email"] = user["email"]
            person["uid"] = user["localId"]
            #Get the name of the user
            data = db.child("users").get()
            person["name"] = data.val()[person["uid"]]["name"]
            p = storage.child("download.jpeg").put("download.jpeg")
            firebase.storage().put("download.jpeg")
            #Redirect to welcome page
            print(p)
            return redirect(url_for('welcome'))
        except:
            #If there is any error, redirect back to login
            return redirect(url_for('login'))
    else:
        if person["is_logged_in"] == True:
            return redirect(url_for('welcome'))
        else:
            return redirect(url_for('login'))

#If someone clicks on register, they are redirected to /register
@app.route("/register", methods = ["POST", "GET"])
def register():
    print(request.method,"drttt")
    if request.method == "POST":        #Only listen to POST
        print("eerrr")
        result = request.form           #Get the data submitted
        email = result["email"]
        password = result["pass"]
        name = result["name"]
        #print(name)
        try:

            #Try creating the user account using the provided data
            auth.create_user_with_email_and_password(email, password)
            #Login the user
            user = auth.sign_in_with_email_and_password(email, password)
            #Add data to global person
            #print("fwfewfwefwf")
            global person
            
          
            person["is_logged_in"] = True
            person["email"] = user["email"]
            person["uid"] = user["localId"]
            person["name"] = name
            #Append data to the firebase realtime database
            data = {"name": name, "email": email}
            #print(data)
            db.child("users").child(person["uid"]).set(data)
            #Go to welcome page
            #print("thedata")
            #img = cv2.imread("download.jpeg")
            #n = np.array(img)
            #data = {"image":n}
           # db.child("pic").set(data1)
            #storage.child("images/example.jpeg").put("download1.jpeg")
            return redirect(url_for('welcome'))
        except:
            #If there is any error, redirect to register
            return redirect(url_for('register'))

    else:
        if person["is_logged_in"] == True:
            return redirect(url_for('welcome'))
        else:
            return redirect(url_for('register'))
@app.route("/upload", methods = ["POST", "GET"])
def upload():
    if request.method == "POST":
        f = request.files['file']
        temp = tempfile.NamedTemporaryFile(delete=False)
        f.save(temp.name)
       # os.remove(temp.name)



if __name__ == "__main__":
    app.run(debug=True)
