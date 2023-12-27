import pygame
from sys import exit 
from random import randint

def display_score():
    score = int(pygame.time.get_ticks()/1000) - start_score
    score_surf = text_font.render(f"Score : {score}",False,"Black")
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf,score_rect)
    return score

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list :
            obstacle_rect.x -= 5
            if obstacle_rect.bottom == 300:
                screen.blit(snail_surf,obstacle_rect)
            else : 
                screen.blit(fly_surf,obstacle_rect)
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100 ]
        return obstacle_list
    else : return []

def collision_check(obstacle_list,player_rect):
    global game_active 
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            if obstacle_rect.colliderect(player_rect) :
                game_active = False

def player_animation():
    global player_surf, player_index 
    if player_rect.bottom == 300:
        player_index += 0.1
        if player_index >= len(player_walk) : player_index = 0
        player_surf = player_walk[int(player_index)]
    else :
        player_surf = player_stand

#Setup
pygame.init() 
screen = pygame.display.set_mode((800,400)) 
pygame.display.set_caption("Runner")
clock = pygame.time.Clock() 
text_font = pygame.font.Font("Font/Pixeltype.ttf",50)                           
sky_surface = pygame.image.load("Graphics/Sky.png")
ground_surface = pygame.image.load("Graphics/ground.png")
bg_music = pygame.mixer.Sound("Music/music.wav")
bg_music.play(loops = -1)

#Text
text2_surf = text_font.render("Press  'SPACE'  to restart",False,"Black")
text2_rect = text2_surf.get_rect(center = (400,280))

#Obstacles
obstacle_rect_list = []
#fly
fly1 = pygame.image.load("Graphics/fly1.png").convert_alpha()
fly2 = pygame.image.load("Graphics/fly2.png").convert_alpha()
fly_frames = [fly1,fly2]
fly_index = 0 
fly_surf = fly_frames[fly_index]
#snail
snail1 = pygame.image.load("Graphics/snail1.png").convert_alpha()
snail2 = pygame.image.load("Graphics/snail2.png").convert_alpha()
snail_frames = [snail1,snail2]
snail_index = 0 
snail_surf = snail_frames[snail_index]


#Player 
player_walk1 = pygame.image.load("Graphics/player_walk_1.png").convert_alpha()
print(player_walk1.get_size())
player_walk2 = pygame.image.load("Graphics/player_walk_2.png").convert_alpha()
player_walk = [player_walk1,player_walk2]
player_index = 0 
player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom = (100,300))
player_stand = pygame.image.load("Graphics/player_stand.png").convert_alpha()
player_rect2 = player_stand.get_rect(center = (400,200))

#Variables
player_gravity = 0
start_score = 0 
score = 0 
game_active = True

#Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer,500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer,200)

while True : 

    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            pygame.quit()
            exit()
        if game_active :
            if event.type == pygame.MOUSEBUTTONDOWN and player_rect.bottom == 300:
                player_gravity -= 30

            if event.type == pygame.KEYDOWN and player_rect.bottom == 300 :
                if pygame.K_SPACE : 
                    player_gravity -= 30 
            if event.type == obstacle_timer :
                if randint(0,2):
                    obstacle_rect_list.append(snail_surf.get_rect(midbottom = (randint(900,1100),300)))
                else : 
                    obstacle_rect_list.append(fly_surf.get_rect(midbottom = (randint(900,1100),200)))

            if event.type == snail_animation_timer :
                if snail_index == 0 : snail_index = 1
                else :  snail_index = 0
                snail_surf = snail_frames [snail_index]

            if event.type == fly_animation_timer :
                if fly_index == 0 : fly_index = 1
                else :  fly_index = 0
                fly_surf = fly_frames [fly_index]

                

        else :
            if event.type == pygame.KEYDOWN and player_rect.bottom == 300 :
                if pygame.K_SPACE :
                    game_active = True
                    start_score = int(pygame.time.get_ticks()/1000)

    if game_active:

        screen.blit(sky_surface,(0,0))        
        screen.blit(ground_surface,(0,300))
        score = display_score()

        player_animation()
        screen.blit(player_surf,player_rect)
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        player_gravity += 0.7
        player_rect.y += player_gravity
        if player_rect.bottom >= 300 : player_rect.bottom = 300

        collision_check(obstacle_rect_list,player_rect)

    else :
        text1_surf = text_font.render(f"Your Score : {score}",False,"Black")
        text1_rect = text1_surf.get_rect(center = (400,130))
        obstacle_rect_list.clear()
        player_rect.midbottom = (80,300)
        player_gravity = 0 
        screen.fill((94,129,162))
        screen.blit(player_stand,player_rect2)
        screen.blit(text2_surf,text2_rect)
        screen.blit(text1_surf,text1_rect)

    pygame.display.update()
    clock.tick(60)              




