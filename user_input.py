import tty, sys, termios


class UserInput:
    def __init__(self):
        pass

    def next_command(self):
        pass


class MockUserInput(UserInput):
    def __init__(self, fname):
        self._file = open(fname, 'r')

    def next_command(self):
        char = self._file.read(1)
        if char == '':
            return "EOF"
        return char


class ConsoleOneCharInput(UserInput):
    def __init__(self):
        pass

    def next_command(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
            if ch == 'q':
                ch = "EOF"
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


