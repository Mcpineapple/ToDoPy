from datetime import datetime
import json

from ToDoPy.variables import *
 

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

        date = datetime(year, month, day)

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
                              datetime.strftime(task.date, "%y-%m-%d"),
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
                 datetime.strptime(raw_task[2], "%y-%m-%d"),
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
                 datetime.strptime(raw_task[2], "%y-%m-%d"),
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


