from datetime import datetime


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
    def create(self):
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

        return self(title, content, date)

    def __str__(self):
        return f"{self.title} \n{self.content}\n{self.date}"

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
    """"""

    def __init__(self):
        self.list = list()

    def add_task(self, task: Task) -> None:
        """Adds a new task to the ToDoList."""
        self.list.append(task)

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
        Return list of tasks:
            - with a date attribute superior to the current date
            - that are incomplete
        """
        return [task for task in self.list
                if task.date > datetime.now() and not task.complete]

    def __str__(self):
        string = ""
        for task in self.list:
            string += str(task) + "\n\n"
        return string


#task1 = Task.create()
task1 = Task("test1", "first task", datetime(1,1,1))
list1 = ToDoList()
list1.add_task(task1)
task2 = Task("test2", "second task", datetime.now(), True)
task3 = Task("test3", "oops ! i forgor", datetime(2020, 1, 1))
list1.add_task(task2)
list1.add_task(task3)
print(task1)
print(list1)
print(list1.late_tasks())
print(list1.completed_tasks())
print(list1.upcoming_tasks())
