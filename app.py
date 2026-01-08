import sqlite3
import AlphaBot
from flask import Flask, render_template, request, jsonify
from flask_login import(
    LoginManager, UserMixin,
    login_user, login_required,
    logout_user, current_uesr
)

app = Flask(__name__)
app.secret_key = "SKIBIDI67"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

def requestDB(dbName, act):
    con = sqlite3.connect(dbName)

    cur = con.cursor() #oggetto che opera sul db
    #res risultato della query
    res = cur.execute(f"SELECT move_action FROM moves WHERE move_char = \"{act}\"") # fa le query
    data = res.fetchall()
    con.close()
    print(data)
    return (data[0])[0].split("|")


actions = ["w", "a", "s", "d", "q", "e", "stop", "r"]

ab = AlphaBot.AlphaBot()
act = "stop"

@app.route("/api/v1/sensors", methods = ['GET'])
def getSensors():
    sensors = {}
    sensors["left"] = ab.getSensors()[0]
    sensors["right"] = ab.getSensors()[1]

    return jsonify(sensors)

@app.route("/api/v1/stopMotors")
def stopMotors():
    act = "stop"
    actt = requestDB("robot.db", act)
    getattr(ab, actt[0])()  
    # state = act
    return render_template("index.html")


@app.route("/move")
def move():
    data = request.args.get("data")
    print("DAAAAAAAAAAAAAAAAAAAAAAAAAAA: " + data)
    act = "stop"
    if(data):
        if data == 'w':
            print("wwwwwwwwwwwwwwwwwww")
            act = "w"
        elif data == 's':
            print("ssssssssssssssssssss")
            act = "s"
        elif data == 'a':
            print("aaaaaaaaaaaaaaaaaaaa")
            act = "a"
        elif data == 'd':
            print("dddddddddddddddddddd")
            act = "d"
        elif data == 'stop':
            print("STOPPPPPPPPPPPP")
            act = "stop"
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
    # state = act
    return render_template("index.html")

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')