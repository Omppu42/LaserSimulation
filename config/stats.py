class Stats():
    def __init__(self) -> None:
        self.num_collisions = 0
        self.frame_num = 0
        self.current_ray_step = 0
        self.updating_ray = False

stats = Stats()