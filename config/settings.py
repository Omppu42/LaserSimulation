class Settings():
    def __init__(self) -> None:
        self.screen_width = 1100
        self.screen_height = 800
        self.sidebar_width = 300
        self.bg_color = (0, 0, 0)

        self.profile = False

        self.start_fps_limit = 60

        self.max_fps = 600
        self.total_steps = 500000
        self.ray_updates_per_frame = 50


settings = Settings()