from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="db",
    user=open("/run/secrets/db_user").read().strip(),
    password=open("/run/secrets/db_password").read().strip(),
    database="notesdb"
)

cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS notes (id INT AUTO_INCREMENT PRIMARY KEY, note TEXT)")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        note = request.form['note']
        cursor.execute("INSERT INTO notes (note) VALUES (%s)", (note,))
        db.commit()
        return redirect('/')
    cursor.execute("SELECT * FROM notes")
    notes = cursor.fetchall()
    return render_template('index.html', notes=notes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
