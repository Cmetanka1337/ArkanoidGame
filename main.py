# import pygame
# import pygame_gui
# from pygame_gui import UIManager, UI_BUTTON_PRESSED
# from pygame_gui.elements import UIButton
#
# from Views.Ball import BallObject
# from Views.Scene import SceneObject
# from Views.UserPlate import UserPlateObject
# from Views.LevelPlate import LevelPlateObject
# from Models.LevelManager import LevelManager
# # from Views import UserPlate.UserPlateObject
#
# pygame.init()
#
# # plate = UserPlateObject()
# # levelPlate = LevelPlateObject()
#
# sc = pygame.display.set_mode((SceneObject.width, SceneObject.height))
# pygame.display.set_caption("Arkanoid Game")
#
# clock = pygame.time.Clock()
# plate = UserPlateObject(400,500,100,30,pygame.Color(255,255,255),20)
# ball = BallObject(200,100,10,10,pygame.Color(255,0,0),5,[1,1],5)
# #user_plate = pygame.rect.Rect(SceneObject.width//2,SceneObject.height//2,200,50)
# # 0,"standart",False,100,200,50,200,pygame.Color(255,255,255),True)
# level_manager = LevelManager(SceneObject.width, SceneObject.height)
# selected_level = 1  # Вибираємо рівень вручну
# level_manager.load_level(selected_level)
# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             exit()
#
#     keys = pygame.key.get_pressed()
#     if keys[pygame.K_LEFT]:
#
#         plate.move_to(plate.rect.x - plate.speed, plate.rect.y)
#     if keys[pygame.K_RIGHT]:
#
#         plate.move_to(plate.rect.x + plate.speed, plate.rect.y)
#
#     sc.fill((0, 0, 0))
#
#     ball.update_position()
#     ball.calculate_reflection(plate, level_manager)
#
#     ball.render(sc)
#     plate.render(sc)
#     level_manager.render(sc)
#     pygame.display.flip()
#     clock.tick(60)
#
#
#
#

#some comments to test ci