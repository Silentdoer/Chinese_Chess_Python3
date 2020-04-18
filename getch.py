class Getch():
    """ 用来实现不需要按enter键读取输入字符 """

    def __init__(self):
        import platform
        system_name = platform.system()
        if system_name == 'Windows':
            self.impl = GetchWindows()
        else:  # 默认是Linux（目前就支持Windows和Linux即可）
            self.impl = GetchUnix()

    def __call__(self): return self.impl()


class GetchUnix:
    def __init__(self):
        pass

    def __call__(self):
        # 不要用import sys, tty这种逗号的方式导入
        import sys
        import tty
        import termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class GetchWindows:
    def __init__(self):
        pass

    def __call__(self):
        import msvcrt
        return msvcrt.getch()
