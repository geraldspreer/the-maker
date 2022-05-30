import threading


def newThread(function, *arg, **kwds):
    """for now, this works for functions with a single argument
    also only for functions who do not return a value
    """

    class MyThread(threading.Thread):
        def run(self):
            function(*arg, **kwds)

    MyThread().start()
