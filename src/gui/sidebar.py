import pygame

from gui.button import Button
from gui.image_button import ImageButton

from gui.text.text_object import TextObject
from gui.text.text_manager import TextManager

from gui.text.text_with_input import TextWithInputObject
from gui.text.text_with_input_manager import TextWithInputManager

from obstacles.obstacle_manager import obstacle_manager

from config.stats import stats
from config.settings import settings

from import_export.export import Exporter
from import_export._import import Importer

from ray import Ray

from enum import Enum
pygame.init()

class SelectedState(Enum):
    NO_OBSTACLE = 0
    OBSTACLE = 1
    RAY = 2
    RUNNING = 3

class Sidebar():
    def __init__(self, pos: tuple, size: tuple, ray: Ray, screen) -> None:
        self.x, self.y = pos
        self.w, self.h = size

        self.surf = pygame.Surface((self.w, self.h))
        self.surf.fill((10, 10, 10))

        self.ray_ref = ray

        button_font = pygame.font.Font(settings.global_font_path, 26)
        self.play_button = Button(self.x + self.w / 2, self.h - 50, 200, 50, text="Start Simulation", font=button_font, border=2)
        self.reset_button = Button(self.x + self.w / 2, self.h - 50, 100, 50, text="Reset", font=button_font, border=2)

        self.spawn_square_button = ImageButton((self.x + 40, 20), (48, 48), "assets/sqare_icon.png", border=2)
        self.spawn_circle_button = ImageButton((self.x + 90, 20), (48, 48), "assets/circle_icon.png", border=2)

        self.export_button = ImageButton((self.x + 160, 20), (48, 48), "assets/export.png", border=2)
        self.import_button = ImageButton((self.x + 210, 20), (48, 48), "assets/import.png", border=2)

        self.selected_state = SelectedState(SelectedState.NO_OBSTACLE)
        self.exporter = Exporter(screen, self.ray_ref)
        self.importer = Importer(self, screen, self.ray_ref)

        self.__init_keys()
        self.__update_texts_data()

        self.__init_inputfields()
        self.__init_texts()


    def __init_keys(self) -> None:
        self.RAY_POS_KEY = "ray_pos"
        self.RAY_ROT_KEY = "ray_rot"
        self.RAY_SPEED_KEY = "ray_speed"

        self.FPS_KEY = "fps"
        self.NUM_COLLS_KEY = "num_colls"
        self.CUR_STEP_KEY = "current_step"

        self.CUR_OBST_POS_KEY = "current_pos"
        self.CUR_OBST_ROT_KEY = "current_rot"
        self.CUR_OBST_SCALE_KEY = "current_scale"

        self.UPDATES_PER_FRAME_KEY = "updates_per_frame"
        self.TOTAL_OBSTACLES_KEY = "total_obsts"
        self.CURRENT_SCENE = "current_scene"


    def __update_texts_data(self) -> None:
        _curr_obst = obstacle_manager.get_selected_obstacle()

        stats.sidebar_texts_data[self.RAY_POS_KEY] = str(stats.ray_pos_rounded)
        stats.sidebar_texts_data[self.RAY_ROT_KEY] = stats.ray_rotation
        stats.sidebar_texts_data[self.RAY_SPEED_KEY] = '{0:.1f}'.format(settings.ray_step_size)

        stats.sidebar_texts_data[self.FPS_KEY] = stats.fps
        stats.sidebar_texts_data[self.NUM_COLLS_KEY] = stats.num_collisions
        stats.sidebar_texts_data[self.CUR_STEP_KEY] = stats.current_ray_step

        stats.sidebar_texts_data[self.CUR_OBST_POS_KEY] = str(_curr_obst.get_pos())
        stats.sidebar_texts_data[self.CUR_OBST_ROT_KEY] = _curr_obst.get_rotation()
        stats.sidebar_texts_data[self.CUR_OBST_SCALE_KEY] = _curr_obst.get_size()

        stats.sidebar_texts_data[self.UPDATES_PER_FRAME_KEY] = settings.ray_updates_per_frame
        stats.sidebar_texts_data[self.TOTAL_OBSTACLES_KEY] = stats.total_obstacles
        stats.sidebar_texts_data[self.CURRENT_SCENE] = stats.current_scene


    def __init_inputfields(self) -> None:
        textfield_font = pygame.font.Font(settings.global_font_path, 20)

        self.CONFIG_FPS_INDEX = 0
        self.CONFIG_UPDATES_FRAME_INDEX = 1

        self.inputfields = TextWithInputManager( [TextWithInputObject("Max FPS",          self.x + 20, 400, "60", 3, textfield_font, empty_field_value=1, int_only=True),
                                                  TextWithInputObject("Updates / Frame",  self.x + 20, 440, "15", 2, textfield_font, empty_field_value=1, int_only=True)] )


    def __init_texts(self) -> None:
        font = pygame.font.Font(settings.global_font_path, 20)

        # display these when an obstacle is selected
        self.obstacle_selected_texts = TextManager( [TextObject("Pos %s", self.__get_pos_in_center(self.h - 200), font, placeholder_key=self.CUR_OBST_POS_KEY),
                                                     TextObject("Scale %d", self.__get_pos_in_center(self.h - 180), font, placeholder_key=self.CUR_OBST_SCALE_KEY),
                                                     TextObject("Rotation deg %d", self.__get_pos_in_center(self.h - 160), font, placeholder_key=self.CUR_OBST_ROT_KEY),
                                                     TextObject("Arrows to Rotate and Scale", self.__get_pos_in_center(self.h - 120), font),
                                                     TextObject("'x' to Delete", self.__get_pos_in_center(self.h - 100), font)] )

        # display these when NO obstacle is selected
        self.no_obstacle_selected_texts = TextManager( [TextObject("Select an obstacle to Modify it", self.__get_pos_in_center(self.h - 110), font)] )

        self.not_running_texts = TextManager( [TextObject("Current scene: %s", self.__get_pos_in_center(110), font, placeholder_key=self.CURRENT_SCENE)] )

        # display when simulation running
        self.running_texts = TextManager( [TextObject("FPS %d", self.__get_pos_in_center(30), font, placeholder_key=self.FPS_KEY),
                                           TextObject("Laser Pos %s", self.__get_pos_in_center(70), font, placeholder_key=self.RAY_POS_KEY),
                                           TextObject("Total Collisions %d", self.__get_pos_in_center(90), font, placeholder_key=self.NUM_COLLS_KEY),
                                           TextObject("Total Updates %d", self.__get_pos_in_center(110), font, placeholder_key=self.CUR_STEP_KEY),
                                           TextObject("Obstacles %d", self.__get_pos_in_center(150), font, placeholder_key=self.TOTAL_OBSTACLES_KEY),
                                           TextObject("Moves / Frame %d", self.__get_pos_in_center(170), font, placeholder_key=self.UPDATES_PER_FRAME_KEY),
                                           TextObject("Speed pxl / Update %s", self.__get_pos_in_center(190), font, placeholder_key=self.RAY_SPEED_KEY)] )

        self.ray_selected = TextManager([TextObject("Pos %s", self.__get_pos_in_center(self.h - 180), font, placeholder_key=self.RAY_POS_KEY),
                                         TextObject("Rotation %d", self.__get_pos_in_center(self.h - 160), font, placeholder_key=self.RAY_ROT_KEY),
                                         TextObject("Arrows to Rotate", self.__get_pos_in_center(self.h - 120), font),
                                         TextObject("Mouse to Move", self.__get_pos_in_center(self.h - 100), font)])

        self.cant_start = TextManager([TextObject("Can't start when the ray", self.__get_pos_in_center(self.h - 60), font),
                                       TextObject("is inside and obstacle", self.__get_pos_in_center(self.h - 40), font)])

    def __get_pos_in_center(self, y_pos: int) -> tuple:
        """Returns a tuple position that is in the center of the sidebar with a variable y_pos"""
        return (self.x + self.w / 2, y_pos)


    def __reset_sim(self) -> None:
        stats.simulation_running = False

        self.ray_ref.x, self.ray_ref.y = stats.ray_starting_pos
        self.ray_ref.dir_deg = stats.ray_starting_rotation

        stats.num_collisions = 0
        stats.current_ray_step = 0


    def draw(self, screen) -> None:
        screen.blit(self.surf, (self.x, self.y))
        self.__update_texts_data()
        self.selected_state = self.determine_state()

        # States
        if self.selected_state == SelectedState.NO_OBSTACLE:
            self.draw_not_running(screen)
            self.no_obstacle_selected_texts.render_text(screen)

        elif self.selected_state == SelectedState.OBSTACLE:
            self.draw_not_running(screen)
            self.obstacle_selected_texts.render_text(screen)

        elif self.selected_state == SelectedState.RAY:
            self.draw_not_running(screen)
            self.ray_selected.render_text(screen)

        elif self.selected_state == SelectedState.RUNNING:
            self.running_texts.render_text(screen)
            self.reset_button.draw(screen)


    def draw_not_running(self, screen) -> None:
        if stats.can_start: self.play_button.draw(screen)
        else: self.cant_start.render_text(screen)

        self.not_running_texts.render_text(screen)

        self.import_button.draw(screen)
        self.export_button.draw(screen)

        self.spawn_circle_button.draw(screen)
        self.spawn_square_button.draw(screen)
        self.inputfields.draw(screen)


    def determine_state(self) -> SelectedState:
        if stats.simulation_running:
            return SelectedState.RUNNING
        
        if stats.ray_selected:
            return SelectedState.RAY

        if obstacle_manager.selected_index == -1:
            return SelectedState.NO_OBSTACLE
        else:
            return SelectedState.OBSTACLE


    def check_mouse_motion(self):
        if self.selected_state == SelectedState.RUNNING: 
            self.reset_button.check_hover(pygame.mouse.get_pos())
            return

        # when not running
        if stats.can_start: self.play_button.check_hover(pygame.mouse.get_pos())

        mouse_pos = pygame.mouse.get_pos()

        self.import_button.check_hover(mouse_pos)
        self.export_button.check_hover(mouse_pos)

        self.spawn_square_button.check_hover(mouse_pos)
        self.spawn_circle_button.check_hover(mouse_pos)
    

    def check_click(self, ray: Ray) -> None:
        if self.selected_state == SelectedState.RUNNING:
            if self.reset_button.check_click():
                self.__reset_sim()
                
            return
        
        # when not running
        self.inputfields.check_click()

        if self.import_button.check_click():
            self.importer.import_data()

        if self.export_button.check_click():
            self.exporter.export_data()

        if self.spawn_square_button.check_click():
            obstacle_manager.spawn_square()

        if self.spawn_circle_button.check_click():
            obstacle_manager.spawn_circle()

        if stats.can_start and self.play_button.check_click():
            self.on_simulation_start()
            ray.clear_surface()



    def handle_key_pressed(self, event) -> None:
        self.inputfields.on_keydown(event)


    def on_simulation_start(self) -> None:
        stats.simulation_running = True
        stats.total_obstacles = len(obstacle_manager.get_obstacles())

        settings.max_fps =                  self.inputfields.get_inputfield_at_index(self.CONFIG_FPS_INDEX).return_val()
        settings.ray_updates_per_frame =    self.inputfields.get_inputfield_at_index(self.CONFIG_UPDATES_FRAME_INDEX).return_val()

        self.inputfields.fix_strings()

        stats.ray_starting_pos = (self.ray_ref.x, self.ray_ref.y)
        stats.ray_starting_rotation = self.ray_ref.dir_deg