from flask import Flask, send_from_directory, abort, render_template
from predictors import preprocessor 
from dump import dumpData
import threading 

host = "127.0.0.1"
port = 5000

app = Flask(__name__)

app.config["CLIENT_JSON"] = "./predicted files"

@app.route("/")
def home():
    return render_template("weblayout_final.html", host_port=host+":"+str(port))

@app.route("/get-json/<filename>", methods=["POST"])
def get_json(filename):
    try:
        return send_from_directory(app.config["CLIENT_JSON"], filename=filename, as_attachment=True)
    except FileNotFoundError:
        abort(404)

def getApp():
    return app

if __name__ == "__main__":
    dumper = threading.Thread(target=dumpData)
    dumper.start() 
    app.run(host=host, port=port, threaded=True)
    