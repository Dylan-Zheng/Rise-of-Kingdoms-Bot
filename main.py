import adb

from gui.main_window import MainWindow


def main():
    adb.bridge = adb.enable_adb()
    window = MainWindow()
    window.run()


if __name__ == '__main__':
    main()
