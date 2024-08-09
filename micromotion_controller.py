#Serial communitcation with micromotion controller
from enum import Enum
import serial
import sys
import time


class micromotion_controller:
    wait_time = 0.1
    def __init__(self, port):
        #Open Serical communication to COM8
        # Baudrate of 19200 bps
        # Parity is set to None
        # Stopbits is set to 1
        # Byte size is set to 8
        self.controller = serial.Serial(port, 19200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)

        # To verify the readiness of the controller Send 100 to controller and wait for the acknowledgement 10.
        self.controller.write(bytes([100]))
        time.sleep(self.wait_time)
        ack = self.controller.read_all()

        #if int.from_bytes(ack, byteorder=sys.byteorder) == 200:
            #print("Controller is ready")
        #else:
            #print("Check Serial Port! ack: ",  int.from_bytes(ack, byteorder=sys.byteorder))

    #XByte2, XByte1 & XByte0 are the number of steps to move for X axis broken into three bytes.
    # Convert x_coord from decimal to hexadecimal of length 6
    @staticmethod
    def calculate_x_byte_sequence(x_coord):
        x_coord = format(x_coord, 'X').zfill(6)
        x_byte2 = bytes.fromhex(x_coord[0:2])
        x_byte1 = bytes.fromhex(x_coord[2:4])
        x_byte0 = bytes.fromhex(x_coord[4:6])
        return [x_byte2, x_byte1, x_byte0]


    def move(self, x_coord, direction, acceleration = 0, deceleration = 0):
        # To initialize the movement write 19 to the controller and wait for the acknowledgement 10.
        r = self.controller.write(bytes([19]))
        time.sleep(self.wait_time)
        ack = self.controller.read_all()
        #print("Initiate Movement: ", int.from_bytes(ack, byteorder=sys.byteorder))

        x2,x1,x0 = micromotion_controller.calculate_x_byte_sequence(x_coord)

        self.controller.write(x2)
        time.sleep(self.wait_time)
        ack = self.controller.read_all()

        self.controller.write(x1)
        time.sleep(self.wait_time)
        ack = self.controller.read_all()

        self.controller.write(x0)
        time.sleep(self.wait_time)
        ack = self.controller.read_all()

        #print("Ack Byte", i ,  int.from_bytes(ack, byteorder=sys.byteorder))

        self.controller.write(bytes([direction]))
        time.sleep(self.wait_time)
        ack = self.controller.read_all()
        #print("Ack Direction: ",  int.from_bytes(ack, byteorder=sys.byteorder))

        self.controller.write(bytes([acceleration]))
        time.sleep(self.wait_time)
        ack = self.controller.read_all()
        #print("Ack Acceleration: ",  int.from_bytes(ack, byteorder=sys.byteorder))

        self.controller.write(bytes([deceleration]))
        time.sleep(self.wait_time)
        ack = self.controller.read_all()
        #print("Ack Deceleration: ",  int.from_bytes(ack, byteorder=sys.byteorder))

        if(int.from_bytes(ack, byteorder=sys.byteorder) != 10):
            # stop the current program
            self.controller.write(bytes([104]))
            ack = self.controller.read_all()
            #print("Ack Stop: ",  int.from_bytes(ack, byteorder=sys.byteorder))

        #time.sleep(5)
        status = self.controller.read()
        status = int.from_bytes(status, byteorder=sys.byteorder)
        if(status == 40):
            print("Home limit reached")
        elif(status == 41):
            print("Far limit reached")
        # elif(status == 170):
        #     print("Movement completed")
        # else:
        #     print("Unknown status")

        self.controller.write(bytes([163]))
        time.sleep(self.wait_time)
        ack = self.controller.read_all()
        #print("Complete Movement: ",  int.from_bytes(ack, byteorder=sys.byteorder))

        for i in range(3):
            self.controller.write(bytes([10]))
            time.sleep(self.wait_time)
            ack = self.controller.read_all()
            #print("Ack", i,  int.from_bytes(ack, byteorder=sys.byteorder))

    def speed(self, speed):
        if(4000 <= speed <= 5):
            print("Speed should be within the range of 5 to 4000")
            return
        self.controller.write(bytes([34]))
        ack = self.controller.read()
        if(int.from_bytes(ack, byteorder=sys.byteorder) == 10):
            #Convert the speed into hexadecimal and spilt to MSB and LSB
            speed = format(speed, 'X').zfill(4)
            self.controller.write(bytes([int(speed[0:2], 16)]))
            ack = self.controller.read()
            self.controller.write(bytes([int(speed[2:4], 16)]))
            ack = self.controller.read()
            #print("Speed set to ", speed)

            for i in range(6):
                self.controller.write(bytes([0]))
                time.sleep(self.wait_time)
                ack = self.controller.read_all()
                #print("Ack", i,  int.from_bytes(ack, byteorder=sys.byteorder))

        else:
            #print("Speed set failed with ack: ", ack)
            pass
        

    def close(self):
        self.controller.close()

def __init__(self):
    pass

# create a enum for direction
class Direction(Enum):
    positive = 125
    negative = 175