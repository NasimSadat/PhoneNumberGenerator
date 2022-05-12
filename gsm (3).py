#!/usr/bin/env python

"""\
Demo: dial a number (simple example using polling to check call status)

Simple demo app that makes a voice call and plays sone DTMF tones (if supported by modem)
when the call is answered, and hangs up the call.
It polls the call status to see if the call has been answered

Note: you need to modify the NUMBER variable for this to work
"""

from __future__ import print_function
from numbertest import WriteSheet
import sys, time, logging, random

PORT = '/dev/ttyUSB0'
BAUDRATE = 115200
#NUMBER = '0799603222' # Number to dial - CHANGE THIS TO A REAL NUMBER
PIN = 2533 # SIM card PIN (if any)
PRE = '0787'

providers = {'AWCC':['070','071'], 'Roshan': ['079','072'] ,'Etisalat': ['078','073'], 'MTN': ['077','076'],'Salaam': ['074']}

from gsmmodem.modem import GsmModem
from gsmmodem.exceptions import InterruptedException, CommandError, TimeoutException



def main():
    print('Initializing modem...')
    modem = GsmModem(PORT, BAUDRATE)
    modem.connect(PIN)
    print('Waiting for network coverage...')
    modem.waitForNetworkCoverage(30)
    #file = open('numbers.txt', 'a')

    i = ChooseProvider()
    a = ChooseAmount()
    j=0
    while j<a:
        # Generating Random phone NUMBER
        n = "%07d" % random.randint(0,9999999)
        NUMBER = PRE + str(n)
        print('Dialing number: {0}'.format(NUMBER))
        linefree=False
        while not linefree:
            try:
                call = modem.dial(NUMBER)
                linefree=True
            except TimeoutException:
                print("DIAL ERROR")
                linefree=False

        #call=modem.dial(NUMBER)
        print('Waiting for call to be answered/rejected')
        wasAnswered = False
        while call.active:
            if call.answered:
                wasAnswered = True
                print('Call has been answered...')
                #file = open('etisalat.csv', 'a')
                #file.write('Unknown,'+NUMBER+',Nothing'+'\n')
                #file.close()
                WriteSheet(NUMBER,i)
                # Wait for a bit - some older modems struggle to send DTMF tone immediately after answering a call
                call.hangup()

                j=j+1
            else:
                # Wait a bit and check again
                time.sleep(0.5)


        if not wasAnswered:
            print('Call was not answered by remote party')
            print('Done.')
            call.hangup()

    #sudo lsof /dev/ttyUSB3

def ChooseProvider():
    global PRE
    print("Which Provider would you like to use?")
    separator = ' '
    for i in providers:
        print(i + ': ' +separator.join(providers[i]))
    val = str(input("Choose prefix: "))
    for i in providers:
        if val in providers[i]:
            print(i+' Network chosen!')
            PRE=val
            return i
    print("Invalid Network, choose again")
    ChooseProvider()

def ChooseAmount():
    val = input("How many numbers to you wish to obtain?")
    return int(val)

if __name__ == '__main__':
    main()