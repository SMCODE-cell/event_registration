import sqlite3
import pandas as pd
import tkinter as tk
from tkinter import messagebox


conn = sqlite3.connect('events.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS registrations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student TEXT,
    event TEXT
)''')
conn.commit()


def register():
    student = entry_name.get()
    event = entry_event.get()
    if student and event:
        c.execute("INSERT INTO registrations (student, event) VALUES (?, ?)", (student, event))
        conn.commit()
        messagebox.showinfo("Success", f"{student} registered for {event}")
        entry_name.delete(0, tk.END)
        entry_event.delete(0, tk.END)
    else:
        messagebox.showwarning("Input Error", "Both fields are required!")

def show_summary():
    df = pd.read_sql_query("SELECT * FROM registrations", conn)
    summary = df['event'].value_counts().to_string()
    messagebox.showinfo("Event Summary", summary)


root = tk.Tk()
root.title("Event Registration System")
root.geometry("350x250")

tk.Label(root, text="Student Name:", font=("Arial", 12)).pack(pady=5)
entry_name = tk.Entry(root, width=30)
entry_name.pack()

tk.Label(root, text="Event Name:", font=("Arial", 12)).pack(pady=5)
entry_event = tk.Entry(root, width=30)
entry_event.pack()

tk.Button(root, text="Register", command=register, bg="green", fg="white", width=20).pack(pady=10)
tk.Button(root, text="Show Summary", command=show_summary, bg="blue", fg="white", width=20).pack(pady=5)

root.mainloop()
