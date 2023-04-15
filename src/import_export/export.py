import os, json, datetime
import tkinter as tk
import pygame
pygame.init()

from config.settings import settings
from config.stats import stats
from obstacles.obstacle_manager import obstacle_manager
from obstacles.square import SquareObstacle
from obstacles.circle import CircleObstacle

class Exporter():
    ALLOWED_CHARS = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","1","2","3","4","5","6","7","8","9","0"," ", "_"]

    def __init__(self, sidebar, screen, ray) -> None:
        self.sidebar = sidebar
        self.screen = screen
        self.ray = ray

    def validate(self, P):
        P = P.lower()

        if len(P) == 0:
            # empty Entry is ok
            return True
        
        elif len(P) <= 20:
            for char in P:
                if not char in Exporter.ALLOWED_CHARS:
                    return False
            
            # bellow limit and all chars are allowed
            return True
        
        # Anything else, reject it
        return False

    def export_data(self) -> None:
        self.no_name_error_label = None

        self.window = tk.Tk()
        self.window.geometry("400x300")
        self.window.title("Export")

        tk.Label(text="Export the current state of the scene into a file.", font=22).place(relx=0.5, rely=0.2, anchor=tk.CENTER)

        self.give_name_label = tk.Label(text="Give the file a name", font=18)
        self.give_name_label.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

        vcmd = (self.window.register(self.validate), '%P')
        self.name_entry = tk.Entry(width=20, font=18, validate="key", validatecommand=vcmd)
        self.name_entry.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

        self.cancel_button = tk.Button(text="Cancel", command=self.cancel)
        self.cancel_button.place(relx=0.4, rely=0.85, anchor=tk.CENTER)

        self.export_button = tk.Button(text="Export", command=self.confirm)
        self.export_button.place(relx=0.6, rely=0.85, anchor=tk.CENTER)

        self.window.resizable(False, False)

        self.window.mainloop()


    def cancel(self) -> None:
        self.window.destroy()


    def confirm(self) -> None:
        name = self.name_entry.get()
        
        if name == "":
            self.no_name_error_label = tk.Label(text="Please provide a name", font=22, fg="red")
            self.no_name_error_label.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
            # Stop here if no name provided
            return
        
        self.export_into_folder(name)


    def export_into_folder(self, folder_name: str) -> None:
        path = os.path.join(settings.export_dir, folder_name)

        self.give_name_label.destroy()
        self.name_entry.destroy()
        self.cancel_button.destroy()
        self.export_button.destroy()

        if not os.path.exists(settings.export_dir):
            os.mkdir(settings.export_dir)

        if self.no_name_error_label:
            self.no_name_error_label.destroy()

        exporting = tk.Label(text="Exporting...", font=22, fg="green3")
        exporting.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        saved_as = tk.Label(text=f"Saved into {path}", font=22)
        saved_as.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
        
        self.export_no_gui(folder_name)

        self.window.update()

        exporting.destroy()

        tk.Label(text="Done exporting!", font=22, fg="green3").place(relx=0.5, rely=0.4, anchor=tk.CENTER)
        tk.Button(text="Done", command=self.cancel).place(relx=0.5, rely=0.85, anchor=tk.CENTER)


    def export_no_gui(self, folder_name: str) -> None:
        stats.edited = False
        path = os.path.join(settings.export_dir, folder_name)

        if not os.path.exists(path):
            os.mkdir(path)

        self.take_screenshot(path)
        json_obj = self.create_json_output()

        with open(path + "/data.json", "w") as f:
            json.dump(json_obj, f, indent=2)

        self.sidebar.importer.load_scene_no_gui(path)


    def take_screenshot(self, folder: str) -> None:
        ss_rect = pygame.Rect(0, 0, settings.screen_width - settings.sidebar_width, settings.screen_height)
        ss_sub = self.screen.subsurface(ss_rect)
        pygame.image.save(ss_sub, folder + "/preview.png")


    def create_json_output(self) -> list:
        output = {}

        output["saved_time"] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        output["ray"] = self.ray.make_json_object()

        square_data = []
        circle_data = []

        for _obs in obstacle_manager.get_obstacles():
            if isinstance(_obs, SquareObstacle):
                square_data.append(_obs.make_json_save())

            elif isinstance(_obs, CircleObstacle):
                circle_data.append(_obs.make_json_save())

        output["squares"] = square_data
        output["circles"] = circle_data

        return output