from datetime import datetime
import tkinter as tk
import json

SAVEFILE = "data.json"


class Task:
    """"""

    def __init__(self, title: str, content: str,
                 date: datetime, completed=False):
        """"""
        self.title = title
        self.content = content
        self.date = date
        self.complete = completed

    @classmethod
    def create(cls):
        """
        Interactively creates a new task at the cli.
        """
        title = input("Name of the task : ")
        content = input("Content of the task : ")

        print("Date of the task : ")
        year = int(input("Year : "))
        month = int(input("Month : "))
        day = int(input("Day : "))
        hour = int(input("Hour : "))

        date = datetime(year, month, day, hour)

        return cls(title, content, date)

    def __str__(self):
        return f"{self.title} \n{self.content}\n{self.date}\n{self.complete}"

    def is_identical(self, task):
        """Checks if another task is identical."""
        return self.title == task.title and self.date == task.date

    def __lt__(self, task):
        return self.date < task.date

    def __le__(self, task):
        return self.date <= task.date

    def __eq__(self, task):
        return self.date == task.date

    def __ne__(self, task):
        return self.date != task.date

    def __ge__(self, task):
        return self.date >= task.date

    def __gt__(self, task):
        return self.date > task.date


class ToDoList:
    """List of tasks manipulation."""

    def __init__(self):
        self.list = list()

    def add_task(self, task: Task) -> bool:
        """
        Adds a new unique task to the ToDoList.
        Parameters :
            task : Task object
        Returns:
            bool, identicating success
        """
        for existing_task in self.list:
            if task.is_identical(existing_task):
                return False
        self.list.append(task)
        return True

    def late_tasks(self) -> list:
        """
        Returns list of late tasks.
        A late task is a task where:
            - the date attribute is inferior to the current date
            - the task is not completed
        """
        return [task for task in self.list
                if task.date < datetime.now() and not task.complete]

    def completed_tasks(self) -> list:
        """
        Returns list of completed tasks.
        """
        return [task for task in self.list if task.complete]

    def upcoming_tasks(self) -> list:
        """
        Return list of tatsks:
            - with a datate attribute superior to the current date
            - that are incomplete
        """
        return [task for task in self.list
                if task.date > datetime.now() and not task.complete]

    def store_data(self, filename: str) -> bool:
        """Stores ToDoList in a json file."""
        dump_list = []
        for task in self.list:
            dump_list.append([task.title, task.content, 
                              datetime.strftime(task.date, "%Y-%m-%d %H:%M"),
                              task.complete])
        
        print(json.dumps(dump_list))

        try:
            with open(filename, 'w') as outfile:
                json.dump(dump_list, outfile)
        except:
            return False
        
        return True

    def load_data(self, filename: str) -> bool:
        """Load tasks from a json file."""

        try:
            with open(filename, 'r') as data_file:
                data = json.load(data_file)
        except:
            return False
        
        for raw_task in data:
            
            self.list.append(
                Task(
                 raw_task[0],
                 raw_task[1],
                 datetime.strptime(raw_task[2], "%Y-%m-%d %H:%M"),
                 raw_task[3]
                )
            )

        return True

    @classmethod
    def instance_from_data(cls, filename: str):
        """Creates ToDoList containing tasks from a json file."""
        
        with open(filename, 'r') as data_file:
            data = json.load(data_file)

        task_list = []
        
        for raw_task in data:
            
            task_list.append(
                Task(
                 raw_task[0],
                 raw_task[1],
                 datetime.strptime(raw_task[2], "%Y-%m-%d %H:%M"),
                 raw_task[3]
                )
            )

        todolist = cls()
        todolist.list = task_list

        return todolist
    
    def __str__(self):
        string = ""
        for task in self.list:
            string += str(task) + "\n\n"
        return string


class NewTaskGUI():

    def __init__(self, gui: GUI):
        """Constructor"""
        self.gui = gui

        self.master = tk.Tk()

        self.title_entry = tk.Entry(self.master)

        
class GUI(tk.Label, ToDoList):
    """Graphical interface for the todolist."""

    def __init__(self, filename = None):
        """Constructor."""
        
        self.master = tk.Tk()

        self.text = tk.StringVar()
        self.text.set("ToDoPy !")
        tk.Label.__init__(self, self.master, textvariable=self.text, anchor=tk.NW)
        self.pack(expand=True, fill=tk.BOTH)
        
        ToDoList.__init__(self)
        if filename is not None:
            self.load_data(filename)


        self.menubar = tk.Menu(self.master)

        self.task_menu = tk.Menu(self.menubar, tearoff=0)
        self.task_menu.add_command(label="All", command=self.show_all_tasks)
        self.task_menu.add_command(label="Upcoming", command=self.show_upcoming_tasks)
        self.task_menu.add_command(label="Late", command=self.show_late_tasks)
        self.task_menu.add_command(label="Complete", command=self.show_completed_tasks)
        self.menubar.add_cascade(label="View", menu=self.task_menu)
        
        self.menubar.add_separator()
        def save():
            self.store_data("SAVEFILE")
        self.menubar.add_command(label="Save", command=save)
        
        self.menubar.add_separator()
        self.menubar.add_command(label="Exit", command=self.master.quit)

    
        

        self.master.config(menu=self.menubar)

        self.master.mainloop()
 
    def show_late_tasks(self):
        """"""
        self.show_tasks(self.late_tasks())

    def show_completed_tasks(self):
        """"""
        self.show_tasks(self.completed_tasks())

    def show_upcoming_tasks(self):
        self.show_tasks(self.upcoming_tasks())

    def show_all_tasks(self):
        self.show_tasks(self.list)
        
    def show_tasks(self, task_list):
        text = ""
        for task in task_list:
            text += f"{task.title}\nDate:  {task.date}\n"
            text += "Complete task." if task.complete else "TODO"
            text += f"\n\n{task.content}\n\n\n"
        self.text.set(text)
        
            
    




                                   
                                   
if __name__ == '__main__':
    #task1 = Task.create()
    #task1 = Task("test1", "first task", datetime(1001,1,1))
    #list1 = ToDoList()
    #list1.add_task(task1)
    #task2 = Task("test2", "second task", datetime(2023, 5, 20), True)
    #task3 = Task("test3", "oops ! i forgor", datetime(2020, 1, 1))
    #task4 = Task("test4", "signing test", datetime(2022, 2, 2))
    #list1.add_task(task4)
    #list1.add_task(task2)
    #list1.add_task(task3)
    #print(task4)
    #print(task1)
    #print(list1)
    #print(list1.late_tasks())
    #print(list1.completed_tasks()[0].title)
    #print(list1.upcoming_tasks())
    #print()
    #list1.store_data("data.json")
    #
    #list2 = ToDoList.instance_from_data("data.json")
    #
    #print(list2)


    appli = GUI(SAVEFILE)
 

    
