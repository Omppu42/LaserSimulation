import tkinter as tk

from config.stats import stats


class UnsavedChangesDialog:
    def __init__(self, text: str, sidebar):
        self.top = tk.Tk()
        self.top.title("Unsaved Changes")
        self.top.geometry("300x150")
        self.top.resizable(False, False)

        self.top.protocol("WM_DELETE_WINDOW", self.on_x)
        
        self.sidebar = sidebar
        
        message_label = tk.Label(self.top, text=text, font=("Arial", 14))
        message_label.pack(pady=10)

        save_button = tk.Button(self.top, text="Save", command=self.save_changes, width=10)
        save_button.place(relx=0.3, rely=0.8, anchor=tk.CENTER)
        discard_button = tk.Button(self.top, text="Don't Save", command=self.discard_changes, width=10)
        discard_button.place(relx=0.7, rely=0.8, anchor=tk.CENTER)

        self.top.mainloop()

    def save_changes(self):
        self.top.destroy()

        if stats.current_scene == "Empty":
            self.sidebar.exporter.export_data(no_button_text="Don't Save")
        else:
            self.sidebar.exporter.export_no_gui(stats.current_scene)


    def discard_changes(self):
        self.top.destroy()

    def on_x(self):
        pass