class Stats():
    def __init__(self) -> None:
        self.num_collisions = 0
        self.frame_num = 0
        self.fps = 60
        self.current_ray_step = 0
        self.ray_rotation = 0
        self.total_obstacles = 0

        self.simulation_running = False
        self.can_start = True
        self.ray_selected = False

        self.ray_pos_rounded = (0, 0)
        self.sidebar_texts_data = {}

stats = Stats()