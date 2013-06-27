#
# Project 2
#
# 01435 Practiacal Cryptanalysis
# Technical University of Denmark

# Markus Faerevaag              (s123692@student.dtu.dk)
# Christian Mathias Rohde Kiaer (s123812@student.dtu.dk)
# Jonathan Becktor              (s123094@student.dtu.dk)
#

from termcolor import colored
import md5, random, csv

BIT_SIZE = 28
CHAIN_LEN  = 2**10
TABLE_NAME = "table.csv"
SERIAL_NO = "0123456"

#s ='0x337169e'
s ='0xb33d90d'
#s ='0xc276a22'
#s ='0xbea3eac'
#s = hex(random.getrandbits(BIT_SIZE))[:-1]

u = "daffeda"

#0xcbf2536
#0xc4d0b67
#0xcbf2536

def f(s, i=0):
    """Lowest 28 bits of (MD5(s||u) % i)"""    
    digest = '0x' + md5.new(str(s) + str(u)).hexdigest()
    result = hex((int(digest, 16) + i) % 2**BIT_SIZE)[:BIT_SIZE/4+2]
    return result


def read_table():
    """Read Rainbow Table from csv file"""
    dict = {}
    with open(TABLE_NAME, 'rb') as csvfile:
        table = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in table:
            dict[str(row[0])] = str(row[1])
    return dict


def find_key(table, r):
    """Search for matching respons in Rainbow-table"""
    succ = [r]
    print r
    for i in xrange(1, CHAIN_LEN):
        succ.append(f(succ[i-1],i))

    for key, value in table.iteritems():
        if value in succ:
            hest = succ.index(value)
            print succ[hest]
            print "\tCollition: %s -> %s" % (key, value)
            #print succ(value)
            print succ.index(value)
            #print r
            ss = key
            #print ss,
            for i in xrange(0, CHAIN_LEN):
                rs = f(ss, i)
            #    print rs,
                if rs==r:
                    print 'din mor'
                    return ss
#                print "%s" % rs,
                ss = rs
                #print rs,
    return -1


def main():
  #  for i in xrange(0, 1000):
        #

        print " Fob > Hello, key fob no. %s is here!" % SERIAL_NO
        
        print " Eve > Challenge: 0x%s" % u

        r = f(s)
        print " Fob > Response:  %s" % r

        table = read_table()
        print " Eve > Cracking..."
        
        key = find_key(table, r)

        if key is -1:
            print " Eve > %s" % colored('No key found!', 'red')
        else:
            print " Eve > %s: %s" % (colored('Key found', 'green'), key)

        print "\tActual key: %s" % s



if __name__ == '__main__':
    main()