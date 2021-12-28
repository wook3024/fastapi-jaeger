import time


def deps1():
    time.sleep(0.5)
    deps2()


def deps2():
    time.sleep(0.5)
    deps3()


def deps3():
    time.sleep(0.5)
