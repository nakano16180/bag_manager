from flask import Flask, render_template
import os, sys


app = Flask(__name__)

def file_list():
    path = "../data/"
    dirs_key ={}
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        files[:] = [f for f in files if not f.startswith('.')]
        dirs_key[root] = files
    return dirs_key

@app.route("/data")
def data():
    dic = file_list()
    return render_template("data.html", message=dic)

if __name__ == '__main__':
    app.run()
