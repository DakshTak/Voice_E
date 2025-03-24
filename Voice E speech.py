import speech_recognition as sr
from pyfirmata import Arduino, SERVO, util
from time import sleep

r=sr.Recognizer()
mic = sr.Microphone(device_index=1)

port = 'COM3'
fpin = 10
rlpin = 7
glpin = 6
board = Arduino(port)



#for led=> Start an iterator thread to avoid buffer overflow
it = util.Iterator(board)
it.start()

#set the pin modes to OUTPUT
board.digital[rlpin].mode = 1 
board.digital[glpin].mode = 1


#for fan On the arduino uno board at the digital pin 10 the component connected is servo motor
board.digital[fpin].mode=SERVO 

def rotate(pin,angle):
    board.digital[pin].write(angle)
    sleep(0.015)

with mic as source:
    
    r.adjust_for_ambient_noise(source,duration=1)
    while True:
        print("Listening...")
        audio = r.listen(source)

        try:
            command = r.recognize_google(audio).lower()
            if command =='switch on fan':
                print("switch on fan")
                for x in range(3):
                    for i in range(0,180):
                            rotate(fpin,i)
                                
                                

            elif command =='switch on red light':
                print("switching on red light")
                board.digital[rlpin].write(1)
                # sleep(0.5)
                # board.digital[rlpin].write(0)
                # sleep(0.5)

            elif command =='switch on green light':
                print("switching on green light")
                board.digital[glpin].write(1)
                # sleep(0.5)
                # board.digital[glpin].write(0)
                # sleep(0.5)

            elif command =='switch off all':
                print("switch off all devices")
                board.digital[rlpin].write(0)
                board.digital[glpin].write(0)
                

            elif command =='thank you':
                print("Your welcome")
                break

            else:
                print("speak again")
        except:
            print("no audio")