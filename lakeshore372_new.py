import serial
import socket
import time


class LS372:
    def __init__(self,contype='ethernet',port='130.132.159.75',baud=57600,timeout=10,num_channels=16):
        if contype == 'usb':
            self.com = serial.Serial(port=port, baudrate=baud, parity=serial.PARITY_ODD, stopbits=serial.STOPBITS_ONE, bytesize=serial.SEVENBITS, timeout=timeout)
        elif contype == 'ethernet':
            self.IPAddress = port
            self.com = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.com.connect((self.IPAddress,7777))
            self.num_chans = num_channels
            self.com.settimeout(timeout)
#
        self.idn = self.test()

#        self.channels = []
#        for i in range(num_channels):
#            c = chan(self, i+1)

    def msg(self, message):
        msg_str = f'{message}\r\n'.encode()
        self.com.send(msg_str)
        if '?' in message:
            time.sleep(0.01)
            resp = str(self.com.recv(4096)[:-2], 'utf-8')
        else:
            resp = ''
        return resp

    def test(self):
        return self.msg('*IDN?')

    def set_autoscan(self):
        for i in range(self.num_chans):
            self.msg('INSET %d,1,3,3'%i)
        self.msg('SCAN 1,1')

    def gettemp(self,unit="S",chan=-1):

        if (chan==-1):
            resp = self.msg("SCAN?")
            c = resp.split(',')[0]
        elif (chan==0):
            c = 'A'
        else:
            c=str(chan)

        if unit == 'S':
            return float(self.msg('SRDG? %s'%c))
        if unit == 'K':
            return float(self.msg('KRDG? %s'%c))

if __name__=="__main__":
  ls = LS372(contype="ethernet", port="130.132.159.75")
  print(ls.test())
