import tkinter as tk
from tkinter import ttk

class ScrollableFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        # Create a canvas widget and add it to the frame
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0, width=500, height=500)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create a vertical scrollbar and attach it to the canvas
        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y, expand=True)
        self.canvas.config(yscrollcommand=self.scrollbar.set)

        # Create a frame inside the canvas for the widgets to be placed on
        self.inner_frame = tk.Frame(self.canvas)
        self.inner_frame_id = self.canvas.create_window((0, 0), window=self.inner_frame, anchor=tk.NW)

        # Bind events to update the scroll region when the inner frame size changes
        self.inner_frame.bind("<Configure>", self.on_inner_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)

        # Bind the mousewheel event to the canvas
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

        self.frames = []

    def on_inner_frame_configure(self, event):
        # Update the scroll region to match the size of the inner frame
        self.inner_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event):
        # Update the width of the inner frame to match the canvas width
        canvas_width = event.width
        self.canvas.itemconfig(self.inner_frame_id, width=canvas_width)

    def on_mousewheel(self, event):
        # Scroll the canvas up or down depending on the mousewheel direction
        if event.delta < 0:
            self.canvas.yview_scroll(1, "units")
        elif event.delta > 0:
            self.canvas.yview_scroll(-1, "units")

    def add_frame(self, frame):
        # Add a frame to the inner frame container
        self.frames.append(frame)
        frame.pack(in_=self.inner_frame, pady=5, padx=5)

    def delete_frame(self, index):
        self.frames[index].destroy()

    def delete_scrollable_frame(self):
        self.canvas.unbind_all("<MouseWheel>")
        self.pack_forget()

        # Destroy all child widgets of the ScrollableFrame
        for child_widget in self.winfo_children():
            child_widget.destroy()

        # Destroy the ScrollableFrame itself
        self.destroy()