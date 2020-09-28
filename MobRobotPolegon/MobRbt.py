#
"""
Полегон для исследования поведения мобильных роботов

"""
import numpy as np                            # Для работы с массивами элементов одного типа
import matplotlib.pyplot as plt               # для визуализации данных
import datetime                               # Классы для работы с датой и временем
import pygame                                 # Управл. графикой, анимацией, звуком
import seaborn as sns

from MobRbt_Setting import Settings           # Параметры настройки полегона и робота
from MobRbt_Robot import Robot                # Загрузка класса "Робот"
from MobRbt_DvPrp import DvPrp                # Загрузка класса "Подвижное препятствие"

pygame.init()                                 # Инициализация настроек PyGame
st = Settings()                               # Загрузка параметров конфигурации
sns.set()                                     # Установка стилей
"""************** Начальные установки **************************************"""

Xt, Yt = 1100, 700                            # Координаты цели (начальные)
Rt = 5                                        # радиус маркера цели

Xr, Yr = 100, 100                             # начальные координаты робота
fir = np.pi/4                                 # курсовой угол робота
RB1 = Robot(Xr, Yr, fir, st)                  # Создание робота

# Создание подвижных препятствий
prDv1 = DvPrp(st.prDv1, st.prDv1_dX, st.prDv1_dY, 
              st.prDv1_Vx, st.prDv1_Vy, st)  

prDv2 = DvPrp(st.prDv2, st.prDv2_dX, st.prDv2_dY, 
              st.prDv2_Vx, st.prDv2_Vy, st) 

prDv3 = DvPrp(st.prDv3, st.prDv3_dX, st.prDv3_dY, 
              st.prDv3_Vx, st.prDv3_Vy, st)                   

BLACK = (  0,   0,   0)                       # RGB color triplet for BLACK
BLUE  = (  0,   0, 255)                       # RGB color triplet for BLUE
GREEN = (  0, 255,   0)                       # RGB color triplet for GREEN
RED   = (255,   0,   0)                       # RGB color triplet for RED

"""*************************************************************************"""

# Создаём объект экрана 
screen = pygame.display.set_mode([st.screen_width, st.screen_height])
pygame.display.set_caption("Robot Polegon")

font = pygame.font.SysFont("Times", 18)       # Шрифт для надписей

clock = pygame.time.Clock()                   # создаёи объект класса Clock -"Timer" 
                                              # (для задавания частоты смены кадров)
# ГЛАВНЫЙ ЦИКЛ
keepGoing = True
start_time = datetime.datetime.now()          # время начала эксперимента
while keepGoing:                              # *** Главный цикл **************
  
    # Обработка событий
    for event in pygame.event.get(): 
    # print(event)
        if event.type == pygame.QUIT:         # нажатие на кнопку закрытия программы 
            keepGoing = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            (Xt, Yt) = event.pos              # позиция мыши во время щелчка           
    
    # Подготовка нового экрана для смены кадра    
    screen.fill(st.bg_color)                  # очистка экрана перед прорисовкой

    """************** Содержание кадра *************************************"""
    
    # Препятствия на полнгоне (неподвижные)

    pygame.draw.polygon(screen, st.pr_color, st.pr1)
    pygame.draw.polygon(screen, st.pr_color, st.pr2)
    pygame.draw.polygon(screen, st.pr_color, st.pr3)
    pygame.draw.polygon(screen, st.pr_color, st.pr4)
    pygame.draw.polygon(screen, st.pr_color, st.pr5)
    pygame.draw.polygon(screen, st.pr_color, st.pr6)
    pygame.draw.polygon(screen, st.pr_color, st.pr7)
    pygame.draw.polygon(screen, st.pr_color, st.pr8)
    pygame.draw.polygon(screen, st.pr_color, st.pr9)
    pygame.draw.polygon(screen, st.pr_color, st.pr10)
    pygame.draw.polygon(screen, st.pr_color, st.pr11)
    pygame.draw.polygon(screen, st.pr_color, st.pr12)
    pygame.draw.polygon(screen, st.pr_color, st.pr13)
    pygame.draw.polygon(screen, st.pr_color, st.pr14)
    pygame.draw.polygon(screen, st.pr_color, st.pr15)
    pygame.draw.polygon(screen, st.pr_color, st.pr16)
    pygame.draw.polygon(screen, st.pr_color, st.pr17)
    pygame.draw.polygon(screen, st.pr_color, st.pr18)
    pygame.draw.polygon(screen, st.pr_color, st.pr19)
    pygame.draw.polygon(screen, st.pr_color, st.pr20)
    pygame.draw.polygon(screen, st.pr_color, st.pr21)
    pygame.draw.polygon(screen, st.pr_color, st.pr22)

    # Оодвижные препятствия
    prDv1.MovPr(screen)                      
    prDv2.MovPr(screen)
    prDv3.MovPr(screen)    
    
    # Робот
    RB1.MovT(screen, Xt, Yt)      # движение к цели
        
    # Цель, направление   
    pygame.draw.circle(screen, BLUE, (Xt, Yt), Rt)
    pygame.draw.line(screen, GREEN, (RB1.x_pos, RB1.y_pos), (Xt, Yt))
    
    # Отображение надписей на полегоне
    txt = font.render("Дальность до цели: " + str(round(RB1.D,1)) + " пкс",  True, BLACK)      
    screen.blit(txt, (10,2))
    txt = font.render("Пеленг цели: " + str(round(RB1.At/np.pi,2)) + " пи-рад",  True, BLACK)
    screen.blit(txt, (10,22)) 
    txt = font.render("Скорость робота: " + str(round(RB1.Vr,1)) + " пкс/с",  True, BLACK)     
    screen.blit(txt, (510,2))  
    txt = font.render("Угл.скор. робота: " + str(round(RB1.Wr,2)) + " рад/с",  True, BLACK)     
    screen.blit(txt, (510,22))             
    txt = font.render("Курс.угол робота: " + str(round(RB1.fi/np.pi,2)) + " пи-рад",  True, BLACK)
    screen.blit(txt, (510,42)) 
    
    now_time = datetime.datetime.now()                                         # текущее время 
    delta_time = now_time - start_time
    dT = delta_time.seconds + delta_time.microseconds / float(1000000)         # [с + mc]
    
    txt = font.render("Время: " + str(round(dT,3)) + " с",  True, RED)   
    screen.blit(txt, (910,2))     
    
    """*********************************************************************"""    
    
    # Запись протокола эксперимента
    st.PrtklExpr = np.vstack([st.PrtklExpr, 
                             [round(dT,3),           RB1.x_pos,               RB1.y_pos, 
                              round(RB1.D,1),  round(RB1.At/np.pi,2), round(RB1.fi/np.pi,2),
                              round(RB1.Vr,1), round(RB1.Wr,2),               RB1.StlknPr]])
    
    clock.tick(st.kps)                        # задание частоты смены кадров 
    
    # Смена кадров
    pygame.display.update()                   # перерисовка кадра       
            
pygame.quit()                                 # Выход. Освобождение ресурсов        

"""**************************** Завершение *********************************"""  

# Запись протокола эксперимента в файл
f = open('PrtklExpr.txt', 'w')
for i in range(st.PrtklExpr.shape[0]):
    f.write(str(st.PrtklExpr[i,0]) + '\t' +
            str(st.PrtklExpr[i,1]) + '\t' +
            str(st.PrtklExpr[i,2]) + '\t' +
            str(st.PrtklExpr[i,3]) + '\t' +
            str(st.PrtklExpr[i,4]) + '\t' +
            str(st.PrtklExpr[i,5]) + '\t' +
            str(st.PrtklExpr[i,6]) + '\t' +
            str(st.PrtklExpr[i,7]) + '\t' +
            str(st.PrtklExpr[i,8]) + '\t' + '\n')
f.close()

print('')
print('Эксперимент завершён.')
print("Время: " + str(round(dT,3)) + " с")
print("Период дискретизации: " + str(RB1.dt) + " с")
print('')

# Построение графиков

fig = plt.figure(1)
ax = plt.axes([0.1, 0.1, 1.0, 1.0])   # [низ, левый угол, ширина, высота] 
plt.plot(st.PrtklExpr[:,1], -st.PrtklExpr[:,2], '-b')
plt.title("Траектория робота")
plt.xlabel("X, [пкс]")
plt.ylabel("Y, [пкс]")

fig = plt.figure(2)
ax = plt.axes([0.1, 0.1, 2.0, 0.7])   # [низ, левый угол, ширина, высота] 
plt.plot(st.PrtklExpr[:,0], st.PrtklExpr[:,3], '-g')
plt.plot(st.PrtklExpr[:,0], st.PrtklExpr[:,8] * 100, '-k')
plt.title(" Дальность до цели (g). Cтолкновения с препятствиями (k) ")
plt.xlabel("t, [c]")
plt.ylabel("D, [пкс]")

fig = plt.figure(3)
ax = plt.axes([0.1, 0.1, 2.0, 0.7])   # [низ, левый угол, ширина, высота] 
plt.plot(st.PrtklExpr[:,0], st.PrtklExpr[:,4], '-r')
plt.plot(st.PrtklExpr[:,0], st.PrtklExpr[:,5], ':c')
plt.title(" Пеленг цели (r).  Курс.угол робота (c)")
plt.xlabel("t, [c]")
plt.ylabel("At,  fi, [пи-рад]")

fig = plt.figure(4)
ax = plt.axes([0.1, 0.1, 2.0, 0.7])   # [низ, левый угол, ширина, высота] 
plt.plot(st.PrtklExpr[:,0], st.PrtklExpr[:,6], '-m')
plt.title(" Скорость робота")
plt.xlabel("t, [c]")
plt.ylabel("Vr, [пкс/c]")

fig = plt.figure(5)
ax = plt.axes([0.1, 0.1, 2.0, 0.7])   # [низ, левый угол, ширина, высота] 
plt.plot(st.PrtklExpr[:,0], st.PrtklExpr[:,7], '-r')
plt.title(" Угловая скорость робота")
plt.xlabel("t, [c]")
plt.ylabel("Wr, [рад/с]")
plt.show()