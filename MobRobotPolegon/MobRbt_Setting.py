# -*- coding: utf-8 -*-
"""
Модуль содержит класс для хранения всех параметров полегона и роботов
"""
import numpy as np                            # Для работы с массивами элементов одного типа

class Settings():
    """Класс для хранения всех настроек параметров полегона и роботов."""
    def __init__(self):
        """Инициализирует настройки полегона и роботов."""
        
        # Параметры экрана
        self.screen_width = 1200              # ширина поля
        self.screen_height = 800              # высота поля
        self.bg_color = (230, 230, 230)       # цвет фона
        
        self.kps  = 40                        # Колич.смены кадров в секунду        
        
        
        # Препятствия
        self.pr_color = (100, 120, 120)       # цвет припятствий   
        
        # Образующие точки препятствий (неподвижных)        
        self.pr1  = np.array([[200,  75], [225,  75], [225, 150], [250, 150], 
                              [250, 175], [200, 175]],  dtype = 'int')
        
        self.pr2  = np.array([[375, 100], [400, 100], [400, 275], [350, 275], 
                              [350, 250], [375, 250]],  dtype = 'int')
        
        self.pr3  = np.array([[125, 275], [250, 275], [250, 350], [225, 350], 
                              [225, 300], [125, 300]],  dtype = 'int')
        
        self.pr4  = np.array([[ 50, 175], [ 75, 175], [ 75, 200], [ 50, 200]],
                             dtype = 'int')
        
        self.pr5  = np.array([[ 50, 450], [150, 450], [150, 575], [250, 575], 
                              [250, 600], [125, 600], [125, 475], [ 50, 475]],  
                             dtype = 'int')
        
        self.pr6  = np.array([[350, 450], [400, 450], [400, 500], [375, 500],
                              [375, 475], [350, 475]],  dtype = 'int')
        
        self.pr7  = np.array([[125, 675], [150, 675], [150, 750], [125, 750],
                              [125, 725], [100, 725], [100, 700], [125, 700]],  
                             dtype = 'int')
        
        self.pr8  = np.array([[325, 675], [400, 675], [400, 700], [350, 700],
                              [350, 725], [275, 725], [275, 700], [325, 700]],  
                             dtype = 'int')
        
        self.pr9  = np.array([[500, 100], [700, 100], [700, 125], [525, 125],
                              [525, 200], [500, 200]],  dtype = 'int')
        
        self.pr10 = np.array([[600, 200], [625, 200], [625, 350], [525, 350],
                              [525, 325], [600, 325]],  dtype = 'int')
        
        self.pr11 = np.array([[550, 450], [600, 450], [600, 475], [575, 475],
                              [575, 525], [525, 525], [525, 550], [500, 550], 
                              [500, 500], [550, 500]],  dtype = 'int')
        
        self.pr12 = np.array([[675, 550], [700, 550], [700, 675], [675, 675],
                              [675, 625], [625, 625], [625, 600], [675, 600]],
                             dtype = 'int')
        
        self.pr13 = np.array([[500, 675], [550, 675], [550, 700], [575, 700],
                              [575, 725], [525, 725], [525, 700], [500, 700]],
                             dtype = 'int')
        
        self.pr14 = np.array([[800,  25], [825,  25], [825,  75], [875,  75],
                              [875, 100], [800, 100]], dtype = 'int')
        
        self.pr15 = np.array([[1025, 100], [1125, 100], [1125, 125], [1025, 125]],
                             dtype = 'int')
        
        self.pr16 = np.array([[800, 250], [825, 250], [825, 275], [925, 275],
                              [925, 200], [950, 200], [950, 350], [925, 350], 
                              [925, 300], [800, 300]],  dtype = 'int')
        
        self.pr17 = np.array([[1075, 250], [1100, 250], [1100, 325], [1175, 325],
                              [1175, 350], [1075, 350]], dtype = 'int')
        
        self.pr18 = np.array([[800, 450], [875, 450], [875, 475], [825, 475],
                              [825, 525], [800, 525]], dtype = 'int')
        
        self.pr19 = np.array([[1025, 450], [1050, 450], [1050, 550], [1075, 550],
                              [1075, 575], [1000, 575], [1000, 550], [1025, 550]], 
                             dtype = 'int')
        
        self.pr20 = np.array([[800, 650], [925, 650], [925, 675], [900, 675],
                              [900, 775], [875, 775], [875, 675], [800, 675]], 
                             dtype = 'int')
        
        self.pr21 = np.array([[1025, 725], [1050, 725], [1050, 775], [1025, 775]],
                             dtype = 'int')
                
        self.pr22 = np.array([[1150, 625], [1175, 625], [1175, 650], [1150, 650]],
                             dtype = 'int')
        
                        
        # Базовые точки препятствий (подвижных)      
        self.prDv1 = np.array([[  0,   0], [ 25,   0], [ 25,  50], [ 75,  50], 
                               [ 75,  25], [100,  25], [100,  50], [150,  50], 
                               [150,  75], [100,  75], [100, 100], [ 75, 100],                               
                               [ 75,  75], [  0,  75]],  dtype = 'float32')
        self.prDv1_dX = 0                     # начальное смещение по оси X
        self.prDv1_dY = 350                   # начальное смещение по оси Y
        self.prDv1_Vx = 0.2                   # скорость перемещю по оси X
        self.prDv1_Vy = 0                     # скорость перемещю по оси Y        
        
        self.prDv2 = np.array([[  0,   0], [ 75,   0], [ 75,  25], [ 50,  25], 
                               [ 50,  75], [100,  75], [100, 100], [ 25, 100], 
                               [ 25,  25], [  0,  25]],  dtype = 'float32')
        self.prDv2_dX = 400                   # начальное смещение по оси X
        self.prDv2_dY = 0                     # начальное смещение по оси Y
        self.prDv2_Vx = 0                     # скорость перемещю по оси X
        self.prDv2_Vy = 0.3                   # скорость перемещю по оси Y                
        
        self.prDv3 = np.array([[  0,   0], [ 25,  25], [ 75,  25], [ 75,  75], 
                               [100, 100], [100, 125], [ 75, 100], [ 50, 100], 
                               [ 25, 125], [  0, 125], [  0, 100], [ 25, 100],
                               [ 50,  75], [ 50,  50], [ 25,  50], [  0,  25]],
                              dtype = 'float32')
        self.prDv3_dX = 700                   # начальное смещение по оси X
        self.prDv3_dY = 400                   # начальное смещение по оси Y
        self.prDv3_Vx = 0                     # скорость перемещю по оси X
        self.prDv3_Vy = 0.1                   # скорость перемещю по оси Y                
    
        # Протокол эксперимента   
        """ Столбцы:
              - 0 - Время  [c]                 (dT) 
              - 1 - Коорд. x робота [пкс]      (RB1.x_pos)
              - 2 - Коорд. y робота [пкс]      (RB1.y_pos)            
              - 3 - Дальность до цели  [пкс]   (RB1.D) 
              - 4 - Пеленг цели  [пи-рад]      (RB1.At/math.pi) 
              - 5 - Курс.угол робота  [пи-рад] (RB1.fi/math.pi)
              - 6 - Скорость робота  [пкс/с]   (RB1.Vr) 
              - 7 - Угл.скор. робота  [рад/с]  (RB1.Wr) 
              - 8 - Флаг столкновений с преп.  (RB1.StlknPr)
        """      
        self.PrtklExpr = np.zeros((1, 9), dtype = 'float32')
        
 
 