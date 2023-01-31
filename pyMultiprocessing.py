import multiprocessing

class MultiProcess:
    def __init__(self):
        self.queue = multiprocessing.Queue()
    def createProcess(self, target, args):
        self.pid = multiprocessing.Process(target=target, args=args)
        
    def start(self):
        self.pid.start()
    