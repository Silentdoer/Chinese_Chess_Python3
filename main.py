# coding:utf-8
import platform
import sys

if __name__ == '__main__':
    system = platform.system()
    if system == 'Windows':
        print('请使用Linux系统，最好是Ubuntu18.x版本，否则其他的控制台输出的布局可能会不整齐')
        # exit()
    if sys.version_info < (3, 0) or sys.version_info >= (4, 0):
        print('请使用Python3.x')
        exit()
    print("Game started.")
    import game_context
    import constants
    game = game_context.GameContext(constants.CAMP_WHITE)
    game.start()
