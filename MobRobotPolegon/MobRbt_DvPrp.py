"""
Модуль содержит класс движущихся препятствий для полегона
"""
import pygame  # Управл. графикой, анимацией, звуком


class DvPrp():
    """Класс движущиеся препятствия"""

    def __init__(self, prDv, prDv_dX, prDv_dY, prVx, prVy, SetPlg):
        """Инициализирует положение препятствия на полегоне"""

        self.prDv = prDv + [prDv_dX, prDv_dY]  # базовые точки текущего полож.преп.
        self.prVx = prVx  # сост.скорости Vx перемещ.преп.
        self.prVy = prVy  # сост.скорости Vy перемещ.преп.
        self.prClr = SetPlg.pr_color  # цвет отображения препятствия
        self.scr_width = SetPlg.screen_width  # ширина поля
        self.scr_height = SetPlg.screen_height  # высота поля

    def update(self, screen):
        """ Рисует препятствие в текущей позиции """

        pygame.draw.polygon(screen, self.prClr, self.prDv)

    def MovPr(self, screen):
        """ Движение препятствия """

        self.prDv += [self.prVx, self.prVy]  # смещение препятствия

        if self.prDv[:, 0].min() <= 0 or self.prDv[:, 0].max() >= self.scr_width:
            self.prVx = -self.prVx

        if self.prDv[:, 1].min() <= 0 or self.prDv[:, 1].max() >= self.scr_height:
            self.prVy = -self.prVy

        self.update(screen)  # отрисовка препятствия
