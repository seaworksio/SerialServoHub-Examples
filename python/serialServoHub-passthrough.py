import serial

STX = '\x02'
ETX = '\x03'
FDT = ';'

port = 'COM13' #change accordingly
baud = 115200

PWM_data = ""
PWM_in = ["1500"] *5
PWM_out = ["1500"] *4

ser = serial.Serial(port, baud, timeout=None)
if ser.isOpen():
    ser.close()
    ser.open()

def bufferReset():
    ser.reset_input_buffer()
    ser.reset_output_buffer()

def syncPorts():
    PWM_out[0] = PWM_in[0]
    PWM_out[1] = PWM_in[1]
    PWM_out[2] = PWM_in[2]
    PWM_out[3] = PWM_in[3]

def writeOutputs():
    SA = STX.encode('ascii') + "SA".encode('ascii') + PWM_out[0].encode('ascii') + ETX.encode('ascii')
    SB = STX.encode('ascii') + "SB".encode('ascii') + PWM_out[1].encode('ascii') + ETX.encode('ascii')
    SC = STX.encode('ascii') + "SC".encode('ascii') + PWM_out[2].encode('ascii') + ETX.encode('ascii')
    SD = STX.encode('ascii') + "SD".encode('ascii') + PWM_out[3].encode('ascii') + ETX.encode('ascii')
    ser.write(SA)
    ser.write(SB)
    ser.write(SC)
    ser.write(SD)

bufferReset()

while True:
    data_raw = ser.read(1)
    if data_raw == b'\x02':
        data_raw = ser.read_until(b'\x03').decode("utf-8")
        PWM_data = data_raw[:-1]
        PWM_in = list(filter(None, PWM_data.split(FDT)))
        bufferReset()
        syncPorts()
        writeOutputs()