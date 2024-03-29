from pathlib import Path
import os
import time
import uuid
import PIL
from PIL import Image, ImageChops
import socket
import boto3
import requests

class RasPi(object):

    # Setting Up the Server Settings for Raspberry Pi
    localIP     = "169.254.204.164"
    localPort   = 22222
    bufferSize  = 1024

    #Defining Attributes
    msgFromServer       = "This is sent from the server"
    bytesToSend         = str.encode(msgFromServer)

    # Create a datagram socket
    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    # Bind to address and ip
    UDPServerSocket.bind((localIP, localPort))

    # Set OCR FilePath
    filepath = 'card.txt'
    
    def __init__(self): # stuff here might have to be outside?
        pass

    def convert(self, list):
        list.pop() #removes last empty element due to conversion
        globals()['colNocr'] = list[0] #Store Type of element in symbol table
        list.remove(list[0]) # remove it from the list before going to a static tuple
        return tuple(list)

    def resizer(self, src, dest):
        im = Image.open(src)
        im2 = im.resize((224, 224), Image.BICUBIC)
        im2.save(dest, "png")
        print(dest)
        
    def ocr_image(self, image_path):
        # Read document content
        with open(image_path, 'rb') as document:
            imageBytes = bytearray(document.read())

        # Amazon Textract client
        textract = boto3.client('textract')

        # Call Amazon Textract
        response = textract.detect_document_text(Document={'Bytes': imageBytes})

        #print(response)

        # Print detected text
        file = open("card.txt", "w")
        for item in response["Blocks"]:
            if item["BlockType"] == "LINE":
                print ('\033' +  item["Text"] + '\033')
                file.write('\033' +  item["Text"] + '\033 \n')
        file.close()

    def assescnc(self, image_path):

        resizer(image_path, image_path)
        
        #Sends image to the server
        url = "http://169.254.182.43:5000"
        files = {'image': open(image_path, 'rb')}
        response = requests.request("POST", url, files=files)
        print(response)

    # Listen for incoming datagrams
    def readyToReceive(self):
        print("UDP server up and listening")
        while(True):
            bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)

            message = bytesAddressPair[0]
            address = bytesAddressPair[1]
            clientMsg = "Message from Client:{}".format(message)
            clientIP  = "Client IP Address:{}".format(address)    
            print(clientMsg)

            if b"READY" in message:
                globals()['upcode'] = 1
                break;
            
            if b"REQUEST" in message:
                globals()['upcode'] = 2
                break;

            print(clientIP)
        return bytesAddressPair;

    def classification(self):
        with open(filepath) as fp:
            line = fp.readline()
            while line:
                line = fp.readline()
                if box_list[0] in line:
                    print("of class Artifact")
                    return 1
                if box_list[1] in line:
                    print("of class Artifact Creature")
                    return 2
                if box_list[2] in line:
                    print("This is a Creature")
                    return 3
                if box_list[3] in line:
                    print("This is an Instant Spell")
                    return 4
                if box_list[4] in line:
                    print("This is a Sorcery Spell")
                    return 5
                if box_list[5] in line:
                    print("This is an Enchantment")
                    return 6
                if box_list[6] in line:
                    print("This is a Land")
                    return 7

    def startConfig(self):
        globals()['upcode'] = 0

        f = open("file.log", "r")
        a = f.read().split(";")
        globals()['box_list'] = convert(a)

    def main(self):
        while(True):
            print("in ready to receive")
            bytesAddr = readyToReceive();
            address = bytesAddr[1]
            print("out of ready to receive")
            
            # Checking if there is a card
            if (upcode == 1):
                print (" Taking Picture and upload to MS")
                image_path = "/home/pi/Desktop/cnc.png"
                os.system("raspistill -sa 55 -q 90 -sh 100 -ISO 50 -t 1000 -o " + image_path )
                assescnc(image_path)
                res = requests.get('http://169.254.182.43:5000/isCard')
                bytesToSend = str.encode(res.text)
                UDPServerSocket.sendto(bytesToSend, address)
            
            # Checking OCR of the card
            if (upcode == 2):
                print("In UPCODE 2 + COL IS")
                print(type(colNocr))

                if(colNocr == "0"):
                    print (" Taking Picture with AWS")
                    image_path = "/home/pi/Desktop/ocr_card.png"
                    os.system("raspistill -sa 55 -q 90 -sh 100 -ISO 50 -t 1000 -o " + image_path )
                    ocr_image(image_path)
                    class_upcode = classification()
                    print("THIS BOX INDEX : ")
                    print(class_upcode)
                    bytesToSend = str.encode(str(class_upcode))
                    UDPServerSocket.sendto(bytesToSend, address)
                    print (" out of protocol")

                if(colNocr == "1"):
                    print (" Assessing color")
                    assescnc()
                    res = requests.get('http://169.254.182.43:5000/whichCard')
                    print("THIS BOX INDEX : ")
                    box = box_list.index(res.text)
                    print("Read Card color :" +  str(res.text))
                    print("Read box index : " + str(box))
                    bytesToSend = str.encode(str(box))
                    UDPServerSocket.sendto(bytesToSend, address)

if __name__ == '__main__':
    rp = RasPi()
    rp.startConfig()
    rp.main()