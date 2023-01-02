import csv

max_speed_ball = 0
min_speed_ball = 0
max_speed_player1 = 0
speed_player1 = 0
max_speed_player2 = 0
speed_player2 = 0

with open('physics/ball.cvt', encoding="utf8") as f:
    reader = csv.reader(f, delimiter='=')
    for index, row in enumerate(reader):
        if row[0] == 'max_speed':
            max_speed_ball = int(row[-1])
        if row[0] == 'min_speed':
            min_speed_ball = int(row[-1])

with open('physics/Player_1.cvt', encoding="utf8") as f:
    reader = csv.reader(f, delimiter='=')
    for index, row in enumerate(reader):
        if row[0] == 'max_speed':
            max_speed_player1 = int(row[-1])
        if row[0] == 'speed':
            speed_player1 = int(row[-1])

with open('physics/Player_2.cvt', encoding="utf8") as f:
    reader = csv.reader(f, delimiter='=')
    for index, row in enumerate(reader):
        if row[0] == 'max_speed':
            max_speed_player2 = int(row[-1])
        if row[0] == 'speed':
            speed_player2 = int(row[-1])
