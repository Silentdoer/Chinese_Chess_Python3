import math

from chess_piece import ChessPiece
import constants


# 好吧，Python规范里要求类和其他代码之间空两行，而且要求整个文件最后一行是空行，然后#和前面的代码空两个空格
class ChessStrategy:

    pieces: []

    _height = 0
    _width = 0

    _red_up = True
    _red_line = 4
    _white_line = 5
    _boss_x_left = 3
    _boss_x_right = 5
    _boss_y_red = 2
    _boss_y_white = 7

    # [ChessPiece]限定列表元素类型为ChessPiece
    def __init__(self, pieces: [ChessPiece], red_up: bool = True):
        self.pieces = pieces
        self._height = len(pieces)
        self._height = len(pieces[0])
        # 红方是否在地图上方，这关乎到兵不能后退等问题
        self._red_up = red_up
        # 红方和白方的楚河汉界线
        if red_up:
            self._red_line = 4
            self._white_line = 5
            self._boss_y_red = 2
            self._boss_y_white = 7
        else:
            self._red_line = 5
            self._white_line = 4
            self._boss_y_red = 7
            self._boss_y_white = 2

    """ 是否直着走 """
    def is_straight(self, origin: {}, dest: {}) -> bool:
        if (origin['x'] - dest['x']) * (origin['y'] - dest['y']) == 0:
            return True

    """ 兵的阵营，象棋地图，待移动兵的坐标 """
    def bing(self, active: ChessPiece, origin: {}, dest: {}):
        # 存在斜着走判定
        if not self.is_straight(origin, dest):
            return False
        # 存在移动超过多步判定
        if abs(origin['x'] - dest['x']) > 1 or abs(origin['y'] - dest['y']) > 1:
            return False
        # 不能后退判定和过了河才能左右移动判定
        if self._red_up:
            if active.get_camp() == constants.CAMP_RED:
                if dest['y'] - origin['y'] < 0:
                    return False
                # 过河才能左右移动
                if abs(dest['x'] - origin['x']) > 0:
                    if origin['y'] <= self._red_line:
                        return False
            else:
                if dest['y'] - origin['y'] > 0:
                    return False
                # 过了河才能左右移动
                if abs(dest['x'] - origin['x']) > 0:
                    if origin['y'] >= self._white_line:
                        return False
        else:  # 红方在下面
            if active.get_camp() == constants.CAMP_RED:
                if dest['y'] - origin['y'] > 0:
                    return False
                # 过了河才能左右移动
                if abs(dest['x'] - origin['x']) > 0:
                    if origin['y'] >= self._white_line:
                        return False
            else:
                if dest['y'] - origin['y'] < 0:
                    return False
                # 过了河才能左右移动
                if abs(dest['x'] - origin['x']) > 0:
                    if origin['y'] <= self._white_line:
                        return False
        return True

    """ 車 """
    def che(self, origin: {}, dest: {}):
        if not self.is_straight(origin, dest):
            return False
        if abs(origin['x'] - dest['x']) == 1 or abs(origin['y'] - dest['y']) == 1:
            return True
        # 横着走
        if origin['x'] - dest['x'] != 0:
            for idx in range(min(origin['x'], dest['x']) + 1, max(origin['x'], dest['x'])):
                if self.pieces[dest['y']][idx].get_type() != constants.CHESS_PIECE:
                    return False
        else:  # 竖着走
            for idx in range(min(origin['y'], dest['y']) + 1, max(origin['y'], dest['y'])):
                if self.pieces[idx][dest['x']].get_type() != constants.CHESS_PIECE:
                    return False
        return True

    """ 炮 """
    def pao(self, dest_piece: ChessPiece, origin: {}, dest: {}):
        if not self.is_straight(origin, dest):
            return False

        middle_count = 0
        if origin['x'] - dest['x'] != 0:  # 横着走
            for idx in range(min(origin['x'], dest['x']) + 1, max(origin['x'], dest['x'])):
                if self.pieces[dest['y']][idx].get_type() != constants.CHESS_PIECE:
                    middle_count += 1
        else:  # 竖着走
            for idx in range(min(origin['y'], dest['y']) + 1, max(origin['y'], dest['y'])):
                if self.pieces[idx][dest['x']].get_type() != constants.CHESS_PIECE:
                    middle_count += 1
        if middle_count > 1:
            return False
        if middle_count == 1 and dest_piece.get_camp() == constants.CAMP_NONE:
            return False
        if middle_count == 0 and dest_piece.get_camp() != constants.CAMP_NONE:
            return False
        return True

    def ma(self, origin: {}, dest: {}):
        # 走日字判断
        if abs((origin['x'] - dest['x']) * (origin['y'] - dest['y'])) != 2:
            return False
        # 拗马脚判断
        tmpy = math.trunc((dest['y'] - origin['y'])/2)
        tmpx = math.trunc((dest['x'] - origin['x'])/2)
        middlex = origin['x'] + tmpx
        middley = origin['y'] + tmpy
        if self.pieces[middley][middlex].get_camp() != constants.CAMP_NONE:
            return False
        return True

    def xiang(self, active: ChessPiece, origin: {}, dest: {}):
        # 判断是否是田字走法
        if abs(origin['x'] - dest['x']) != 2 or abs(origin['y'] - dest['y']) != 2:
            return False
        # 判断是否拗象脚
        tmpx = (dest['x'] - origin['x'])//2 + origin['x']
        tmpy = (dest['y'] - origin['y'])//2 + origin['y']
        if self.pieces[tmpy][tmpx].get_camp() != constants.CAMP_NONE:
            return False
        # 象不能过河的判断
        if self._red_up:
            if active.get_camp() == constants.CAMP_RED:
                if dest['y'] > self._red_line:
                    return False
            else:
                if dest['y'] < self._white_line:
                    return False
        else:  # 红方在下面
            if active.get_camp() == constants.CAMP_RED:
                if dest['y'] < self._red_line:
                    return False
            else:
                if dest['y'] > self._white_line:
                    return False
        return True

    def shi(self, active: ChessPiece, origin: {}, dest: {}):
        # 判断是否走的斜线且距离为1
        if abs((dest['x'] - origin['x']) * (dest['y'] - origin['y'])) != 1:
            return False
        # 判断是否移出左右边界
        if dest['x'] < self._boss_x_left or dest['x'] > self._boss_x_right:
            return False
        # 判断是否移出Y轴边界
        if self._red_up:
            if active.get_camp() == constants.CAMP_RED:
                if dest['y'] > self._boss_y_red:
                    return False
            else:
                if dest['y'] < self._boss_y_white:
                    return False
        else:  # 红方在下面
            if active.get_camp() == constants.CAMP_RED:
                if dest['y'] < self._boss_y_red:
                    return False
            else:
                if dest['y'] > self._boss_y_white:
                    return False
        return True

    def boss(self, active: ChessPiece, dest_piece: ChessPiece, origin: {}, dest: {}):
        # 判断是否将帅见面，这种情况下可以移动到对方大本营里吃对方主将
        if active.get_type() == constants.CHESS_BOSS and dest_piece.get_type() == constants.CHESS_BOSS and origin['x'] == dest['x']:
            middle_count = 0
            for idx in range(min(origin['y'], dest['y']) + 1, max(origin['y'], dest['y'])):
                if self.pieces[idx][dest['x']].get_type() != constants.CHESS_PIECE:
                    middle_count += 1
                    break
            if middle_count == 0:
                return True
        # 判断是否走的直线且距离为1
        if abs(dest['x'] - origin['x']) + abs(dest['y'] - origin['y']) != 1:
            return False
        # 判断是否移出左右边界
        if dest['x'] < self._boss_x_left or dest['x'] > self._boss_x_right:
            return False
        # 判断是否移出Y轴边界
        if self._red_up:
            if active.get_camp() == constants.CAMP_RED:
                if dest['y'] > self._boss_y_red:
                    return False
            else:
                if dest['y'] < self._boss_y_white:
                    return False
        else:  # 红方在下面
            if active.get_camp() == constants.CAMP_RED:
                if dest['y'] < self._boss_y_red:
                    return False
            else:
                if dest['y'] > self._boss_y_white:
                    return False
        return True
