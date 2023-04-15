import os, json
import tkinter as tk
import pygame
pygame.init()

from datetime import datetime
from functools import partial
from PIL import ImageTk, Image

from config.settings import settings

import import_export.level_loader as level_loader

from gui.scrollable_frame import ScrollableFrame

class Importer():
    SELECTION_W = 500
    SELECTION_H = 500

    BTN_UNSELECTED_COLOR = "gray60"
    BTN_SELECTED_COLOR = "gray75"
    FRAME_BG = "gray50"
    
    def __init__(self, sidebar, screen, ray) -> None:
        self.sidebar = sidebar
        self.screen = screen
        self.ray = ray

        self.error_label = None

    def import_data(self) -> None:
        self.selected_save = {}
        self.selected_save["index"] = -1
        self.selected_save["path"] = ""

        self.error_label = None

        self.window = tk.Tk()
        self.window.geometry("600x600")
        self.window.title("Import")
        
        self.selection_frame_f = tk.Frame(self.window, width=Importer.SELECTION_W, height=Importer.SELECTION_H)
        self.selection_frame_f.pack()

        self.selection_frame = ScrollableFrame(self.selection_frame_f, width=Importer.SELECTION_W, height=Importer.SELECTION_H)
        self.selection_frame.pack()

        self.select_a_save_label = tk.Label(self.window, text="Select a save to load.", font=("Arial", 18))
        self.select_a_save_label.place(relx=0.5, rely=0.87, anchor=tk.CENTER)

        self.cancel_button = tk.Button(text="Exit", command=self.__cancel, font=22, width=15, height=2, bg="gray99")
        self.cancel_button.place(relx=0.65, rely=0.95, anchor=tk.CENTER)

        self.confirm_button = tk.Button(text="Load", command=self.__confirm, font=22, width=15, height=2, bg="gray99")
        self.confirm_button.place(relx=0.35, rely=0.95, anchor=tk.CENTER)

        self.window.resizable(False, False)
        self.__get_folders_to_selection()

        self.window.mainloop()

    def __cancel(self) -> None:
        self.window.destroy()

    def __confirm(self) -> None:
        if self.selected_save["index"] == -1:
            self.select_a_save_label.destroy()

            self.error_label = tk.Label(self.window, text="Please select a save", font=("Arial", 18), fg="red")
            self.error_label.place(relx=0.5, rely=0.87, anchor=tk.CENTER)
            return

        if self.error_label:
            self.error_label.destroy()

        name = os.path.basename(self.selected_save["path"])

        level_loader.load_level(name, self.ray, self.sidebar, self.screen)

        self.select_a_save_label.config(text=f"Loaded: {name}")


    def __get_folders_to_selection(self) -> None:
        dirs = os.listdir(settings.export_dir)
        dirs = [settings.export_dir + _dir for _dir in dirs]

        # If no saves exist
        if dirs == []:
            tk.Label(self.window, text="You don't have any saves.", font=("Arial", 18)).place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            tk.Label(self.window, text="Export something first.", font=("Arial", 16)).place(relx=0.5, rely=0.55, anchor=tk.CENTER)
            self.selection_frame.delete_scrollable_frame()
            self.select_a_save_label.destroy()
            self.confirm_button.destroy()
            self.cancel_button.place(relx=0.5, rely=0.9, anchor=tk.CENTER)
            return

        self.selection_buttons = []
        sorted_dirs = []

        # Sort by time saved
        for _dir in dirs:
            with open(_dir + "/data.json", "r") as f:
                data = json.load(f)

            saved = data["saved_time"]
            diff = datetime.now() - datetime.strptime(saved, "%d/%m/%Y %H:%M")
            minutes = diff.total_seconds() / 60
            
            sorted_dirs.append( (_dir, minutes) )

        # sort by the difference to current time: Most recently exported will be on top
        sorted_dirs.sort(key=lambda x: x[1])

        # if less than 3 saves, adjust the scrollable frame height to not allow scrolling
        if len(sorted_dirs) < 3:
            self.selection_frame.canvas.config(height=len(sorted_dirs) * 176)

        # Create selection frames
        for _index, _data in enumerate(sorted_dirs):
            self.__create_selectable(_index, _data[0])


    def __create_selectable(self, _index, _dir) -> None:
        # Read data
        with open(_dir + "/data.json", "r") as f:
            data = json.load(f)

        name = os.path.basename(_dir)
        saved = data["saved_time"]
        
        # Frame
        frame = tk.Frame(master=self.selection_frame.inner_frame, bg=Importer.FRAME_BG, width=Importer.SELECTION_W, height=int(Importer.SELECTION_H / 3))
        
        # Select button
        button = tk.Button(master=frame, text="Select", command=partial(self.__select_btn, _dir, _index), width=30, height=4, bg=Importer.BTN_UNSELECTED_COLOR)
        button.place(relx=0.65, rely=0.6, anchor=tk.CENTER)
        self.selection_buttons.append(button)

        # Name and Saved time
        tk.Label(master=frame, text=f"Name: {name}", bg=Importer.FRAME_BG, font=("Arial", 12)).place(relx=0.65, rely=0.1, anchor=tk.CENTER)
        tk.Label(master=frame, text=f"Saved: {saved}", bg=Importer.FRAME_BG, font=("Arial", 12)).place(relx=0.65, rely=0.25, anchor=tk.CENTER)

        # Load preview image
        image = Image.open(_dir+"/preview.png")
        image = image.resize((150, 150), Image.ANTIALIAS)
        photo_image = ImageTk.PhotoImage(image)

        # Display preview image
        label_img = tk.Label(master=frame, image=photo_image)
        label_img.place(relx=0.17, rely=0.5, anchor=tk.CENTER)
        label_img.image = photo_image

        # Add the result to the scrollable frame
        self.selection_frame.add_frame(frame)
        
        
    def __select_btn(self, path_to_folder: str, selection_btn_index: int) -> None:
        self.selected_save["index"] = selection_btn_index
        self.selected_save["path"] = path_to_folder

        for _index, _btn in enumerate(self.selection_buttons):
            if _index == self.selected_save["index"]:
                _btn.config(bg=Importer.BTN_SELECTED_COLOR, text="Selected")
            else:
                _btn.config(bg=Importer.BTN_UNSELECTED_COLOR, text="Select")