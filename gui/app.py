import json
import tkinter as tk
from collections import Counter
from tkinter import messagebox
from tkcalendar import Calendar
import matplotlib.pyplot as plt


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
        delete_button.grid(row=0, column=1, padx=5)

        chart_button = tk.Button(frame, text='Wykres', command=self.chart, font=('Arial', 12))
        chart_button.grid(row=0, column=2, padx=5)

        filter_frame = tk.Frame(root)
        filter_frame.pack(pady=10)

        filter_label = tk.Label(filter_frame, text='Filtruj według daty:', font=('Arial', 12))
        filter_label.grid(row=0, column=0, padx=5)

        self.filter_calendar = Calendar(filter_frame, selectmode='day', date_pattern='dd-mm-yyyy')
        self.filter_calendar.grid(row=0, column=1, padx=5)

        filter_button = tk.Button(filter_frame, text='Filtruj', command=self.filter_tasks, font=('Arial', 12))
        filter_button.grid(row=0, column=2, padx=5)

        show_button = tk.Button(filter_frame, text='Pokaż listę', command=self.update_listbox, font=('Arial', 12))
        show_button.grid(row=0, column=3, padx=5)

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
        if hasattr(self, 'edit_window') and self.edit_window.winfo_exists():
            messagebox.showinfo('Edycja', 'Okno edycji jest już otwarte')
            return

        try:
            select_index = self.task_listbox.curselection()[0]
            current_task = self.tasks[select_index]

            self.edit_window = tk.Toplevel(self.root)
            self.edit_window.title('Edytuj zadanie')
            self.edit_window.geometry('400x350')

            task_label = tk.Label(self.edit_window, text='Treść zadania:', font=('Arial', 12))
            task_label.pack(pady=5)
            task_entry = tk.Entry(self.edit_window, width=40, font=('Arial', 12))
            task_entry.pack(pady=5)
            task_entry.insert(0, current_task['task'])

            date_label = tk.Label(self.edit_window, text='Data zadania:', font=('Arial', 12))
            date_label.pack(pady=5)
            calendar = Calendar(self.edit_window, selectmode='day', date_pattern='dd-mm-yyyy')
            calendar.pack(pady=5)
            calendar.selection_set(current_task['date'])

            def save_edit():
                new_task = task_entry.get().strip()
                new_date = calendar.get_date()
                if new_task:
                    self.tasks[select_index] = {'task': new_task, 'date': new_date}
                    self.update_listbox()
                    self.save_tasks()
                    self.edit_window.destroy()
                else:
                    messagebox.showwarning('Błąd', 'Nie można zapisac pustego zadania')

            save_button = tk.Button(self.edit_window, text='Zapisz', command=save_edit, font=('Arial', 12))
            save_button.pack(pady=10)

        except IndexError:
            messagebox.showwarning('Błąd', 'Nie wybrano żadnego zadania do edycji')

    def delete_task(self):
        try:
            select_index = self.task_listbox.curselection()[0]

            self.tasks.pop(select_index)
            self.task_listbox.delete(select_index)
            self.save_tasks()
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
        self.tasks.sort(key=lambda task: task['date'])

        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            self.task_listbox.insert(tk.END, f'{task['task']} (Data: {task['date']})')

    def filter_tasks(self):
        select_task = self.filter_calendar.get_date()
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            if task['date'] == select_task:
                self.task_listbox.insert(tk.END, f'{task['task']} (Data: {task['date']})')

    def chart(self):
        if not self.tasks:
            messagebox.showinfo('Statystyki', 'Brak danyhc do wyświetlenia')
            return
        task_count = Counter(task['date'] for task in self.tasks)

        date = list(task_count.keys())
        number = list(task_count.values())

        plt.figure(figsize=(10, 5))
        plt.bar(date, number)
        plt.title('Liczba zadań w podizale na daty')
        plt.xlabel('Data')
        plt.ylabel('Liczba zadań')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
