class Settings():
    def __init__(self) -> None:
        self.screen_width = 1100
        self.screen_height = 800
        self.sidebar_width = 300
        self.bg_color = (0, 0, 0)

        self.max_fps = 60
        self.total_steps = 500000
        self.updates_at_a_time = 5


settings = Settings()