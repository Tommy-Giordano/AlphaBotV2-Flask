import sqlite3
import AlphaBot
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_login import(
    LoginManager, UserMixin,
    login_user, login_required,
    logout_user, current_user
)
import hashlib

app = Flask(__name__)
app.secret_key = "SKIBIDI67"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

def requestUsersFromDB(dbName):
    con = sqlite3.connect(dbName)

    cur = con.cursor() #oggetto che opera sul db
    #res risultato della query
    res = cur.execute("SELECT * FROM Users") # fa le query
    data = res.fetchall()
    con.close()
    print(data)
    users = {}
    for d in data:
        users[d[1]] = {"password": d[2]} 

    return users


USERS = requestUsersFromDB("robot.db")
print(USERS)
class User(UserMixin):
    def __init__(self, id):
        self.id = id



# USERS = {
#     "admin": {"password": "alphabot"}
# }


@login_manager.user_loader
def load_user(user_id):
    if user_id in USERS:
        return User(user_id)
    return None

@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hashed = hashlib.sha256(password.encode())
        hashed = hashed.hexdigest()

        # print("HARDDDDDDDDDDDDDDDDDDD:" + hashed)
        #query
        if username in USERS and USERS[username]["password"] == hashed:
            login_user(User(username))
            return redirect(url_for("control"))
        
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/control")
@login_required
def control():
    return render_template("control.html")

def requestDB(dbName, act):
    con = sqlite3.connect(dbName)

    cur = con.cursor() #oggetto che opera sul db
    #res risultato della query
    res = cur.execute(f"SELECT move_action FROM moves WHERE move_char = \"{act}\"") # fa le query
    data = res.fetchall()
    con.close()
    print(data)
    return (data[0])[0].split("|")


actions = ["w", "a", "s", "d", "wa", "wd", "sa", "sd", "q", "e", "stop", "r"]

# 

chill = True
ab = None

    
if(chill):
    ab = AlphaBot.ChillBot()
else:
    ab = AlphaBot.AlphaBot()

act = "stop"
state = ""

@app.route("/api/v1/sensors", methods = ['GET'])
def getSensors():
    sensors = {}
    sensors["left"] = ab.getSensors()[0]
    sensors["right"] = ab.getSensors()[1]

    return jsonify(sensors)

@app.route("/api/v1/dbCommand")
def dbCommand():
    data = request.args.get("data")
    print(data)

@app.route("/api/v1/stopMotors")
def stopMotors():
    global state
    act = "stop"
    actt = requestDB("robot.db", act)
    getattr(ab, actt[0])()  
    state = act
    return render_template("control.html")


@app.route("/move")
def move():
    global state
    data = request.args.get("data")
    print("DAAAAAAAAAAAAAAAAAAAAAAAAAAA: " + data)
    act = "stop"
    if data:
        if data == state:
            return render_template("control.html")
        if data in actions:
            print(data + data + data + data + data + data + data + data + data + data + data)
            act = data
        # if data == 'w':
        #     print("wwwwwwwwwwwwwwwwwww")
        #     act = "w"
        # elif data == 's':
        #     print("ssssssssssssssssssss")
        #     act = "s"
        # elif data == 'a':
        #     print("aaaaaaaaaaaaaaaaaaaa")
        #     act = "a"
        # elif data == 'd':
        #     print("dddddddddddddddddddd")
        #     act = "d"
        # elif data == 'stop':
        #     print("STOPPPPPPPPPPPP")
        #     act = "stop"
        else:
            print("Unknown")
    
    nextActions = requestDB("robot.db", act)
    for i in range(0, len(nextActions), 2):
        nact = nextActions[i]
        params = nextActions[i+1]
        if(params == "null"):
            getattr(ab, nact)()  
        else:
            getattr(ab,nact)(float(params))
    state = act
    return render_template("control.html")

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')