import pygame
import sys
import random
import time


class Bird(object):
    """定义一个鸟类"""

    def __init__(self):
        """定义初始化方法"""
        # 鸟的矩形有四个参数：前两个是小鸟矩形左上角的坐标点，后两个是矩形的长宽
        self.birdRect = pygame.Rect(65, 50, 50, 50)
        # 定义鸟的3种状态图片列表：向上飞、向下坠、死亡
        self.birdStatus = [pygame.image.load("image/bird.png"),
                           pygame.image.load("image/bird2.png"),
                           pygame.image.load("image/birdd.png")]
        self.status = 0  # 默认飞行状态
        self.birdX = 120  # 鸟所在X轴坐标,即是向右飞行的速度
        self.birdY = 350  # 鸟所在Y轴坐标,即上下飞行高度
        self.jump = False  # 默认情况小鸟自动降落
        self.jumpSpeed = 10  # 跳跃高度
        self.gravity = 5  # 重力
        self.dead = False  # 默认小鸟生命状态为活着

    def birdUpdate(self):
        if self.jump:
            # 小鸟跳跃
            self.jumpSpeed -= 1  # 速度递减，上升越来越慢
            self.birdY -= self.jumpSpeed  # 鸟Y轴坐标减小，小鸟上升
        else:
            # 小鸟坠落
            self.gravity += 0.2  # 重力递增，下降越来越快
            self.birdY += self.gravity  # 鸟Y轴坐标增加，小鸟下降
        self.birdRect[1] = self.birdY  # 更改Y轴位置


class Pipeline(object):
    """定义一个管道类"""

    def __init__(self):
        """定义初始化方法"""
        self.wallx = 400;  # 管道所在X轴坐标,最右边位置
        self.pineUp = pygame.image.load("image/top.png")  # 加载上管道图片
        self.pineDown = pygame.image.load("image/under.png")  # 加载管道图片

    def updatePipeline(self):
        """"管道移动方法"""
        self.wallx -= 5  # 管道X轴坐标递减，即管道向左移动
        # 当管道运行到一定位置，即小鸟飞越管道，分数加1，并且重置管道
        if self.wallx < -80:  # 管道宽度为94，当管道快移除屏幕时重置管道位置
            global score  # 设置得分加1并声明为全局变量
            score += 1
            self.wallx = 400


def createMap():
    """定义创建地图的方法"""
    screen.fill((255, 255, 255))  # 填充颜色
    screen.blit(background, (0, 0))  # 填入到背景
    start_text = "press any key to start game"
    ft1_font = pygame.font.SysFont("Arial", 70)  # 设置第一行文字字体
    ft1_surf = font.render(start_text, 1, (242, 3, 36))  # 设置第一行文字颜色
    screen.blit(ft1_surf, [screen.get_width() / 2 - ft1_surf.get_width() / 2, 100])  # 设置第一行文字显示位置


    # 显示管道
    # 因为管道长度为495几乎占满屏幕了，为了让管道小一点设置为屏幕外的上下方
    screen.blit(Pipeline.pineUp, (Pipeline.wallx, -300));  # 上管道坐标位置
    screen.blit(Pipeline.pineDown, (Pipeline.wallx, 500));  # 下管道坐标位置
    Pipeline.updatePipeline()  # 管道移动

    # 显示小鸟
    if Bird.dead:  # 撞管道状态
        Bird.status = 2
    elif Bird.jump:  # 起飞状态
        Bird.status = 1
    screen.blit(Bird.birdStatus[Bird.status], (Bird.birdX, Bird.birdY))  # 设置小鸟的坐标
    Bird.birdUpdate()  # 鸟移动

    # 显示分数
    # font.render（）用于显示字体有三个参数：字符串、是否平滑、颜色
    screen.blit(font.render(str(score), -1, (255, 255, 255)), (200, 50))  # 设置颜色及坐标位置

    pygame.display.update()  # 更新显示


def checkDead():
    # 上方管子的矩形位置
    upRect = pygame.Rect(Pipeline.wallx, -300,
                         Pipeline.pineUp.get_width() - 10,
                         Pipeline.pineUp.get_height())

    # 下方管子的矩形位置
    downRect = pygame.Rect(Pipeline.wallx, 500,
                           Pipeline.pineDown.get_width() - 10,
                           Pipeline.pineDown.get_height())
    # 检测小鸟与上下方管子是否碰撞
    if upRect.colliderect(Bird.birdRect) or downRect.colliderect(Bird.birdRect):
        Bird.dead = True
    # 检测小鸟是否飞出上下边界
    if not 0 < Bird.birdRect[1] < height:
        Bird.dead = True
        return True
    else:
        return False


def getResutl():
    final_text1 = "Game Over"
    final_text2 = "Your final score is:  " + str(score)
    final_text3 = "Press R Restart game"

    ft1_font = pygame.font.SysFont("Arial", 70)  # 设置第一行文字字体
    ft1_surf = font.render(final_text1, 1, (242, 3, 36))  # 设置第一行文字颜色
    ft2_font = pygame.font.SysFont("Arial", 50)  # 设置第二行文字字体
    ft2_surf = font.render(final_text2, 1, (253, 177, 6))  # 设置第二行文字颜色
    ft3_font = pygame.font.SysFont("Arial", 70)  # 设置第二行文字字体
    ft3_surf = font.render(final_text3, 1, (200, 180, 160))  # 设置第二行文字颜色

    screen.blit(ft1_surf, [screen.get_width() / 2 - ft1_surf.get_width() / 2, 100])  # 设置第一行文字显示位置
    screen.blit(ft2_surf, [screen.get_width() / 2 - ft2_surf.get_width() / 2, 200])  # 设置第二行文字显示位置
    screen.blit(ft3_surf, [screen.get_width() / 2 - ft3_surf.get_width() / 2, 300])  # 设置第二行文字显示位置
    pygame.display.flip()  # 更新整个待显示的Surface对象到屏幕上


if __name__ == '__main__':
    """主程序"""
    pygame.init()  # 初始化pygame
    pygame.font.init()  # 初始化字体
    font = pygame.font.SysFont("Arial", 50)  # 设置字体和大小
    size = width, height = 400, 680  # 设置窗口
    screen = pygame.display.set_mode(size)  # 显示窗口
    clock = pygame.time.Clock()  # 设置时钟
    Pipeline = Pipeline()  # 实例化管道类
    Bird = Bird()  # 实例化鸟类
    score = 0

    while True:
        clock.tick(60)  # 每秒执行60次
        # 轮询事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # 如果触发键盘和鼠标事件并且小鸟状态不是死亡则Bird.jump值为True并且初始化跳跃跟坠落速度
            if (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN) and not Bird.dead:
                Bird.jump = True  # 跳跃
                Bird.gravity = 5  # 重力
                Bird.jumpSpeed = 10  # 跳跃速度

        background = pygame.image.load("image/background.png")  # 加载背景图片
        key_pressed = pygame.key.get_pressed()

        if checkDead():  # 检测小鸟生命状态
            getResutl()  # 如果小鸟死亡，显示游戏总分数
        else:
            createMap()  # 创建地图
        if key_pressed[pygame.K_a] or key_pressed[pygame.K_LEFT]:
            k = 0# kaishiyouxi
        if key_pressed[pygame.K_d] or key_pressed[pygame.K_RIGHT]:
            r = 1 # 重新开始游戏
