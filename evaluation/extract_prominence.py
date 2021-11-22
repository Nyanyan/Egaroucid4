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

def push_data(record, player, score):
    raw_record = ''
    for i in range(0, len(record), 2):
        p = int(record[i])
        raw_record += record[i + 1]
        if p == player:
            if not raw_record in record_all:
                record_all[raw_record] = [1, score]
            else:
                record_all[raw_record][0] += 1
                record_all[raw_record][1] += score

for i in trange(127):
    try:
        with open('third_party/book_data/' + digit(i, 7) + '.txt', 'r') as f:
            records = f.read().splitlines()
        for datum in records:
            record, score = datum.split()
            score = int(score)
            push_data(record, 0, score)
            push_data(record, 1, -score)
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
        record_all[record_proc] = [10, 0]
    else:
        record_all[record_proc][0] += 10
        record_all[record_proc][1] += 0
for record in records[1:]:
    record_proc = ''
    for i in range(0, len(record), 2):
        x = ord(record[i]) - ord('a')
        y = int(record[i + 1]) - 1
        record_proc += all_chars[y * 8 + x]
        if not record_proc in record_all:
            record_all[record_proc] = [10, 0]
        else:
            record_all[record_proc][0] += 10
            record_all[record_proc][1] += 0
print(len(record_all))


book = {}

max_ln = 45

num_threshold1 = 10
val_threshold = 2.0

inf = 100000000

def calc_value(r):
    if record_all[r][0] < num_threshold1:
        return -inf
    val = record_all[r][1] / record_all[r][0]
    #val += 0.01 * record_all[r][0]
    return val

def create_book(record):
    if len(record) > max_ln:
        return
    for i in range(hw2):
        r = record + all_chars[i]
        if r in record_all:
            val = calc_value(r)
            if abs(val) <= val_threshold:
                if record in book:
                    book[record].append(all_chars[i])
                else:
                    book[record] = [all_chars[i]]
                create_book(r)

book = {}
create_book(all_chars[37])
print(len(book))
if (input('sure?: ') == 'yes'):
    with open('third_party/extract_prominence.txt', 'w') as f:
        for record in book.keys():
            for mov in book[record]:
                f.write(translate(record) + ' ' + translate(mov) + '\n')