import tkinter as tk
from contextlib import nullcontext

class PersonalPlannerApp:
    def __init__(self,root):
        self.root = root
        self.root.title('Personal Planner')
        self.root.geometry('800x500')

        header=tk.Label(root, text='Planner Personalny', font=('Arial',16))
        header.pack(pady=10)

        task_entry=tk.Entry(root, width=50, font=('System',14))
        task_entry.pack(pady=10)
        add_task_button=tk.Button(root, text='Dodaj zadanie', command=nullcontext, font=('Arial',12))
        add_task_button.pack()




root = tk.Tk()
app = PersonalPlannerApp(root)
root.mainloop()