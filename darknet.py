import sys, os
sys.path.append(os.path.join(os.getcwd(),'python/'))
from time import sleep

import darknet as dn
import time
import subprocess
import tempfile

from threading  import Thread
from queue import Queue, Empty

start = 0
end = 0

def tic():
    start = time.time()

def toc():
    end = time.time()
    print(end-start)

#./darknet detector test cfg/daimler.data cfg/yolov3-tiny-daimler.cfg yolov3-tiny-daimler.weights '/home/aicore/Projects/Dashboard/darknet/Daimler/data/FramesMerged/100050.jpg'

'''
dn.set_gpu(0)
#net = dn.load_net("cfg/yolo-thor.cfg", "/home/pjreddie/backup/yolo-thor_final.weights", 0)
net = dn.load_net(b"/home/aicore/Projects/Dashboard/darknet/cfg/yolov3-tiny-daimler.cfg", b"/home/aicore/Projects/Dashboard/darknet/yolov3-tiny-daimler.weights", 0)
meta = dn.load_meta(b"/home/aicore/Projects/Dashboard/darknet/cfg/daimler.data")

start = time.time()
result = dn.detect(net, meta, b"/home/aicore/Projects/Dashboard/darknet/Daimler/data/FramesMerged/100050.jpg")
for r in result:
    print(r)
end = time.time()
print(end-start)

'''

cmd=[]
cmd.append('./darknet')
cmd.append('detector')
cmd.append('test')
cmd.append('cfg/daimler.data')
cmd.append('cfg/yolov3-tiny-daimler.cfg')
cmd.append('yolov3-tiny-daimler.weights')
f1 = b'Daimler/data/FramesMerged/010000.jpg\n'     # image1 path 
f2 = b'Daimler/data/FramesMerged/100050.jpg\n'
vf = '/home/aicore/Projects/Dashboard/darknet/Daimler/data/Videos/10.mp4'
#cmd.append(vf)


p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE)




ON_POSIX = 'posix' in sys.builtin_module_names
def enqueue_output(out, queue):
    for line in iter(out.readline, b''):
        queue.put(line)
    out.close()

q = Queue()
t = Thread(target=enqueue_output, args=(p.stdout, q))
t.daemon = True
t.start()

p.stdin.write(f1)
p.stdin.flush()
sleep(1.3)
while 1:
    try:  line = q.get_nowait() # or q.get(timeout=.1)
    except Empty:
        break
    else: print(line.rstrip())

p.stdin.write(f2)
p.stdin.flush()
sleep(0.1)
while 1:
    try:  line = q.get_nowait() # or q.get(timeout=.1)
    except Empty:
        break
    else: print(line.rstrip())
