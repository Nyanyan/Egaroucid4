import subprocess
from tqdm import trange

def digit(n, r):
    n = str(n)
    l = len(n)
    for i in range(r - l):
        n = '0' + n
    return n

evaluate = subprocess.Popen('./ai.out'.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

hw = 8

for idx in trange(127):
    with open('data/raw/' + digit(idx, 7) + '.txt', 'r') as f:
        data = [list(elem.split()) for elem in f.read().splitlines()]
    new_data = ''
    for board, player, _, _, _, result in data:
        stdin = player + '\n'
        for y in range(hw):
            for x in range(hw):
                stdin += board[y * hw + x]
            stdin += '\n'
        evaluate.stdin.write(stdin.encode('utf-8'))
        evaluate.stdin.flush()
        add_data = evaluate.stdout.readline().decode().replace('\r\n', '')
        new_data += board + ' ' + player + ' ' + add_data + ' ' + result + '\n'
    with open('data/' + digit(idx, 7) + '.txt', 'w') as f:
        f.write(new_data)

evaluate.kill()