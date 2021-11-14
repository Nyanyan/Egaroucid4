from math import tan, atan
from time import time
from random import randrange
import subprocess
from tqdm import trange

f_weight = 0.000105
ln_char = 27605
ln_char_d2 = ln_char // 2
tl = 10000000000

def f(x):
    return tan(f_weight * (x - ln_char_d2))

def rev_f(y):
    return round(atan(y) / f_weight + ln_char_d2)

nums = [f(i) for i in range(ln_char)]

play_num = 98
parallel_num = 7
parallel_exe_num = play_num // parallel_num

self_plays = [subprocess.Popen('python self_play.py'.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=None) for _ in range(parallel_num)]

def self_play():
    strt = time()
    old_win = 0
    new_win = 0
    draw_num = 0
    played_num = 0
    for i in range(parallel_num):
        self_plays[i].stdin.write((str(parallel_exe_num) + '\n').encode('utf-8'))
        self_plays[i].stdin.flush()
    for i in range(parallel_num):
        p, o, n, d = [int(elem) for elem in self_plays[i].stdout.readline().split()]
        played_num += p
        old_win += o
        new_win += n
        draw_num += d
    print('')
    print(time() - strt, played_num, old_win, new_win, draw_num)
    return (new_win - old_win) / played_num

with open('param/raw_param.txt', 'r') as f:
    raw_params = [float(i) for i in f.read().splitlines()]

params = []
for elem in raw_params:
    params.append(rev_f(elem))
ln_params = len(params)

with open('param/param.txt', 'w') as f:
    for elem in params:
        f.write(str(nums[elem]) + '\n')

strt = time()
while True: #time() - strt < tl:
    idx = randrange(0, ln_params)
    delta = randrange(-10, 10 + 1)
    if params[idx] + delta < 0 or params[idx] + delta >= ln_params:
        continue
    params[idx] += delta
    with open('param/param_new.txt', 'w') as f:
        for elem in params:
            f.write(str(nums[elem]) + '\n')
    result = self_play()
    if result >= 0.0:
        print('update')
        with open('param/param.txt', 'w') as f:
            for elem in params:
                f.write(str(nums[elem]) + '\n')
    else:
        params[idx] -= delta

for i in range(2):
    ais[i].kill()