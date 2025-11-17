import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Класс для корабля игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 30))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

# Класс для пуль
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -10

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

# Класс для врагов (звуки/слоги для логопедии)
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Русские слоги для практики произношения (можно расширить)
        self.syllables = ["ба", "ва", "га", "да", "е", "ё", "жа", "за", "и", "й", "ка", "ла", "ма", "на", "о", "па", "ра", "са", "та", "у", "фа", "ха", "ца", "ча", "ша", "ща", "ю", "я"]
        self.syllable = random.choice(self.syllables)
        self.image = syllable_font.render(self.syllable, True, RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed = random.randint(1, 3)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

# Функция для "произношения" слога (симуляция, вывод в консоль)
def pronounce_syllable(syllable):
    print(f"Произноси: {syllable}!")  # В реальной игре можно интегрировать TTS, например, pyttsx3

# Настройка экрана и шрифта
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Логопедический Космический Стрелок")
clock = pygame.time.Clock()
syllable_font = pygame.font.Font(None, 36)

# Группы спрайтов
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Создание игрока
player = Player()
all_sprites.add(player)

# Переменные игры
score = 0
running = True

# Основной цикл игры
while running:
    clock.tick(FPS)
    
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
    
    # Обновление
    all_sprites.update()
    
    # Создание врагов
    if random.randint(1, 20) == 1:
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)
    
    # Проверка столкновений пуль с врагами
    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for hit in hits:
        score += 10
        pronounce_syllable(hit.syllable)
    
    # Проверка столкновений игрока с врагами
    if pygame.sprite.spritecollideany(player, enemies):
        running = False
    
    # Отрисовка
    screen.fill(BLACK)
    all_sprites.draw(screen)
    
    # Отображение счета
    score_text = pygame.font.Font(None, 36).render(f"Счет: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    
    pygame.display.flip()

pygame.quit()
sys.exit()
