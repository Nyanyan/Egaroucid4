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

xs = 'ABCDEFGH'
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
'''
inf = 100000
with open('third_party/records3.txt', 'r') as f:
    records = f.read().splitlines()
for record in records:
    record_proc = ''
    for i in range(0, len(record), 2):
        x = ord(record[i]) - ord('a')
        y = int(record[i + 1]) - 1
        record_proc += all_chars[y * 8 + x]
        if not record_proc in record_all:
            record_all[record_proc] = [1, inf]
        else:
            record_all[record_proc][0] += 1
            record_all[record_proc][1] += inf
print(len(record_all))
'''
print(black_win, white_win)

book = {}

max_ln = 40

num_threshold1 = 2
num_threshold2 = 5

inf = 100000000

def calc_value(r):
    if record_all[r][0] < num_threshold1:
        return -inf
    #if record_all[r][0] < num_threshold2 and record_all[r][1] < 0:
    #    return -inf
    #if translate(r) == 'F5D6':
    #    return inf
    val = record_all[r][1] / record_all[r][0]
    val += 0.1 * record_all[r][0]
    #val += 0.1 * (1.0 - 2 ** (-0.1 * record_all[r][0]))
    #print(r, record_all[r], val)
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