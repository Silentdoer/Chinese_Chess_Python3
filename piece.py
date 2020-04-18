class Piece:
    """ 定义棋子基类 """

    def __init__(self, pic):
        self._pic = pic

    def show(self, new_line=False):
        if new_line:
            print(self._pic)
        else:
            print(self._pic, end='')
