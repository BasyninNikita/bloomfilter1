import math
import sys

M = (1 << 31) - 1  # M-31th Mersen's number


def get_command():
    ss = False
    for line in sys.stdin:
        if 'set' in line:
            if len(line.replace('set', '').strip().split(' ')) == 2 \
                    and ss == 0 and int(line.split()[1]) > 1 and 0.7 > float(line.split()[2]) > 0:
                bf = BloomFilter(int(line.split()[1]), float(line.split()[2]))
                print(str(bf.size()) + ' ' + str(bf.num_hashs()))
                ss = True
            else:
                print('error')
        elif 'add' in line:
            if len(line.replace('add', '').strip().split(
                    ' ')) == 1 and ss:  # line.replace('push ', '')[:-1] != 1 and ss != 0:
                bf.add(int(line.split()[1]))
                print('', end='')
            else:
                print('error')
        elif 'search' in line:
            if len(line.replace('search', '').strip().split(
                    ' ')) == 1 and ss:  # line.replace('push ', '')[:-1] != 1 and ss != 0:
                succ = bf.search(int(line.split()[1]))
                print('1' if succ else '0')
                # if succ:
                #     print('1')
                # else:
                #     print('0')
            else:
                print('error')
        elif 'print' in line:
            if line.replace("print", '') != '\n' or ss == False:
                print('error')
            else:
                print(bf.print())  # , end='')
        elif line == '\n':
            continue
        else:
            print('error')


# def bit_sieve(n):
#     if n < 2:
#         return []
#     bits = [1] * n
#     sqrt_n = int(math.sqrt(n)) + 1
#     for i in range(2, sqrt_n):
#         if bits[i - 2]:
#             for j in range(i + i, n + 1, i):
#                 bits[j - 2] = 0
#     return bits
#
#
# def prime(k):
#     if k == 1:
#         return 2
#     sieve = bit_sieve(int(1.5 * k * math.log(k)) + 1)
#     i = 0
#     while k:
#         k -= sieve[i]
#         i += 1
#     return (i + 1)

def primes(n):
    a = list(range(n + 1))
    a[1] = 0
    lst = []
    i = 2
    while i <= n:
        if a[i] != 0:
            lst.append(a[i])
            for j in range(i, n + 1, i):
                a[j] = 0
        i += 1
    return lst


class Bits:

    def __init__(self, m, num_hashes):
        self.m = m
        self.num_hashes = num_hashes
        self.bits = 0

    def add(self, key_hash):
        self.bits = self.bits | (1 << key_hash)

    def print(self):
        return (bin(self.bits)[:1:-1]) + '0' * (self.m - len(bin(self.bits)[2:]))  # + '\n'

    def search(self, key_hash):
        return self.bits & (1 << key_hash) != 0


class BloomFilter:

    def __init__(self, n, P):
        self.num_hashes = round(-(math.log2(P)))
        self.m = round(- (n * math.log2(P)) / math.log(2))
        self.bits = Bits(self.m, self.num_hashes)
        self.primes = primes(int(1.5 * self.num_hashes * math.log(self.num_hashes)) + 1)

    def size(self):
        return self.m

    def num_hashs(self):
        return self.num_hashes

    def hash_search(self, key, i, m):
        return (((i + 1) * key + self.primes[i]) % M) % m  # M-31th Mersen's number

    def add(self, key):
        for i in range(self.num_hashes):
            self.bits.add(self.hash_search(key, i, self.m))
        return

    def search(self, key):
        for i in range(self.num_hashes):
            succ = self.bits.search(self.hash_search(key, i, self.m))
            if not succ:
                return False
        return True

    def print(self):
        return self.bits.print()


get_command()
