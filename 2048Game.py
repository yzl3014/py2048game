# -*- coding: UTF-8 -*-
import pygame, random, math, time
from pygame.locals import *
from copy import deepcopy

gameMap = [[0 for _ in range(4)] for _ in range(4)]  # 游戏地图。前者是宽度，后者是高度。可以随意更改
INTERVAL = 500  # 常量(毫秒): 新方块生成时等待一段时间，便于用户查看
SIDE = 90  # 常量: 方块边长(像素)
score = 0  # 计分
step = 0  # 有效操作步数。如果按键后没有方块移动就不算有效操作


pygame.init()
screen = pygame.display.set_mode((410, 500))
pygame.display.set_caption("2048 Game (yzl3014@github)")
bg_color = (187, 173, 160)
isGameOver = False


def getBlockColor(num):  # 获取每个数值对应的块的颜色
    match num:
        case 2:
            return (238, 228, 218)
        case 4:
            return (237, 224, 200)
        case 8:
            return (242, 177, 121)
        case 16:
            return (245, 149, 99)
        case 32:
            return (246, 124, 95)
        case 64:
            return (247, 96, 63)
        case 128:
            return (237, 209, 124)
        case 256:
            return (237, 206, 109)
        case 512:
            return (237, 203, 93)
        case 1024:
            return (237, 201, 79)
        case 2048:
            return (237, 197, 62)
        case 4096:
            return (249, 139, 73)
        case 8192:
            return (251, 132, 57)
        case 16384:
            return (252, 118, 38)
        case _:
            return (36, 36, 36)


def show():  # 窗口内容的显示
    screen.fill(bg_color)  # 清空画面
    spacing = 10  # 方块间距
    # 绘制gameMap
    for i in range(len(gameMap)):  # 遍历每一行
        for j in range(len(gameMap[0])):
            leftPos = j * (SIDE + spacing) + 10  # 方块左侧位置 (详见PyGame开发文档Rect)
            topPos = i * (SIDE + spacing) + 10  # 方块顶部位置
            if gameMap[i][j] == 0:
                pygame.draw.rect(screen, (205, 193, 180), (leftPos, topPos, SIDE, SIDE), border_radius=8)
            else:
                # 绘制矩形
                pygame.draw.rect(screen, (getBlockColor(gameMap[i][j])), (leftPos, topPos, SIDE, SIDE), border_radius=8)
                # 显示方块对应的数字。字号根据文字宽度自适应，但是 **非常不好用**。
                font_block = pygame.font.SysFont("Microsoft YaHei", math.floor(70 - len(str(gameMap[i][j])) * 8), True)
                # 字体颜色：浅色方块用黑色，深色方块用白色
                if gameMap[i][j] == 2 or gameMap[i][j] == 4:
                    fontColor = (124, 115, 106)
                else:
                    fontColor = (249, 246, 242)
                # 设置文字
                text_blockNum = font_block.render(str(gameMap[i][j]), True, fontColor)
                # 计算出字符与居中的偏移，也就是该移动多少像素就能使文字居中
                centerOffset_lateral = SIDE / 2 - text_blockNum.get_width() / 2  # 水平
                centerOffset_vertical = SIDE / 2 - text_blockNum.get_height() / 2  # 垂直
                # 显示文字
                screen.blit(text_blockNum, (leftPos + centerOffset_lateral, topPos + centerOffset_vertical))
    textsBase = (SIDE + spacing) * len(gameMap)

    # 显示游戏数据
    font_yahei = pygame.font.SysFont("Microsoft YaHei", 20)
    text_info = font_yahei.render("分数：" + str(score) + "  步数：" + str(step), True, (0, 0, 0))
    screen.blit(text_info, (10, textsBase + 20))  # 根据计算，显示在游戏区域下方

    # 显示提示或版权文字
    text_tips = font_yahei.render("若按键无效请按Shift键 | ©2024.7 Yzl3014", True, (0, 0, 0))
    screen.blit(text_tips, (10, textsBase + 50))

    # 判断是否输了游戏，是则显示Game Over文字
    if referee() == 2:
        global isGameOver
        isGameOver = True
        font_lostGame = pygame.font.SysFont("Microsoft YaHei", 40, True)
        text_lostGame = font_lostGame.render("Game Over!", True, (255, 255, 255), (0, 0, 0))
        text_lostGame_PosX = screen.get_width() / 2 - text_lostGame.get_width() / 2
        text_lostGame_PosY = screen.get_height() / 2 - text_lostGame.get_height() / 2
        screen.blit(text_lostGame, (text_lostGame_PosX, text_lostGame_PosY))

    # 更新画面，让所有绘制显示出来
    pygame.display.flip()


def getRandomPos():  # 获取随机位置，而且该位置的数值必须为0
    randomX = random.randint(0, len(gameMap) - 1)
    randomY = random.randint(0, len(gameMap[0]) - 1)
    if gameMap[randomX][randomY] != 0:
        return getRandomPos()
    else:
        return [randomX, randomY]


def referee():  # 判断游戏输赢 (可继续游戏0, 赢1, 输2)
    movable = False  # 是否可以移动
    for i in range(len(gameMap)):  # 遍历每一行
        for j in range(len(gameMap[0])):  # 遍历每一行的每一个方块
            if i != 0 and gameMap[i - 1][j] == gameMap[i][j]:
                movable = True  # 该方块上方是否有同类(可移动，游戏可以进行)
            if i != len(gameMap) - 1 and gameMap[i + 1][j] == gameMap[i][j]:
                movable = True  # 该方块下方是否有同类
            if j != 0 and gameMap[i][j - 1] == gameMap[i][j]:
                movable = True  # 该方块左方是否有同类
            if j != len(gameMap[0]) - 1 and gameMap[i][j + 1] == gameMap[i][j]:
                movable = True  # 该方块右方是否有同类
            if gameMap[i][j] == 0:
                movable = True
            if gameMap[i][j] == 2048:
                return 1
    if movable is True:
        return 0
    else:
        return 2


def makeMap():  # 游戏开始时，生成两个方块
    block1 = getRandomPos()
    block2 = getRandomPos()
    if random.randint(0, 9) == 0:
        gameMap[block1[0]][block1[1]] = 4
    else:
        gameMap[block1[0]][block1[1]] = 2
    gameMap[block2[0]][block2[1]] = 2


def getBestKeySimple():  # 计算上下左右所得分数，返回加分最高的方向，没有最高的则返回随机方向
    aiMap = deepcopy(gameMap)  # 直接画等号的话，修改会应用到原变量。了解更多：DeepCopy
    wasdKey = ["w", "a", "s", "d"]
    keyID = 0  # 读写数组时使用
    keyScoreList = [0, 0, 0, 0]  # wasd
    for key in "wasd":
        keyScore = 0
        for i in range(len(aiMap)):  # 遍历每一行
            for j in range(len(aiMap[0])):  # 遍历每一行的每一个方块
                if aiMap[i][j] == 0:
                    continue

                # 模拟按键操作后的结果，看谁的分最高
                # 按下w键，上移
                if key == "w" and i != 0 and aiMap[i][j] == aiMap[i - 1][j]:  # 上方的块是同数字，合并这两个块
                    keyScore += aiMap[i - 1][j]
                # 按下s键，下移
                if key == "s" and i != len(aiMap) - 1 and aiMap[i][j] == aiMap[i + 1][j]:
                    keyScore += aiMap[i + 1][j]
                # 按下a键，左移
                if key == "a" and j != 0 and aiMap[i][j] == aiMap[i][j - 1]:
                    keyScore += aiMap[i][j - 1]
                # 按下d键，右移
                if key == "d" and j != len(aiMap[0]) - 1 and aiMap[i][j] == aiMap[i][j + 1]:
                    keyScore += aiMap[i][j + 1]

        keyScoreList[keyID] = keyScore  # 按顺序记录加分
        keyID += 1  # 为了数组读写
    print(step, keyScoreList, wasdKey[keyScoreList.index(max(keyScoreList))])
    if max(keyScoreList) == 0:  # 最高和最低一样，即没有最高分
        return random.choice("wasd")
    else:
        return wasdKey[keyScoreList.index(max(keyScoreList))]


if __name__ == "__main__":
    # pygame init
    clock = pygame.time.Clock()
    run = True

    makeMap()
    show()  # 展示初始地图
    while run:
        # pyGame
        clock.tick(60)
        key = ""
        # 监听事件
        for event in pygame.event.get():
            if event.type == QUIT:  # 按下窗口右上角关闭键
                run = False
                break
            if event.type == KEYDOWN:  # WASD或方向键，用来操作游戏
                if event.key == K_w or event.key == K_UP:
                    key = "w"
                if event.key == K_a or event.key == K_LEFT:
                    key = "a"
                if event.key == K_s or event.key == K_DOWN:
                    key = "s"
                if event.key == K_d or event.key == K_RIGHT:
                    key = "d"

        # 不使用X和Y是因为在数学的坐标系中，横是X，纵是Y，不符合本程序
        hasMoved = False  # 本次按键是否移动了方块，移动则生成新方块
        for Process in range(len(gameMap[0]) - 1):  # 根据实际测试得出，需要循环每行成员数减一才能将所有块移动到位
            if key not in "wasd":
                print("not key")
                break
            for i in range(len(gameMap)):  # 遍历每一行
                for j in range(len(gameMap[0])):  # 遍历每一行的每一个方块
                    if gameMap[i][j] == 0:  # 如果当前方块是0的话，就不必执行任何移动
                        continue

                    # 按下w键，上移
                    if (
                        key == "w" and i != 0 and gameMap[i][j] == gameMap[i - 1][j]
                    ):  # 上方的块是同数字，向上合并这两个块
                        gameMap[i - 1][j] *= 2  # 上面的块的数值乘2
                        score += gameMap[i - 1][j]  # 按照2048游戏规则加分
                        gameMap[i][j] = 0  # 当前块设置为0
                        hasMoved = True
                    if key == "w" and i != 0 and gameMap[i - 1][j] == 0:  # 上方的块是0，则上移但不合并
                        gameMap[i - 1][j] = gameMap[i][j]
                        gameMap[i][j] = 0
                        hasMoved = True

                    # 按下s键，下移
                    if key == "s" and i != len(gameMap) - 1 and gameMap[i][j] == gameMap[i + 1][j]:
                        gameMap[i + 1][j] *= 2
                        score += gameMap[i + 1][j]
                        gameMap[i][j] = 0
                        hasMoved = True
                    if key == "s" and i != len(gameMap) - 1 and gameMap[i + 1][j] == 0:
                        gameMap[i + 1][j] = gameMap[i][j]
                        gameMap[i][j] = 0
                        hasMoved = True

                    # 按下a键，左移
                    if key == "a" and j != 0 and gameMap[i][j] == gameMap[i][j - 1]:
                        gameMap[i][j - 1] *= 2
                        score += gameMap[i][j - 1]
                        gameMap[i][j] = 0
                        hasMoved = True
                    if key == "a" and j != 0 and gameMap[i][j - 1] == 0:
                        gameMap[i][j - 1] = gameMap[i][j]
                        gameMap[i][j] = 0
                        hasMoved = True

                    # 按下d键，右移
                    if key == "d" and j != len(gameMap[0]) - 1 and gameMap[i][j] == gameMap[i][j + 1]:
                        gameMap[i][j + 1] *= 2
                        score += gameMap[i][j + 1]
                        gameMap[i][j] = 0
                        hasMoved = True
                    if key == "d" and j != len(gameMap[0]) - 1 and gameMap[i][j + 1] == 0:
                        gameMap[i][j + 1] = gameMap[i][j]
                        gameMap[i][j] = 0
                        hasMoved = True
        show()
        if hasMoved is True:  # 如果有方块移动，才会增加新方块
            step += 1  # 移动次数加一
            randomPos = getRandomPos()  # 数组。第一个是行，第二个是列。
            if random.randint(0, 9) == 0:
                gameMap[randomPos[0]][randomPos[1]] = 4
            else:
                gameMap[randomPos[0]][randomPos[1]] = 2
        if hasMoved is True:
            time.sleep(INTERVAL / 1000)  # 便于用户看见哪个是新增的块
            show()
    pygame.quit()
    exit(0)  # 0代表正常退出
