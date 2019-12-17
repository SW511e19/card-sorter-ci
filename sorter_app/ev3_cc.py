import sys
sys.path.append("test/mock")
import ev3_mock as ev3 # Simulated Test Environment
#import ev3dev.ev3 as ev3 # Live Environment
import time
import socket

class CardCollector(object):
        
    # Setting Up the Server Settings for Raspberry Pi
    localIP     = "192.168.2.4"
    localPort   = 60000
    bufferSize  = 1024

    # Create a datagram socket
    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    # Bind to address and ip
    # UDPServerSocket.bind((localIP, localPort))

    colorsensor = ev3.ColorSensor()
    colorsensor.MODE_COL_COLOR
    m1 = ev3.LargeMotor('outB')  # Cord has to go over the wheel (right of the wheel)
    m2 = ev3.LargeMotor('outC')  # Cord has to go under the wheel

    def __init__(self):
        pass
    
    # Listen for incoming datagrams
    def readyToReceive(self):
        print("UDP server up and listening")
        while(True):
            bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
            message = bytesAddressPair[0]

            globals()["address"] = bytesAddressPair[1]

            #clientMsg = "Message from Client:{}".format(message)

            clientMsg = str(message)
            print("returned: " + clientMsg)

            # For debugging purposes
            if("calibrate" in clientMsg or "stop" in clientMsg):
                return clientMsg

            if "1" in clientMsg:
                return 1

            if "2" in clientMsg:
                return 2

            if "3" in clientMsg:
                return 3

            if "4" in clientMsg:
                return 4

            if "5" in clientMsg:
                return 5

            if "6" in clientMsg:
                return 6

            if "7" in clientMsg:
                return 7

        return 0


    def run(self, speed):
        m1.on(ev3.SpeedPercent(speed))
        m2.on(ev3.SpeedPercent(-speed))

    def stop(self):
        m1.on(ev3.SpeedPercent(0))
        m2.on(ev3.SpeedPercent(0))

    #run(-100)
    #time.sleep(3)
    #run(100)
    #time.sleep(3)
    #stop()

    def calibrate(self, speed):
        calibration_color = colorsensor.COLOR_RED
        run(-speed)
        while True:
            if(colorsensor.color == calibration_color):
                stop()
                break

    def cc(self, current_box, box_offset, speed, secs_skip_looking):
        calibration_color = colorsensor.COLOR_RED
        is_box_color = True
        look_for_box = False
        box_color = colorsensor.color
        
        #Sets the first box color it looks for to be the opposite of what it reads at first
        if box_color == colorsensor.COLOR_GREEN:
            box_color = colorsensor.COLOR_YELLOW
        else:
            box_color = colorsensor.COLOR_GREEN
        
        # The red calibrating position and the first box is very close to each other.
        # Set a flag so if the machine just calibrated, it start looking for the first box immediately
        if (colorsensor.color == calibration_color):
            look_for_box = True
            box_color = colorsensor.COLOR_YELLOW
        
        run(speed)

        while current_box != box_offset:
            if(look_for_box == False):
                time.sleep(secs_skip_looking)
            
            #Look for changes from no-box to box so it doesn't dont count the same box multiple times when the color dosen't change
            if is_box_color == False and colorsensor.color == box_color:
                print(box_color)
                is_box_color = True
                print("was at " + str(current_box))
                if speed >= 0:
                    current_box += 1
                else:
                    current_box -= 1
                print("is at " + str(current_box))
                look_for_box = False
                if box_color == colorsensor.COLOR_GREEN:
                    box_color = colorsensor.COLOR_YELLOW
                else:
                    ox_color = colorsensor.COLOR_GREEN
                    
            
            if colorsensor.color != box_color:
                is_box_color = False

        return current_box

    def cc_one_color(self, current_box, box_offset, speed, secs_skip_looking):
        calibration_color = colorsensor.COLOR_RED
        is_box_color = True
        look_for_box = False
        box_color = colorsensor.color
        
        
        # The red calibrating position and the first box is very close to each other.
        # Set a flag so if the machine just calibrated, it start looking for the first box immediately
        if (colorsensor.color == calibration_color):
            look_for_box = True
        
        run(speed)

        while current_box != box_offset:
            if(look_for_box != True):
                time.sleep(secs_skip_looking)
            
            #Look for changes from no-box to box so it doesn't dont count the same box multiple times when the color dosen't change
            if is_box_color == False and (colorsensor.color == colorsensor.COLOR_GREEN or colorsensor.color == colorsensor.COLOR_YELLOW):
                is_box_color = True
                print("was at " + str(current_box))
                if speed >= 0:
                    current_box += 1
                else:
                    current_box -= 1
                print("is at " + str(current_box))
                look_for_box = False
                    
            
            if (colorsensor.color != colorsensor.COLOR_GREEN and colorsensor.color != colorsensor.COLOR_YELLOW):
                is_box_color = False

        return current_box

    def go_to_box(self, current_box, dest_box, speed, secs_skip_looking):
        if (dest_box == current_box):
            print("Was already at box")
        if dest_box > current_box:
            current_box = cc(current_box, dest_box, speed, secs_skip_looking)
        else:
            current_box = cc(current_box, dest_box, -speed, secs_skip_looking)
        stop()
        return current_box


    def go_to_box2(self, current_box, dest_box, speed, secs_skip_looking):
        if (dest_box == current_box):
            print("Was already at box")
        if dest_box > current_box:
            current_box = cc_one_color(current_box, dest_box, speed, secs_skip_looking)
        else:
            current_box = cc_one_color(current_box, dest_box, -speed, secs_skip_looking)
        stop()
        return current_box

    def run_until_stopped(self):
        run(speed)
        while True:
            #Look for changes from no-box to box so it doesn't dont count the same box multiple times when the color dosen't change
            if is_box_color == False and (colorsensor.color == colorsensor.COLOR_GREEN or colorsensor.color == colorsensor.COLOR_YELLOW):
                time.sleep(5)
                    
            
            if (colorsensor.color != colorsensor.COLOR_GREEN and colorsensor.color != colorsensor.COLOR_YELLOW):
                is_box_color = False

    def main(self):
        secs_skip_looking = 0.4
        current_box = 0
        globals()["cbox"] = 0

        calibrate(15)
        print("Calibrated")

        while True:
            dest_box = readyToReceive()
            #globals()["cbox"] = go_to_box(cbox, dest_box, 7, secs_skip_looking)
            if(isinstance(dest_box, str)):
                if("stop" in dest_box ):
                    run(0)
                if("calibrate" in dest_box):
                    calibrate(15)
                    globals()["cbox"] = 0

            else:
                globals()["cbox"] = go_to_box(cbox, int(dest_box), 7, secs_skip_looking)
            bytesToSend = str.encode("OK")
            UDPServerSocket.sendto(bytesToSend, address)

if __name__ == '__main__':
    cc = CardCollector()
    cc.main()
