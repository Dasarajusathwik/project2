import tkinter as tk
from tkinter import messagebox, simpledialog

class Task:
    def __init__(self, description, category=None, priority=None):
        self.description = description
        self.completed = False
        self.category = category
        self.priority = priority

    def mark_complete(self):
        self.completed = True

    def edit(self, description=None, category=None, priority=None):
        if description is not None:
            self.description = description
        if category is not None:
            self.category = category
        if priority is not None:
            self.priority = priority

    def __str__(self):
        status = "✓" if self.completed else " "
        cat = f"[{self.category}]" if self.category else ""
        prio = f"(Priority: {self.priority})" if self.priority else ""
        return f"[{status}] {self.description} {cat} {prio}".strip()

class ToDoList:
    def __init__(self):
        self.tasks = []

    def add_task(self, description, category=None, priority=None):
        task = Task(description, category, priority)
        self.tasks.append(task)

    def delete_task(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]

    def mark_task_complete(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index].mark_complete()

    def edit_task(self, index, description=None, category=None, priority=None):
        if 0 <= index < len(self.tasks):
            self.tasks[index].edit(description, category, priority)

class ToDoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("To-Do List - Touch Interface")
        self.geometry("400x600")
        self.todo_list = ToDoList()
        self.selected_index = None

        self.create_widgets()
        self.refresh_task_list()

    def create_widgets(self):
        self.task_listbox = tk.Listbox(self, height=15, width=40, font=("Arial", 14))
        self.task_listbox.pack(pady=10)
        self.task_listbox.bind('<<ListboxSelect>>', self.on_task_select)

        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        # Buttons arranged like a calculator keypad
        buttons = [
            ("Add", self.add_task),
            ("Edit", self.edit_task),
            ("Delete", self.delete_task),
            ("Complete", self.mark_complete),
            ("Up", self.move_up),
            ("Down", self.move_down),
            ("Clear Selection", self.clear_selection),
            ("Exit", self.exit_app)
        ]

        rows = 4
        cols = 2
        for i, (text, cmd) in enumerate(buttons):
            btn = tk.Button(button_frame, text=text, command=cmd, width=15, height=3, font=("Arial", 14))
            btn.grid(row=i // cols, column=i % cols, padx=5, pady=5)

    def refresh_task_list(self):
        self.task_listbox.delete(0, tk.END)
        for i, task in enumerate(self.todo_list.tasks):
            self.task_listbox.insert(tk.END, f"{i+1}. {task}")

    def on_task_select(self, event):
        try:
            self.selected_index = self.task_listbox.curselection()[0]
        except IndexError:
            self.selected_index = None

    def add_task(self):
        description = simpledialog.askstring("Add Task", "Enter task description:")
        if description:
            category = simpledialog.askstring("Add Task", "Enter category (optional):")
            priority = simpledialog.askstring("Add Task", "Enter priority (optional):")
            self.todo_list.add_task(description, category, priority)
            self.refresh_task_list()

    def edit_task(self):
        if self.selected_index is None:
            messagebox.showwarning("Edit Task", "Please select a task to edit.")
            return

        task = self.todo_list.tasks[self.selected_index]
        description = simpledialog.askstring("Edit Task", "Enter new description:", initialvalue=task.description)
        if description is None:
            description = task.description
        category = simpledialog.askstring("Edit Task", "Enter new category (optional):", initialvalue=task.category)
        if category == "":
            category = None
        priority = simpledialog.askstring("Edit Task", "Enter new priority (optional):", initialvalue=task.priority)
        if priority == "":
            priority = None

        self.todo_list.edit_task(self.selected_index, description, category, priority)
        self.refresh_task_list()

    def delete_task(self):
        if self.selected_index is None:
            messagebox.showwarning("Delete Task", "Please select a task to delete.")
            return

        self.todo_list.delete_task(self.selected_index)
        self.selected_index = None
        self.refresh_task_list()

    def mark_complete(self):
        if self.selected_index is None:
            messagebox.showwarning("Mark Complete", "Please select a task to mark as complete.")
            return

        self.todo_list.mark_task_complete(self.selected_index)
        self.refresh_task_list()

    def move_up(self):
        if self.selected_index is None or self.selected_index == 0:
            return
        self.todo_list.tasks[self.selected_index], self.todo_list.tasks[self.selected_index - 1] = \
            self.todo_list.tasks[self.selected_index - 1], self.todo_list.tasks[self.selected_index]
        self.selected_index -= 1
        self.refresh_task_list()
        self.task_listbox.select_set(self.selected_index)

    def move_down(self):
        if self.selected_index is None or self.selected_index == len(self.todo_list.tasks) - 1:
            return
        self.todo_list.tasks[self.selected_index], self.todo_list.tasks[self.selected_index + 1] = \
            self.todo_list.tasks[self.selected_index + 1], self.todo_list.tasks[self.selected_index]
        self.selected_index += 1
        self.refresh_task_list()
        self.task_listbox.select_set(self.selected_index)

    def clear_selection(self):
        self.task_listbox.selection_clear(0, tk.END)
        self.selected_index = None

    def exit_app(self):
        self.destroy()

if __name__ == "__main__":
    app = ToDoApp()
    app.mainloop()
