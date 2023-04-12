class Settings():
    def __init__(self) -> None:
        self.screen_width = 1100
        self.screen_height = 800
        self.sidebar_width = 300
        self.bg_color = (0, 0, 0)
        self.global_font_path = "Assets/Roboto-Regular.ttf"

        self.profile = False

        self.start_fps_limit = 60
        self.ray_step_size = .5

        # set by user
        self.max_fps = 0
        self.ray_updates_per_frame = 0


settings = Settings()