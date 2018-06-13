import serial
import socket
import time


class LS372:
    def __init__(self,driver):
        driver_dict = self.driver_parser(driver)
        if driver_dict['contype'] == 'ethernet':
            self.IPAddress = str(driver_dict['port'])
            self.tcp_port = int(driver_dict['tcp'])
            self.num_chans = int(driver_dict['num_channels'])
            self.com = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.com.connect((self.IPAddress,self.tcp_port))
            self.com.settimeout(float(driver_dict['timeout']))
        elif driver_dict['contype'] == 'usb':
            self.port = str(driver_dict['port'])
            self.baud = int(driver_dict['baud'])
            tmout = float(driver_dict['timeout'])
            if str(driver_dict['parity']) == 'odd':
                parityinput = serial.PARITY_ODD
            elif str(driver_dict['parity']) == 'even':
                parityinput = serial.PARITY_EVEN
            elif str(driver_dict['parity']) == 'none':
                parityinput = serial.PARITY_NONE
            if int(driver_dict['stopbits']) == 1:
                stopbitsin = serial.STOPBITS_ONE
            elif int(driver_dict['stopbits']) == 2:
                stopbitsin = serial.STOPBITS_TWO
            if int(driver_dict['bytesize']) == 7:
                byte = serial.SEVENBITS
            self.com = serial.Serial(port = self.port, baudrate = self.baud, parity = parityinput, bytesize = byte, timeout = tmout)
#    def __init__(self,contype,port='130.132.159.75',baud=57600,timeout=10,num_channels=16):
#        if contype == 'usb':
#            self.com = serial.Serial(port=port, baudrate=baud, parity=serial.PARITY_ODD, stopbits=serial.STOPBITS_ONE, bytesize=serial.SEVENBITS, timeout=timeout)
#        elif contype == 'ethernet':
#            self.IPAddress = port
#            self.com = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#            self.com.connect((self.IPAddress,7777))
#            self.num_chans = num_channels
#            self.com.settimeout(timeout)
#
        self.idn = self.test()

#        self.channels = []
#        for i in range(num_channels):
#            c = chan(self, i+1)


    def driver_parser(self,driverfile):
        out = {}
        with open(str(driverfile),'r') as f:
			for line in f:
				listedline = line.strip().decode('unicode-escape').split('=')
				if len(listedline)>1:
					out[listedline[0]] = listedline[1]
			f.close()
			return out

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
