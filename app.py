from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="productivity_dashboard"
    )

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM study_sessions ORDER BY study_date DESC")
    sessions = cursor.fetchall()

    cursor.execute("SELECT IFNULL(SUM(study_hours), 0) AS total_hours FROM study_sessions")
    total_hours = cursor.fetchone()['total_hours']

    cursor.execute("""
        SELECT subject, SUM(study_hours) AS total
        FROM study_sessions
        GROUP BY subject
        ORDER BY total DESC
    """)
    subject_data = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'index.html',
        sessions=sessions,
        total_hours=total_hours,
        subject_data=subject_data
    )

@app.route('/add', methods=['POST'])
def add_session():
    subject = request.form['subject']
    study_hours = request.form['study_hours']
    study_date = request.form['study_date']
    notes = request.form['notes']

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO study_sessions (subject, study_hours, study_date, notes) VALUES (%s, %s, %s, %s)",
        (subject, study_hours, study_date, notes)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)