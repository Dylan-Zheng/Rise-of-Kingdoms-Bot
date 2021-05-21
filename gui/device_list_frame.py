from tkinter import Frame, Label, Entry, Button, LabelFrame
from tkinter import N, W, LEFT, CENTER
from gui.selected_device_frame import SelectedDeviceFrame
from gui.creator import write_device_config, load_device_config
import adb
import re
import traceback

RUNNING = 'running'
DISCONNECTED = 'disconnected'
CONNECTED = 'connected'


class DeviceListFrame(Frame):

    def __init__(self, notebook, main_frame, cnf={}, **kwargs):
        Frame.__init__(self, notebook, kwargs)
        self.windows_size = [kwargs['width'], kwargs['height']]

        self.devices_config = load_device_config()

        self.main_frame = main_frame
        adf = AddDeviceFrame(self, main_frame)
        dlt = DeviceListTable(self, main_frame)

        for config in self.devices_config:
            dlt.add_row(config.get('name', 'None'), config['ip'], config['port'])

        adf.set_on_add_click(dlt.add_row)
        adf.grid(row=0, column=0, pady=(10, 0), sticky=N + W)
        dlt.grid(row=1, column=0, pady=(10, 0), sticky=N + W)


class DeviceListTable(Frame):
    def __init__(self, parent, main_frame, cnf={}, **kwargs):
        Frame.__init__(self, parent, kwargs)
        self.main_frame = main_frame
        self.title = Label(self, text="Devices:")
        self.title.grid(row=0, column=0, sticky=W, padx=(5, 0))
        self.device_rows = []

    def add_row(self, name, ip, port):
        try:
            new_row = DeviceRow(self, self.main_frame, name, ip, port)
            new_row.set_on_display_click(self.on_display_click)
            new_row.set_on_del_click(self.on_delete_click)
            self.device_rows.append(new_row)
            self.render()

        except Exception as e:
            traceback.print_exc()
            return

    def remove_row(self, row):
        try:
            idx = self.device_rows.index(row)
            if row.device_frame is not None:
                row.device_frame.stop()
                row.device_frame.destroy()
            self.device_rows.remove(row)
            row.destroy()
        except Exception as e:
            traceback.print_exc()
            return

    def on_display_click(self, row):
        self.master.master.select(1)
        for device_row in self.device_rows:
            if device_row.device_frame is not None:
                device_row.device_frame.grid_forget()
        row.device_frame.grid()

    def on_delete_click(self, row):
        ip, port = row.ip, row.port
        # tmp = list(filter(lambda addr: addr['ip'] == ip and addr['port'] == port, self.master.devices_config))
        self.master.devices_config.remove(
            next(addr for addr in self.master.devices_config if addr['ip'] == ip and addr['port'] == port)
        )
        write_device_config(self.master.devices_config)
        self.remove_row(row)

    def render(self):
        for i in range(len(self.device_rows)):
            self.device_rows[i].grid(row=i + 1, column=0, sticky=W, padx=(10, 0), pady=(10, 0))


class DeviceRow(Frame):
    def __init__(self, device_list_table, main_frame, name, ip, port, cnf={}, **kwargs):
        Frame.__init__(self, device_list_table, kwargs)

        self.main_frame = main_frame
        self.name = name
        self.ip = ip
        self.port = port

        self.device = adb.bridge.get_device(ip, port)
        self.device_frame = None

        self.name_label = Label(
            self, text=self.name, bg='white', height=1, width=10)
        self.ip_port_label = Label(
            self, text='{}:{}'.format(ip, port), bg='white', height=1, width=19)
        self.status_label = Label(
            self, text=DISCONNECTED if self.device is None else CONNECTED, bg='white', width=11
        )

        self.display_btn = Button(self, text='Display')
        self.del_btn = Button(self, text='Delete')

        self.name_label.grid(row=0, column=0, sticky=W, padx=(10, 0))
        self.ip_port_label.grid(row=0, column=1, sticky=W, padx=(10, 0))
        self.status_label.grid(row=0, column=2, sticky=W, padx=(10, 0))
        self.display_btn.grid(row=0, column=3, sticky=W, padx=(10, 0))
        self.del_btn.grid(row=0, column=4, sticky=W, padx=(10, 0))

    def set_on_del_click(self, on_click=lambda self: self):
        self.del_btn.config(command=lambda: on_click(self))

    def set_on_display_click(self, on_click=lambda self: self):

        def callback():
            device = adb.bridge.get_device(self.ip, self.port)
            if device is None:
                return
            if self.device_frame is None:
                self.status_label.config(text=DISCONNECTED if device is None else CONNECTED)
                width, height = self.master.master.windows_size
                self.device_frame = SelectedDeviceFrame(self.main_frame, device, width=width, height=height)
                self.device_frame.grid(row=0, column=0, sticky=N + W)
                self.device_frame.grid_forget()
            on_click(self)

        self.display_btn.config(command=callback)


class AddDeviceFrame(Frame):

    def __init__(self, parent, cnf={}, **kwargs):
        Frame.__init__(self, parent, kwargs)

        self.name_label = Label(self, text='name: ')
        self.name_entry = Entry(self)

        self.ip_label = Label(self, text='ip: ')
        self.ip_entry = Entry(self)

        self.port_label = Label(self, text='port: ')
        self.port_entry = Entry(self)

        self.add_btn = Button(self, text='Add', width=10)

        def ip_entry_validate_cmd(value, action_type):
            if action_type == '1':
                if not value[-1].isdigit() and value[-1] != '.':
                    return False
                if value[0] == '0':
                    return False
            return True

        def port_entry_validate_cmd(value, action_type):
            if action_type == '1':
                if not value[-1].isdigit():
                    return False
                if value[0] == '0':
                    return False
            return True

        self.name_entry.config(width=10)

        self.ip_entry.config(width=15, validate='key', validatecommand=(
            self.register(ip_entry_validate_cmd), '%P', '%d'
        ))
        self.port_entry.config(width=8, validate='key', validatecommand=(
            self.register(port_entry_validate_cmd), '%P', '%d'))

        self.name_label.grid(row=0, column=0, sticky=W, padx=5)
        self.name_entry.grid(row=0, column=1, sticky=W, padx=5)
        self.ip_label.grid(row=0, column=2, sticky=W, padx=5)
        self.ip_entry.grid(row=0, column=3, sticky=W, padx=5)
        self.port_label.grid(row=0, column=4, sticky=W, padx=5)
        self.port_entry.grid(row=0, column=5, sticky=W, padx=5)
        self.add_btn.grid(row=0, column=6, sticky=W, padx=5)

    def set_on_add_click(self, on_click=lambda ip, port: None):
        def callback():
            name = self.name_entry.get()
            ip = self.ip_entry.get()
            port = self.port_entry.get()
            if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", ip) is None:
                return
            if not (1 <= int(port) <= 65535):
                return
            on_click(name, ip, port)
            self.master.devices_config.append(
                {
                    'name': self.name_entry.get(),
                    'ip': self.ip_entry.get(),
                    'port': self.port_entry.get()
                }
            )
            write_device_config(self.master.devices_config)

        self.add_btn.config(command=callback)
