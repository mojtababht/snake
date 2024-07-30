class Snake:

    def __init__(self, color=(68, 113, 230)):
        self.color = color
        self.points = [(0, 0), (1, 0)]
        self.dir = 'r'

    def move(self, ate=False):
        x, y = self.points[-1]
        match self.dir:
            case 'r':
                if x == 14:
                    x = 0
                else:
                    x += 1
            case 'l':
                if x == 0:
                    x = 14
                else:
                    x -= 1
            case 'u':
                if y == 0:
                    y = 14
                else:
                    y -= 1
            case 'd':
                if y == 14:
                    y = 0
                else:
                    y += 1
        self.points.append((x, y))
        if not ate:
            self.points.pop(0)

    def change_dir(self, dir):
        if {self.dir, dir} == {'l', 'r'} or {self.dir, dir} == {'u', 'd'}:
            return
        self.dir = dir
