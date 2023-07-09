import pygame
import random
import time

# ウィンドウのサイズ
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600

# 色
BLACK = (0,0,0)
PURPLE = (128, 0, 128)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255,165,0)
GREENYELLOW = (173,255,47)

#カラーインデックスの定義
colors = [RED, ORANGE, YELLOW, GREENYELLOW , GREEN]

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

#弾の発射間隔設定
bullet_cooldown = 1000  # 弾のクールダウン時間（ミリ秒）
last_shoot_time = 0

#複数の弾の移動管理用
bullets = []

# 敵の初期位置とスピード
enemy_width = 20
enemy_height = 20
enemy_speed = 5

#敵のスポーン間隔設定
enemy_spawn_interval = 2000  #スポーン間隔（ミリ秒）
last_enemy_spawn_time = 0

#複数の敵の移動管理用
enemies = []

#ループフラグ
waiting = True
running = False

# スコア
score = 0

# 初期化
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

# フォントの設定
font = pygame.font.Font(None, 36)

#ループフラグ
waiting = True
running = False



#ゲームオーバーとクリア時の動作停止フラグ
stopper = False

#自機の描画
def draw_player():
    pygame.draw.rect(window, BLUE, (player_x, player_y, player_width, player_height))

#弾の描画    
def draw_bullet(x,y):
    pygame.draw.rect(window, RED, (x, y, 10, 5))

#敵の描画
def draw_enemy(x,y):
    pygame.draw.rect(window, WHITE, (x, y, enemy_width, enemy_height))

#スコアの描画
def draw_score():
    score_text = font.render("Score: " + str(score), True, WHITE)
    window.blit(score_text, (10, 10))

#体力バーの描画
def draw_health():
    for i in range(player_health):
        # バーの幅と高さを指定
        bar_width = 30
        bar_height = 5
        
        # バーの位置を計算
        bar_x = 10 + (bar_width + 5) * i
        bar_y = 50
        
        # カラーインデックスを取得
        color_index = min(i, len(colors) - 1)
        color = colors[color_index]
        
        # バーを描画
        pygame.draw.rect(window, color, (bar_x, bar_y, bar_width, bar_height))



#ゲームオーバーの描画
def game_over():
    game_over_text = font.render("GAME OVER", True, RED)
    window.blit(game_over_text, (WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2))

#ゲームクリアの描画
def game_clear(): 
    clear_text = font.render("GAME CLEAR", True, YELLOW)
    score_text = font.render("Score: " + str(score), True, YELLOW)
    window.blit(clear_text, (WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 - 50))
    window.blit(score_text, (WINDOW_WIDTH // 2 - 80, WINDOW_HEIGHT // 2))

#スタートメニューの描画    
def start_menu():
    start_text = font.render("Press ENTER to START", True, WHITE)
    end_text = font.render("Press Esc to EXIT", True, WHITE)
    window.blit(start_text, (WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT // 2))
    window.blit(end_text, (WINDOW_WIDTH - 250, WINDOW_HEIGHT - 50))

#GAME STARTの描画
def start_game():
    game_start_text = font.render("GAME START", True, WHITE)
    window.blit(game_start_text, (WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2))

#テキストの表示時間管理
def process_for_seconds(seconds, game_function):
    start_time = time.time()
    while time.time() - start_time < seconds:
        window.fill(BLACK)
        game_function()
        pygame.display.update()

#システム全体のループ
while True:

    # Pless ENTER to STARTの画面を表示
    while waiting:
        window.fill(BLACK)
        start_menu()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    process_for_seconds(3, start_game)
                    running = True
                    waiting = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()



    #ゲームのメイン処理
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
            current_time = pygame.time.get_ticks()
            if keys[pygame.K_SPACE] and current_time - last_shoot_time > bullet_cooldown:
                bullet_x = player_x + player_width
                bullet_y = player_y
                last_shoot_time = pygame.time.get_ticks()
                bullets.append([bullet_x,bullet_y])	

        # 自機の移動範囲を制限
        player_x = max(0, min(player_x, WINDOW_WIDTH // 2 - (player_width + 100)))
        player_y = max(60, min(player_y, WINDOW_HEIGHT - player_height))

        # 弾の移動と描画
        for bullet in bullets:
            bullet[0] += bullet_speed
            draw_bullet(bullet[0], bullet[1])
        
            # 弾が画面外に出たら削除
            if bullet[0] + enemy_width < 0:
                bullets.remove(bullet)

        # 敵の生成
        current_time = pygame.time.get_ticks()
        if current_time - last_enemy_spawn_time > enemy_spawn_interval :
            enemy_y = random.randint(60, WINDOW_HEIGHT - enemy_height)
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
            for bullet in bullets:
                bullet_rect = pygame.Rect(bullet[0], bullet[1], 10, 5)
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

        # 自機の体力が0以下になった場合ゲームオーバーにする
        if player_health <= 0:
            stopper = True
            process_for_seconds(5, game_over)
            running = False
            waiting = True

        # スコアが3000を超えた場合ゲームクリアにする
        if score >= 3000:
            stopper = True
            process_for_seconds(5, game_clear)
            running = False
            waiting = True


        draw_player()
        draw_score()
        draw_health()

        pygame.display.update()
        clock.tick(60)

   


