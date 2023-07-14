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
GOLD = (255,215,0)
GRAY =(128,128,128)

#カラーインデックスの定義
colors = [RED, ORANGE, YELLOW, GREENYELLOW , GREEN]

class position:
	def __init__(self,x,y,width,height,color):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.color = color

	def draw(self, window):
		pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))

#難易度dictの定義
options = [
    {'name': 'Easy', 'difficulty': 'Easy Mode', 'speed': 2},
    {'name': 'Normal', 'difficulty': 'Normal Mode', 'speed': 5},
    {'name': 'Hard', 'difficulty': 'Hard Mode', 'speed': 7}
]

#選択フラグ
selected_option = 0

#ゲーム管理フラグの設定
game_count = 0

#スコアの定義
score = 0

# 自機の設定
player_x = 50 #初期位置のx座標
player_y = WINDOW_HEIGHT // 2 #初期位置のy座標
player_width = 20 #自機の幅
player_height = 20 #自機の高さ
player_health = 1 #自機の体力


# 弾の設定
bullet_width = 10
bullet_height = 5
bullet_speed = 5

#弾の発射間隔設定
bullet_cooldown = 1000  # 弾のクールダウン時間（ミリ秒）
last_shoot_time = 0

#複数の弾の移動管理用
bullets = []

# 敵の幅と高さ
enemy_width = 20
enemy_height = 20

#敵のスポーン間隔設定
enemy_spawn_interval = 2000  #スポーン間隔（ミリ秒）
last_enemy_spawn_time = 0

#複数の敵の移動管理用
enemies = []

#ループフラグ
waiting = True
running = False

# 初期化
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

# フォントの設定
font = pygame.font.Font(None, 36)

#ループフラグ
waiting = True
running = False

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

        drawhealth = position(bar_x, bar_y, bar_width, bar_height, color)

        # バーを描画
        drawhealth.draw(window)



#ゲームオーバーの描画
def game_over():
    game_over_text = font.render("GAME OVER", True, RED)
    score_text = font.render("Score: " + str(score), True, GOLD)
    window.blit(score_text, (WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2))
    window.blit(game_over_text, (WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 - 50))

#スタートメニューの描画    
def start_menu():
    start_text = font.render("Press ENTER to START", True, WHITE)
    end_text = font.render("Press Esc to EXIT", True, WHITE)
    window.blit(start_text, (WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT // 2))
    window.blit(end_text, (WINDOW_WIDTH - 250, WINDOW_HEIGHT - 50))


# 選択肢の描画
def draw_options():
    for i, option in enumerate(options):
        text = font.render(option['name'], True, WHITE if i == selected_option else GRAY)
        text_rect = text.get_rect()
        text_rect.center = (WINDOW_WIDTH // 2, 100 + i * 50)
        pygame.draw.rect(window, WHITE, (text_rect.left - 5, text_rect.top - 5, text_rect.width + 10, text_rect.height + 10), 2)
        window.blit(text, text_rect)

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
        draw_options()
        start_menu()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                waiting = False
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    selected_difficulty = options[selected_option]['difficulty']
                    enemy_speed = options[selected_option]['speed']
                    process_for_seconds(2,start_game)
                    running = True
                    waiting = False
                elif event.key == pygame.K_ESCAPE:
                    running = False
                    waiting = False
                    pygame.quit()
                    exit()
        


    #ゲームのメイン処理
    while running:
        window.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()

 
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

        drawplayer = position(player_x, player_y, player_width, player_height, BLUE)
        drawplayer.draw(window)
        draw_score()
        draw_health()

        # 弾の移動と描画
        for bullet in bullets:
            bullet[0] += bullet_speed
            drawbullet = position(bullet[0], bullet[1], bullet_width, bullet_height, RED)
            drawbullet.draw(window)
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
            drawenemy = position(enemy[0], enemy[1], enemy_width, enemy_height, WHITE)
            drawenemy.draw(window)
        
            # 敵が画面外に出たら削除
            if enemy[0] + enemy_width < 0:
                enemies.remove(enemy)
                score -= 100
                if score <= 0:
                    score = 0

        # 敵と弾の衝突判定
        if len(bullets) != 0:
            for bullet in bullets:
                bullet_rect = pygame.Rect(bullet[0], bullet[1], bullet_width, bullet_height)
                for enemy in enemies:
                    enemy_rect = pygame.Rect(enemy[0], enemy[1], enemy_width, enemy_height)
                    if bullet_rect.colliderect(enemy_rect):
                        enemies.remove(enemy)
                        game_count += 1
                        score +=1000
                        break

        #敵と自機の衝突判定  
        if player_health >= 1:
            player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
            for enemy in enemies:
                enemy_rect = pygame.Rect(enemy[0], enemy[1], enemy_width, enemy_height)
                if player_rect.colliderect(enemy_rect):
                
                    enemies.remove(enemy)

                    score -= 500
                    if score <= 0:
                        score = 0
                    player_health -= 1
                    break         

        # 自機の体力が0以下になった場合ゲームオーバーにする
        if player_health <= 0:
            running = False
            process_for_seconds(5,game_over)
            
           
            #ゲーム管理フラグのリセット
            game_count = 0

            # スコアのリセット
            score = 0

            player_health = 1 #自機の体力のリセット

            #弾リストのリセット
            bullets.clear()

            #敵リストのリセット
            enemies.clear()

            waiting = True

            

        pygame.display.update()
        clock.tick(60)

