import sqlite3
import pandas as pd
import tkinter as tk
from tkinter import messagebox, ttk, filedialog


conn = sqlite3.connect('events.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS registrations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student TEXT,
    event TEXT
)''')
conn.commit()


EVENTS = ["Hackathon", "Workshop", "Seminar", "Tech Talk"]


def register():
    student = entry_name.get()
    event = event_var.get()
    if student and event:
        c.execute("INSERT INTO registrations (student, event) VALUES (?, ?)", (student, event))
        conn.commit()
        messagebox.showinfo("Success", f"{student} registered for {event}")
        entry_name.delete(0, tk.END)
        event_dropdown.set(EVENTS[0])
    else:
        messagebox.showwarning("Input Error", "Both fields are required!")

def show_summary():
    df = pd.read_sql_query("SELECT * FROM registrations", conn)
    summary = df['event'].value_counts().to_string()
    messagebox.showinfo("Event Summary", summary)


def show_all_registrations():
    df = pd.read_sql_query("SELECT * FROM registrations", conn)

    top = tk.Toplevel(root)
    top.title("All Registrations")
    top.geometry("400x300")

    tree = ttk.Treeview(top, columns=("ID", "Name", "Event"), show='headings')
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Student Name")
    tree.heading("Event", text="Event")

    for _, row in df.iterrows():
        tree.insert("", tk.END, values=(row["id"], row["student"], row["event"]))

    tree.pack(expand=True, fill="both")


def export_to_excel():
    df = pd.read_sql_query("SELECT * FROM registrations", conn)
    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])
    if file_path:
        df.to_excel(file_path, index=False)
        messagebox.showinfo("Exported", f"Data exported to {file_path}")

root = tk.Tk()
root.title("Event Registration System")
root.geometry("400x350")

tk.Label(root, text="Student Name:", font=("Arial", 12)).pack(pady=5)
entry_name = tk.Entry(root, width=30)
entry_name.pack()

tk.Label(root, text="Select Event:", font=("Arial", 12)).pack(pady=5)
event_var = tk.StringVar(value=EVENTS[0])
event_dropdown = ttk.Combobox(root, textvariable=event_var, values=EVENTS, state="readonly", width=28)
event_dropdown.pack()

tk.Button(root, text="Register", command=register, bg="green", fg="white", width=25).pack(pady=10)
tk.Button(root, text="Show Summary", command=show_summary, bg="blue", fg="white", width=25).pack(pady=5)
tk.Button(root, text="View All Registrations", command=show_all_registrations, bg="orange", fg="black", width=25).pack(pady=5)
tk.Button(root, text="Export to Excel", command=export_to_excel, bg="purple", fg="white", width=25).pack(pady=10)

root.mainloop()


