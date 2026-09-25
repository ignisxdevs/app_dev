import json
import os
import tkinter as tk
from tkinter import messagebox, ttk

# Name of the file where our planner data gets saved
DATA_FILE = "planner_data.json"


# ---------------- DATA STORAGE HELPERS ---------------- #
def load_data():
    """Loads saved data from file, or creates empty structure if file doesn't exist."""
    default_data = {
        "tasks": [],
        "deadlines": [],
        "ideas": "",
        "schedule": {
            "09:00 AM": "",
            "11:00 AM": "",
            "02:00 PM": "",
            "04:00 PM": "",
            "07:00 PM": "",
        },
    }
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return default_data
    return default_data


def save_data(data):
    """Saves the current data dictionary to our JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


# ---------------- MAIN APPLICATION ---------------- #
class StudentPlannerApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Student Workspace & Planner")
        self.root.geometry("820x620")
        self.root.configure(bg="#f4f6f9")

        # Load existing data
        self.data = load_data()

        # Header Title
        title_frame = tk.Frame(root, bg="#1e293b", pady=15)
        title_frame.pack(fill="x")
        title_label = tk.Label(
            title_frame,
            text="🎓 B.Tech Study & Task Hub",
            font=("Helvetica", 18, "bold"),
            fg="#ffffff",
            bg="#1e293b",
        )
        title_label.pack()

        # Setup Tabs using ttk.Notebook
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "TNotebook.Tab",
            font=("Helvetica", 11, "bold"),
            padding=[15, 6],
            background="#cbd5e1",
        )
        style.map("TNotebook.Tab", background=[("selected", "#3b82f6")])

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=15)

        # Tab Frames
        self.task_tab = tk.Frame(self.notebook, bg="#ffffff")
        self.deadline_tab = tk.Frame(self.notebook, bg="#ffffff")
        self.idea_tab = tk.Frame(self.notebook, bg="#ffffff")
        self.routine_tab = tk.Frame(self.notebook, bg="#ffffff")

        self.notebook.add(self.task_tab, text="📝 Tasks & To-Dos")
        self.notebook.add(self.deadline_tab, text="⏳ Deadlines")
        self.notebook.add(self.idea_tab, text="💡 Project Ideas")
        self.notebook.add(self.routine_tab, text="📅 Daily Timetable")

        # Build each tab screen
        self.build_task_tab()
        self.build_deadline_tab()
        self.build_idea_tab()
        self.build_routine_tab()

    # ================= 1. TASKS TAB ================= #
    def build_task_tab(self):
        input_frame = tk.Frame(self.task_tab, bg="#ffffff", pady=10)
        input_frame.pack(fill="x", padx=15)

        tk.Label(
            input_frame,
            text="New Task:",
            font=("Helvetica", 11),
            bg="#ffffff",
        ).pack(side="left", padx=5)
        self.task_entry = tk.Entry(
            input_frame, font=("Helvetica", 11), width=40
        )
        self.task_entry.pack(side="left", padx=5)

        add_btn = tk.Button(
            input_frame,
            text="+ Add Task",
            bg="#22c55e",
            fg="white",
            font=("Helvetica", 10, "bold"),
            command=self.add_task,
        )
        add_btn.pack(side="left", padx=5)

        # Task Listbox
        self.task_listbox = tk.Listbox(
            self.task_tab, font=("Helvetica", 12), height=14, selectmode=tk.SINGLE
        )
        self.task_listbox.pack(fill="both", expand=True, padx=15, pady=5)

        # Populate tasks
        for task in self.data["tasks"]:
            self.task_listbox.insert(tk.END, task)

        btn_bar = tk.Frame(self.task_tab, bg="#ffffff", pady=10)
        btn_bar.pack(fill="x", padx=15)

        tk.Button(
            btn_bar,
            text="✓ Mark Completed",
            bg="#3b82f6",
            fg="white",
            font=("Helvetica", 10, "bold"),
            command=self.complete_task,
        ).pack(side="left", padx=5)
        tk.Button(
            btn_bar,
            text="✕ Delete Task",
            bg="#ef4444",
            fg="white",
            font=("Helvetica", 10, "bold"),
            command=self.delete_task,
        ).pack(side="left", padx=5)

    def add_task(self):
        task_text = self.task_entry.get().strip()
        if task_text:
            self.task_listbox.insert(tk.END, f"[ ] {task_text}")
            self.data["tasks"].append(f"[ ] {task_text}")
            save_data(self.data)
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Task cannot be empty!")

    def complete_task(self):
        selected = self.task_listbox.curselection()
        if selected:
            idx = selected[0]
            current_text = self.task_listbox.get(idx)
            if current_text.startswith("[ ]"):
                updated = current_text.replace("[ ]", "[✔ DONE]", 1)
                self.task_listbox.delete(idx)
                self.task_listbox.insert(idx, updated)
                self.data["tasks"][idx] = updated
                save_data(self.data)

    def delete_task(self):
        selected = self.task_listbox.curselection()
        if selected:
            idx = selected[0]
            self.task_listbox.delete(idx)
            del self.data["tasks"][idx]
            save_data(self.data)

    # ================= 2. DEADLINES TAB ================= #
    def build_deadline_tab(self):
        input_frame = tk.Frame(self.deadline_tab, bg="#ffffff", pady=10)
        input_frame.pack(fill="x", padx=15)

        tk.Label(
            input_frame,
            text="Subject/Event:",
            font=("Helvetica", 10),
            bg="#ffffff",
        ).grid(row=0, column=0, padx=5, pady=5)
        self.sub_entry = tk.Entry(input_frame, font=("Helvetica", 10), width=18)
        self.sub_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(
            input_frame,
            text="Date (DD/MM/YYYY):",
            font=("Helvetica", 10),
            bg="#ffffff",
        ).grid(row=0, column=2, padx=5, pady=5)
        self.date_entry = tk.Entry(
            input_frame, font=("Helvetica", 10), width=15
        )
        self.date_entry.grid(row=0, column=3, padx=5, pady=5)

        add_dl_btn = tk.Button(
            input_frame,
            text="+ Add Deadline",
            bg="#f59e0b",
            fg="white",
            font=("Helvetica", 10, "bold"),
            command=self.add_deadline,
        )
        add_dl_btn.grid(row=0, column=4, padx=10, pady=5)

        # Table for deadlines
        columns = ("Subject", "Due Date")
        self.dl_tree = ttk.Treeview(
            self.deadline_tab, columns=columns, show="headings", height=12
        )
        self.dl_tree.heading("Subject", text="Subject / Work")
        self.dl_tree.heading("Due Date", text="Due Date")
        self.dl_tree.column("Subject", width=450)
        self.dl_tree.column("Due Date", width=250)
        self.dl_tree.pack(fill="both", expand=True, padx=15, pady=5)

        for dl in self.data["deadlines"]:
            self.dl_tree.insert("", tk.END, values=(dl["subject"], dl["date"]))

        btn_bar = tk.Frame(self.deadline_tab, bg="#ffffff", pady=10)
        btn_bar.pack(fill="x", padx=15)
        tk.Button(
            btn_bar,
            text="✕ Remove Selected Deadline",
            bg="#ef4444",
            fg="white",
            font=("Helvetica", 10, "bold"),
            command=self.delete_deadline,
        ).pack(side="left")

    def add_deadline(self):
        sub = self.sub_entry.get().strip()
        dt = self.date_entry.get().strip()
        if sub and dt:
            self.dl_tree.insert("", tk.END, values=(sub, dt))
            self.data["deadlines"].append({"subject": sub, "date": dt})
            save_data(self.data)
            self.sub_entry.delete(0, tk.END)
            self.date_entry.delete(0, tk.END)
        else:
            messagebox.showwarning(
                "Input Missing", "Please provide both Subject and Date."
            )

    def delete_deadline(self):
        selected_item = self.dl_tree.selection()
        if selected_item:
            item_data = self.dl_tree.item(selected_item[0])["values"]
            self.dl_tree.delete(selected_item[0])
            self.data["deadlines"] = [
                d
                for d in self.data["deadlines"]
                if not (d["subject"] == item_data[0] and d["date"] == item_data[1])
            ]
            save_data(self.data)

    # ================= 3. IDEAS TAB ================= #
    def build_idea_tab(self):
        tk.Label(
            self.idea_tab,
            text="Brainstorming Pad (Mini-Projects, Hackathons, Notes):",
            font=("Helvetica", 11, "bold"),
            bg="#ffffff",
        ).pack(anchor="w", padx=15, pady=(10, 5))

        self.idea_text = tk.Text(
            self.idea_tab,
            font=("Helvetica", 11),
            wrap="word",
            bg="#fefce8",
            padx=10,
            pady=10,
        )
        self.idea_text.pack(fill="both", expand=True, padx=15, pady=5)
        self.idea_text.insert("1.0", self.data.get("ideas", ""))

        save_idea_btn = tk.Button(
            self.idea_tab,
            text="💾 Save Notes / Ideas",
            bg="#3b82f6",
            fg="white",
            font=("Helvetica", 10, "bold"),
            command=self.save_ideas,
        )
        save_idea_btn.pack(anchor="e", padx=15, pady=10)

    def save_ideas(self):
        text_content = self.idea_text.get("1.0", tk.END).strip()
        self.data["ideas"] = text_content
        save_data(self.data)
        messagebox.showinfo("Saved", "Ideas saved successfully!")

    # ================= 4. ROUTINE / TIMETABLE TAB ================= #
    def build_routine_tab(self):
        tk.Label(
            self.routine_tab,
            text="Daily Routine & Study Slots:",
            font=("Helvetica", 11, "bold"),
            bg="#ffffff",
        ).pack(anchor="w", padx=15, pady=(10, 5))

        self.routine_entries = {}
        slots_frame = tk.Frame(self.routine_tab, bg="#ffffff")
        slots_frame.pack(fill="both", expand=True, padx=15, pady=5)

        for i, (slot, desc) in enumerate(self.data.get("schedule", {}).items()):
            tk.Label(
                slots_frame,
                text=slot,
                font=("Helvetica", 10, "bold"),
                width=12,
                anchor="w",
                bg="#ffffff",
            ).grid(row=i, column=0, padx=5, pady=8)
            e = tk.Entry(slots_frame, font=("Helvetica", 10), width=65)
            e.insert(0, desc)
            e.grid(row=i, column=1, padx=5, pady=8)
            self.routine_entries[slot] = e

        save_sched_btn = tk.Button(
            self.routine_tab,
            text="💾 Update Schedule",
            bg="#10b981",
            fg="white",
            font=("Helvetica", 10, "bold"),
            command=self.save_routine,
        )
        save_sched_btn.pack(anchor="e", padx=15, pady=10)

    def save_routine(self):
        for slot, entry in self.routine_entries.items():
            self.data["schedule"][slot] = entry.get().strip()
        save_data(self.data)
        messagebox.showinfo("Success", "Schedule updated!")


# ---------------- RUN APPLICATION ---------------- #
if __name__ == "__main__":
    root = tk.Tk()
    app = StudentPlannerApp(root)
    root.mainloop()