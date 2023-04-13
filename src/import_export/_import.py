import os, json, datetime
import tkinter as tk
from tkinter import ttk
import pygame
pygame.init()

from functools import partial
from PIL import ImageTk, Image

from config.settings import settings
from config.stats import stats
from obstacles.obstacle_manager import obstacle_manager
from obstacles.square import SquareObstacle
from obstacles.circle import CircleObstacle

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
        frame.pack(in_=self.inner_frame, pady=5, padx=5)



class Importer():
    SELECTION_W = 500
    SELECTION_H = 500
    
    def __init__(self) -> None:
        pass

    def import_data(self) -> None:
        self.window = tk.Tk()
        self.window.geometry("600x600")
        self.window.title("Import")

        self.selection_frame_f = tk.Frame(self.window, width=Importer.SELECTION_W, height=Importer.SELECTION_H, bg="gray10")
        self.selection_frame_f.pack()

        self.selection_frame = ScrollableFrame(self.selection_frame_f, width=Importer.SELECTION_W, height=Importer.SELECTION_H)
        self.selection_frame.pack()

        self.cancel_button = tk.Button(text="Cancel", command=self.cancel, font=22, width=15, height=2, bg="gray99")
        self.cancel_button.place(relx=0.35, rely=0.95, anchor=tk.CENTER)

        self.confirm_button = tk.Button(text="Confirm", command=self.confirm, font=22, width=15, height=2, bg="gray99")
        self.confirm_button.place(relx=0.65, rely=0.95, anchor=tk.CENTER)

        self.window.resizable(False, False)
        self.get_folders_to_selection()

        self.window.mainloop()

    def cancel(self) -> None:
        self.window.destroy()

    def confirm(self) -> None:
        print("confirm")

    def get_folders_to_selection(self) -> None:
        dirs = os.listdir(settings.export_dir)
        dirs = [settings.export_dir + _dir for _dir in dirs]

        for _dir in dirs:
            
            frame = tk.Frame(master=self.selection_frame.inner_frame, bg="red", width=Importer.SELECTION_W, height=int(Importer.SELECTION_H / 3))

            tk.Button(master=frame, command=partial(self.load_save, _dir), width=70, height=11, bg="gray50").place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    
            image = Image.open(_dir+"/preview.png")
            image = image.resize((150, 150), Image.ANTIALIAS)
            photo_image = ImageTk.PhotoImage(image)

            label_img = tk.Label(master=frame, image=photo_image)
            label_img.place(relx=0.2, rely=0.5, anchor=tk.CENTER)
            label_img.image = photo_image
            
            self.selection_frame.add_frame(frame)

    def load_save(self, path_to_folder: str) -> None:
        print("load save at:", path_to_folder)
    
