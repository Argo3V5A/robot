# -*- coding: utf-8 -*-
"""
Модуль содержит класс робота
"""
import numpy as np                            # Для работы с массивами элементов одного типа
import math
import pygame                                 # Управл. графикой, анимацией, звуком

pygame.mixer.init()                           # Добавление звука
pop = pygame.mixer.Sound("pop.wav")

class Robot():
    """Класс Робота."""
    
    def __init__(self, Xr, Yr, fi, SetPlg):
        """Инициализирует свойства роботов."""
        
        # Положение робота на экране (начало коорд - верхний левый угол экрана,
        #                             курсовой угол - от 12 часов по час.стрелке )
        self.x_pos = Xr                       # координата x робота
        self.y_pos = Yr                       # координата y робота
        self.fi    = fi                       # [рад] курсовой угол робота 
        
        self.dt = 1/SetPlg.kps                # [c] период дискретизации
 
        # Оформление робота (внешний вид)
        self.f_color = (255,   0,   0)        # фон       - RGB color triplet for RED
        self.o_color = (0,    0,    0)        # окантовка - RGB color triplet for BLACK
        self.bg_color = SetPlg.bg_color       # цвет фона полегона (для обнаружения препятствий)
        self.pr_color = SetPlg.pr_color       # цвет припятствий (для обнаружения столкновений)  
       
        # Геометрические размеры робота
        self.dxm = 4                          # продольный полуразмер 1                                 
        self.dx  = 7                          # продольный полуразмер 2 
        self.dym = 3                          # поперечный полуразмер 1 
        self.dy  = 10                         # поперечный полуразмер 2
        
        self.PosOrient()                      # Позиционирование и ориентация робота   
        
        self.D  = 0                           # Расстояние от робота до цели
        self.Bt = 0                           # [рад] Угол цели
        self.At = 0                           # [рад] Пеленг цели
        self.Mrmax = 4                        # [Нм] максимальный вращающий момент робота при повороте
        self.Frmax = 8                        # [Н] максимальное усилие силовой установки робота
        self.Vrmax = 20                       # [pk/с] максимальная линейная скорость робота 
        self.Wrmax = 2                        # [рад/с] максимальная угловая скорость робота
        
        self.Wr = 0                           # [рад/с] угловая скорость робота        
        self.Jr = 0.05                        # [кг*m^2] момент инерции робота      
        self.Vr = 0                           # [pk/с] линейная скорость робота        
        self.mr = 2                           # [кг] масса робота
   
        self.scr_width = SetPlg.screen_width           # ширина поля
        self.scr_height = SetPlg.screen_height         # высота поля  
      
        # Датчики препятствий
        self.SnsR = np.array([20, 30, 40], dtype = 'float32')      # дальность видения
        
        self.SnsU = np.array([ 0.0,          math.pi/8,  2*math.pi/8,  3*math.pi/8, 
                               math.pi/2,  5*math.pi/8,  6*math.pi/8,  7*math.pi/8,
                               math.pi,   -7*math.pi/8, -6*math.pi/8, -5*math.pi/8,
                              -math.pi/2, -3*math.pi/8, -2*math.pi/8, -math.pi/8], 
                             dtype = 'float32')                    # угол видения 
      
        self.SnsP = np.zeros((self.SnsR.shape[0], self.SnsU.shape[0]),
                             dtype = 'int')                  # обнаружение препятствий 
                                                             #                         0   1   2   3   4   5   6   7
        self.SnsFlag  = np.zeros((3, 8), dtype = 'int')      # флаги сраб.датч.преп. [FF,FFR, FR, RR, ZZ, LL, FL,FFL]  
        self.SnsKFrOP = np.zeros((3, 8), dtype = 'float32')  # Усилие СУ обх.преп.   [FF,FFR, FR, RR, ZZ, LL, FL,FFL]  
        self.SnsKMrOP = np.zeros((3, 8), dtype = 'float32')  # Повор.мом.при об.преп.[FF,FFR, FR, RR, ZZ, LL, FL,FFL]        

        self.StlknPr = 0                      # флаг столкновения с препятствием    


    def PosOrient(self):    
        """ Позиционирование и ориентация робота """
        
        # образующие точки робота до позиционирования 
        self.RP = np.array([[       0, -self.dy],   
                            [ self.dx, -self.dym], 
                            [ self.dx,  self.dym],  
                            [ self.dxm, self.dy],
                            [-self.dxm, self.dy], 
                            [-self.dx,  self.dym],  
                            [-self.dx, -self.dym]], dtype = 'float32')
                                                                                                 
        RP1 = np.zeros(self.RP.shape)         # поворот робота на заданный угол
        RP1[:,0] = self.RP[:,0]*math.cos(self.fi) - self.RP[:,1]*math.sin(self.fi) 
        RP1[:,1] = self.RP[:,0]*math.sin(self.fi) + self.RP[:,1]*math.cos(self.fi)   
                                              
        self.RP[:,0] = RP1[:,0] + self.x_pos  # перенос робота в заданную точку
        self.RP[:,1] = RP1[:,1] + self.y_pos
       

    def cnfg(self, FCLR=(255, 0, 0), OCLR=(0, 0, 0),
                   dXM=4, dX=7, dYM=3, dY=10):
        """ Устанавливает параметры робота (отличные от умолчания) """
        
        self.dxm = dXM                        # продольный полуразмер 1                                 
        self.dx  = dX                         # продольный полуразмер 2 
        self.dym = dYM                        # поперечный полуразмер 1 
        self.dy  = dY                         # поперечный полуразмер 2
        self.f_color = FCLR                   # фон  (RGB)
        self.o_color = OCLR                   # оконтовка (RGB)
        
        self.PosOrient()                      # Позиционирование и ориентация робота            


    def update(self, screen):
        """ Рисует робот в текущей позиции и ориентации """
        
        pygame.draw.polygon(screen, self.f_color, self.RP)
        pygame.draw.polygon(screen, self.o_color, self.RP, 1)    
             
        
    def RotT(self, screen, Xt, Yt):
        """ Поворот робота к цели без перемещения """
        
        # Расстояние от робота до цели      
        self.D = math.hypot((self.x_pos - Xt), (self.y_pos - Yt))       
             
        # Угол цели (угол между направлением на север и направлением на цель) 
        if Xt >= self.x_pos:
            self.Bt = math.acos((self.y_pos - Yt) / self.D)        
        else:
            self.Bt = 2*math.pi - math.acos((self.y_pos - Yt) / self.D)
            
        self.fi = self.Bt                     # новый курсовой угол робота 
        self.PosOrient()                      # новое позиционирование робота
        self.update(screen)                   # отрисовка робота
  

    def snsPr(self, screen):
        """ Датчики препятствий """

        for r in range(self.SnsR.size):
            for u in range(self.SnsU.size):
                SnsX = int(self.x_pos + self.SnsR[r] * math.sin(self.fi + self.SnsU[u]))
                SnsY = int(self.y_pos - self.SnsR[r] * math.cos(self.fi + self.SnsU[u]))  
                
                # Ограничение шиоины и высоты экрана   
                if SnsX > self.scr_width-1:
                    SnsX = self.scr_width-1
                elif SnsX < 1:
                    SnsX = 1
            
                if SnsY > self.scr_height-1:
                    SnsY = self.scr_height-1
                elif SnsY < 1:
                    SnsY = 1   
                
                PksClr = screen.get_at([SnsX, SnsY])
                if PksClr[0:3] == self.bg_color or PksClr[0:3] == (250,250,0):
                    self.SnsP[r,u] = 0                
                    pygame.draw.circle(screen, (250,250,0), (SnsX, SnsY), 2) 
                else:
                    self.SnsP[r,u] = 1                
                    pygame.draw.circle(screen, (180,0,0), (SnsX, SnsY), 2) 
    
  
    def RbPr(self, screen):
        """ Отслеживание столкновений робота с препятствиями """
    
        for k in range(self.RP.shape[0]):
            PksClr = screen.get_at(self.RP[k,:])   # цвет экрана на месте робота до его прорисовки
            if PksClr[0:3] == self.pr_color:       # сравнение с цветом препятствий
                self.StlknPr = 1                   # флаг столкновения с препятствием
                pop.play()                         #  звук
            else:
                self.StlknPr = 0                           
                
    
    def MovT(self, screen, Xt, Yt):
        """ Движение робота к цели """
        
        # Расстояние от робота до цели      
        Dk = math.hypot((self.x_pos - Xt), (self.y_pos - Yt))  
        
        self.D = Dk                            # Обновление расстояния до цели            
           
        if self.D > 160:                       # Определение требуемой скорости робота 
            Vrzd = self.Vrmax
        elif self.D > 30:
            Vrzd = 0.7 * self.Vrmax
        else:    
            Vrzd = 0.02 * self.D * self.Vrmax           
                          
        eVr = Vrzd - self.Vr                   # Ошибка по скорости 
               
        # Угол цели (угол между направлением на север и направлением на цель)
        if self.D > 1:                        # при малых D не вычисл., что бы не /0
            if Xt >= self.x_pos:
                self.Bt = math.acos((self.y_pos - Yt) / self.D)     
            else:
                self.Bt = 2*math.pi - math.acos((self.y_pos - Yt) / self.D)    
      
        # Пеленг цели (угол между прод.осью робота и напр. на цель)
        Atk = self.Bt - self.fi    
        
        if Atk < -math.pi:                    # Приведение к диапазону -p...p
            Atk = Atk + 2*math.pi           
        if Atk > math.pi:
            Atk = Atk - 2*math.pi 
            
        dAt = Atk - self.At                   # Приращение пеленга цели
        
        self.At = Atk                         # Обновление паленга цели 
               
        if self.D < 3:                        # ЦЕЛЬ ДОСТИГНУТА?
            self.Wr = 0                       #     - Да  
            self.Vr = 0
        else:                                 #     - Нет
          
            self.snsPr(screen)                # ОПРОС ДАТЧИКОВ ПРЕПЯТСТВИЙ  ***   
            
            Fr, Mr = self.__MFrSUop(eVr, Atk, dAt)     # Вращ.мом. и усилие, развиваемые СУ 
                    
            
            # РАСЧЁТ ПАРАМЕТРОВ ДВИЖЕНИЯ И ПОЛОЖЕНИЯ РОБОТА            
            self.Wr = Mr*self.dt/self.Jr + self.Wr     # Угловая скорость робота 
            if self.Wr > self.Wrmax:
                self.Wr = self.Wrmax
            elif self.Wr < -self.Wrmax:   
                self.Wr = -self.Wrmax            
            
            self.fi = self.fi + self.Wr * self.dt      # приращение курсового угола робота   
            
            if self.fi < -math.pi:                     # Приведение к диапазону -p...p
                self.fi = self.fi + 2*math.pi           
            if self.fi > math.pi:
                self.fi = self.fi - 2*math.pi                    
            
            self.Vr = Fr*self.dt/self.mr + self.Vr     # Линейная скорость робота   
            if self.Vr > self.Vrmax:
                self.Vr = self.Vrmax
            if self.Vr < -self.Vrmax:
                self.Vr = -self.Vrmax
    
            Vrx = self.Vr * math.sin(self.fi)          # Составляющие скорости робота
            Vry = -self.Vr * math.cos(self.fi)

            self.x_pos = self.x_pos + Vrx * self.dt    # новая координата x робота
            self.y_pos = self.y_pos + Vry * self.dt    # новая координата y робота    

            # Ограничение шиоины и высоты экрана   
            if self.x_pos > self.scr_width:
                self.x_pos = self.scr_width
            elif self.x_pos < 0:
                self.x_pos = 0
            
            if self.y_pos > self.scr_height:
                self.y_pos = self.scr_height
            elif self.y_pos < 0:
                self.y_pos = 0    
   
        self.PosOrient()                               # новое позиционирование робота
        self.RbPr(screen)                              # oбн.столкн. робота с препятст
        self.update(screen)                            # отрисовка робота     
  
    
    def __MrSU(self, Atk, dAt):
        """ Вращающий момент при повороте робота """   
    
        # Движение к цели    
        if Atk < -math.pi/2:
            KMr = -1
        elif Atk < -math.pi/4:
            if dAt < -0.01:
                KMr = -1
            elif dAt < 0.01:    
                KMr = -0.5
            else:
                KMr = -0.3
        elif Atk < 0:        
            if dAt < -0.01:
                KMr = -0.5
            elif dAt < 0.01:    
                KMr = 0.02*Atk
            else:
                KMr = 0.02*Atk
        elif Atk < math.pi/4:        
            if dAt < -0.01:
                KMr = 0.02*Atk
            elif dAt < 0.01:    
                KMr = 0.02*Atk
            else:
                KMr = 0.5                
        elif Atk < math.pi/2:        
            if dAt < -0.01:
                KMr = 0.3
            elif dAt < 0.01:    
                KMr = 0.5
            else:
                KMr = 1                               
        else:
            KMr = 1      
                 
        Mr = KMr * self.Mrmax        
        return Mr     
    
    
    def __FrSU(self, eVr):
        """ Усилие, развиваемое силовой установкой робота """
    
        # Движение к цели            
        if eVr > 0.4 * self.Vrmax:
            KFr = 1
        elif eVr > 0.2 * self.Vrmax:
            KFr = 0.5
        elif eVr > -0.2 * self.Vrmax:
            KFr = 0.5 * eVr
        elif eVr > -0.4 * self.Vrmax:
            KFr = -0.5
        else:    
            KFr = -1  
            
        Fr = KFr * self.Frmax         
        return Fr    
    

    def __MFrSUop(self, eVr, Atk, dAt):
        """ Вращ.мом. и усилие, развиваемое СУ при обходе препятствий """           
        
        # Угловое положение датчиков     
        FF  = [0]                             # Впереди
        FFR = [1]                             # Впереди справа
        FR  = [2]                             # Cправа впереди
        RR  = [3, 4, 5]                       # Справа
        ZZ  = [6, 7, 8, 9, 10]                # Сзади 
        LL  = [11, 12, 13]                    # Слева
        FL  = [14]                            # Слева впереди
        FFL = [15]                            # Впереди слева   
                                              #                         0   1   2   3   4   5   6   7
        self.SnsFlag[:,:]  = 0                # флаги сраб.датч.преп. [FF,FFR, FR, RR, ZZ, LL, FL,FFL]  
        self.SnsKFrOP[:,:] = 0                # Усилие СУ обх.преп. 
        self.SnsKMrOP[:,:] = 0                # Повор.мом.при об.преп.       

        # Ближний контур   
        
        if self.SnsP[0,FF].any() > 0:        # препятствие впереди
            self.SnsFlag[0,0] = 1 
            self.SnsKFrOP[0,0] = -3.0                 
            self.SnsKMrOP[0,0] = 0.0  

        if self.SnsP[0,FFR].any() > 0:        # препятствие впереди справа
            self.SnsFlag[0,1] = 1 
            self.SnsKFrOP[0,1] = 0.5                 
            self.SnsKMrOP[0,1] = -0.08 

        if self.SnsP[0,FR].any() > 0:         # препятствие справа впереди 
            self.SnsFlag[0,2] = 1 
            self.SnsKFrOP[0,2] = 0.5                 
            self.SnsKMrOP[0,2] = -0.1 

        if self.SnsP[0,RR].any() > 0:         # препятствие справа 
            self.SnsFlag[0,3] = 1 
            self.SnsKFrOP[0,3] = 1.0                 
            self.SnsKMrOP[0,3] = 0 

        if self.SnsP[0,ZZ].any() > 0:         # препятствие сзади 
            self.SnsFlag[0,4] = 1 
            self.SnsKFrOP[0,4] = 1.0                 
            self.SnsKMrOP[0,4] = 0.0 

        if self.SnsP[0,LL].any() > 0:         # препятствие слева 
            self.SnsFlag[0,5] = 1 
            self.SnsKFrOP[0,5] = 1.0                 
            self.SnsKMrOP[0,5] = 0 
            
        if self.SnsP[0,FL].any() > 0:         # препятствие впереди слева
            self.SnsFlag[0,6] = 1 
            self.SnsKFrOP[0,6] = 0.5                 
            self.SnsKMrOP[0,6] = 0.1    
        
        if self.SnsP[0,FFL].any() > 0:         # препятствие слева впереди 
            self.SnsFlag[0,7] = 1 
            self.SnsKFrOP[0,7] = 0.5                 
            self.SnsKMrOP[0,7] = 0.08 

        # Средний контур      
             
        if self.SnsP[1,FFR].any() > 0:        # препятствие впереди справа
            self.SnsFlag[1,1] = 1 
            self.SnsKFrOP[1,1] = 0.4                 
            self.SnsKMrOP[1,1] = -0.06 

        if self.SnsP[1,FR].any() > 0:         # препятствие справа впереди 
            self.SnsFlag[1,2] = 1 
            self.SnsKFrOP[1,2] = 0.4                 
            self.SnsKMrOP[1,2] = -0.03 

        if self.SnsP[1,FL].any() > 0:         # препятствие впереди слева
            self.SnsFlag[1,6] = 1 
            self.SnsKFrOP[1,6] = 0.4                 
            self.SnsKMrOP[1,6] = 0.03    
        
        if self.SnsP[1,FFL].any() > 0:         # препятствие слева впереди 
            self.SnsFlag[1,7] = 1 
            self.SnsKFrOP[1,7] = 0.4                 
            self.SnsKMrOP[1,7] = 0.06 

        # Дальний контур      
             
        if self.SnsP[2,FFR].any() > 0:        # препятствие впереди справа
            self.SnsFlag[2,1] = 1 
            self.SnsKFrOP[2,1] = 0.4                 
            self.SnsKMrOP[2,1] = -0.05 
        
        if self.SnsP[2,FFL].any() > 0:        # препятствие слева впереди 
            self.SnsFlag[2,7] = 1 
            self.SnsKFrOP[2,7] = 0.4                 
            self.SnsKMrOP[2,7] = 0.05 

        if self.SnsFlag[0,:].any() > 0:       # есть препятстния на БЛИЖНЕМ контуре  
            if  self.SnsKFrOP[0,:].min() < 0:  
                Fr = self.SnsKFrOP[0,:].min() * self.Frmax 
            else:
                Fr = self.SnsKFrOP[0,:].max() * self.Frmax      
            Mr = self.SnsKMrOP[0,:].sum() * self.Mrmax    
                
        elif self.SnsFlag[1,:].any() > 0:     # есть препятстния на СРЕДНЕМ контуре   
            Fr = self.SnsKFrOP[1,:].max() * self.Frmax      
            Mr = self.SnsKMrOP[1,:].sum() * self.Mrmax    
          
        elif self.SnsFlag[2,:].any() > 0:     # есть препятстния на ДАЛЬНЕМ контуре   
            Fr = self.SnsKFrOP[2,:].max() * self.Frmax      
            Mr = self.SnsKMrOP[2,:].sum() * self.Mrmax  
            
        else:                                 # "НЕ ВИЖУ ПРЕПЯТСТВИЙ"
            Fr = self.__FrSU(eVr)             # Усилие, развиваемое силовой установкой робота   
            Mr = self.__MrSU(Atk, dAt)        # Вращающий момент при повороте робота     
   
        return Fr, Mr     