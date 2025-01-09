import random
import pgzrun
from pygame import Rect

# Configurações iniciais
WIDTH = 400
HEIGHT = 600

HERO_SPEED = 2
ENEMY_SPEED = 1.5
COINS = 0
LIFE = 3

SHOOT_COOLDOWN = 50
shoot_timer = 0  

enemy_spawn_timer = 0
ENEMY_SPAWN_INTERVAL = 60

CONT_ENEMY = 3

frame = 0
hero = None
enemies = []
survival_time = 0  

is_music_playing = True
music.set_volume(0.5)  
if is_music_playing:
    music.play("background_music")

# Estados do jogo (telas)
STATE_MENU = "menu"
STATE_PLAYING = "playing"
STATE_GAMEOVER = "gameover"
game_state = STATE_MENU

# Classe do jogador
class Hero:
    def __init__(self):
        self.sprite = Actor("hero_idle_1", (WIDTH // 2, HEIGHT - 50))
        self.sprite.images = ["hero_idle_1", "hero_idle_2", "hero_idle_3", "hero_idle_4", "hero_idle_5", "hero_idle_6", "hero_idle_7", "hero_idle_8"]
        self.rect = Rect(self.sprite.x, self.sprite.y, 64, 64)
        self.is_moving = False
        self.direction = "idle"
        self.shots = []

    def move(self):
        global frame
        self.is_moving = False

        # Movimentação para a direita
        if keyboard.right and self.sprite.x < WIDTH - 30:
            self.sprite.x += HERO_SPEED
            self.is_moving = True
            self.direction = "right"

        # Movimentação para a esquerda
        elif keyboard.left and self.sprite.x > 30:
            self.sprite.x -= HERO_SPEED
            self.is_moving = True
            self.direction = "left"

        # Atualizar a posição do retângulo
        self.rect.x = self.sprite.x - 32
        self.rect.y = self.sprite.y - 32

        # Atualizar animação com base na direção e movimento
        if self.is_moving:
            if self.direction == "right":
                self.sprite.image = f"hero_move_r_{frame % 8 + 1}"
            elif self.direction == "left":
                self.sprite.image = f"hero_move_l_{frame % 8 + 1}"
        else:
            self.sprite.image = f"hero_idle_{frame % 8 + 1}"
            self.direction = "idle"

    def attack(self):
        global shoot_timer  

        if shoot_timer == 0:
            shot = Shot(self.sprite.x, self.sprite.y)
            self.shots.append(shot)
            shoot_timer = SHOOT_COOLDOWN  

    def update_shots(self):
        for shot in self.shots[:]:
            shot.move()
            if shot.is_off_screen():
                self.shots.remove(shot)

# Classe do tiro
class Shot:
    def __init__(self, x, y):
        self.sprite = Actor("bone", (x, y))
        self.speed = 5
        self.rect = Rect(self.sprite.x, self.sprite.y, 64, 64)
    
    def move(self):
        self.sprite.y -= self.speed
        self.rect.topleft = (self.sprite.x, self.sprite.y)

    def is_off_screen(self):
        return self.sprite.y + self.sprite.height < 0

# Classe do inimigo
class Enemy:
    def __init__(self, x, y):
        self.sprite = Actor("enemy_1", (x, y))
        self.sprite.images = ["enemy_1", "enemy_2", "enemy_3", "enemy_4", "enemy_5", "enemy_6", "enemy_5", "enemy_8"]
        self.speed = ENEMY_SPEED
        self.rect = Rect(self.sprite.x, self.sprite.y, self.sprite.width, self.sprite.height)

    def move(self):
        self.sprite.y += self.speed
        self.rect.topleft = (self.sprite.x - self.sprite.width // 2, self.sprite.y - self.sprite.height // 2)
        self.sprite.image = f"enemy_{frame % 8 + 1}"

    def is_off_screen(self):
        return self.sprite.y > HEIGHT

def spawn_enemy():
    x = random.randint(50, WIDTH - 50)
    y = -50 
    enemies.append(Enemy(x, y))

# Desenhar a tela
def draw():
    screen.clear()
    if game_state == STATE_MENU:
        screen.blit("background", (0, 0))
        draw_menu()
    elif game_state == STATE_PLAYING:
        screen.blit("background_game", (0, 0))
        draw_game()
    elif game_state == STATE_GAMEOVER:
        screen.blit("background", (0, 0))
        draw_gameover()

# tela de menur inicial
def draw_menu():
    screen.draw.text("Skeleton Attack!", center=(WIDTH // 2, HEIGHT // 2 - 50), fontsize=40, color="white")
    
    screen.draw.rect(Rect(WIDTH // 2 - 50, HEIGHT // 2 + 10, 100, 40), color="white")
    screen.draw.text("Iniciar", center=(WIDTH // 2, HEIGHT // 2 + 30), fontsize=30, color="white")
    
    screen.draw.rect(Rect(WIDTH // 2 - 50, HEIGHT // 2 + 60, 100, 40), color="white")
    screen.draw.text("Sair", center=(WIDTH // 2, HEIGHT // 2 + 80), fontsize=30, color="white")
    
    music_text = "Music: ON" if is_music_playing else "Music: OFF"
    screen.draw.text(music_text, center=(WIDTH // 2, HEIGHT // 2 + 120), fontsize=25, color="green")

# tela princial gamepalayer
def draw_game():
    hero.sprite.draw()
    for shot in hero.shots: 
        shot.sprite.draw()
    for enemy in enemies:
        enemy.sprite.draw()
    
    screen.draw.text(f"Tempo: {survival_time} s", (10, 10), fontsize=30, color="white")
    screen.draw.text(f"Life: {LIFE}", (150, 10), fontsize=30, color="white")
    screen.draw.text(f"Coins: {COINS}", (10, 40), fontsize=30, color="yellow")

# tela de game over
def draw_gameover():
    screen.draw.text("Game Over!", center=(WIDTH // 2, HEIGHT // 2 - 50), fontsize=40, color="red")
    screen.draw.text(f"Coins: {COINS}", center=(WIDTH // 2, HEIGHT // 2), fontsize=30, color="yellow")
    
    if COINS >= 5:
        screen.draw.rect(Rect(WIDTH // 2 - 150, HEIGHT // 2 + 20, 300, 38), color="yellow")

    screen.draw.text("Aumentar velocidade de ataque", center=(WIDTH // 2, HEIGHT // 2 + 40), fontsize=25, color="white")
    
    screen.draw.rect(Rect(WIDTH // 2 - 150, HEIGHT // 2 + 60, 300, 38), color="white")
    screen.draw.text("Jogar novamente", center=(WIDTH // 2, HEIGHT // 2 + 80), fontsize=25, color="white")
    
    screen.draw.rect(Rect(WIDTH // 2 - 150, HEIGHT // 2 + 100, 300, 38), color="white")
    screen.draw.text("Sair", center=(WIDTH // 2, HEIGHT // 2 + 120), fontsize=25, color="white")

def on_mouse_down(pos):
    global is_music_playing, game_state, COINS, SHOOT_COOLDOWN
    if game_state == STATE_MENU:
        if Rect(WIDTH // 2 - 50, HEIGHT // 2 + 10, 100, 40).collidepoint(pos):
            game_state = STATE_PLAYING
            init_game()
        
        elif Rect(WIDTH // 2 - 50, HEIGHT // 2 + 60, 100, 40).collidepoint(pos):
            pgzrun.quit()

        elif Rect(WIDTH // 2 - 50, HEIGHT // 2 + 110, 100, 20).collidepoint(pos):
            is_music_playing = not is_music_playing
            if is_music_playing:
                music.play("background_music")
            else:
                music.stop()
    
    elif game_state == STATE_GAMEOVER:
        if Rect(WIDTH // 2 - 150, HEIGHT // 2 + 20, 300, 38).collidepoint(pos) and COINS >= 5 :
            COINS -= 5
            SHOOT_COOLDOWN = max(10, SHOOT_COOLDOWN - 10) 
        elif Rect(WIDTH // 2 - 150, HEIGHT // 2 + 60, 300, 38).collidepoint(pos):
            game_state = STATE_PLAYING  
            init_game() 
        elif Rect(WIDTH // 2 - 150, HEIGHT // 2 + 100, 300, 38).collidepoint(pos):
            pgzrun.quit()
            
def update():
    global frame, enemy_spawn_timer, shoot_timer, game_state, survival_time, LIFE, COINS, SHOOT_COOLDOWN

    if game_state == STATE_PLAYING:
        frame += 1
        enemy_spawn_timer += 1

        if frame % 60 == 0:
            survival_time += 1

        hero.move()
        hero.update_shots()

        if shoot_timer > 0:
            shoot_timer -= 1

        for enemy in enemies[:]:
            enemy.move()
            if enemy.is_off_screen():
                LIFE -= 1
                enemies.remove(enemy)
                if LIFE <= 0:
                    game_state = STATE_GAMEOVER

        for shot in hero.shots[:]:
            for enemy in enemies[:]:
                if shot.rect.colliderect(enemy.rect):  
                    hero.shots.remove(shot)
                    enemies.remove(enemy)
                    if random.random() < 0.15:
                        COINS += 1
                    break

        if enemy_spawn_timer >= ENEMY_SPAWN_INTERVAL:
            spawn_enemy()
            enemy_spawn_timer = 0

        if keyboard.space:
            hero.attack()

def init_game():
    global hero, enemies, survival_time, LIFE, COINS
    hero = Hero()
    enemies = []
    survival_time = 0
    LIFE = 3

init_game()
pgzrun.go()
