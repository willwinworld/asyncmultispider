# asyncmultispider
利用tornado实现异步，同时增加多进程，多线程的功能
理解进程，线程这两个概念:1.进程:程序的一次执行2.线程:CPU的基本调度单位
大概理解就是这样，而在Linux系统里面，在最底层，线程和进程确实是不区分的。


在处理 IO 的时候，阻塞和非阻塞都是同步 IO。
只有使用了特殊的 API 才是异步 IO。



“阻塞”与"非阻塞"与"同步"与“异步"不能简单的从字面理解，提供一个从分布式系统角度的回答。
1.同步与异步
同步和异步关注的是消息通信机制 (synchronous communication/ asynchronous communication)
所谓同步，就是在发出一个*调用*时，在没有得到结果之前，该*调用*就不返回。但是一旦调用返回，就得到返回值了。
换句话说，就是由*调用者*主动等待这个*调用*的结果。

而异步则是相反，*调用*在发出之后，这个调用就直接返回了，所以没有返回结果。换句话说，当一个异步过程调用发出后，调用者不会立刻得到结果。而是在*调用*发出后，*被调用者*通过状态、通知来通知调用者，或通过回调函数处理这个调用。

典型的异步编程模型比如Node.js

举个通俗的例子：
你打电话问书店老板有没有《分布式系统》这本书，如果是同步通信机制，书店老板会说，你稍等，”我查一下"，然后开始查啊查，等查好了（可能是5秒，也可能是一天）告诉你结果（返回结果）。
而异步通信机制，书店老板直接告诉你我查一下啊，查好了打电话给你，然后直接挂电话了（不返回结果）。然后查好了，他会主动打电话给你。在这里老板通过“回电”这种方式来回调。

2. 阻塞与非阻塞
阻塞和非阻塞关注的是程序在等待调用结果（消息，返回值）时的状态.

阻塞调用是指调用结果返回之前，当前线程会被挂起。调用线程只有在得到结果之后才会返回。
非阻塞调用指在不能立刻得到结果之前，该调用不会阻塞当前线程。

还是上面的例子，
你打电话问书店老板有没有《分布式系统》这本书，你如果是阻塞式调用，你会一直把自己“挂起”，直到得到这本书有没有的结果，如果是非阻塞式调用，你不管老板有没有告诉你，你自己先一边去玩了， 当然你也要偶尔过几分钟check一下老板有没有返回结果。
在这里阻塞与非阻塞与是否同步异步无关。跟老板通过什么方式回答你结果无关。
如果是关心blocking IO/ asynchronous IO, 参考 Unix Network Programming View Book


老张爱喝茶，废话不说，煮开水。
出场人物：老张，水壶两把（普通水壶，简称水壶；会响的水壶，简称响水壶）。
1 老张把水壶放到火上，立等水开。（同步阻塞）
老张觉得自己有点傻
2 老张把水壶放到火上，去客厅看电视，时不时去厨房看看水开没有。（同步非阻塞）
老张还是觉得自己有点傻，于是变高端了，买了把会响笛的那种水壶。水开之后，能大声发出嘀~~~~的噪音。
3 老张把响水壶放到火上，立等水开。（异步阻塞）
老张觉得这样傻等意义不大
4 老张把响水壶放到火上，去客厅看电视，水壶响之前不再去看它了，响了再去拿壶。（异步非阻塞）
老张觉得自己聪明了。


所谓同步异步，只是对于水壶而言。
普通水壶，同步；响水壶，异步。
虽然都能干活，但响水壶可以在自己完工之后，提示老张水开了。这是普通水壶所不能及的。
同步只能让调用者去轮询自己（情况2中），造成老张效率的低下。

所谓阻塞非阻塞，仅仅对于老张而言。
立等的老张，阻塞；看电视的老张，非阻塞。
情况1和情况3中老张就是阻塞的，媳妇喊他都不知道。虽然3中响水壶是异步的，可对于立等的老张没有太大的意义。所以一般异步是配合非阻塞使用的，这样才能发挥异步的效用。

——来源网络，作者不明。


同步与异步关乎做事情的方式。
同步：做完一件事再去做另一件。
异步：同时做多件事情，某个事情有结果了再去处理（又一个新事情）。

阻塞与非阻塞关乎如何对待事情产生的结果。
阻塞：不等到想要的结果我就不走了。
非阻塞：有结果我就带走，没结果我就空手而回，总之一句话：爷等不起。


至于协程，又称微线程(coroutine)，tornado好像就是用协程来实现异步的
协程，又称微线程，纤程。英文名Coroutine。

协程的概念很早就提出来了，但直到最近几年才在某些语言（如Lua）中得到广泛应用。

子程序，或者称为函数，在所有语言中都是层级调用，比如A调用B，B在执行过程中又调用了C，C执行完毕返回，B执行完毕返回，最后是A执行完毕。

所以子程序调用是通过栈实现的，一个线程就是执行一个子程序。

子程序调用总是一个入口，一次返回，调用顺序是明确的。而协程的调用和子程序不同。

协程看上去也是子程序，但执行过程中，在子程序内部可中断，然后转而执行别的子程序，在适当的时候再返回来接着执行。

注意，在一个子程序中中断，去执行其他子程序，不是函数调用，有点类似CPU的中断。比如子程序A、B：

def A():
    print '1'
    print '2'
    print '3'

def B():
    print 'x'
    print 'y'
    print 'z'
假设由协程执行，在执行A的过程中，可以随时中断，去执行B，B也可能在执行过程中中断再去执行A，结果可能是：

1
2
x
y
3
z
但是在A中是没有调用B的，所以协程的调用比函数调用理解起来要难一些。

看起来A、B的执行有点像多线程，但协程的特点在于是一个线程执行，那和多线程比，协程有何优势？

最大的优势就是协程极高的执行效率。因为子程序切换不是线程切换，而是由程序自身控制，因此，没有线程切换的开销，和多线程比，线程数量越多，协程的性能优势就越明显。

第二大优势就是不需要多线程的锁机制，因为只有一个线程，也不存在同时写变量冲突，在协程中控制共享资源不加锁，只需要判断状态就好了，所以执行效率比多线程高很多。

因为协程是一个线程执行，那怎么利用多核CPU呢？最简单的方法是多进程+协程，既充分利用多核，又充分发挥协程的高效率，可获得极高的性能。

Python对协程的支持还非常有限，用在generator中的yield可以一定程度上实现协程。虽然支持不完全，但已经可以发挥相当大的威力了。

来看例子：

传统的生产者-消费者模型是一个线程写消息，一个线程取消息，通过锁机制控制队列和等待，但一不小心就可能死锁。

如果改用协程，生产者生产消息后，直接通过yield跳转到消费者开始执行，待消费者执行完毕后，切换回生产者继续生产，效率极高：

import time

def consumer():
    r = ''
    while True:
        n = yield r
        if not n:
            return
        print('[CONSUMER] Consuming %s...' % n)
        time.sleep(1)
        r = '200 OK'

def produce(c):
    c.next()
    n = 0
    while n < 5:
        n = n + 1
        print('[PRODUCER] Producing %s...' % n)
        r = c.send(n)
        print('[PRODUCER] Consumer return: %s' % r)
    c.close()

if __name__=='__main__':
    c = consumer()
    produce(c)
执行结果：

[PRODUCER] Producing 1...
[CONSUMER] Consuming 1...
[PRODUCER] Consumer return: 200 OK
[PRODUCER] Producing 2...
[CONSUMER] Consuming 2...
[PRODUCER] Consumer return: 200 OK
[PRODUCER] Producing 3...
[CONSUMER] Consuming 3...
[PRODUCER] Consumer return: 200 OK
[PRODUCER] Producing 4...
[CONSUMER] Consuming 4...
[PRODUCER] Consumer return: 200 OK
[PRODUCER] Producing 5...
[CONSUMER] Consuming 5...
[PRODUCER] Consumer return: 200 OK
注意到consumer函数是一个generator（生成器），把一个consumer传入produce后：

首先调用c.next()启动生成器；

然后，一旦生产了东西，通过c.send(n)切换到consumer执行；

consumer通过yield拿到消息，处理，又通过yield把结果传回；

produce拿到consumer处理的结果，继续生产下一条消息；

produce决定不生产了，通过c.close()关闭consumer，整个过程结束。

整个流程无锁，由一个线程执行，produce和consumer协作完成任务，所以称为“协程”，而非线程的抢占式多任务。

最后套用Donald Knuth的一句话总结协程的特点：

“子程序就是协程的一种特例。”

协程的好处是什么？
1.历史上是先有协程，是OS用来模拟多任务并发，但是因为它是非抢占式的，导致多任务时间片不能公平分享，所以后来全部废弃了协程改成抢占式的线程。

2.线程确实比协程性能更好。因为线程能利用多核达到真正的并行计算，如果任务设计的好，线程能几乎成倍的提高你的计算能力，说线程性能不好的很多
是因为没有设计好导致大量的锁，切换，等待，这些很多都是应用层的问题。而协程因为是非抢占式，所以需要用户自己释放使用权来切换到其它协程，因此
同一时间其实只有一个协程拥有运行权，相当于单线程的能力。
我们在x360,xbox1和ps4上做游戏的时候，开线程用来做数据加载，解压这种不需要或者很少需要数据同步的任务时效率杠杠的，而协程用来处理一些应用层逻辑
调度的时候非常方便。官方文档也建议，协程只是为了老代码移植和兼容性，不推荐新代码使用。

3.说协程性能好的，其实真正的原因是因为瓶颈在IO上面，而这个时候真正发挥不了线程的作用。

4.协程的确可以减少callback的使用但是不能完全替代callback。基于事件驱动的编程里面反而不能发挥协程的作用而用callback更适合。想象一下用协程来写GUI
的时间处理你怎么写。计算密集型的异步代码里面也只能用callback。而node.js那种io瓶颈单任务流程用协程的确很适合，但是也需要callback做补充。

5.LUA的标准版5.1里协程有一个内伤，不能跨C函数切协程，而JIT版没有这个问题。但是ios上面又不能用JIT所以我直接把协程禁了免得到时候其它平台都是好的，
到ios上就出奇怪的问题。

6.状态机用协程其实也有问题，比如状态里面嵌套子状态，再由子状态切换到其它状态的子状态，开销和代码都会变差，反而不如经典的状态机简单明了高效。

7.其实node.js早就有协程模块了，只是底层用的os的协程而不是v8里面js的协程，因此性能最多只有callback版本的80%左右，而且scale的很不好，但是代码是简单清晰多了。
其实无论你是os的还是vm的，协程的开销必然比callback的开销大很多。

差不多就这些，总之，协程不是万能药，选择合适的工具同样很重要。通俗易懂的回答：让原来要使用异步+回调方式写的非人类代码，可以用看似同步的方式写出来...


而联系到爬虫，再贴几个有用的对话:
楼主，最近我为了实现异步多进程爬虫，查了很多资料，毕竟python多线程就是鸡肋，但我看你的代码还有tornado的文档里例子中都有一种写法，在try,except外部raise gen.Return(urls),难道是每次都抛出异常吗？还有我看tornado的文档exception tornado.gen.Return(value=None),Special exception to return a value from a coroutine,if this exception is raised, its value argument is used as the result of the coroutine,意思是说gen.Return(urls)当这个异常抛出时，urls将作为协程的结果吗？楼主能跟我这个菜鸟解释一下吗？谢谢！

hi，异步写起来是不太好维护的，所以我建议用多线程。虽然python有GIL，但是IO期间会释放GIL，所以对于爬虫这种IO密集型应用几乎是没有任何影响的。你可以测试下多线程是可以大幅提升爬虫效率的。可以尝试下https://docs.python.org/3/library/concurrent.futures.html 这个模块，对线程使用封装很好，具体开多少个线程比较合适还是需要自己测试。

hi，raise Return这种写法在python2里边是为了返回值的一种比较trick的写法，在python3里边可以直接用return返回结果。另外其实对于爬虫这种IO密集应用，python的GIL几乎是没有任何影响的，在IO期间会释放GIL，所以即使用多线程在爬虫里还是可以极大提升爬虫效率的。实际上我测试了发现用多线程并不比异步差很多。而且楼主最近由于使用requests比较多，开始用多线程+requests写了。实际上最近要抓的网站都有放爬虫措施，反而效率不是成了主要因素，如何破解反爬策略比较重要。如果觉得效率不行也可尝试celery这种异步框架分发任务。代码的可维护性可能才是最重要的。

def wait_for_complete(self):
while len(self.workers):
worker = self.workers.pop() # 从池中取出一个线程处理请求
worker.join()
if worker.isAlive() and not self.workQueue.empty():
self.workers.append(worker) # 重新加入线程池中
print 'All jobs were complete.'
请问博主 这里当worker.join()结束后才执行下面的if语句块吧.但是这个时候worker.isAlive()的值不是就为false了么.下边的if块是不是就是永远也不会执行了?

引用python文档一句话：As join() always returns None, you must call isAlive() after join() to decide whether a timeout happened .这里的join是为了阻塞调用线程，只有当worker线程结束后才允许主线程结束。调用join不会使is_alive为true吧，只有当线程结束执行或者超时了is_alive才是True

最后再贴上一个进程与线程的一个简单解释:http://www.ruanyifeng.com/blog/2013/04/processes_and_threads.html

利用tornado实现python多线程，异步，异步+多进程爬虫的三个例子:http://ningning.today/2015/09/18/python/python%E5%A4%9A%E7%BA%BF%E7%A8%8B%E3%80%81%E5%BC%82%E6%AD%A5%E3%80%81%E5%A4%9A%E8%BF%9B%E7%A8%8B%EF%BC%8B%E5%BC%82%E6%AD%A5%E7%88%AC%E8%99%AB/

多线程常用的两种实现模式：http://www.jianshu.com/p/86b8e78c418a




