from uiautomator import Adb, AutomatorServer, AutomatorDevice, next_local_port, DEVICE_PORT

from filepath.file_relative_paths import FilePaths
from utils import resource_path


class Adbed(Adb):
    def __init__(self, serial=None, adb_server_host=None, adb_server_port=None):
        super().__init__(serial, adb_server_host, adb_server_port)

    def adb(self):
        adb_cmd = resource_path(FilePaths.ADB_EXE_PATH.value)
        self.__adb_cmd = adb_cmd
        return adb_cmd


class AdbServer(AutomatorServer):
    def __init__(self, serial=None, local_port=None, device_port=None, adb_server_host=None, adb_server_port=None):
        self.uiautomator_process = None
        self.adb = Adbed(serial=serial, adb_server_host=adb_server_host, adb_server_port=adb_server_port)
        self.device_port = int(device_port) if device_port else DEVICE_PORT
        if local_port:
            self.local_port = local_port
        else:
            try:  # first we will try to use the local port already adb forwarded
                for s, lp, rp in self.adb.forward_list():
                    if s == self.adb.device_serial() and rp == 'tcp:%d' % self.device_port:
                        self.local_port = int(lp[4:])
                        break
                else:
                    self.local_port = next_local_port(adb_server_host)
            except:
                self.local_port = next_local_port(adb_server_host)


class AdbDevice(AutomatorDevice):
    def __init__(self, serial=None, local_port=None, adb_server_host=None, adb_server_port=None):
        self.server = AdbServer(
            serial=serial,
            local_port=local_port,
            adb_server_host=adb_server_host,
            adb_server_port=adb_server_port
        )