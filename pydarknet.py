import sys, os
sys.path.append(os.path.join(os.getcwd(),'python/'))
from time import sleep

import darknet as dn
import time
import subprocess
import tempfile
import numpy as np

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
data_path = 'cfg/daimler.data'
cfg_path = 'cfg/yolov3-tiny-daimler.cfg'
weight_path = 'yolov3-tiny-daimler_final.weights'

stdweight_path = 'yolov3-tiny.weights'
pretrained_path = 'yolov3-tiny.conv.15'

def weight_partial(n):
    cmd=[]
    cmd.append('./darknet')
    cmd.append('partial')
    cmd.append(cfg_path)
    cmd.append(stdweight_path)
    cmd.append(pretrained_path)
    cmd.append(str(n))
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())
    rc = process.poll()



def train():
    timeout = 0

    cmd=[]
    cmd.append('./darknet')
    cmd.append('detector')
    cmd.append('train')
    cmd.append(data_path)
    cmd.append(cfg_path)
    cmd.append(pretrained_path)

    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    '''
    Getting realtime output using Python Subprocess
    https://www.endpoint.com/blog/2015/01/28/getting-realtime-output-using-python
    '''
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())
    rc = process.poll()


def predict(imgfile=[]):

    t_init = 1.3
    t_running = 0.06


    cmd=[]
    cmd.append('./darknet')
    cmd.append('detector')
    cmd.append('test')
    cmd.append(data_path)
    cmd.append(cfg_path)
    cmd.append(weight_path)


    imgfile.append(b'Daimler/data/FramesMerged/010000.jpg\n')
    imgfile.append(b'Daimler/data/FramesMerged/100050.jpg\n')

    #vf = '/home/aicore/Projects/Dashboard/darknet/Daimler/data/Videos/10.mp4'
    #cmd.append(vf)


    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    '''
    Non-blocking read on a subprocess.PIPE in python
    https://stackoverflow.com/questions/375427/non-blocking-read-on-a-subprocess-pipe-in-python/4896288#4896288
    '''

    ON_POSIX = 'posix' in sys.builtin_module_names
    def enqueue_output(out, queue):
        for line in iter(out.readline, b''):
            queue.put(line)
        out.close()

    q = Queue()
    t = Thread(target=enqueue_output, args=(p.stdout, q))
    t.daemon = True
    t.start()

    i=0
    for f in imgfile:
        start = time.time()
        p.stdin.write(f)
        p.stdin.flush()
        timeout= t_init if i==0 else t_running
        i += 1
        outs = []
        while 1:
            try:  line = q.get(timeout=timeout) # or q.get_nowait()
            except Empty:
                break
            else: outs.append(line.decode('utf-8').replace('\n','').split(' '))
        if len(outs)==1:
            continue

        outs = map(lambda x: [int(x[0]), list(map(lambda y: float(y), x[1:]))], outs[1:])
        out = list(outs)
        print(out)
        end = time.time()
        print(end - start)

predict()

