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

play_num = 12000
parallel_num = 6
parallel_exe_num = play_num // parallel_num

self_plays = [subprocess.Popen('python self_play.py'.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=None) for _ in range(parallel_num)]

def self_play():
    for i in range(parallel_num):
        self_plays[i].stdin.write((str(parallel_exe_num) + '\n' + str(i * parallel_exe_num // 1000) + '\n').encode('utf-8'))
        self_plays[i].stdin.flush()
    for i in range(parallel_num):
        self_plays[i].wait()


self_play()

for i in range(parallel_num):
    self_plays[i].kill()
