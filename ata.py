from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
import sqlite3

app = Flask(__name__)
app.secret_key = 'terbinos_secret_key'

def init_db():
    conn = sqlite3.connect('school.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS attendance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_name TEXT,
                    student_id TEXT,
                    date TEXT,
                    status TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/attendance', methods=['GET', 'POST'])
def attendance():
    if request.method == 'POST':
        student_name = request.form['student_name']
        student_id = request.form['student_id']
        status = request.form['status']
        date = datetime.now().strftime('%Y-%m-%d')

        conn = sqlite3.connect('school.db')
        cur = conn.cursor()
        cur.execute('INSERT INTO attendance (student_name, student_id, date, status) VALUES (?, ?, ?, ?)',
                    (student_name, student_id, date, status))
        conn.commit()
        conn.close()
        flash('Attendance Recorded Successfully!', 'success')
        return redirect(url_for('attendance'))
    
    conn = sqlite3.connect('school.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM attendance')
    attendance_data = cur.fetchall()
    conn.close()
    return render_template('attendance.html', attendance=attendance_data)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
