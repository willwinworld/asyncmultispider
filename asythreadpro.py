#! python2
# -*- coding:utf-8 -*-
import re
import json
import time
import sys
import threading
import Queue
import requests
from datetime import timedelta
from dateutil.parser import parse
from pyquery import PyQuery as pq

"""一般来说，使用线程有两种模式, 一种是创建线程要执行的函数, 把这个函数传递进Thread对象里，
让它来执行. 另一种是直接从Thread继承，创建一个新的class，把线程执行的代码放到这个新的class里,
1.在构造函数中传入用于线程运行的函数(这种方式更加灵活)
2.在子类中重写threading.Thread基类中run()方法(只重写__init__()和run()方法)"""

"""关于守护进程的一些知识:A thread can be flagged as a "daemon thread".
 The significance of this flag is that the entire Python program exits when only daemon threads are left.
  The initial value is inherited from the creating thread."""

"""Some threads do background tasks, like sending keepalive packets, or performing periodic garbage collection,
or whatever. These are only useful when the main program is running,
 and it's okay to kill them off once the other, non-daemon, threads have exited."""

"""Without daemon threads, you'd have to keep track of them, and tell them to exit,
 before your program can completely quit. By setting them as daemon threads, you can let them run and forget about them,
 and when your program quits, any daemon threads are killed automatically."""


class Worker(threading.Thread):  # 处理工作请求
    def __init__(self, work_queue, result_queue, **kwargs):
        # threading.Thread.__init__(self, **kwargs)
        super(Worker, self).__init__()
        self.setDaemon(True)
        self.work_queue = work_queue
        self.result_queue = result_queue
        self.kwargs = kwargs

    def run(self):
        while True:
            try:
                call, args, kwargs = self.work_queue.get(False)  # get task

                """非阻塞，Otherwise (block is false), return an item if one is immediately available,
                else raise the Empty exception (timeout is ignored in that case)"""

                res = call(*args, **kwargs)
                self.result_queue.put(res)  # put result
            except Queue.Empty:
                break


class WorkManager:
    def __init__(self, num_of_workers=10):
        self.work_queue = Queue.Queue()  # 请求队列
        self.result_queue = Queue.Queue()  # 输出结果队列
        self.workers = []
        self._recruit_threads(num_of_workers)

    def _recruit_threads(self, num_of_workers):
        for i in range(num_of_workers):
            worker = Worker(self.work_queue, self.result_queue)  # 创建工作线程
            self.workers.append(worker)  # 加入到线程队列

    def start(self):
        for w in self.workers:
            w.start()

    def wait_for_complete(self):
        while len(self.workers):
            worker = self.workers.pop()
            worker.join()

            """As join() always returns None, you must call isAlive() after join() to decide whether a timeout happened
            这里的join是为了阻塞调用线程，只有当worker线程结束后才允许主线程结束。
            调用join不会使is_alive为true吧，只有当线程结束执行或者超时了is_alive才是True"""

            if worker.isAlive() and not self.work_queue.empty():
                self.workers.append(worker)
        print('All jobs were complete.')

    def add_job(self, call, *args, **kwargs):
        self.work_queue.put((call, args, kwargs))  # 向工作队列中加入请求

    def get_result(self, *args, **kwargs):
        return self.result_queue.get(*args, **kwargs)


def download_file(url):
    return requests.get(url).text


def main():
    try:
        num_of_threads = int(sys.argv[1])
    except:
        num_of_threads = 10
    _st = time.time()
    wm = WorkManager(num_of_threads)
    print(num_of_threads)
    urls = ['http://www.baidu.com'] * 1000
    for i in urls:
        wm.add_job(download_file, i)
    wm.start()
    wm.wait_for_complete()
    print(time.time() - _st)


if __name__ == '__main__':
    main()

