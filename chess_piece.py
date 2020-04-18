# coding:utf-8
import piece
import constants
import common


class ChessPiece(piece.Piece):
    """
    定义象棋棋子
    """

    __camp = ''

    __type = ''

    def __init__(self, pic, camp):
        piece.Piece.__init__(self, pic)
        self.__camp = camp

    def get_camp(self):
        return self.__camp

    def get_pic(self):
        return self._pic

    def set_camp(self, camp):
        self.__camp = camp

    def set_pic(self, pic):
        self._pic = pic

    def set_type(self, chess_type):
        self.__type = chess_type

    def get_type(self):
        return self.__type

    def show(self, new_line=False):
        if self.__camp == constants.CAMP_RED:
            common.printc(new_line, self._pic, constants.FORE_RED)
        elif self.__camp == constants.CAMP_WHITE:
            common.printc(new_line, self._pic, constants.FORE_WHITE)
        elif self.__camp == constants.CAMP_CURSOR:
            common.printc(new_line, self._pic, constants.FORE_YELLOW)
        else:
            common.printc(new_line, self._pic, constants.FORE_BLUE)
