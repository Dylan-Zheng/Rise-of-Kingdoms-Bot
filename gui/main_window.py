from gui.creator import *
from gui.main_frame import MainFrame



class MainWindow:

    def __init__(self, adb, size=(450, 800)):
        self.adb = adb

        self.window = Tk()
        self.size = size

        self.window.title('Rise Of Kingdom Bot')
        self.window.geometry('{}x{}'.format(size[0], size[1]))
        self.window.resizable(0, 0)

        MainFrame(self.window, size, self.adb.get_device())

    def run(self):
        self.window.mainloop()
