class Stats():
    def __init__(self) -> None:
        self.num_collisions = 0
        self.frame_num = 0
        self.fps = 60
        self.current_ray_step = 0
        self.ray_rotation = 0
        self.total_obstacles = 0

        self.current_scene = "Empty"
        self.edited = False

        self.simulation_running = False
        self.can_start = True
        self.ray_selected = False

        self.ray_starting_rotation = 0
        self.ray_starting_pos = (0, 0)

        self.ray_pos_rounded = (0, 0)
        self.sidebar_texts_data = {}

        self.tkinter_func_to_run = (None, 0)
        self.tkinter_can_new_func = False

stats = Stats()