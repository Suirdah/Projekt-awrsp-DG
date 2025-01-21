import json
import tkinter as tk
from tkinter import messagebox


class PersonalPlannerApp:
    DATA = 'tasks.json'

    def __init__(self, root):
        self.root = root
        self.root.title('Personal Planner')
        self.root.geometry('800x500')

        header = tk.Label(root, text='Planner Personalny', font=('Arial', 16))
        header.pack(pady=10)

        self.task_entry = tk.Entry(root, width=50, font=('System', 14))
        self.task_entry.pack(pady=10)
        add_task_button = tk.Button(root, text='Dodaj zadanie', command=self.add_task, font=('Arial', 12))
        add_task_button.pack(pady=5)

        self.task_listbox = tk.Listbox(root, width=50, height=15, font=('Arial', 12))
        self.task_listbox.pack(pady=10)

        self.tasks = []
        self.load_tasks()

        frame = tk.Frame(root)
        frame.pack(pady=10)

        edit_button = tk.Button(frame, text='Edytuj', command=self.edit_task, font=('Arial', 12))
        edit_button.grid(row=0, column=0, padx=5)

        delete_button = tk.Button(frame, text='Usuń', command=self.delete_task, font=('Arial', 12))
        delete_button.grid(row=0, column=1)

        self.update_listbox()
    def add_task(self):
        task = self.task_entry.get().strip()
        if task:
            self.tasks.append(task)
            self.task_listbox.insert(tk.END, task)
            self.task_entry.delete(0,tk.END)
            self.save_tasks()
        else:
            messagebox.showwarning('Błąd', 'Nie można dodać pustego zadania')

    def edit_task(self):
        try:
            select_index = self.task_listbox.curselection()[0]
            current_task = self.tasks[select_index]

            self.task_entry.delete(0, tk.END)
            self.task_entry.insert(0, current_task)
        except IndexError:
            messagebox.showwarning('Błąd', 'Nie wybrano żadnego zadania do edycji')

    def delete_task(self):
        try:
            select_index = self.task_listbox.curselection()[0]

            self.task_listbox.delete(select_index)
        except IndexError:
            messagebox.showwarning('Błąd', 'Nie wybrano żadnego zadania do edycji')

    def save_tasks(self):
        try:
            with open(self.DATA, 'w') as file:
                json.dump(self.tasks, file)
        except Exception:
            messagebox.showwarning('Błąd', 'Nie udało sie zapisać danych')

    def load_tasks(self):
        try:
            with open(self.DATA, 'r') as file:
                self.tasks = json.load(file)
        except Exception:
            messagebox.showwarning('Błąd', 'Nie udało sie odczytać danych')

    def update_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            self.task_listbox.insert(tk.END, task)
