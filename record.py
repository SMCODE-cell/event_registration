import sqlite3
import pandas as pd

conn = sqlite3.connect('events.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS registrations (
    id INTEGER PRIMARY KEY,
    student TEXT,
    event TEXT
)''')

def register(student, event):
    c.execute("INSERT INTO registrations (student, event) VALUES (?, ?)", (student, event))
    conn.commit()

def event_summary():
    df = pd.read_sql_query("SELECT * FROM registrations", conn)
    print(df['event'].value_counts())


register("Aman", "Hackathon")
register("Priya", "Hackathon")
register("Ravi", "Workshop")
event_summary()
