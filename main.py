from adb import enable_adb
from gui.main_window import MainWindow



def main():

    adb = enable_adb()
    window = MainWindow(adb)
    window.run()



if __name__ == '__main__':
    main()
