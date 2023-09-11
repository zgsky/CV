# -*- coding:utf-8 -*-
import sys  # 导入sys模块
import pygame  # 导入pygame模块

pygame.init()  # 初始化pygame
size = width, height = 640, 480  # 设置窗口，这是一个数组
screen = pygame.display.set_mode(size)  # 显示窗口
color = (0, 0, 0)  # 设置颜色

ball = pygame.image.load("ball.jpg")  # 加载图片../../image/niuniu.jpeg
# ball = ball.blit(ball, (0, 0), (360, 480, 60, 60))
ballrect = ball.get_rect()  # 根据图片大小获取矩形区域

speed = [5, 5]  # 设置移动的X轴、Y轴距离
clock = pygame.time.Clock()  # 创建时钟对象
# 执行死循环，确保窗口一直显示
while True:
    clock.tick(240)  # 每秒执行60次
    # 检查事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # 如果点击关闭窗口，则退出
            pygame.quit()  # 退出pygame
            sys.exit()

    ballrect = ballrect.move(speed)  # 通过再次赋值移动小球
    # 碰到左右边缘
    if ballrect.left < 0 or ballrect.right > width:
        speed[0] = -speed[0]  # 如果碰到边距则反方向移动
    # 碰到上下边缘
    if ballrect.top < 0 or ballrect.bottom > height:
        speed[1] = -speed[1]

    screen.fill(color)  # 填充颜色
    screen.blit(ball, ballrect)  # 此函数是将图片推送到窗口上，第一个参数为图片第二个参数为图片位置
    pygame.display.flip()  # 更新全部显示

