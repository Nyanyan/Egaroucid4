from random import randint, randrange
import subprocess
from tqdm import trange
from time import sleep, time
from math import exp
from random import random
import statistics

inf = 10000000.0

hw = 8
min_n_stones = 4 + 10

def digit(n, r):
    n = str(n)
    l = len(n)
    for i in range(r - l):
        n = '0' + n
    return n

def calc_n_stones(board):
    res = 0
    for elem in board:
        res += int(elem != '.')
    return res

evaluate = subprocess.Popen('./mpc.out'.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
sleep(1)

vhs = [[] for _ in range(6)]
vds = [[] for _ in range(6)]

vh_vd = []


def collect_data(num):
    global vhs, vds, vh_vd
    try:
        with open('data/' + digit(num, 7) + '.txt', 'r') as f:
            data = list(f.read().splitlines())
    except:
        print('cannot open')
        return
    for _ in trange(5000):
        datum = data[randrange(0, len(data))]
        board, player, _, _, _, _ = datum.split()
        n_stones = calc_n_stones(board)
        depth = randint(3, 10)
        board_proc = player + '\n' + str(depth // 4) + '\n' + str(int(depth)) + '\n'
        for i in range(hw):
            for j in range(hw):
                board_proc += board[i * hw + j]
            board_proc += '\n'
        #print(board_proc)
        evaluate.stdin.write(board_proc.encode('utf-8'))
        evaluate.stdin.flush()
        vd, vh = [float(i) for i in evaluate.stdout.readline().decode().strip().split()]
        #print(score)
        vhs[(n_stones - 4) // 10].append(vh)
        vds[(n_stones - 4) // 10].append(vd)

for i in range(1):
    collect_data(i)
for i in range(6):
    print(len(vhs[i]), vhs[i][:10])
    print(len(vds[i]), vds[i][:10])

start_temp = 1000.0
end_temp   = 10.0
def temperature_x(x):
    #return pow(start_temp, 1 - x) * pow(end_temp, x)
    return start_temp + (end_temp - start_temp) * x

def prob(p_score, n_score, strt, now, tl):
    dis = p_score - n_score
    if dis >= 0:
        return 1.0
    return exp(dis / temperature_x((now - strt) / tl))

a = 1.0
b = 0.0
'''
def scoring():
    dv = 0
    for i in range(1, 6):
        dv += len(vhs[i])
    return sum([sum([(vhs[j][i] - (a * vds[j][i] + b)) ** 2 for i in range(len(vhs[j]))]) for j in range(1, 6)]) / dv

f_score = scoring()
print(f_score)

tl = 60.0
strt = time()
while time() - strt < tl:
    rnd = random()
    if rnd < 0.5:
        fa = a
        a += random() * 0.02 - 0.01
        score = scoring()
        if prob(f_score, score, strt, time(), tl) > random():
            f_score = score
            #print(f_score)
        else:
            a = fa
    else:
        fb = b
        b += random() * 0.02 - 0.01
        score = scoring()
        if prob(f_score, score, strt, time(), tl) > random():
            f_score = score
            #print(f_score)
        else:
            b = fb

print(f_score)
'''
vh_vd = [[vhs[j][i] - (a * vds[j][i] + b) for i in range(len(vhs[j]))] for j in range(6)]
sd = [statistics.stdev(vh_vd[j]) for j in range(6)]
print(a, b, sd)
evaluate.kill()