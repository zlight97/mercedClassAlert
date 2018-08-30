import time
import threading
from multiprocessing import Process
c = 10
def inp():
    global c
    while(1):
        c = raw_input()

def f(name):
    global c
    while(1):
        print('hello', c)
        time.sleep(5)
        if c == 'x':
            break
    print('end')


if __name__ == '__main__':
    # p = Process(target=f, args=('bob',))
    # e = Process(target=inp, args=())
    # p.start()
    # e.start()
    # p.join()
    # e.join()
    th = threading.Thread(target=f, args=('t'))
    th.daemon = True
    th.start()
    inp()