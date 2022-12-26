

def move(obj, rule, rep):
    x, y = obj.pos
    if rule == 'right_d' and x + obj.image.get_rect().size[0] < width - 30:
        for i in range(rep):
            obj.move(x + speed_player2, y)
    if rule == 'left_a' and x > 5:
        for i in range(rep):
            obj.move(x - speed_player2, y)
    if rule == 'left_s' and x > 5:
        for i in range(rep):
            obj.move(x - speed_player1, y)
    if rule == 'right_s' and x + obj.image.get_rect().size[0] < width - 30:
        for i in range(rep):
            obj.move(x + speed_player1, y)
    if rule == 'up' and x + obj.image.get_rect().size[0] < width - 30:
        for i in range(rep):
            obj.move(x, y - speed_player1)
    if rule == 'down' and x + obj.image.get_rect().size[0] < width - 30:
        for i in range(rep):
            obj.move(x, y + speed_player1)