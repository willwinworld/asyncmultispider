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


class Worker(threading.Thread):  # 处理工作请求
    def __init__(self, work_queue, result_queue, **kwargs):
        threading.Thread.__init__(self, **kwargs)
        self.setDaemon(True)
        self.work_queue = work_queue
        self.result_queue = result_queue
        self.kwargs = kwargs

    def run(self):
        while True:
            try:
                call, args, kwargs = self.work_queue.get(False)

                """非阻塞，Otherwise (block is false), return an item if one is immediately available,
                else raise the Empty exception (timeout is ignored in that case)"""

                res = call(*args, **kwargs)
                self.result_queue.put(res)
            except Queue.Empty:
                break


class WorkManager:
    def __init__(self, num_of_workers=10):
        self.work_queue = Queue.Queue()
        self.result_queue = Queue.Queue()
        self.workers = []
        self._recruit_threads(num_of_workers)

    def _recruit_threads(self, num_of_workers):
        for i in range(num_of_workers):
            worker = Worker(self.work_queue, self.result_queue)
            self.workers.append(worker)

    def start(self):
        for w in self.workers:
            w.start()

    def wait_for_complete(self):
        while len(self.workers):
            worker = self.workers.pop()
            worker.join()

            """As join() always returns None, you must call isAlive() after join() to decide whether a timeout happened .
            这里的join是为了阻塞调用线程，只有当worker线程结束后才允许主线程结束。
            调用join不会使is_alive为true吧，只有当线程结束执行或者超时了is_alive才是True"""

            if worker.isAlive() and not self.work_queue.empty():
                self.workers.append(worker)
        print('All jobs were complete.')

    def add_job(self, call, *args, **kwargs):
        self.work_queue.put((call, args, kwargs))

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

