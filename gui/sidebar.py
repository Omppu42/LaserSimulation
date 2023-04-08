import pygame

from gui.button import Button
from gui.image_button import Image_Button
from gui.text.text_object import Text_Object
from gui.text.text_group import Text_Group

from obstacles.obstacle_manager import obstacle_manager

from config.stats import stats
from config.settings import settings

from ray import Ray

pygame.init()


class Sidebar():
    def __init__(self, pos: tuple, size: tuple) -> None:
        self.x, self.y = pos
        self.w, self.h = size

        self.surf = pygame.Surface((self.w, self.h))
        self.surf.fill((10, 10, 10))

        button_font = pygame.font.Font(settings.global_font_path, 26)
        self.play_button = Button(self.x + self.w / 2, self.h - 50, 200, 50, text="Start Simulation", font=button_font, border=2)

        self.spawn_square_button = Image_Button((self.x + self.w - 50, self.h - 250), (48, 48), "assets/sqare_icon.png", border=2)
        self.spawn_circle_button = Image_Button((self.x + self.w - 50, self.h - 300), (48, 48), "assets/circle_icon.png", border=2)

        self.init_texts()


    def init_texts(self) -> None:
        font = pygame.font.Font(settings.global_font_path, 20)

        # display these when an obstacle is selected
        self.POS_INDEX = 0
        self.SCALE_INDEX = 1
        self.ROTATION_INDEX = 2

        self.obstacle_selected_texts = Text_Group( [Text_Object("Pos %s", self.__get_pos_in_center(self.h - 200), font),
                                                    Text_Object("Scale %d", self.__get_pos_in_center(self.h - 180), font),
                                                    Text_Object("Rotation deg %d", self.__get_pos_in_center(self.h - 160), font),
                                                    Text_Object("Arrows to Rotate and Scale", self.__get_pos_in_center(self.h - 120), font),
                                                    Text_Object("'x' to Delete", self.__get_pos_in_center(self.h - 100), font)] )

        # display these when NO obstacle is selected
        self.no_obstacle_selected_texts = Text_Group( [Text_Object("Select an obstacle to Modify it", self.__get_pos_in_center(self.h - 110), font)] )

        # display when simulation running
        self.FPS_INDEX = 0
        self.LASER_POS_INDEX = 1
        self.TOTAL_COLLS_INDEX = 2
        self.TOTAL_OBSTS_INDEX = 3
        self.MOVES_PER_FRAME = 4

        self.running_texts = Text_Group( [Text_Object("FPS %d", self.__get_pos_in_center(30), font),
                                          Text_Object("Laser Pos %s", self.__get_pos_in_center(70), font),
                                          Text_Object("Total Collisions %d", self.__get_pos_in_center(90), font),
                                          Text_Object("Obstacles %d", self.__get_pos_in_center(130), font),
                                          Text_Object("Moves / Frame %d", self.__get_pos_in_center(150), font)] )


    def __get_pos_in_center(self, y_pos: int) -> tuple:
        """Returns a tuple position that is in the center of the sidebar with a variable y_pos"""
        return (self.x + self.w / 2, y_pos)


    def draw(self, screen) -> None:
        screen.blit(self.surf, (self.x, self.y))

        if not stats.simulation_running:
            self.render_texts(screen)
            self.play_button.draw(screen)
            self.spawn_square_button.draw(screen)
            self.spawn_circle_button.draw(screen)
        else:
            self.__update_texts()
            self.running_texts.render_text(screen)


    def render_texts(self, screen) -> None:
        if obstacle_manager.selected_index == -1:
            # No obstacle selected
            self.no_obstacle_selected_texts.render_text(screen)

        else:
            # Obstacle is selected
            _curr_obst = obstacle_manager.get_selected_obstacle()

            self.obstacle_selected_texts.text_objects[self.POS_INDEX]       .set_placeholder(str(_curr_obst.get_pos()))
            self.obstacle_selected_texts.text_objects[self.SCALE_INDEX]     .set_placeholder(_curr_obst.get_size())
            self.obstacle_selected_texts.text_objects[self.ROTATION_INDEX]  .set_placeholder(_curr_obst.get_rotation())

            self.obstacle_selected_texts.render_text(screen)


    def __update_texts(self) -> None:
        self.running_texts.text_objects[self.LASER_POS_INDEX]       .set_placeholder( str(stats.ray_pos_rounded) )
        self.running_texts.text_objects[self.FPS_INDEX]             .set_placeholder( stats.fps )
        self.running_texts.text_objects[self.TOTAL_COLLS_INDEX]     .set_placeholder( stats.num_collisions )
        

    def check_mouse_motion(self):
        if stats.simulation_running == True: return

        self.play_button.check_hover(pygame.mouse.get_pos())
        self.spawn_square_button.check_hover(pygame.mouse.get_pos())
        self.spawn_circle_button.check_hover(pygame.mouse.get_pos())
    

    def check_click(self, ray: Ray) -> None:
        if stats.simulation_running == True: return

        if self.spawn_square_button.check_click():
            obstacle_manager.spawn_square()

        if self.spawn_circle_button.check_click():
            obstacle_manager.spawn_circle()

        if self.play_button.check_click():
            self.on_simulation_start()
            ray.clear_surface()

    def on_simulation_start(self) -> None:
        stats.simulation_running = True

        self.running_texts.text_objects[self.TOTAL_OBSTS_INDEX]     .set_placeholder( stats.total_obstacles )
        self.running_texts.text_objects[self.MOVES_PER_FRAME]       .set_placeholder( settings.ray_updates_per_frame )