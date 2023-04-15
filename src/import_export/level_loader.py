import pygame, os, json
pygame.init()

from config.stats import stats
from config.settings import settings

from obstacles.obstacle_manager import obstacle_manager

def load_on_start(ray):
    # check if last_session exists
    if not os.path.exists("src/config/last_session.json"): 
        return

    # load data from last_session
    with open("src/config/last_session.json", "r") as f:
        data = json.load(f)
    
    # path to last save's data
    data_path = settings.export_dir + data["last_save"] + "/data.json"

    # check if the path is valid
    if not os.path.exists(data_path):
        print(data_path, "not found")
        return

    # read the last save's data
    with open(data_path, "r") as f:
        scene_data = json.load(f)
    
    # load it
    ray.load_from_json(scene_data)
    obstacle_manager.load_from_json(scene_data)
    
    stats.current_scene = data["last_save"]


def load_level(level_name: str, ray, sidebar, screen: pygame.Surface):
    path = settings.export_dir + level_name

    # check if path is valid
    if not os.path.exists(path):
        print(path, "doesn't exits")
        return

    # read the data
    with open(path + "/data.json", "r") as f:
        data = json.load(f)
    
    # load the data
    ray.load_from_json(data)
    obstacle_manager.load_from_json(data)
    
    # configure stats
    stats.edited = False
    stats.current_scene = level_name

    # update everything
    ray.draw_ray(screen)
    sidebar.draw(screen)
    obstacle_manager.draw_obstacles(screen)
    pygame.display.update()