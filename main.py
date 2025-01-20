import tkinter as tk

root= tk.Tk()
root.title('Personal Planner')
root.geometry('800x500')

label = tk.Label(root, text="test test test", font=('Arial',16))
label.pack(pady=20)
root.mainloop()