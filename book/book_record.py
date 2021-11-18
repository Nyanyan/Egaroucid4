from tqdm import trange

all_chars = [
    '!', '#', '$', '&', "'", '(', ')', '*', 
    '+', ',', '-', '.', '/', '0', '1', '2', 
    '3', '4', '5', '6', '7', '8', '9', ':', 
    ';', '<', '=', '>', '?', '@', 'A', 'B', 
    'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 
    'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 
    'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 
    '[', ']', '^', '_', '`', 'a', 'b', 'c', 
    'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~']

xs = 'abcdefgh'
ys = '12345678'

char_translate = {}
for i in range(64):
    char_translate[all_chars[i]] = xs[i % 8] + ys[i // 8]

def translate(r):
    return ''.join([char_translate[i] for i in r])

hw2 = 64

def digit(n, r):
    n = str(n)
    l = len(n)
    for i in range(r - l):
        n = '0' + n
    return n

record_all = {}

def win_data(record, player):
    raw_record = ''
    for i in range(0, len(record), 2):
        p = int(record[i])
        raw_record += record[i + 1]
        if p == player:
            if not raw_record in record_all:
                record_all[raw_record] = [1, 1]
            else:
                record_all[raw_record][0] += 1
                record_all[raw_record][1] += 1


def lose_data(record, player):
    raw_record = ''
    for i in range(0, len(record), 2):
        p = int(record[i])
        raw_record += record[i + 1]
        if p == player:
            if not raw_record in record_all:
                record_all[raw_record] = [1, -1]
            else:
                record_all[raw_record][0] += 1
                record_all[raw_record][1] -= 1

def draw_data(record, player):
    raw_record = ''
    for i in range(0, len(record), 2):
        p = int(record[i])
        raw_record += record[i + 1]
        if p == player:
            if not raw_record in record_all:
                record_all[raw_record] = [1, 0]
            else:
                record_all[raw_record][0] += 1
'''
rec = 'd3c5f6f5e6e3d6f7g6e7f4c4c6c3d8e8d7c8b5b6b4a4c7a5g8b8f2f3e2d2b3d1c1g4'
rec_num = ''
for i in range(0, len(rec), 2):
    x = ord(rec[i]) - ord('a')
    y = int(rec[i + 1]) - 1
    yy = 7 - x
    xx = 7 - y
    rec_num += all_chars[yy * 8 + xx]
print(translate(rec_num))
exit()
'''
black_win = 0
white_win = 0

for i in trange(127):
    try:
        with open('data/' + digit(i, 7) + '.txt', 'r') as f:
            records = f.read().splitlines()
        for datum in records:
            record, score = datum.split()
            score = int(score)
            if score == 0:
                draw_data(record, 0)
                draw_data(record, 1)
            elif score > 0:
                win_data(record, 0)
                lose_data(record, 1)
                black_win += 1
            else:
                lose_data(record, 0)
                win_data(record, 1)
                white_win += 1
    except:
        print('cannot open', i)
        continue
print(len(record_all))


inf = 1000000000
with open('third_party/records4.txt', 'r') as f:
    records = f.read().splitlines()
record = records[0]
record_proc = ''
for i in range(0, len(record), 2):
    x = ord(record[i]) - ord('a')
    y = int(record[i + 1]) - 1
    record_proc += all_chars[y * 8 + x]
    if not record_proc in record_all:
        record_all[record_proc] = [1000, inf * 1000]
    else:
        record_all[record_proc][0] += 1000
        record_all[record_proc][1] += inf * 1000
for record in records[1:]:
    record_proc = ''
    for i in range(0, len(record), 2):
        x = ord(record[i]) - ord('a')
        y = int(record[i + 1]) - 1
        record_proc += all_chars[y * 8 + x]
        if not record_proc in record_all:
            record_all[record_proc] = [100, 100]
        else:
            record_all[record_proc][0] += 100
            record_all[record_proc][1] += 100
print(len(record_all))
print(black_win, white_win)


book = {}

max_ln = 45

num_threshold1 = 3

inf = 100000000

def calc_value(r):
    if translate(r) == 'f5f6e6f4e3c5c4d6b5d3c3e2f2c2f1b4c1a6g5':
        print('a')
        return inf
    if translate(r) == 'f5d6c3d3c4f4f6f3e6e7f7c5b6g6e3e2f1d2e1c1':
        print('b')
        return inf
    if translate(r) == 'f5f6e6f4e3c5c4d3f3e2g4':
        print('c')
        return inf
    if translate(r) == 'f5d6c3d3c4f4c5b3c2b4e3':
        print('d')
        return inf
    '''
    if translate(r) == 'f5d6c4d3c3f4f6f3e6e7f7c5b6g6e3e2f1d2e1c1':
        print('e')
        return inf
    if translate(r) == 'f5d6c5f4e3c6d3f6e6d7g4c4g5c3f7d2e7f2c8f3c7d8e2b8':
        print('f')
        return inf
    if translate(r) == 'f5d6c5f4e3c6d3f6e6d7g4c4g5c3f7d2e7f2c8f3c7d8e8g3e2h4f1e1h5h6':
        print('g')
        return inf
    if translate(r) == 'f5d6c5f4e3c6d3f6e6d7g4c4g5c3f7d2e7f2c8f3e2e8':
        print('h')
        return inf
    if translate(r) == 'f5d6c5f4e3c6d3f6e6d7g4c4g5c3f7d2e7f2c8f3c7d8e8g3e2h4f1e1h5h6c1d1h3g6':
        print('i')
        return inf
    if translate(r) == 'f5d6c5f4e3c6d3f6e6d7g3c4b4b3b5a4a2a3a5c3':
        print('j')
        return inf
    if translate(r) == 'f5d6c3f4f6d3f3b3c7':
        print('k')
        return inf
    if translate(r) == 'f5f6e6f4e3c5c4e7c6e2f3f2g5g4h4':
        print('l')
        return inf
    if translate(r) == 'f5d6c3d3c4f4c5b3c2e3d2c6b4a4b5b6d7e7a3e2c7c1g4d1f7e6f6g3a5a7f3':
        print('m')
        return inf
    if translate(r) == 'f5d6c3d3c4f4f6f3e6e7c6g6f8f7g5h6h4g4':
        print('n')
        return inf
    if translate(r) == 'f5d6c3d3c4f4f6f3e6e7f7c5b6g6e3e2f1d2e1c1c2b5a6b4a5a3g3e8':
        print('o')
        return inf
    if translate(r) == 'f5d6c3d3c4f4c5b3c2e3d2c6b4b5f2e6f3c1a3a4a5g6f6':
        print('p')
        return inf
    if translate(r) == 'f5d6c3d3c4f4c5b3c2b4c6d2e6b5e3f3a5a6':
        print('q')
        return inf
    '''
    if record_all[r][0] < num_threshold1 and record_all[r][1] < inf:
        return -inf
    val = record_all[r][1] / record_all[r][0]
    val += 0.01 * record_all[r][0]
    return val

def create_book(record):
    if len(record) > max_ln:
        return
    policy = -1
    max_val = -inf
    for i in range(hw2):
        r = record + all_chars[i]
        if r in record_all:
            val = calc_value(r)
            if max_val < val:
                max_val = val
                policy = i
    if policy != -1:
        book[record] = all_chars[policy]
        for i in range(hw2):
            r = record + all_chars[policy] + all_chars[i]
            if r in record_all:
                create_book(r)



book = {}
create_book(all_chars[37])
print(len(book))
create_book(all_chars[37] + all_chars[43])
create_book(all_chars[37] + all_chars[45])
create_book(all_chars[37] + all_chars[29])
print(len(book))
if (input('sure?: ') == 'yes'):
    with open('learned_data/book.txt', 'w') as f:
        for record in book.keys():
            f.write(record[1:] + ' ' + book[record])