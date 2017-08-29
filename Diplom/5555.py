import time
for i in range(0, 101, 10):
    print('\rYou have finished %3d%%' % i, end='', flush=True)
    time.sleep(1)
else:
    print()