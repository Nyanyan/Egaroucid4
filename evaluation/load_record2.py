from tqdm import trange
import subprocess
import glob

hw = 8
hw2 = 64
board_index_num = 38
dy = [0, 1, 0, -1, 1, 1, -1, -1]
dx = [1, 0, -1, 0, 1, -1, 1, -1]

def digit(n, r):
    n = str(n)
    l = len(n)
    for i in range(r - l):
        n = '0' + n
    return n

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

evaluate = subprocess.Popen('./ai.out'.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

def change_f5(y, x):
    return y, x

def change_d3(y, x):
    return 7 - x, 7 - y

def change_c4(y, x):
    return 7 - y, 7 - x

def change_e6(y, x):
    return x, y

def collect_data(num, s):
    grids = []
    rv = reversi()
    idx = 0
    turn = 0
    first_f = s[0] + s[1]
    while True:
        if idx >= len(s):
            return 0
        if rv.check_pass() and rv.check_pass():
            break
        x = ord(s[idx]) - ord('A')
        y = int(s[idx + 1]) - 1
        if first_f == 'D3':
            y, x = change_d3(y, x)
        elif first_f == 'C4':
            y, x = change_c4(y, x)
        elif first_f == 'E6':
            y, x = change_e6(y, x)
        idx += 2
        grid_str = ''
        for i in range(hw):
            for j in range(hw):
                grid_str += '0' if rv.grid[i][j] == 0 else '1' if rv.grid[i][j] == 1 else '.'
            grid_str += '\n'
        evaluate.stdin.write((str(rv.player) + '\n' + grid_str + '\n').encode('utf-8'))
        evaluate.stdin.flush()
        add_data = evaluate.stdout.readline().decode().replace('\r\n', '')
        grids.append(grid_str.replace('\n', '') + ' ' + str(rv.player) + ' ' + add_data)
        if rv.move(y, x):
            print('error')
            exit()
        turn += 1
        if rv.end():
            break
    rv.check_pass()
    #score = 1 if rv.nums[0] > rv.nums[1] else 0 if rv.nums[0] == rv.nums[1] else -1
    result = rv.nums[0] - rv.nums[1]
    score = 1 if result > 0 else -1 if result < 0 else 0
    with open('data/' + digit(num, 7) + '.txt', 'a') as f:
        for grid in grids:
            f.write(grid + ' ' + str(result) + '\n')
    return 1

files = glob.glob('./third_party/records2_raw/*')
used = 0
for file_idx in trange(len(files)):
    file = files[file_idx]
    with open(file, 'r') as f:
        raw_data = f.read()
    record = raw_data.replace(';', '').replace('-', '')
    used += collect_data(file_idx // 1000, record)
print(used)