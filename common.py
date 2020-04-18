def printc(new_line, content, forecolor='', backcolor=''):
    if forecolor != '':
        forecolor = ';' + forecolor
    if backcolor != '':
        backcolor = ';' + backcolor

    flag = ''
    if new_line:
        flag = '\n'
    print('\033[0' + forecolor + backcolor + 'm' + content + '\033[0m', end=flag)

def clear_console():
    import platform
    import os
    system_name = platform.system()
    if system_name == 'Windows':
        os.system("cls")
    else:  # 默认是Linux（目前就支持Windows和Linux即可）
        os.system("clear")