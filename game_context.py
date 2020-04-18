# coding:utf-8
import sys

from chess_piece import ChessPiece
import constants
from getch import Getch
import chess_strategy
import common


class GameContext:
    """ 游戏环境类 """

    game_over = False
    winner = ''
    # 是否已经选中棋子
    piece_checked = False
    # 红方先行
    firster = constants.CAMP_RED
    _pieces = []
    _width = 9
    _height = 10
    _getch = Getch()
    # 字符串默认值可以是''，数组默认值是[]，字典默认值是{}，数值默认值是0，而对象默认值是None
    _cursor_original_backup = None
    _cursor_loc = {'x': 4, 'y': 1}
    # 用于记录checked后，被checked的piece的坐标，用于判定是否是取消checked
    _checked_loc = {}
    _checked = False

    CURSOR_CHECKED = ' 〠 '
    CURSOR_UNCHECKED = ' 〄 '
    PIECE_NONE = ' ＊ '

    strategies = None

    def __init__(self, camp=constants.CAMP_RED):
        if camp == constants.CAMP_WHITE:
            self._cursor_loc['y'] = 8
        elif camp != constants.CAMP_RED:
            print('阵营参数错误，游戏退出')
            exit()
        self.firster = camp
        # init pieces
        # init NONE Camp
        for y in range(self._height):
            line = []
            for x in range(self._width):
                tmp = ChessPiece(self.PIECE_NONE, constants.CAMP_NONE)
                tmp.set_type(constants.CHESS_PIECE)
                line.append(tmp)
            self._pieces.append(line)
        del line
        # init RED Camp and Pic
        for idx in range(self._width):
            self._pieces[0][idx].set_camp(constants.CAMP_RED)
        self._pieces[0][0].set_pic(' 車 ')
        self._pieces[0][0].set_type(constants.CHESS_CHE)
        self._pieces[0][1].set_pic(' 馬 ')
        self._pieces[0][1].set_type(constants.CHESS_MA)
        self._pieces[0][2].set_pic(' 象 ')
        self._pieces[0][2].set_type(constants.CHESS_XIANG)
        self._pieces[0][3].set_pic(' 士 ')
        self._pieces[0][3].set_type(constants.CHESS_SHI)
        self._pieces[0][4].set_pic(' 將 ')
        self._pieces[0][4].set_type(constants.CHESS_BOSS)
        self._pieces[0][5].set_pic(' 士 ')
        self._pieces[0][5].set_type(constants.CHESS_SHI)
        self._pieces[0][6].set_pic(' 象 ')
        self._pieces[0][6].set_type(constants.CHESS_XIANG)
        self._pieces[0][7].set_pic(' 馬 ')
        self._pieces[0][7].set_type(constants.CHESS_MA)
        self._pieces[0][8].set_pic(' 車 ')
        self._pieces[0][8].set_type(constants.CHESS_CHE)
        # 上面的camp已经通过循环统一设置过了
        self._pieces[2][1].set_pic(' 炮 ')
        self._pieces[2][1].set_type(constants.CHESS_PAO)
        self._pieces[2][1].set_camp(constants.CAMP_RED)
        self._pieces[2][7].set_pic(' 炮 ')
        self._pieces[2][7].set_type(constants.CHESS_PAO)
        self._pieces[2][7].set_camp(constants.CAMP_RED)
        self._pieces[3][0].set_pic(' 卒 ')
        self._pieces[3][0].set_type(constants.CHESS_BING)
        self._pieces[3][0].set_camp(constants.CAMP_RED)
        self._pieces[3][2].set_pic(' 卒 ')
        self._pieces[3][2].set_type(constants.CHESS_BING)
        self._pieces[3][2].set_camp(constants.CAMP_RED)
        self._pieces[3][4].set_pic(' 卒 ')
        self._pieces[3][4].set_type(constants.CHESS_BING)
        self._pieces[3][4].set_camp(constants.CAMP_RED)
        self._pieces[3][6].set_pic(' 卒 ')
        self._pieces[3][6].set_type(constants.CHESS_BING)
        self._pieces[3][6].set_camp(constants.CAMP_RED)
        self._pieces[3][-1].set_pic(' 卒 ')
        self._pieces[3][-1].set_type(constants.CHESS_BING)
        self._pieces[3][-1].set_camp(constants.CAMP_RED)

        # init WHITE Camp and Pic
        for idx in range(self._width):
            self._pieces[-1][idx].set_camp(constants.CAMP_WHITE)
        self._pieces[-1][0].set_pic(' 車 ')
        self._pieces[-1][0].set_type(constants.CHESS_CHE)
        self._pieces[-1][1].set_pic(' 馬 ')
        self._pieces[-1][1].set_type(constants.CHESS_MA)
        self._pieces[-1][2].set_pic(' 相 ')
        self._pieces[-1][2].set_type(constants.CHESS_XIANG)
        self._pieces[-1][3].set_pic(' 仕 ')
        self._pieces[-1][3].set_type(constants.CHESS_SHI)
        self._pieces[-1][4].set_pic(' 帥 ')
        self._pieces[-1][4].set_type(constants.CHESS_BOSS)
        self._pieces[-1][5].set_pic(' 仕 ')
        self._pieces[-1][5].set_type(constants.CHESS_SHI)
        self._pieces[-1][6].set_pic(' 相 ')
        self._pieces[-1][6].set_type(constants.CHESS_XIANG)
        self._pieces[-1][7].set_pic(' 馬 ')
        self._pieces[-1][7].set_type(constants.CHESS_MA)
        self._pieces[-1][8].set_pic(' 車 ')
        self._pieces[-1][8].set_type(constants.CHESS_CHE)
        # 上面的camp已经通过循环统一设置过了
        self._pieces[-3][1].set_pic(' 砲 ')
        self._pieces[-3][1].set_type(constants.CHESS_PAO)
        self._pieces[-3][1].set_camp(constants.CAMP_WHITE)
        self._pieces[-3][7].set_pic(' 砲 ')
        self._pieces[-3][7].set_type(constants.CHESS_PAO)
        self._pieces[-3][7].set_camp(constants.CAMP_WHITE)
        self._pieces[-4][0].set_pic(' 兵 ')
        self._pieces[-4][0].set_type(constants.CHESS_BING)
        self._pieces[-4][0].set_camp(constants.CAMP_WHITE)
        self._pieces[-4][2].set_pic(' 兵 ')
        self._pieces[-4][2].set_type(constants.CHESS_BING)
        self._pieces[-4][2].set_camp(constants.CAMP_WHITE)
        self._pieces[-4][4].set_pic(' 兵 ')
        self._pieces[-4][4].set_type(constants.CHESS_BING)
        self._pieces[-4][4].set_camp(constants.CAMP_WHITE)
        self._pieces[-4][6].set_pic(' 兵 ')
        self._pieces[-4][6].set_type(constants.CHESS_BING)
        self._pieces[-4][6].set_camp(constants.CAMP_WHITE)
        self._pieces[-4][8].set_pic(' 兵 ')
        self._pieces[-4][8].set_type(constants.CHESS_BING)
        self._pieces[-4][8].set_camp(constants.CAMP_WHITE)

        # init cursor 〄 〠
        self._cursor_original_backup: ChessPiece = self._pieces[self._cursor_loc['y']][self._cursor_loc['x']]
        tmp = ChessPiece(self.cursor_pic(), constants.CAMP_CURSOR)
        tmp.set_type(constants.CHESS_CURSOR)
        self._pieces[self._cursor_loc['y']][self._cursor_loc['x']] = tmp
        del tmp

        self.strategies = chess_strategy.ChessStrategy(self._pieces, True)

    def show_map(self):
        for y in range(self._height):
            for x in range(self._width):
                self._pieces[y][x].show()
            if y == 4:
                print()
                # 楚汉分割线
                print('***********************************')
            else:
                print('\n')

    def clear_map(self):
        return common.clear_console()

    def cursor_move(self, p_target):
        self._pieces[self._cursor_loc['y']][self._cursor_loc['x']] = self._cursor_original_backup
        self._cursor_original_backup = self._pieces[p_target['y']][p_target['x']]
        tmp = ChessPiece(self.cursor_pic(), constants.CAMP_CURSOR)
        tmp.set_type(constants.CHESS_CURSOR)
        self._pieces[p_target['y']][p_target['x']] = tmp
        self._cursor_loc = p_target
        # 刷新地图
        self.clear_map()
        self.show_map()

    # 参数类型限定和返回值类型限定可以不要【类似ts里可以不要】
    def can_move(self, direct: str) -> bool:
        if direct == 'w':
            if self._cursor_loc['y'] - 1 < 0:
                return False
        elif direct == 'd':
            if self._cursor_loc['x'] + 1 >= self._width:
                return False
        elif direct == 's':
            if self._cursor_loc['y'] + 1 >= self._height:
                return False
        elif direct == 'a':
            if self._cursor_loc['x'] - 1 < 0:
                return False
        else:
            return False
        return True

    def cursor_pic(self) -> str:
        if self._checked:
            return self.CURSOR_CHECKED
        else:
            return self.CURSOR_UNCHECKED

    """ Python3里可以手动指定返回值类型，而且参数类型也是可以指定的 """
    def control(self) -> None:
        while True:
            ch = self._getch()
            # 清空之前的显示状态
            self.clear_map()
            # 重新绘制象棋布局
            self.show_map()

            if ch == 'w' or ch == 'A' or ch == b'w' or ch == b'H':
                if self.can_move('w'):
                    self.cursor_move({'x': self._cursor_loc['x'], 'y': self._cursor_loc['y'] - 1})
                print('↑', end='')
            elif ch == 'd' or ch == 'C' or ch == b'd' or ch == b'M':
                if self.can_move('d'):
                    self.cursor_move({'x': self._cursor_loc['x'] + 1, 'y': self._cursor_loc['y']})
                print('→', end='')
            elif ch == 's' or ch == 'B' or ch == b's' or ch == b'P':
                if self.can_move('s'):
                    self.cursor_move({'x': self._cursor_loc['x'], 'y': self._cursor_loc['y'] + 1})
                print('↓', end='')
            elif ch == 'a' or ch == 'D' or ch == b'a' or ch == b'K':
                if self.can_move('a'):
                    self.cursor_move({'x': self._cursor_loc['x'] - 1, 'y': self._cursor_loc['y']})
                print('←', end='')
            elif ch.lower() == 'q' or ch == b'q':
                print('game quit!')
                sys.stdout.flush()
                break
            elif ch == ' ' or ch == b' ':
                if not self._checked:
                    self.do_check()
                    print('选中', end='')
                else:
                    self.do_release()
                    print('释放', end='')
                # 判定游戏是否结束
                if self.game_over:
                    print('\ngame over!, 胜利方是:' + self.winner)
                    sys.stdout.flush()
                    break
            else:
                print('无效按键', end='')
            # 立刻刷新输入流，否则getch()获取的字符不会立刻显示
            sys.stdout.flush()

    def can_check(self):
        tmp = self._cursor_original_backup.get_camp()
        if tmp != constants.CAMP_RED and tmp != constants.CAMP_WHITE:
            return False
        if self.firster == constants.CAMP_RED and tmp == constants.CAMP_WHITE:
            return False
        if self.firster == constants.CAMP_WHITE and tmp == constants.CAMP_RED:
            return False
        return True

    def do_check(self):
        if self.can_check():
            self._checked = ~self._checked
            self._pieces[self._cursor_loc['y']][self._cursor_loc['x']].set_pic(self.cursor_pic())
            # 复制一份，和Java一样基础类型是值赋值，而对象是引用赋值
            self._checked_loc = self._cursor_loc.copy()
            self.clear_map()
            self.show_map()

    def do_release(self):
        # 判定是否是取消，是取消则不翻转当前选手
        if self._cursor_loc['x'] == self._checked_loc['x'] and self._cursor_loc['y'] == self._checked_loc['y']:
            self._checked = ~self._checked
            self._pieces[self._cursor_loc['y']][self._cursor_loc['x']].set_pic(self.cursor_pic())
            self.clear_map()
            self.show_map()
            return
        if self.can_release():
            self._checked = ~self._checked
            # 判断游戏是否结束
            if self._cursor_original_backup.get_camp() != constants.CAMP_NONE and self._cursor_original_backup.get_type() == constants.CHESS_BOSS:
                self.game_over = True
                self.winner = self.firster
            # 切换释放棋子后的布局
            self._cursor_original_backup = self._pieces[self._checked_loc['y']][self._checked_loc['x']]
            tmp = ChessPiece(self.PIECE_NONE, constants.CAMP_NONE)
            tmp.set_type(constants.CHESS_PIECE)
            self._pieces[self._checked_loc['y']][self._checked_loc['x']] = tmp
            self._pieces[self._cursor_loc['y']][self._cursor_loc['x']].set_pic(self.cursor_pic())
            self.clear_map()
            self.show_map()
            # 切换选手
            self.reverse_role()

    """ 策略层，TODO 待完善 """
    def can_release(self):
        # 初步判定，至少不能吃自己这边的子【Python里函数调用太坑了吧，刚才self._cursor_original_backup.get_camp这种方式居然不报错。。】
        if self._cursor_original_backup.get_camp() == self.firster:
            return False
        # 其他规则
        tmp = self._pieces[self._checked_loc['y']][self._checked_loc['x']]
        if tmp.get_type() == constants.CHESS_BING:
            return self.strategies.bing(tmp, self._checked_loc, self._cursor_loc)
        if tmp.get_type() == constants.CHESS_CHE:
            return self.strategies.che(self._checked_loc, self._cursor_loc)
        if tmp.get_type() == constants.CHESS_PAO:
            return self.strategies.pao(self._cursor_original_backup, self._checked_loc, self._cursor_loc)
        if tmp.get_type() == constants.CHESS_MA:
            return self.strategies.ma(self._checked_loc, self._cursor_loc)
        if tmp.get_type() == constants.CHESS_XIANG:
            return self.strategies.xiang(tmp, self._checked_loc, self._cursor_loc)
        if tmp.get_type() == constants.CHESS_SHI:
            return self.strategies.shi(tmp, self._checked_loc, self._cursor_loc)
        if tmp.get_type() == constants.CHESS_BOSS:
            return self.strategies.boss(tmp, self._cursor_original_backup, self._checked_loc, self._cursor_loc)
        return True

    def reverse_role(self):
        if self.firster == constants.CAMP_RED:
            self.firster = constants.CAMP_WHITE
        else:
            self.firster = constants.CAMP_RED

    def start(self):
        self.clear_map()
        self.show_map()
        self.control()


# 和类定义相关的代码就要求空两行，上面是类结束，所以这里需要空两行（当然不是强制的）
if __name__ == '__main__':
    game = GameContext()
    game.clear_map()
    game.show_map()
    game.control()
