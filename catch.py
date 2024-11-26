import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch the Loot")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Load images
player_img = pygame.image.load("basket.png")
player_img = pygame.transform.scale(player_img, (120, 120))

good_item_imgs = [
    pygame.image.load("apple.png"),
    pygame.image.load("banana.png"),
    pygame.image.load("cherry.png"),
]
good_item_imgs = [pygame.transform.scale(img, (70, 70)) for img in good_item_imgs]

bonus_item_img = pygame.image.load("golden_star.png")
bonus_item_img = pygame.transform.scale(bonus_item_img, (80, 80))

bad_item_img = pygame.image.load("bomb.png")
bad_item_img = pygame.transform.scale(bad_item_img, (120, 120))

# Load sounds
good_sound = pygame.mixer.Sound("good_item.mp3")
bad_sound = pygame.mixer.Sound("bad_item.mp3")
bonus_sound = pygame.mixer.Sound("bonus_item.mp3")

# Player class
class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 80
        self.width = 120
        self.height = 120
        self.speed = 10

    def draw(self):
        screen.blit(player_img, (self.x, self.y))

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < WIDTH - self.width:
            self.x += self.speed

# Item class
class Item:
    def __init__(self, x, y, item_type):
        self.x = x
        self.y = y
        self.item_type = item_type  # "good", "bad", "bonus"
        self.speed = random.randint(3, 6)
        if item_type == "good":
            self.img = random.choice(good_item_imgs)
        elif item_type == "bad":
            self.img = bad_item_img
        elif item_type == "bonus":
            self.img = bonus_item_img

    def draw(self):
        screen.blit(self.img, (self.x, self.y))

    def fall(self):
        self.y += self.speed

# Collision detection
def check_collision(player, item):
    return (
        player.x < item.x + 50 and
        player.x + player.width > item.x and
        player.y < item.y + 50 and
        player.y + player.height > item.y
    )

# Game initialization
player = Player()
items = []
score = 0
level = 1
running = True
game_over = False

while running:
    screen.fill(WHITE)
    keys = pygame.key.get_pressed()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            # Restart the game on 'R'
            score = 0
            level = 1
            items = []
            game_over = False

    if not game_over:
        # Update player
        player.move(keys)
        player.draw()

        # Spawn items
        if random.randint(1, 100) < 3 + level:
            x = random.randint(0, WIDTH - 70)
            item_type = random.choices(
                ["good", "bad", "bonus"], weights=[70, 25, 5], k=1
            )[0]
            items.append(Item(x, 0, item_type))

        # Update items
        for item in items[:]:
            item.fall()
            item.draw()
            if check_collision(player, item):
                if item.item_type == "good":
                    score += 1
                    good_sound.play()
                elif item.item_type == "bad":
                    bad_sound.play()
                    game_over = True  # Game over on bad item
                elif item.item_type == "bonus":
                    score += 5  # Bonus points
                    bonus_sound.play()
                items.remove(item)
            elif item.y > HEIGHT:
                items.remove(item)

        # Display score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        # Level up
        if score // 10 > level - 1:
            level += 1

        # Display level
        level_text = font.render(f"Level: {level}", True, BLACK)
        screen.blit(level_text, (WIDTH - 150, 10))
    else:
        # Game Over Screen
        font = pygame.font.Font(None, 72)
        game_over_text = font.render("GAME OVER", True, RED)
        restart_text = pygame.font.Font(None, 36).render(
            "Press R to Restart or Close Window to Exit", True, BLACK
        )
        screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2 - 50))
        screen.blit(restart_text, (WIDTH // 2 - 250, HEIGHT // 2 + 20))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
