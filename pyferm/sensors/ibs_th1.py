# pybrew - sensor - Inkbird IBS-TH1 Plus

from . import brewsensor, brewinput
from bluepy import btle
import time
import binascii


class ibs_th1(brewsensor):
    def __init__(self, mac=None):
        self.inputs = [
            brewinput("Temperature", input_type="temperature"),
            brewinput("Humidity", input_type="humidity"),
        ]
        self.mac = mac
        self.peripheral = btle.Peripheral()
        # else:
        #     self.scanner = self.get_scanner()
        super().__init__("Inkbird IBS-TH1")

    def get_inputs(self):
        # self.scanner.start()
        # time.sleep(scantime)
        if self.mac:
            self.peripheral.connect(self.mac)
        characteristic = self.get_characteristic(self.peripheral, 0x002D)
        self.inputs[0].set_value(self.get_temp(characteristic))
        self.inputs[1].set_value(self.get_hum(characteristic))
        self.peripheral.disconnect()
        # if self.uuid:
        #     self.scanner = self.get_scanner()

    # def get_scanner(self):
    #     # if uuid is set, filter Tilts
    #     if self.uuid:
    #         filters = [IBeaconFilter(uuid=self.uuid)]
    #     # otherwise find all Tilts and use the first one seen
    #     else:
    #         filters = [IBeaconFilter(uuid=t) for t in TILTS.keys()]
    #     return BeaconScanner(self.scan_callback, device_filter=filters)

    # def scan_callback(self, bt_addr, rssi, packet, additional_info):
    #     # set uuid of first seen Tilt for better filtering
    #     if not self.uuid:
    #         self.uuid = additional_info["uuid"]

    #     # if uuid is the correct one, set values
    #     if self.uuid == additional_info["uuid"]:
    #         self.inputs[0].set_value(additional_info["major"])
    #         self.inputs[1].set_value(additional_info["minor"] / 1000)

    def get_characteristic(self, peripheral, handle):
        return self.peripheral.readCharacteristic(handle)

    def get_temp(self, characteristic):
        temp_hex = binascii.b2a_hex(characteristic[1]) + binascii.b2a_hex(
            characteristic[0]
        )
        return float(int(temp_hex, 16)) / 100

    def get_hum(self, characteristic):
        humid_hex = binascii.b2a_hex(characteristic[3]) + binascii.b2a_hex(
            characteristic[2]
        )
        return float(int(humid_hex, 16)) / 100
