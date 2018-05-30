import sqlite3
import re
from flask import Flask, render_template, request

def createquery(executevar):
    with sqlite3.connect('comments.db') as db:
        cursor = db.cursor()
        cursor.execute('''SELECT * FROM sqlite_master''')
        answer = cursor.fetchone()
        if answer == None:
            cursor.execute('''CREATE TABLE comments
                         (comment text)''')
            db.commit()
        elif not 'comments' in answer:
            cursor.execute('''CREATE TABLE comments
                         (comment text)''')
            db.commit()
        cursor.execute(executevar)
        db.commit()
        return cursor

app = Flask(__name__)

@app.route('/')
def main():
    return render_template("main.html")

@app.route('/comments')
def comments():
    arr = []
    for comment in createquery("SELECT comment FROM comments"):
        arr += [comment[0]]
    print(arr)
    arr.sort(key = lambda str: len(set(re.split("; |, |\s", str))), reverse = True)
    print(arr)
    return render_template("comments.html", comments = arr)

@app.route('/create', methods=['POST'])
def save():
    error = None
    if request.method == 'POST':
        createquery("INSERT INTO comments VALUES ('%s')" % request.form["Note"])
        for i in createquery("SELECT comment FROM comments"):
            print(i[0])
        return render_template('main.html', notification = "Note created", error=error)

    else:
        error = 'Another method'
    return render_template('main.html', error=error)