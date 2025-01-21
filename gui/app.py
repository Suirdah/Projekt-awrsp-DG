import json
import tkinter as tk
from contextlib import nullcontext
from tkinter import messagebox
from tkcalendar import Calendar


class PersonalPlannerApp:
    DATA = 'tasks.json'

    def __init__(self, root):
        self.root = root
        self.root.title('Personal Planner')
        self.root.geometry('900x850')

        header = tk.Label(root, text='Planner Personalny', font=('Arial', 16))
        header.pack(pady=10)

        form_frame = tk.Frame(root)
        form_frame.pack(pady=10)

        self.task_entry = tk.Entry(form_frame, width=40, font=('Arial', 14))
        self.task_entry.grid(row=0, column=0, padx=5)

        self.calendar = Calendar(form_frame, selectmode='day', date_pattern='dd-mm-yyyy')
        self.calendar.grid(row=0, column=1, padx=5)

        add_task_button = tk.Button(form_frame, text='Dodaj zadanie', command=self.add_task, font=('Arial', 12))
        add_task_button.grid(row=0, column=2, padx=5)

        self.task_listbox = tk.Listbox(root, width=80, height=15, font=('Arial', 12))
        self.task_listbox.pack(pady=10)

        self.tasks = []
        self.load_tasks()

        frame = tk.Frame(root)
        frame.pack(pady=10)

        edit_button = tk.Button(frame, text='Edytuj', command=self.edit_task, font=('Arial', 12))
        edit_button.grid(row=0, column=0, padx=5)

        delete_button = tk.Button(frame, text='Usuń', command=self.delete_task, font=('Arial', 12))
        delete_button.grid(row=0, column=1)

        filter_frame = tk.Frame(root)
        filter_frame.pack(pady=10)

        filter_label = tk.Label(filter_frame, text='Filtruj według daty:', font=('Arial', 12))
        filter_label.grid(row=0, column=0, padx=5)

        self.filter_calendar = Calendar(filter_frame, selectmode='day', date_pattern='dd-mm-yyyy')
        self.filter_calendar.grid(row=0, column=1, padx=5)

        filter_button = tk.Button(filter_frame, text='Filtruj', command=self.filter_tasks, font=('Arial', 12))
        filter_button.grid(row=0, column=2, padx=5)

        self.update_listbox()

    def add_task(self):
        task = self.task_entry.get().strip()
        date = self.calendar.get_date()
        if task:
            self.tasks.append({'task': task, 'date': date})
            self.update_listbox()
            self.task_entry.delete(0, tk.END)
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
            self.task_listbox.insert(tk.END, f'{task['task']} (Data: {task['date']})')

    def filter_tasks(self):
        select_task = self.filter_calendar.get_date()
        for task in self.tasks:
            if task['date'] == select_task:
                self.task_listbox.insert(tk.END, f'{task['task']} (Data: {task['date']})')
