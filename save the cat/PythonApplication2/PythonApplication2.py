
import pygame
import time
import random

pygame.font.init()

WIDTH, HEIGHT = 1500, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("star game")



PLAYER_WIDTH = 120
PLAYER_HEIGHT = 120
PLAYER_VAL = 5

FONT = pygame.font.SysFont("comicsans", 30)

STAR_WIDTH = 90
STAR_HEIGHT = 90


BG = pygame.transform.scale(pygame.image.load("picture.jpg"), (WIDTH, HEIGHT))
PLAYER_IMG = pygame.transform.scale(pygame.image.load("player.jpg"), (PLAYER_WIDTH, PLAYER_HEIGHT))
STAR_IMG = pygame.transform.scale(pygame.image.load("star.jpg"), (STAR_WIDTH, STAR_HEIGHT))



def draw_start_screen(selected_index):
    WIN.blit(BG, (0, 0))
    
    title_text = FONT.render("Choose a difficulty level using Up/Down arrows and press Enter", 1, "black")
    options = ["Easy", "Medium", "Hard"]
    
    start_w = WIDTH // 2 - title_text.get_width() // 2
    start_h = HEIGHT // 2 - 60
    
    WIN.blit(title_text, (start_w, start_h - 60))
    
    for i, option in enumerate(options):
        color = "red" if i == selected_index else "black"
        prefix = "> " if i == selected_index else "  "
        option_text = FONT.render(prefix + option, 1, color)
        WIN.blit(option_text, (WIDTH // 2 - 50, start_h + (i * 40)))
        
    pygame.display.update()

def draw(player, elapsed_time, stars):
    WIN.blit(BG, (0, 0))
    WIN.blit(PLAYER_IMG, (player.x, player.y))

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "black")
    WIN.blit(time_text, (10, 10))

    for star in stars:
         WIN.blit(STAR_IMG, (star.x, star.y))

    pygame.display.update()




def play_game(star_vel, star_spawn_speed, star_num):
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    star_add_increment = star_spawn_speed
    star_count = 0
    stars = []

    player = pygame.Rect(WIDTH // 2 - PLAYER_WIDTH // 2, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)

    run = True
    hit = False
    
    while run:
        star_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VAL >= 0:
            player.x -= PLAYER_VAL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VAL + player.width <= WIDTH:
            player.x += PLAYER_VAL

        if star_count >= star_add_increment:
            for _ in range(star_num):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)

            star_add_increment = max(600, star_add_increment - 50)
            star_count = 0

        for star in stars[:]:
            star.y += star_vel
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.colliderect(player):
                stars.remove(star)
                hit = True
                break

        if hit:
            lost_text = FONT.render(f"Game Over! Your time: {round(elapsed_time)} seconds", 1, "black")
            WIN.blit(lost_text, (WIDTH // 2 - lost_text.get_width() // 2, HEIGHT // 2 - lost_text.get_height() // 2))
            pygame.display.update()
            pygame.time.delay(4000)
            break

        draw(player, elapsed_time, stars)

    return True

def main():
    run = True
    selected_index = 0
    clock = pygame.time.Clock()
    
    while run:
        clock.tick(60)
        draw_start_screen(selected_index)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % 3
                elif event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % 3
                elif event.key == pygame.K_RETURN:
                    if selected_index == 0:
                        run = play_game(star_vel=5, star_spawn_speed=2500, star_num=3)
                    elif selected_index == 1:
                        run = play_game(star_vel=7, star_spawn_speed=2000, star_num=5)
                    elif selected_index == 2:
                        run = play_game(star_vel=10, star_spawn_speed=1500, star_num=7)

    pygame.quit()

if __name__ == "__main__":
    main()