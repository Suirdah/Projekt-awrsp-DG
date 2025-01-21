import tkinter as tk
from contextlib import nullcontext
from tkinter import messagebox


class PersonalPlannerApp:
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
        self.task_listbox.insert(1, 'aaa')

        self.tasks = []

    def add_task(self):
        task = self.task_entry.get().strip()
        if task:
            self.tasks.append(task)
            self.task_listbox.insert(1, task)
            self.task_entry.delete(0,100)
        else:
            messagebox.showwarning('Błąd', 'Nie można dodać pustego zadania')


root = tk.Tk()
app = PersonalPlannerApp(root)
root.mainloop()
