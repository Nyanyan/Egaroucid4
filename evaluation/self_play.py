from random import randrange
import subprocess
import sys

hw = 8
hw2 = 64
board_index_num = 38
dy = [0, 1, 0, -1, 1, 1, -1, -1]
dx = [1, 0, -1, 0, 1, -1, 1, -1]

def empty(grid, y, x):
    return grid[y][x] == -1 or grid[y][x] == 2

def inside(y, x):
    return 0 <= y < hw and 0 <= x < hw

def check(grid, player, y, x):
    res_grid = [[False for _ in range(hw)] for _ in range(hw)]
    res = 0
    for dr in range(8):
        ny = y + dy[dr]
        nx = x + dx[dr]
        if not inside(ny, nx):
            continue
        if empty(grid, ny, nx):
            continue
        if grid[ny][nx] == player:
            continue
        #print(y, x, dr, ny, nx)
        plus = 0
        flag = False
        for d in range(hw):
            nny = ny + d * dy[dr]
            nnx = nx + d * dx[dr]
            if not inside(nny, nnx):
                break
            if empty(grid, nny, nnx):
                break
            if grid[nny][nnx] == player:
                flag = True
                break
            #print(y, x, dr, nny, nnx)
            plus += 1
        if flag:
            res += plus
            for d in range(plus):
                nny = ny + d * dy[dr]
                nnx = nx + d * dx[dr]
                res_grid[nny][nnx] = True
    return res, res_grid

def pot_canput_line(arr):
    res_p = 0
    res_o = 0
    for i in range(len(arr) - 1):
        if arr[i] == -1 or arr[i] == 2:
            if arr[i + 1] == 0:
                res_o += 1
            elif arr[i + 1] == 1:
                res_p += 1
    for i in range(1, len(arr)):
        if arr[i] == -1 or arr[i] == 2:
            if arr[i - 1] == 0:
                res_o += 1
            elif arr[i - 1] == 1:
                res_p += 1
    return res_p, res_o

class reversi:
    def __init__(self):
        self.grid = [[-1 for _ in range(hw)] for _ in range(hw)]
        self.grid[3][3] = 1
        self.grid[3][4] = 0
        self.grid[4][3] = 0
        self.grid[4][4] = 1
        self.player = 0 # 0: 黒 1: 白
        self.nums = [2, 2]

    def move(self, y, x):
        plus, plus_grid = check(self.grid, self.player, y, x)
        if (not empty(self.grid, y, x)) or (not inside(y, x)) or not plus:
            print('Please input a correct move')
            return 1
        self.grid[y][x] = self.player
        for ny in range(hw):
            for nx in range(hw):
                if plus_grid[ny][nx]:
                    self.grid[ny][nx] = self.player
        self.nums[self.player] += 1 + plus
        self.nums[1 - self.player] -= plus
        self.player = 1 - self.player
        return 0
    
    def check_pass(self):
        for y in range(hw):
            for x in range(hw):
                if self.grid[y][x] == 2:
                    self.grid[y][x] = -1
        res = True
        for y in range(hw):
            for x in range(hw):
                if not empty(self.grid, y, x):
                    continue
                plus, _ = check(self.grid, self.player, y, x)
                if plus:
                    res = False
                    self.grid[y][x] = 2
        if res:
            #print('Pass!')
            self.player = 1 - self.player
        return res

    def output(self):
        print('  ', end='')
        for i in range(hw):
            print(chr(ord('a') + i), end=' ')
        print('')
        for y in range(hw):
            print(str(y + 1) + ' ', end='')
            for x in range(hw):
                print('○' if self.grid[y][x] == 0 else '●' if self.grid[y][x] == 1 else '* ' if self.grid[y][x] == 2 else '. ', end='')
            print('')
    
    def output_file(self):
        res = ''
        for y in range(hw):
            for x in range(hw):
                res += '*' if self.grid[y][x] == 0 else 'O' if self.grid[y][x] == 1 else '-'
        res += ' *'
        return res

    def end(self):
        if min(self.nums) == 0:
            return True
        res = True
        for y in range(hw):
            for x in range(hw):
                if self.grid[y][x] == -1 or self.grid[y][x] == 2:
                    res = False
        return res
    
    def judge(self):
        if self.nums[0] > self.nums[1]:
            #print('Black won!', self.nums[0], '-', self.nums[1])
            return 0
        elif self.nums[1] > self.nums[0]:
            #print('White won!', self.nums[0], '-', self.nums[1])
            return 1
        else:
            #print('Draw!', self.nums[0], '-', self.nums[1])
            return -1


def record_translate(record):
    res = []
    for i in range(0, len(record), 2):
        x = ord(record[i]) - ord('a')
        y = int(record[i + 1]) - 1
        res.append([y, x])
    return res

with open('third_party/records3.txt', 'r') as f:
    tactic = [record_translate(elem) for elem in f.read().splitlines()]
ln_tactic = len(tactic)

ais = []

def init_ai():
    global ais
    ais = [subprocess.Popen('./ai2.out'.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL) for _ in range(2)]
    ais[0].stdin.write('param.txt\n'.encode('utf-8'))
    ais[1].stdin.write('param_new.txt\n'.encode('utf-8'))

init_ai()

def self_play():
    old_win = 0
    new_win = 0
    draw_num = 0
    play_num = int(input())
    for _ in range(play_num):
        for i in range(2): # 0: old-black, new-white  1: new_black, old_white
            print('=', end='', file=sys.stderr, flush=True)
            rv = reversi()
            tactic_idx = randrange(0, ln_tactic)
            for y, x in tactic[tactic_idx]:
                rv.check_pass()
                rv.check_pass()
                rv.move(y, x)
            break_flag = False
            while True:
                if rv.check_pass() and rv.check_pass():
                    break
                ai_idx = (rv.player + i) % 2
                stdin_str = str(rv.player) + '\n'
                for yy in range(hw):
                    for xx in range(hw):
                        stdin_str += '0' if rv.grid[yy][xx] == 0 else '1' if rv.grid[yy][xx] == 1 else '.'
                    stdin_str += '\n'
                #print(stdin_str)
                try:
                    ais[ai_idx].stdin.write(stdin_str.encode('utf-8'))
                    ais[ai_idx].stdin.flush()
                    y, x = [int(elem) for elem in ais[ai_idx].stdout.readline().split()]
                except:
                    print('err')
                    break_flag = True
                    for j in range(2):
                        try:
                            ais[j].kill()
                        except:
                            continue
                    init_ai()
                    break
                rv.move(y, x)
            if not break_flag:
                if rv.nums[i] > rv.nums[(i + 1) % 2]: # old won
                    old_win += 1
                elif rv.nums[i] < rv.nums[(i + 1) % 2]: # new won
                    new_win += 1
                else:
                    draw_num += 1
    print(play_num * 2, old_win, new_win, draw_num)

while True:
    self_play()