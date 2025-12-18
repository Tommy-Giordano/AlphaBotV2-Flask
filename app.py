import sqlite3
import AlphaBot
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

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

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form.get('forward') == 'w':
            print("wwwwwwwwwwwwwwwwwww")
            act = "w"
        elif  request.form.get('backward') == 's':
            print("ssssssssssssssssssss")
            act = "s"
        elif  request.form.get('left') == 'a':
            print("aaaaaaaaaaaaaaaaaaaa")
            act = "a"
        elif  request.form.get('right') == 'd':
            print("dddddddddddddddddddd")
            act = "d"
        elif  request.form.get('stop') == 'stop':
            print("STOPPPPPPPPPPPP")
            act = "stop"
        else:
            print("Unknown")
    elif request.method == 'GET':
        return render_template('index.html')
    
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

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')