"""
UI-компоненты PyQuest.
QuestPanel, HUD, StartScreen, DeathScreen.
"""

import pygame
import math
import random

SCREEN_W, SCREEN_H = 1100, 650

# Цветовая палитра
C = {
    "bg":         (10,  10,  26),
    "panel_bg":   (14,  14,  34),
    "panel_bd":   (60,  60,  180),
    "panel_bd2":  (40,  40,  120),
    "text":       (200, 200, 255),
    "text_dim":   (100, 100, 160),
    "text_hint":  (80,  80,  130),
    "code_bg":    (8,   8,   20),
    "code_ok":    (100, 200, 140),
    "code_bug":   (255, 90,  90),
    "code_hint":  (240, 200, 80),
    "code_text":  (180, 180, 240),
    "opt_bg":     (10,  10,  28),
    "opt_bd":     (40,  40,  90),
    "opt_hover":  (25,  25,  60),
    "opt_bd_hov": (90,  90,  200),
    "correct":    (80,  220, 130),
    "wrong":      (230, 70,  70),
    "xp":         (255, 210, 60),
    "hp":         (255, 80,  80),
    "accent":     (70,  70,  220),
    "white":      (255, 255, 255),
    "black":      (0,   0,   0),
    "topic":      (120, 120, 255),
    "hint_bd":    (40,  40,  100),
    "hint_bg":    (12,  12,  30),
}

PANEL_W = 760
PANEL_H = 500


def draw_rounded_rect(surf, color, rect, radius=10, border=0, border_color=None):
    pygame.draw.rect(surf, color, rect, border_radius=radius)
    if border and border_color:
        pygame.draw.rect(surf, border_color, rect, border, border_radius=radius)


class Button:
    def __init__(self, x, y, w, h, text, font,
                 color_bd=None, color_text=None, color_bg=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.font = font
        self.color_bd   = color_bd   or C["opt_bd"]
        self.color_text = color_text or C["text"]
        self.color_bg   = color_bg   or C["opt_bg"]
        self.hovered = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

    def draw(self, surf):
        bg = C["opt_hover"] if self.hovered else self.color_bg
        bd = C["opt_bd_hov"] if self.hovered else self.color_bd
        draw_rounded_rect(surf, bg, self.rect, radius=8, border=1, border_color=bd)
        txt = self.font.render(self.text, True, self.color_text)
        surf.blit(txt, (self.rect.centerx - txt.get_width() // 2,
                        self.rect.centery - txt.get_height() // 2))


class OptionButton:
    H = 52

    def __init__(self, x, y, w, text, font, correct):
        self.rect = pygame.Rect(x, y, w, self.H)
        self.lines = text.split("\n")
        self.font = font
        self.correct = correct
        self.hovered = False
        self.state = "normal"  # normal | correct | wrong

    def handle_event(self, event):
        if self.state != "normal":
            return False
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

    def draw(self, surf):
        if self.state == "correct":
            bg, bd, tc = (15, 50, 30), C["correct"], C["correct"]
        elif self.state == "wrong":
            bg, bd, tc = (50, 15, 15), C["wrong"], C["wrong"]
        else:
            bg = C["opt_hover"] if self.hovered else C["opt_bg"]
            bd = C["opt_bd_hov"] if self.hovered else C["opt_bd"]
            tc = C["text"]

        draw_rounded_rect(surf, bg, self.rect, radius=8, border=1, border_color=bd)

        # Маркер
        marker_col = bd
        pygame.draw.circle(surf, marker_col,
                           (self.rect.x + 16, self.rect.centery), 5)

        total_h = len(self.lines) * self.font.get_linesize()
        start_y = self.rect.centery - total_h // 2
        for i, line in enumerate(self.lines):
            txt = self.font.render(line, True, tc)
            surf.blit(txt, (self.rect.x + 32, start_y + i * self.font.get_linesize()))


class QuestPanel:
    def __init__(self, font_md, font_sm, font_tiny):
        self.font_md   = font_md
        self.font_sm   = font_sm
        self.font_tiny = font_tiny
        self.visible = False
        self.quest = None

        self.answered = False
        self.correct_answered = False
        self.hint_shown = False
        self.buttons: list[OptionButton] = []
        self.btn_hint   = None
        self.btn_skip   = None
        self.btn_cont   = None
        self._result    = None  # "correct" | "wrong" | "skip" | "continue"

        self._build_static_buttons()

    def _build_static_buttons(self):
        px = (SCREEN_W - PANEL_W) // 2
        py = (SCREEN_H - PANEL_H) // 2
        bottom = py + PANEL_H - 18
        self.btn_hint = Button(px + 10, bottom - 38, 130, 36, "[ Подсказка ]",
                               self.font_tiny, C["hint_bd"], C["text_hint"])
        self.btn_skip = Button(px + 150, bottom - 38, 110, 36, "[ Пропуск ]",
                               self.font_tiny, C["wrong"], C["wrong"])
        self.btn_cont = Button(px + 270, bottom - 38, 180, 36, "[ Продолжить → ]",
                               self.font_tiny, C["correct"], C["correct"])

    def open(self, quest):
        self.quest = quest
        self.visible = True
        self.answered = False
        self.correct_answered = False
        self.hint_shown = False
        self._result = None
        self._build_options()

    def close(self):
        self.visible = False

    def _build_options(self):
        px = (SCREEN_W - PANEL_W) // 2
        py = (SCREEN_H - PANEL_H) // 2

        opts = list(self.quest["options"])
        random.shuffle(opts)

        col_w = (PANEL_W - 30) // 2
        gap = 8
        start_y = py + 280

        self.buttons = []
        for i, opt in enumerate(opts):
            col = i % 2
            row = i // 2
            ox = px + 10 + col * (col_w + 10)
            oy = start_y + row * (OptionButton.H + gap)
            self.buttons.append(
                OptionButton(ox, oy, col_w, opt["text"], self.font_tiny, opt["correct"])
            )

    def handle_event(self, event):
        if not self.visible:
            return None

        # Кнопки-опции
        if not self.answered:
            for btn in self.buttons:
                if btn.handle_event(event):
                    self.answered = True
                    if btn.correct:
                        btn.state = "correct"
                        self.correct_answered = True
                        return "correct"
                    else:
                        btn.state = "wrong"
                        self.hint_shown = True
                        return "wrong"

        # Подсказка
        if self.btn_hint.handle_event(event):
            self.hint_shown = True

        # Продолжить
        if self.answered and self.btn_cont.handle_event(event):
            self.close()
            return "continue"

        # Пропуск
        if self.btn_skip.handle_event(event):
            self.close()
            return "skip"

        return None

    def draw(self, surf):
        if not self.visible or not self.quest:
            return

        # Затемнение фона
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 20, 210))
        surf.blit(overlay, (0, 0))

        px = (SCREEN_W - PANEL_W) // 2
        py = (SCREEN_H - PANEL_H) // 2

        # Панель
        draw_rounded_rect(surf, C["panel_bg"],
                          pygame.Rect(px, py, PANEL_W, PANEL_H),
                          radius=14, border=2, border_color=C["panel_bd"])

        q = self.quest
        x = px + 18
        y = py + 16

        # Тема
        topic_txt = self.font_tiny.render(
            f"● {q['topic']}  ·  +{q['xp']} XP", True, C["topic"])
        surf.blit(topic_txt, (x, y))
        y += 22

        # Название
        name_txt = self.font_md.render(q["name"], True, C["text"])
        surf.blit(name_txt, (x, y))
        y += 32

        # Описание
        for line in q["desc"].split("\n"):
            dl = self.font_sm.render(line, True, C["text_dim"])
            surf.blit(dl, (x, y))
            y += 20
        y += 6

        # Блок кода
        code_rect = pygame.Rect(px + 10, y, PANEL_W - 20, 20 + len(q["code"]) * 22)
        draw_rounded_rect(surf, C["code_bg"], code_rect, radius=8,
                          border=1, border_color=C["panel_bd2"])
        cy = y + 10
        for line_text, line_type in q["code"]:
            if line_type == "bug":
                col = C["code_bug"]
                # Подсветка строки
                pygame.draw.rect(surf, (60, 10, 10),
                                 pygame.Rect(px + 11, cy - 2, PANEL_W - 22, 20))
            elif line_type == "hint":
                col = C["code_hint"]
            elif line_type == "ok":
                col = C["code_ok"]
            else:
                col = C["code_text"]
            ct = self.font_tiny.render(line_text, True, col)
            surf.blit(ct, (x + 6, cy))
            if line_type == "bug":
                # Маркер ошибки
                err = self.font_tiny.render("← BUG", True, C["code_bug"])
                surf.blit(err, (px + PANEL_W - err.get_width() - 20, cy))
            cy += 22
        y = code_rect.bottom + 10

        # Подсказка
        if self.hint_shown:
            hint_rect = pygame.Rect(px + 10, y, PANEL_W - 20,
                                    10 + len(q["hint"].split("\n")) * 18)
            draw_rounded_rect(surf, C["hint_bg"], hint_rect, radius=6,
                              border=1, border_color=C["hint_bd"])
            hy = y + 6
            for hl in q["hint"].split("\n"):
                ht = self.font_tiny.render(hl, True, C["text_hint"])
                surf.blit(ht, (px + 18, hy))
                hy += 18
            y = hint_rect.bottom + 6

        # Объяснение после ответа
        if self.answered and self.correct_answered:
            ex_lines = q["explanation"].split("\n")[:3]
            ey = y + 2
            for el in ex_lines:
                et = self.font_tiny.render(el, True, C["correct"])
                surf.blit(et, (x, ey))
                ey += 17

        # Варианты ответа
        for btn in self.buttons:
            btn.draw(surf)

        # Нижние кнопки
        if not self.answered:
            self.btn_hint.draw(surf)
        self.btn_skip.draw(surf)
        if self.answered:
            self.btn_cont.draw(surf)


class HUD:
    def __init__(self, font_sm, font_md, font_tiny):
        self.font_sm   = font_sm
        self.font_md   = font_md
        self.font_tiny = font_tiny

    def draw(self, surf, score, lives, level, total_coins, collected):
        # Верхняя полоска
        bar = pygame.Surface((SCREEN_W, 42), pygame.SRCALPHA)
        bar.fill((0, 0, 20, 160))
        surf.blit(bar, (0, 0))

        # Уровень
        lv = self.font_sm.render(f"УРОВЕНЬ {level}", True, (100, 100, 200))
        surf.blit(lv, (16, 12))

        # XP
        xp = self.font_md.render(f"XP: {score}", True, (255, 210, 60))
        surf.blit(xp, (SCREEN_W // 2 - xp.get_width() // 2, 10))

        # Жизни
        hearts = "♥ " * lives + "♡ " * (3 - lives)
        hp = self.font_sm.render(hearts.strip(), True, (255, 80, 80))
        surf.blit(hp, (SCREEN_W - hp.get_width() - 16, 12))

        # Прогресс монет
        prog_txt = self.font_tiny.render(
            f"Багов исправлено: {collected} / {total_coins}", True, (80, 80, 160))
        surf.blit(prog_txt, (16, SCREEN_H - 22))

        # Управление
        ctrl = self.font_tiny.render(
            "WASD / ← → — движение   ↑ / Пробел — прыжок   ESC — выход",
            True, (50, 50, 100))
        surf.blit(ctrl, (SCREEN_W // 2 - ctrl.get_width() // 2, SCREEN_H - 22))


class StartScreen:
    def __init__(self, font_big, font_md, font_sm):
        self.font_big = font_big
        self.font_md  = font_md
        self.font_sm  = font_sm
        self.stars = [(random.randint(0, SCREEN_W),
                       random.randint(0, SCREEN_H),
                       random.uniform(0.5, 2.0)) for _ in range(120)]

    def draw(self, surf, t):
        surf.fill((8, 8, 20))

        for sx, sy, sr in self.stars:
            a = int(80 + 60 * math.sin(t * 1.5 + sx))
            c = (min(255, 60 + a // 2), min(255, 60 + a // 2), min(255, 120 + a))
            pygame.draw.circle(surf, c, (sx, sy), int(sr))

        # Заголовок
        pulse = 0.5 + 0.5 * math.sin(t * 2)
        r = int(60 + 40 * pulse)
        g = int(60 + 40 * pulse)
        title = self.font_big.render("PyQuest", True, (r + 60, g + 60, 255))
        surf.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 160))

        sub = self.font_md.render("Платформер · Обучение Python · Исправляй баги",
                                  True, (80, 80, 160))
        surf.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, 220))

        # Описание
        lines = [
            "Собирай красные монеты BUG на платформах",
            "Каждая монета — задание по Python",
            "Правильный ответ → XP  |  Неверный → -1 жизнь",
            "Исправь все баги уровня, чтобы продолжить!",
        ]
        for i, line in enumerate(lines):
            t_col = (60, 60, 120) if i < 2 else (80, 80, 140)
            lt = self.font_sm.render(line, True, t_col)
            surf.blit(lt, (SCREEN_W // 2 - lt.get_width() // 2, 290 + i * 26))

        # Кнопка старт
        blink = int(200 + 55 * math.sin(t * 3))
        start = self.font_md.render("[ Нажми любую клавишу для начала ]",
                                    True, (blink // 2, blink // 2, blink))
        surf.blit(start, (SCREEN_W // 2 - start.get_width() // 2, 420))

        # Управление
        ctrl = self.font_sm.render(
            "WASD / стрелки — движение  |  ↑ / Пробел — прыжок",
            True, (40, 40, 80))
        surf.blit(ctrl, (SCREEN_W // 2 - ctrl.get_width() // 2, 470))


class DeathScreen:
    def __init__(self, font_big, font_md):
        self.font_big = font_big
        self.font_md  = font_md

    def draw(self, surf, score, t):
        surf.fill((10, 0, 0))

        # Мерцание
        pulse = int(100 + 60 * math.sin(t * 3))
        title = self.font_big.render("GAME OVER", True, (255, pulse // 2, pulse // 2))
        surf.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 200))

        sc = self.font_md.render(f"Итоговый счёт: {score} XP", True, (255, 210, 60))
        surf.blit(sc, (SCREEN_W // 2 - sc.get_width() // 2, 280))

        restart = self.font_md.render(
            "Нажми любую клавишу для рестарта", True, (100, 100, 160))
        surf.blit(restart, (SCREEN_W // 2 - restart.get_width() // 2, 340))
