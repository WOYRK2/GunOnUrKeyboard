from overlay import start_OL
import multiprocessing
import time
from os import getcwd
from pynput import keyboard

#print(getcwd())

if __name__ == '__main__':
    qcm = multiprocessing.Queue()
    proccess = multiprocessing.Process(
        target=start_OL,
        args=(qcm,)
    )

    proccess.start()

    def shoot():
        qcm.put(('shooot', ))

    listnr = keyboard.Listener(on_press=shoot)
    listnr.start()