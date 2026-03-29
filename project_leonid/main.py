"""
PyQuest — 2D платформер для обучения Python
Запуск: python main.py
Зависимости: pip install pygame
"""

import pygame
import sys
import math
import random
from quests import QUESTS
from ui import QuestPanel, HUD, StartScreen, DeathScreen

pygame.init()

SCREEN_W, SCREEN_H = 1100, 650
FPS = 60

# Цвета
C = {
    "bg_top":     (10, 10, 26),
    "bg_bot":     (15, 15, 40),
    "platform":   (22, 22, 58),
    "plat_top":   (50, 50, 120),
    "player":     (70, 70, 255),
    "player_d":   (40, 40, 180),
    "eye":        (220, 220, 255),
    "pupil":      (20, 20, 60),
    "bug":        (255, 80, 80),
    "bug_glow":   (255, 40, 40),
    "coin_ok":    (100, 255, 160),
    "star":       (100, 100, 200),
    "text":       (200, 200, 255),
    "text_dim":   (100, 100, 160),
    "xp":         (255, 210, 60),
    "hp":         (255, 80, 80),
    "white":      (255, 255, 255),
    "black":      (0, 0, 0),
    "particle_b": (80, 80, 255),
    "particle_g": (100, 255, 160),
    "particle_r": (255, 100, 100),
}

class Star:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = random.randint(0, SCREEN_W)
        self.y = random.randint(0, SCREEN_H)
        self.r = random.uniform(0.5, 2.0)
        self.phase = random.uniform(0, math.pi * 2)
        self.speed = random.uniform(0.5, 2.0)

    def draw(self, surf, t):
        a = int(80 + 60 * math.sin(t * self.speed + self.phase))
        col = (min(255, C["star"][0] + a // 2),
               min(255, C["star"][1] + a // 2),
               min(255, C["star"][2] + a))
        pygame.draw.circle(surf, col, (int(self.x), int(self.y)), int(self.r))


class Particle:
    def __init__(self, x, y, color):
        self.x, self.y = x, y
        self.color = color
        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(2, 6)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed - 3
        self.life = 1.0
        self.size = random.randint(3, 7)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.2
        self.life -= 0.035
        return self.life > 0

    def draw(self, surf):
        a = int(self.life * 255)
        col = tuple(min(255, c) for c in self.color)
        s = max(1, int(self.size * self.life))
        surf = surf  # noqa
        pygame.draw.rect(surf, col,
                         (int(self.x) - s // 2, int(self.y) - s // 2, s, s))


class FloatingText:
    def __init__(self, x, y, text, color, big=False):
        self.x, self.y = float(x), float(y)
        self.text = text
        self.color = color
        self.life = 1.0
        self.big = big

    def update(self):
        self.y -= 1.2
        self.life -= 0.025
        return self.life > 0

    def draw(self, surf, font_sm, font_md):
        a = int(self.life * 255)
        col = (*self.color[:3], a)
        font = font_md if self.big else font_sm
        txt = font.render(self.text, True, self.color)
        txt.set_alpha(a)
        surf.blit(txt, (int(self.x) - txt.get_width() // 2, int(self.y)))


class Platform:
    def __init__(self, x, y, w, h=16, is_ground=False):
        self.rect = pygame.Rect(x, y, w, h)
        self.is_ground = is_ground

    def draw(self, surf):
        r = self.rect
        pygame.draw.rect(surf, C["platform"], r, border_radius=4)
        pygame.draw.rect(surf, C["plat_top"],
                         pygame.Rect(r.x, r.y, r.w, 3), border_radius=4)
        # Декор: «плиты»
        if not self.is_ground:
            for tx in range(r.x + 10, r.x + r.w - 10, 30):
                pygame.draw.rect(surf, (30, 30, 70),
                                 pygame.Rect(tx, r.y + 5, 16, 5), border_radius=2)


class BugCoin:
    """Монета-баг, при подборе открывает квест."""
    RADIUS = 16

    def __init__(self, x, y, quest_idx):
        self.x, self.y = float(x), float(y)
        self.quest_idx = quest_idx
        self.collected = False
        self.phase = random.uniform(0, math.pi * 2)
        self.solved = False  # стал зелёным после решения

    @property
    def rect(self):
        r = self.RADIUS
        return pygame.Rect(self.x - r, self.cy - r, r * 2, r * 2)

    @property
    def cy(self):
        return self.y + math.sin(self.phase) * 6

    def update(self, dt):
        self.phase += dt * 2.5

    def draw(self, surf, font_tiny, t):
        if self.collected:
            return
        cy = int(self.cy)
        color = C["coin_ok"] if self.solved else C["bug"]
        glow_col = (50, 200, 100) if self.solved else C["bug_glow"]

        # Свечение
        glow = pygame.Surface((80, 80), pygame.SRCALPHA)
        pygame.draw.circle(glow, (*glow_col, 40), (40, 40), 30)
        surf.blit(glow, (int(self.x) - 40, cy - 40))

        pygame.draw.circle(surf, color, (int(self.x), cy), self.RADIUS)
        pygame.draw.circle(surf, C["white"], (int(self.x), cy), self.RADIUS, 2)

        label = "OK" if self.solved else "BUG"
        txt = font_tiny.render(label, True, C["white"])
        surf.blit(txt, (int(self.x) - txt.get_width() // 2,
                        cy - txt.get_height() // 2))

        # Название квеста под монетой
        q_name = QUESTS[self.quest_idx]["name"][:14]
        name_txt = font_tiny.render(q_name, True, C["text_dim"])
        surf.blit(name_txt, (int(self.x) - name_txt.get_width() // 2, cy + 22))


class Player:
    W, H = 26, 38
    SPEED = 220
    JUMP = -600      # сильнее прыжок
    GRAVITY = 1000   # чуть мягче гравитация → выше прыжок
    COYOTE = 0.15    # чуть больше прощения у края

    def __init__(self, x, y):
        self.x, self.y = float(x), float(y)
        self.vx, self.vy = 0.0, 0.0
        self.on_ground = False
        self.coyote_time = 0.0
        self.facing = 1
        self.walk_phase = 0.0
        self.jump_squish = 0.0
        self.land_squish = 0.0

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.W, self.H)

    def update(self, dt, keys, platforms):
        # Горизонталь
        ax = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            ax = -self.SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            ax = self.SPEED
        self.vx = ax
        if ax:
            self.facing = 1 if ax > 0 else -1
            self.walk_phase += dt * 9

        # Прыжок
        jump = keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_SPACE]
        if jump and self.coyote_time > 0:
            self.vy = self.JUMP
            self.coyote_time = 0
            self.jump_squish = 0.3

        # Гравитация
        self.vy += self.GRAVITY * dt
        self.vy = min(self.vy, 900)

        # Движение и коллизии
        self.x += self.vx * dt
        self._collide_x(platforms)
        self.y += self.vy * dt
        was_grounded = self.on_ground
        self.on_ground = False
        self._collide_y(platforms)

        if self.on_ground:
            self.coyote_time = self.COYOTE
            if not was_grounded:
                self.land_squish = 0.25
        else:
            self.coyote_time = max(0, self.coyote_time - dt)

        # Границы экрана
        self.x = max(0, min(self.x, SCREEN_W - self.W))

        # Анимационные затухания
        self.jump_squish = max(0, self.jump_squish - dt * 4)
        self.land_squish = max(0, self.land_squish - dt * 6)

    def _collide_x(self, platforms):
        pr = self.rect
        for p in platforms:
            if pr.colliderect(p.rect):
                if self.vx > 0:
                    self.x = p.rect.left - self.W
                elif self.vx < 0:
                    self.x = p.rect.right

    def _collide_y(self, platforms):
        pr = self.rect
        for p in platforms:
            if pr.colliderect(p.rect):
                if self.vy > 0:
                    self.y = p.rect.top - self.H
                    self.vy = 0
                    self.on_ground = True
                elif self.vy < 0:
                    self.y = p.rect.bottom
                    self.vy = 0

    def draw(self, surf):
        cx = int(self.x + self.W // 2)
        cy = int(self.y + self.H // 2)
        f = self.facing

        squish_y = 1.0 + self.land_squish - self.jump_squish
        squish_x = 1.0 - self.land_squish * 0.5 + self.jump_squish * 0.2
        dw = int(self.W * squish_x)
        dh = int(self.H * squish_y)

        body = pygame.Surface((dw, dh), pygame.SRCALPHA)
        # Тело
        pygame.draw.rect(body, C["player"],
                         (0, 0, dw, dh), border_radius=7)
        # Шлем
        pygame.draw.rect(body, C["player_d"],
                         (2, 0, dw - 4, dh // 2), border_radius=7)
        # Ноги
        leg_off = int(math.sin(self.walk_phase) * 5) if self.on_ground else 0
        leg_color = (50, 50, 160)
        pygame.draw.rect(body, leg_color,
                         (2, dh - 10, 9, 10 + leg_off))
        pygame.draw.rect(body, leg_color,
                         (dw - 11, dh - 10, 9, 10 - leg_off))

        surf.blit(body, (cx - dw // 2, cy - dh // 2))

        # Глаз
        ex = cx + f * 5
        ey = int(self.y + 10)
        pygame.draw.circle(surf, C["eye"], (ex, ey), 5)
        pygame.draw.circle(surf, C["pupil"], (ex + f, ey), 3)

        # Тень
        shadow = pygame.Surface((self.W + 10, 8), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow, (0, 0, 0, 60), (0, 0, self.W + 10, 8))
        surf.blit(shadow, (cx - (self.W + 10) // 2,
                           int(self.y + self.H + 2)))


class Level:
    def __init__(self, level_idx):
        self.idx = level_idx
        self.platforms = []
        self.coins = []
        self._generate()

    def _generate(self):
        ground_y = SCREEN_H - 70
        self.platforms.append(Platform(0, ground_y, SCREEN_W, 70, is_ground=True))

        # Физика прыжка: JUMP=-600, GRAVITY=1000
        # Максимальная высота прыжка: v²/(2g) = 600²/2000 ≈ 180 px
        # Максимальное горизонтальное смещение за прыжок: SPEED * 2*(v/g) ≈ 220 * 1.2 ≈ 264 px
        MAX_JUMP_H = 155   # с запасом (платформы имеют ненулевую толщину)
        MAX_JUMP_X = 240   # горизонталь за один прыжок

        count = 9 + self.idx * 2
        placed = [(0, ground_y, SCREEN_W)]  # (x, y, w) — стартовый список

        attempts = 0
        while len(placed) - 1 < count and attempts < 600:
            attempts += 1

            # Выбираем случайную уже размещённую платформу как «точку отправки»
            src = random.choice(placed)
            src_x, src_y, src_w = src

            # Ширина и размер новой платформы
            pw = random.randint(110, 200)

            # Горизонталь: прыгаем влево или вправо от src
            side = random.choice([-1, 1])
            gap = random.randint(30, MAX_JUMP_X - pw - 10)
            if side == 1:
                px = src_x + src_w + gap
            else:
                px = src_x - pw - gap

            # Вертикаль: платформа выше или немного ниже src
            # Вверх не больше MAX_JUMP_H; вниз свободно (падаем)
            dy = random.randint(-MAX_JUMP_H, 80)
            py = src_y + dy

            # Ограничения экрана
            if px < 20 or px + pw > SCREEN_W - 20:
                continue
            if py < 80 or py > ground_y - 60:
                continue

            # Проверка на перекрытие с другими платформами
            nr = pygame.Rect(px - 15, py - 50, pw + 30, 100)
            if any(nr.colliderect(pygame.Rect(p[0]-15, p[1]-50, p[2]+30, 100))
                   for p in placed):
                continue

            placed.append((px, py, pw))
            self.platforms.append(Platform(px, py, pw))

        # Гарантируем хотя бы 4 платформы если генератор не справился
        if len(self.platforms) < 3:
            ground_y = SCREEN_H - 70
            for px in [150, 400, 650, 900]:
                py = ground_y - random.randint(110, 170)
                self.platforms.append(Platform(px, py, 160))

        # Монеты-баги на платформах (не на земле)
        q_indices = random.sample(range(len(QUESTS)),
                                  min(len(QUESTS), 4 + self.idx))
        plat_options = self.platforms[1:]  # без земли
        random.shuffle(plat_options)
        for i, qi in enumerate(q_indices):
            p = plat_options[i % len(plat_options)]
            cx = p.rect.centerx + random.randint(-20, 20)
            cx = max(p.rect.left + 10, min(cx, p.rect.right - 10))
            cy = p.rect.top - 28
            self.coins.append(BugCoin(cx, cy, qi))

    @property
    def all_collected(self):
        return all(c.collected for c in self.coins)


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption("PyQuest — Платформер по Python")
        self.clock = pygame.time.Clock()

        self.font_big   = pygame.font.SysFont("Courier New", 36, bold=True)
        self.font_md    = pygame.font.SysFont("Courier New", 22, bold=True)
        self.font_sm    = pygame.font.SysFont("Courier New", 16)
        self.font_tiny  = pygame.font.SysFont("Courier New", 12, bold=True)

        self.stars = [Star() for _ in range(100)]
        self.particles: list[Particle] = []
        self.floats: list[FloatingText] = []

        self.state = "start"  # start | play | quest | death | win
        self.score = 0
        self.lives = 3
        self.level_idx = 0
        self.level = None
        self.player = None
        self.t = 0.0

        self.hud = HUD(self.font_sm, self.font_md, self.font_tiny)
        self.quest_panel = QuestPanel(self.font_md, self.font_sm, self.font_tiny)
        self.start_screen = StartScreen(self.font_big, self.font_md, self.font_sm)
        self.death_screen = DeathScreen(self.font_big, self.font_md)

        self.active_quest = None
        self.current_coin = None

    def new_level(self):
        self.level = Level(self.level_idx)
        spawn = self.level.platforms[0]  # земля
        self.player = Player(80, spawn.rect.top - Player.H)

    def spawn_particles(self, x, y, color, n=16):
        for _ in range(n):
            self.particles.append(Particle(x, y, color))

    def add_float(self, x, y, text, color, big=False):
        self.floats.append(FloatingText(x, y, text, color, big))

    def run(self):
        while True:
            dt = self.clock.tick(FPS) / 1000.0
            dt = min(dt, 0.05)
            self.t += dt
            self.handle_events()
            self.update(dt)
            self.draw()
            pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == "quest":
                        self._skip_quest()
                    else:
                        pygame.quit()
                        sys.exit()

            if self.state == "start":
                if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                    self._start_game()

            elif self.state == "quest":
                result = self.quest_panel.handle_event(event)
                if result == "correct":
                    self._quest_correct()
                elif result == "wrong":
                    self._quest_wrong()
                elif result == "skip":
                    self._skip_quest()
                elif result == "continue":
                    self.state = "play"

            elif self.state == "death":
                if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                    self._start_game()

    def _start_game(self):
        self.score = 0
        self.lives = 3
        self.level_idx = 0
        self.new_level()
        self.state = "play"

    def _quest_correct(self):
        xp = self.active_quest["xp"]
        self.score += xp
        cx, cy = int(self.current_coin.x), int(self.current_coin.cy)
        self.spawn_particles(cx, cy, C["coin_ok"])
        self.add_float(cx, cy - 30, f"+{xp} XP!", C["coin_ok"], big=True)
        self.current_coin.solved = True

    def _quest_wrong(self):
        self.lives -= 1
        cx, cy = int(self.current_coin.x), int(self.current_coin.cy)
        self.spawn_particles(cx, cy, C["particle_r"])
        self.add_float(cx, cy - 30, "-1 жизнь", C["hp"])
        if self.lives <= 0:
            self.state = "death"

    def _skip_quest(self):
        self.state = "play"
        self.quest_panel.close()

    def update(self, dt):
        # Обновляем частицы и плашки
        self.particles = [p for p in self.particles if p.update()]
        self.floats = [f for f in self.floats if f.update()]

        if self.state != "play":
            return

        keys = pygame.key.get_pressed()
        self.player.update(dt, keys, self.level.platforms)

        # Падение в яму
        if self.player.y > SCREEN_H + 50:
            self.lives -= 1
            self.add_float(SCREEN_W // 2, SCREEN_H // 2, "Упал! -1 ♥", C["hp"], big=True)
            self.spawn_particles(self.player.x, SCREEN_H, C["particle_r"])
            if self.lives <= 0:
                self.state = "death"
            else:
                ground = self.level.platforms[0]
                self.player.x = 80
                self.player.y = ground.rect.top - Player.H
                self.player.vy = 0

        # Монеты
        for coin in self.level.coins:
            coin.update(dt)
            if not coin.collected and self.player.rect.colliderect(coin.rect):
                coin.collected = True
                self.current_coin = coin
                self.active_quest = QUESTS[coin.quest_idx]
                self.quest_panel.open(self.active_quest)
                self.state = "quest"

        # Уровень пройден
        if self.level.all_collected:
            bonus = 150
            self.score += bonus
            self.add_float(SCREEN_W // 2, SCREEN_H // 3,
                           f"Уровень {self.level_idx + 1} пройден! +{bonus} XP",
                           C["xp"], big=True)
            self.spawn_particles(SCREEN_W // 2, SCREEN_H // 2, C["coin_ok"], 30)
            self.level_idx += 1
            if self.level_idx >= 5:
                self.state = "win"
            else:
                self.new_level()

    def draw(self):
        # Фон
        self.screen.fill(C["bg_top"])
        for s in self.stars:
            s.draw(self.screen, self.t)

        if self.state == "start":
            self.start_screen.draw(self.screen, self.t)
            return

        if self.state == "death":
            self.death_screen.draw(self.screen, self.score, self.t)
            return

        if self.state in ("play", "quest"):
            # Платформы
            for p in self.level.platforms:
                p.draw(self.screen)
            # Монеты
            for c in self.level.coins:
                c.draw(self.screen, self.font_tiny, self.t)
            # Игрок
            self.player.draw(self.screen)

        # Частицы и плашки
        for p in self.particles:
            p.draw(self.screen)
        for f in self.floats:
            f.draw(self.screen, self.font_sm, self.font_md)

        # HUD
        self.hud.draw(self.screen, self.score, self.lives,
                      self.level_idx + 1, len(self.level.coins),
                      sum(1 for c in self.level.coins if c.collected))

        # Квест-панель
        if self.state == "quest":
            self.quest_panel.draw(self.screen)

        # Win
        if self.state == "win":
            self._draw_win()

    def _draw_win(self):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 20, 200))
        self.screen.blit(overlay, (0, 0))
        t1 = self.font_big.render("🏆 Ты победил! 🏆", True, C["xp"])
        t2 = self.font_md.render(f"Финальный счёт: {self.score} XP", True, C["text"])
        t3 = self.font_sm.render("Нажми любую клавишу для новой игры", True, C["text_dim"])
        self.screen.blit(t1, (SCREEN_W // 2 - t1.get_width() // 2, 200))
        self.screen.blit(t2, (SCREEN_W // 2 - t2.get_width() // 2, 270))
        self.screen.blit(t3, (SCREEN_W // 2 - t3.get_width() // 2, 330))
        for event in pygame.event.get(pygame.KEYDOWN):
            self._start_game()


if __name__ == "__main__":
    game = Game()
    game.run()
