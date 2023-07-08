import pygame
import random

# ウィンドウのサイズ
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# 色
BLACK = (0,0,0)
PURPLE = (128, 0, 128)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


# 自機の設定
player_x = 50 #初期位置のx座標
player_y = WINDOW_HEIGHT // 2 #初期位置のy座標
player_width = 20 #自機の幅
player_height = 20 #自機の高さ
player_health = 5 #自機の体力

# 弾の初期位置とスピード
bullet_x = player_x + player_width
bullet_y = player_y
bullet_speed = 5
can_shoot = True  # 弾を発射できるかどうかのフラグ
bullet_cooldown = 100  # 弾のクールダウン時間（ミリ秒）
last_shoot_time = 0

# 敵の初期位置とスピード
enemy_width = 20
enemy_height = 20
enemy_spawn_interval = 5000  #スポーン間隔（ミリ秒）
last_enemy_spawn_time = 0
enemy_speed = 5
enemies = []



# スコア
score = 0

# 初期化
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

# フォントの設定
font = pygame.font.Font(None, 36)

# ループフラグ
running = True

# ゲームオーバーとクリアの表示時間
display_time = 5000  # ミリ秒

# ゲームオーバーとクリアの表示開始時間
game_over_start_time = 0
game_clear_start_time = 0

# ゲームオーバーとクリアの表示フラグ
game_over_displayed = False
game_clear_displayed = False

stopper = False

def draw_player():
    pygame.draw.rect(window, BLUE, (player_x, player_y, player_width, player_height))

def draw_bullet():
    pygame.draw.rect(window, GREEN, (bullet_x, bullet_y, 10, 5))


def draw_enemy(x,y):
    pygame.draw.rect(window, WHITE, (x, y, enemy_width, enemy_height))


def draw_score():
    score_text = font.render("Score: " + str(score), True, WHITE)
    window.blit(score_text, (10, 10))

def draw_health():
    health_text = font.render("Health: " + str(player_health), True, WHITE)
    window.blit(health_text, (10, 50))

def game_over():
    game_over_text = font.render("GAME OVER", True, RED)
    window.blit(game_over_text, (WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2))

def game_clear(): 
    clear_text = font.render("GAME CLEAR", True, YELLOW)
    score_text = font.render("Score: " + str(score), True, YELLOW)
    window.blit(clear_text, (WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 - 50))
    window.blit(score_text, (WINDOW_WIDTH // 2 - 80, WINDOW_HEIGHT // 2))

while running:
    window.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if not stopper:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player_y -= 5
        if keys[pygame.K_DOWN]:
            player_y += 5
        if keys[pygame.K_LEFT]:
            player_x -= 5
        if keys[pygame.K_RIGHT]:
            player_x += 5
        if keys[pygame.K_SPACE] and bullet_x >= WINDOW_WIDTH:
            bullet_x = player_x + player_width
            bullet_y = player_y
            can_shoot = False
            last_shoot_time = pygame.time.get_ticks()

    # 自機の移動範囲を制限
    player_x = max(0, min(player_x, WINDOW_WIDTH - player_width))
    player_y = max(0, min(player_y, WINDOW_HEIGHT - player_height))

    # 弾の移動
    if bullet_x < WINDOW_WIDTH:
       bullet_x += bullet_speed
    else:
        can_shoot = True
    # 弾のクールダウン時間経過後、再び発射可能にする
    current_time = pygame.time.get_ticks()
    if not can_shoot and current_time - last_shoot_time >= bullet_cooldown:
        can_shoot = True

    # 敵の生成
    current_time = pygame.time.get_ticks()
    if current_time - last_enemy_spawn_time > enemy_spawn_interval :
        enemy_y = random.randint(0, WINDOW_HEIGHT - enemy_height)
        enemies.append([WINDOW_WIDTH - enemy_width, enemy_y])
        last_enemy_spawn_time = current_time

    # 敵の移動と描画
    for enemy in enemies:
        enemy[0] -= enemy_speed
        draw_enemy(enemy[0], enemy[1])
        
        # 敵が画面外に出たら削除
        if enemy[0] + enemy_width < 0:
            enemies.remove(enemy)
            if not stopper:
                score -= 50

    # 敵と弾の衝突判定
    if bullet_x <= WINDOW_WIDTH:
        bullet_rect = pygame.Rect(bullet_x, bullet_y, 10, 5)
        for enemy in enemies:
            enemy_rect = pygame.Rect(enemy[0], enemy[1], enemy_width, enemy_height)
            if bullet_rect.colliderect(enemy_rect):
                enemies.remove(enemy)
                if not stopper:
                    score +=100
                break

    #敵と自機の衝突判定  
    if player_health >= 1:
        player_rect = pygame.Rect(player_x, player_y, 20, 20)
        for enemy in enemies:
            enemy_rect = pygame.Rect(enemy[0], enemy[1], enemy_width, enemy_height)
            if player_rect.colliderect(enemy_rect):
                
                enemies.remove(enemy)
                if not stopper:
                    score -= 100
                    player_health -= 1
                break         

    # 自機の体力が0以下になった場合
    if player_health <= 0:
        if not game_over_displayed:
            stopper = True
            if game_over_start_time == 0:  # 初めてゲームオーバーになった場合のみ更新する
                game_over_start_time = pygame.time.get_ticks()
            
            current_time = pygame.time.get_ticks()
            if current_time - game_over_start_time < display_time:
                game_over()
            else:
                game_over_displayed = True
                running = False

    # クリア条件
    if score >= 3000:
        if not game_clear_displayed:
            stopper = True
            if game_clear_start_time == 0:  # 初めてクリアになった場合のみ更新する
                game_clear_start_time = pygame.time.get_ticks()
            current_time = pygame.time.get_ticks()
            if current_time - game_clear_start_time < display_time:
                game_clear()
            else:
                game_clear_displayed = True
                running = False


    draw_player()
    draw_bullet()

    draw_score()
    draw_health()

    pygame.display.update()
    clock.tick(60)

pygame.quit()
