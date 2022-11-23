import tkinter as tk
from tkcalendar import DateEntry
from datetime import datetime

from ToDoPy.logic import Task, ToDoList
from ToDoPy.variables import *


class NewTaskGUI():

    def __init__(self, gui):
        """Constructor"""
        self.gui = gui

        self.master = tk.Tk()
        self.master.geometry(TASK_GEOMETRY)

        self.title_entry = tk.Entry(self.master)
        self.date_entry = DateEntry(self.master)
        self.content_entry = tk.Text(self.master, height=6, width=45)
        self.confirm_button = tk.Button(self.master, text="Confirm", command=self.confirm)


        
        self.title_entry.pack()
        self.date_entry.pack()
        self.content_entry.pack()
        self.confirm_button.pack()

        self.master.mainloop()

    def confirm(self):
        """Function run when confirm button is pressed. Fetches information to create task, then destroys window."""
        title = self.title_entry.get()
        date = self.date_entry.get()
        date = datetime.strptime(date, "%m/%d/%y")
        content = self.content_entry.get(1.0, tk.END)
        complete = False


        task = Task(title, content, date, complete)
        self.gui.add_task(task)
        self.master.destroy()
        
        
        
class GUI(tk.Label, ToDoList):
    """Graphical interface for the todolist."""

    def __init__(self, filename = None):
        """Constructor."""
        
        self.master = tk.Tk()

        self.master.geometry(GUI_GEOMETRY)

        self.text = tk.StringVar()
        self.text.set("ToDoPy !")
        tk.Label.__init__(self, self.master, textvariable=self.text, anchor=tk.NW)
        self.pack(expand=True, fill=tk.BOTH)
        
        ToDoList.__init__(self)
        if filename is not None:
            self.load_data(filename)


        self.menubar = tk.Menu(self.master)

        def new_task():
           NewTaskGUI(self)
        self.menubar.add_command(label="New", command=new_task)
        
        self.menubar.add_separator()
        self.task_menu = tk.Menu(self.menubar, tearoff=0)
        self.task_menu.add_command(label="All", command=self.show_all_tasks)
        self.task_menu.add_command(label="Upcoming", command=self.show_upcoming_tasks)
        self.task_menu.add_command(label="Late", command=self.show_late_tasks)
        self.task_menu.add_command(label="Complete", command=self.show_completed_tasks)
        self.menubar.add_cascade(label="View", menu=self.task_menu)
        
        self.menubar.add_separator()
        def save():
            self.store_data(SAVEFILE)
        self.menubar.add_command(label="Save", command=save)
        
        self.menubar.add_separator()
        self.menubar.add_command(label="Exit", command=self.master.quit)
 

        self.master.config(menu=self.menubar)

        self.master.mainloop()
        

        
    def show_late_tasks(self):
        """Lists late tasks using ToDoList methods."""
        self.show_tasks(self.late_tasks())

    def show_completed_tasks(self):
        """Lists completed tasks using ToDoList methods."""
        self.show_tasks(self.completed_tasks())

    def show_upcoming_tasks(self):
        """Lists upcoming tasks using ToDoList methods."""
        self.show_tasks(self.upcoming_tasks())

    def show_all_tasks(self):
        """Shows all tasks using ToDoList methods"""
        self.show_tasks(self.list)
        
    def show_tasks(self, task_list):
        """Takes a list of tasks and shows them in the GUI"""
        text = ""
        for task in task_list:
            text += f"{task.title}\nDate:  {task.date}\n"
            text += "Complete task." if task.complete else "TODO"
            text += f"\n\n{task.content}\n\n\n"
        self.text.set(text)
        
