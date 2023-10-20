import tkinter as tk
from tkinter import messagebox, filedialog
import json
import datetime

class TaskManager:
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = self.load_tasks()

    def add_task(self, task, due_date, priority=1, category="General"):
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        if due_date < current_date:
            messagebox.showerror("Error", "Due date cannot be before the current date.")
            return

        new_task = {
            "task": task,
            "due_date": due_date,
            "completed": False,
            "priority": priority,
            "category": category,
        }
        self.tasks.append(new_task)
        self.save_tasks()

    def load_tasks(self):
        try:
            with open(self.filename, "r") as file:
                tasks = json.load(file)
            return tasks
        except FileNotFoundError:
            return []

    def save_tasks(self):
        with open(self.filename, "w") as file:
            json.dump(self.tasks, file)

    def complete_task(self, task_index):
        if 0 <= task_index < len(self.tasks):
            self.tasks[task_index]["completed"] = True
            self.save_tasks()
        else:
            messagebox.showerror("Error", "Invalid task index.")

    def get_incomplete_tasks(self):
        return [(index, task) for index, task in enumerate(self.tasks) if not task["completed"]]

    def show_tasks(self, category=None, show_completed=False):
        filtered_tasks = self.tasks

        if category:
            filtered_tasks = [task for task in filtered_tasks if task["category"] == category]

        if not show_completed:
            filtered_tasks = [task for task in filtered_tasks if not task["completed"]]

        if not filtered_tasks:
            return "No tasks found."
        else:
            task_list = "\n".join(
                f"{index + 1}. {task['task']} (Due: {task['due_date']}, Priority: {task['priority']}, Category: {task['category']}) - {'Completed' if task['completed'] else 'Not Completed'}"
                for index, task in enumerate(filtered_tasks)
            )
            return task_list

# GUI
class ToDoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("To-Do App")
        self.geometry("800x600")

        self.task_manager = TaskManager()

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="To-Do App", font=("Arial", 24, "bold")).pack(pady=10)

        # Add Task Frame
        add_task_frame = tk.Frame(self)
        add_task_frame.pack(pady=10)

        tk.Label(add_task_frame, text="Task Description:", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
        task_entry = tk.Entry(add_task_frame, font=("Arial", 12))
        task_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(add_task_frame, text="Due Date (YYYY-MM-DD):", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5)
        due_date_entry = tk.Entry(add_task_frame, font=("Arial", 12))
        due_date_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(add_task_frame, text="Priority (1-5):", font=("Arial", 12)).grid(row=2, column=0, padx=5, pady=5)
        priority_entry = tk.Entry(add_task_frame, font=("Arial", 12))
        priority_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(add_task_frame, text="Category:", font=("Arial", 12)).grid(row=3, column=0, padx=5, pady=5)
        category_entry = tk.Entry(add_task_frame, font=("Arial", 12))
        category_entry.grid(row=3, column=1, padx=5, pady=5)

        add_button = tk.Button(
            add_task_frame,
            text="Add Task",
            command=lambda: self.handle_add_task(
                task_entry.get(),
                due_date_entry.get(),
                priority_entry.get(),
                category_entry.get(),
            ),
            font=("Arial", 12, "bold"),
        )
        add_button.grid(row=4, columnspan=2, pady=10)

        # Task List Frame
        task_list_frame = tk.Frame(self)
        task_list_frame.pack(pady=10)

        self.task_display = tk.Text(task_list_frame, height=20, width=70, font=("Arial", 12))
        self.task_display.grid(row=0, column=0, padx=10, pady=10)

        # Complete Task Frame
        complete_task_frame = tk.Frame(self)
        complete_task_frame.pack(pady=10)

        complete_button = tk.Button(
            complete_task_frame,
            text="Complete Task",
            command=self.complete_task,
            font=("Arial", 12, "bold"),
        )
        complete_button.pack(pady=5)

        # Save Tasks Frame
        save_tasks_frame = tk.Frame(self)
        save_tasks_frame.pack(pady=10)

        save_button = tk.Button(
            save_tasks_frame,
            text="Save Tasks",
            command=self.save_tasks,
            font=("Arial", 12, "bold"),
        )
        save_button.pack(pady=5)

    def handle_add_task(self, task, due_date, priority, category):
        try:
            priority = int(priority)
        except ValueError:
            messagebox.showerror("Error", "Priority must be an integer.")
            return

        self.task_manager.add_task(task, due_date, priority, category)
        self.update_ui()

    def complete_task(self):
        incomplete_tasks = self.task_manager.get_incomplete_tasks()

        if not incomplete_tasks:
            messagebox.showinfo("Info", "No incomplete tasks to complete.")
            return

        complete_task_window = tk.Toplevel(self)
        complete_task_window.title("Complete Task")

        tk.Label(complete_task_window, text="Select a task to complete:", font=("Arial", 12)).pack(pady=5)

        for index, task in incomplete_tasks:
            tk.Button(
                complete_task_window,
                text=task['task'],
                command=lambda i=index: self.handle_complete_task(i, complete_task_window),
                font=("Arial", 12),
            ).pack()

    def handle_complete_task(self, task_index, window):
        self.task_manager.complete_task(task_index)
        window.destroy()
        self.update_ui()

    def save_tasks(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if file_path:
            self.task_manager.filename = file_path
            self.task_manager.save_tasks()
            messagebox.showinfo("Success", "Tasks saved successfully.")

    def update_ui(self):
        tasks = self.task_manager.show_tasks()
        self.task_display.config(state=tk.NORMAL)
        self.task_display.delete(1.0, tk.END)
        self.task_display.insert(tk.END, tasks)
        self.task_display.config(state=tk.DISABLED)

if __name__ == "__main__":
    app = ToDoApp()
    app.mainloop()
