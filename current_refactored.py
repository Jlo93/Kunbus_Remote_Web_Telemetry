# Company: M & E Controls Ltd
# Engineer: Jonathan Logue
# Tested by: ------------
# 
# Date: 4/3/2022
# Project: Lake Pumping station - Control & Monitoring System
#
# Code Description: # Program handles the main functionality of both the control logic for the pumps
# as well as the data monitoring and alarming functionality. Code base also manages the controller
# boot process and peripheral configuration and assignments.



# Importing of the relevant code libraries
import revpimodio2
import time
import schedule
import datetime
import smtplib
from datetime import datetime
from twilio.rest import Client
from firebase import firebase


# defining the firebase real time data base end point
firebase = firebase.FirebaseApplication('https://-------------------------------.firebasedatabase.app/',None)



# defining the twillio account api credentials - review
account_sid = '-----------------------------------'
auth_token = '------------------------------------'
db = firebase.put('Telemetry Data/SMS Toggle/','Switch',1)

p1_trip_msg = 0
p2_trip_msg = 0
boot_msg = 0

contacts = ['insert phone numbers']
admin_contact = ['admin number']



# SMS function list for various sms outputs.

def checkTime(time1,time2,day1,day2):
    now = datetime.now()
    dt_string = now.strftime("%H")
    day = now.strftime("%u")

    dt = float(dt_string)
    day = int(day)

    if dt >= time1:
        if dt <= time2:
            if day >= day1:
                if day <= day2:
                    timeCheck = False
                else:
                    timeCheck = True
            else:
                timeCheck = True
        else:
            timeCheck = True
    else:
        timeCheck = True

    return timeCheck


            
                             

# sms function boot start status

# sms function boot status
def boot_end1_sms(sid, token,contacts):
    contactlen = len(contacts)

    for i in range(0,contactlen):
        client = Client(sid, token)
        message = client.messages.create(

            messaging_service_sid='--------------------------------',
            body= 'Lake Pumps Alert System - Boot alert - System has been forced to reboot due to power outage or other circumstances. Details below.- Boot process has finalised Pump No.1 passed start up checks. Start Signal has been sent to VSD No.1.',
            to=contacts[i]
            )

        
# sms function boot status
def boot_end2_sms(sid, token,contacts):

    contactlen = len(contacts)

    for i in range(0,contactlen):
        client = Client(sid, token)
        message = client.messages.create(
            
            messaging_service_sid='--------------------------------',
            body='Lake Pumps Alert System - Boot alert - System has been forced to reboot due to power outage or other circumstances. Details below.- Boot process has finalised Pump No.2 passed start up checks. Start Signal has been sent to VSD No.2.',
            to=contacts[i]
            )
        
# sms function boot status
def boot_end3_sms(sid, token, contacts):
    contactlen = len(contacts)

    for i in range(0,contactlen):
        client = Client(sid, token)
        message = client.messages.create(
            messaging_service_sid='--------------------------------',
            body='Lake Pumps Alert System - Boot alert - System has been forced to reboot due to power outage or other circumstances. Details below.- Boot process has finalised No Pumps available at start up. Start Signal has NOT been sent to any VSD.',
            to=contacts[i]
            )
        
# sms function for the case of a phase failure
def phase_fail_sms(sid, token, contacts):
    contactlen = len(contacts)
    for i in range(0,contactlen):
        client = Client(sid, token)
        message = client.messages.create(
            
            messaging_service_sid='--------------------------------',
            body='Lake Pumps Alert System - Supply Interuption - Power Outage.',
            to=contacts[i]
        )
        
# sms function for the case of a pump no.1 trip    
def p1_trip_sms(sid, token, contacts):
    contactlen = len(contacts)

    for i in range(0,contactlen):
        client = Client(sid, token)
        message = client.messages.create(
            messaging_service_sid='--------------------------------',
            body='Lake Pumps Alert System - Pump Tripped.',
            to=contacts[i]
            )
        
# sms function for the case of a pump no.2 trip       
def p2_trip_sms(sid, token, contacts):
    contactlen = len(contacts)
    
    for i in range(0,contactlen):
        client = Client(sid, token)
        message = client.messages.create(
            messaging_service_sid=''--------------------------------',
            body='Lake Pumps Alert System - Pump No.2 Registered a Trip Signal.',
            to=contacts[i]
            )

# sms function for the case of a pump house door opened       
def pHouse_sms(sid, token, contacts):
    try:
        hr1 = firebase.get('Telemetry Data/Time Data/Start Hour','')
        hr2 = firebase.get('Telemetry Data/Time Data/End Hour','')
        day1 = firebase.get('Telemetry Data/Time Data/Start Day','')
        day2 = firebase.get('Telemetry Data/Time Data/End Day','')
        enable = firebase.get('Telemetry Data/Time Data/SMS Switch/value','')
    except:
        hr1 = 8.0
        hr2 = 18.0
        day1 = 1
        day2 = 5

    permission = checkTime(hr1,hr2,day1,day2)

    try:
        if enable == '1':
            if permission == True:
                contactlen = len(contacts)
        
                for i in range(0,contactlen):
                    client = Client(sid, token)
                    message = client.messages.create(
                        messaging_service_sid='--------------------------------',
                        body='Lake Pumps Alert System - Pump House Door Opened - Check Camera App.',
                        to=contacts[i]
                    )
            else:
                pass
        elif enable == '0':
            contactlen = len(contacts)
        
            for i in range(0,contactlen):
                client = Client(sid, token)
                message = client.messages.create(
                messaging_service_sid='--------------------------------',
                body='Lake Pumps Alert System - Pump House Door Opened - Check Camera App.',
                to=contacts[i]
                ) 
    except:
        pass
    
    
    
        
        
    
# sms function for the case of a generator house door opened       
def genHouse_sms(sid, token, contacts):
    try:
        hr1 = firebase.get('Telemetry Data/Time Data/Start Hour','')
        hr2 = firebase.get('Telemetry Data/Time Data/End Hour','')
        day1 = firebase.get('Telemetry Data/Time Data/Start Day','')
        day2 = firebase.get('Telemetry Data/Time Data/End Day','')
        enable = firebase.get('Telemetry Data/Time Data/SMS Switch/value','')
    except:
        hr1 = 8.0
        hr2 = 18.0
        day1 = 1
        day2 = 5

    permission = checkTime(hr1,hr2,day1,day2)
    try:
        if enable == '1':
            if permission == True:
                contactlen = len(contacts)
                for i in range(0,contactlen):
                    client = Client(sid, token)
                    message = client.messages.create(
                    messaging_service_sid='--------------------------------',
                    body='Lake Pumps Alert System - Generator Container Door Opened - Check Camera App.',
                    to=contacts[i]
                    )
            else:
                pass
        elif enable == '0':
            contactlen = len(contacts)

            for i in range(0,contactlen):
                client = Client(sid, token)
                message = client.messages.create(
                messaging_service_sid='--------------------------------',
                body='Lake Pumps Alert System - Generator Container Door Opened - Check Camera App.',
                to=contacts[i]
                )
    except:
        pass

    
    
    
    
    
# sms function for the case of a pump house door opened       
def dHouse_sms(sid, token, contacts):

    try:
        hr1 = firebase.get('Telemetry Data/Time Data/Start Hour','')
        hr2 = firebase.get('Telemetry Data/Time Data/End Hour','')
        day1 = firebase.get('Telemetry Data/Time Data/Start Day','')
        day2 = firebase.get('Telemetry Data/Time Data/End Day','')
        enable = firebase.get('Telemetry Data/Time Data/SMS Switch/value','')
    except:
        hr1 = 8.0
        hr2 = 18.0
        day1 = 1
        day2 = 5

    permission = checkTime(hr1,hr2,day1,day2)

    try:
        if enable == '1':
            if permission == True:
                contactlen = len(contacts)
                for i in range(0,contactlen):
                    client = Client(sid, token)
                    message = client.messages.create(
                    messaging_service_sid='--------------------------------',
                    body='Lake Pumps Alert System - Diesel Container Door Opened - Check Camera App.',
                    to=contacts[i]
                    )
            else:
                pass
        elif enable == '0':
            contactlen = len(contacts)
            for i in range(0,contactlen):
                client = Client(sid, token)
                message = client.messages.create(
                messaging_service_sid='--------------------------------',
                body='Lake Pumps Alert System - Diesel Container Door Opened - Check Camera App.',
                to=contacts[i]
                )
    except:
        pass
        

    

    
    
    
# sms function for the case of a pump house door opened       
def sump_sms(sid, token, contacts):
    contactlen = len(contacts)
    
    for i in range(0,contactlen):
        client = Client(sid, token)
        message = client.messages.create(
            messaging_service_sid='--------------------------------',
            body='Lake Pumps Alert System - Pump Sump Level Low - Pumps Stopped.',
            to=contacts[i]
            )

# sms function for the case of a pump house door opened       
def fuelLow_sms(sid, token, contacts):
    contactlen = len(contacts)
    
    for i in range(0,contactlen):
        client = Client(sid, token)
        message = client.messages.create(
            messaging_service_sid='--------------------------------',
            body='Lake Pumps Alert System - Diesel Tank Level Low - Refuel Required Soon',
            to=contacts[i]
            )             

def emailFunc():
    gmail_user = '--------------------------------'
    gmail_password = '--------------------------------'

    sent_from = gmail_user
    to = ['insert emails']
    subject = 'Pumping Station'
    body = '''This is a automated email sent through pyhton, triggered by a system reboot by the Kunbus Controller. No Action Required.'''

    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (sent_from, ", ".join(to), subject, body)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text)
        server.close()

        print('Email sent!')
    except:
        print('Something went wrong...')
        
# status led display fucntion to visually state that the controller is in boot process.
#def led_Flicker():
    
#def boot_process():
    
    
# Program initialisation process
class MyRevPiApp():

    #Digital inputs
    # - p1 run 
    # - p1 trip
    # - pump house door 
    # - gen house door
    # - phase fail
    # - p1 SW
    # - diesel house door
    # - p2 SW

    #Digital outputs
    # - vsd1 start
    # - vsd2 start
    # - p1 run lamp
    # - p1 trip lamp 
    # - p2 run lamp
    # - p2 trip lamp
    # - mains healthy lamp
    #
    

     # Main app for Revpi
     # defining the self class
    def __init__(self):
        
        
        # init MyRevAppPi class


        # Initialise events on io triggers on both rising and falling conditions

        self.rpi = revpimodio2.RevPiModIO(autorefresh=True)

        self.rpi.handlesignalend(self.cleanup_revpi)

        # Pump no.1 run signal events
        self.rpi.io.DInBit_1.reg_event(self.event_p1_run_on,edge=revpimodio2.RISING)
        self.rpi.io.DInBit_1.reg_event(self.event_p1_run_off,edge=revpimodio2.FALLING)

        # Pump no.1 trip signal events
        self.rpi.io.DInBit_2.reg_event(self.event_p1_trip,edge=revpimodio2.RISING)
        self.rpi.io.DInBit_2.reg_event(self.event_p1_heal,edge=revpimodio2.FALLING)

        # Pump house door signal events
        #self.rpi.io.DInBit_3.reg_event(self.event_p2_run_on,edge=revpimodio2.RISING)
        self.rpi.io.DInBit_3.reg_event(self.event_pHouse_door_open,edge=revpimodio2.FALLING)

        # Generator house door signal events
        #############################self.rpi.io.DInBit_4.reg_event(self.event_p2_trip,edge=revpimodio2.RISING)
        self.rpi.io.DInBit_4.reg_event(self.event_genHouse_door_open,edge=revpimodio2.FALLING)

        # Panel phase supply events
        self.rpi.io.DInBit_5.reg_event(self.event_phase_fail,edge=revpimodio2.FALLING)
        self.rpi.io.DInBit_5.reg_event(self.event_phase_rehab,edge=revpimodio2.RISING)

        # Pump no.1 enable SW signal events
        self.rpi.io.DInBit_6.reg_event(self.event_p1_sw_off,edge=revpimodio2.FALLING)
        self.rpi.io.DInBit_6.reg_event(self.event_p1_sw_on,edge=revpimodio2.RISING)

        self.rpi.io.DInBit_7.reg_event(self.event_dHouse_door_open,edge=revpimodio2.FALLING)

        #self.rpi.io.DInBit_8.reg_event(self.event_reset,edge=revpimodio2.RISING)
        # Pump no.2 enable SW signal events
        self.rpi.io.DInBit_8.reg_event(self.event_p2_sw_off,edge=revpimodio2.FALLING)
        self.rpi.io.DInBit_8.reg_event(self.event_p2_sw_on,edge=revpimodio2.RISING)

        
        

    def cleanup_revpi(self):
        self.rpi.core.a1green.value = False
        self.rpi.io.DOutBit_1.value = False
        self.rpi.io.DOutBit_2.value = False


################################################################
################< Pump No.1 Events > ###########################

    def event_p1_run_on(self,ioname,iovalue):
        
        self.rpi.io.DOutBit_5.value = True

    def event_p1_run_off(self,ioname,iovalue):
        pass
        self.rpi.io.DOutBit_5.value = False   

    def event_p1_trip(self,ioname,iovalue):
        # turn on trip lamp
        self.rpi.io.DOutBit_6.value = True
        # turn off start signal
        self.rpi.io.DOutBit_2.value = False
        
        #############################if self.rpi.io.DInBit_7.value == True:
        #############################    if self.rpi.io.DInBit_4.value == False:
        #############################        self.rpi.io.DOutBit_2.value = True
        try:
            p1_trip_sms(sid=account_sid, token=auth_token,contacts=contacts)
        except:
            pass
    def event_p1_heal(self,ioname,iovalue):
        # turn off trip lamp
        self.rpi.io.DOutBit_6.value = False
        
        # if p2 not tripped
        if self.rpi.io.DInBit_2.value == False:
            # and if enabled
            if self.rpi.io.DInBit_7.value == True:
                # start p1
                self.rpi.io.DOutBit_2.value = True
            else:
                #else no start
                self.rpi.io.DOutBit_2.value = False
        else:
            #else no start
            self.rpi.io.DOutBit_2.value = False
            
              
        #############################elif self.rpi.io.DInBit_4.value == False:
        #############################      self.rpi.io.DOutBit_2.value = True


    def event_p1_sw_off(self,ioname,iovalue):
        # turn off start signal
        self.rpi.io.DOutBit_1.value = False
        self.rpi.io.DOutBit_3.value = False
        
       ############################# if self.rpi.io.DInBit_4.value == False:
       #############################     if self.rpi.io.DInBit_7.value == True:
       #############################         self.rpi.io.DOutBit_2.value = True

    def event_p1_sw_on(self,ioname,iovalue):
        #self.rpi.io.DOutBit_2.value = False
        #if self.rpi.io.DInBit_2.value == False:
        self.rpi.io.DOutBit_1.value = True
        self.rpi.io.DOutBit_3.value = True
         
                                
##########################< END > ##############################


################################################################
################< Pump No.2 Events >############################           

   ############################# def event_p2_run_on(self,ioname,iovalue):
   #############################     self.rpi.io.DOutBit_5.value = True

   ############################# def event_p2_run_off(self,ioname,iovalue):
   #############################     self.rpi.io.DOutBit_5.value = False 

   ############################# def event_p2_trip(self,ioname,iovalue):
   #############################     self.rpi.io.DOutBit_6.value = True
   #############################     self.rpi.io.DOutBit_2.value = False
   #############################     if self.rpi.io.DInBit_6.value == True:
   #############################         if self.rpi.io.DInBit_2.value == False:
   #############################             self.rpi.io.DOutBit_1.value = True
            
        #p2_trip_sms(sid=account_sid, token=auth_token)

   ############################# def event_p2_heal(self,ioname,iovalue):
   #############################     self.rpi.io.DOutBit_6.value = False
   #############################     if self.rpi.io.DInBit_7.value == True:
   #############################         if self.rpi.io.DInBit_4.value == False:
   #############################             if self.rpi.io.DOutBit_1.value == False:
   #############################                 self.rpi.io.DOutBit_2.value = True
              
   #############################     elif self.rpi.io.DInBit_2.value == False:
   #############################           self.rpi.io.DOutBit_1.value = True


    def event_p2_sw_off(self,ioname,iovalue):
        self.rpi.io.DOutBit_2.value = False
        self.rpi.io.DOutBit_5.value = False
        # Change over code <>
        # if P2 switched off, and P1 not tripped
        # if self.rpi.io.DInBit_2.value == False:
        # and p1 selected, run p1.
        #    if self.rpi.io.DInBit_6.value == True:
        #        self.rpi.io.DOutBit_1.value = True
                    

    def event_p2_sw_on(self,ioname,iovalue):
        self.rpi.io.DOutBit_2.value = True
        self.rpi.io.DOutBit_5.value = True

##########################< END > ##############################


################################################################
################< Phase Supply Events > ########################

    def event_phase_fail(self,ioname,iovalue):
        
        self.rpi.io.DOutBit_1.value = False 
        self.rpi.io.DOutBit_2.value = False
        try:
            phase_fail_sms(sid=account_sid, token=auth_token,contacts=contacts)
        except:
            pass
    def event_phase_rehab(self,ioname,iovalue):
        
        time.sleep(90)
        # if p1 not tripped
        if self.rpi.io.DInBit_2.value == False:
            # and if enabled
            if self.rpi.io.DInBit_6.value == True:
                # start p1
                self.rpi.io.DOutBit_1.value = True
            else:
                #else no start
                self.rpi.io.DOutBit_1.value = False
        else:
            #else no start
            self.rpi.io.DOutBit_1.value = False

##########################< END > ##############################

########################< DOOR EVENTS > ########################            

    def event_pHouse_door_open(self,ioname,iovalue):
        try:
            pHouse_sms(sid=account_sid,token=auth_token,contacts=contacts)
        except:
            pass

    def event_genHouse_door_open(self,ioname,iovalue):
        try:
            genHouse_sms(sid=account_sid,token=auth_token,contacts=contacts)
        except:
            pass
    def event_dHouse_door_open(self,ioname,iovalue):
        try:
            dHouse_sms(sid=account_sid,token=auth_token,contacts=contacts)
        except:
            pass

##########################< END > ##############################

        
################################################################
################< Pump No.2 Events > ###########################
 

    def event_reset(self,ioname,iovalue):
        if self.rpi.io.DInBit_2.value == False:
                self.rpi.io.DOutBit_1.value = True
              
        elif self.rpi.io.DInBit_4.value == False:
              self.rpi.io.DOutBit_2.value = True                  
        
         
        # program start point - - runs once at boot
    def start(self):
        # Imediatley manually clear outputs
        self.rpi.io.DOutBit_1.value = False
        self.rpi.io.DOutBit_2.value = False
        self.rpi.io.DOutBit_3.value = False
        self.rpi.io.DOutBit_4.value = False
        self.rpi.io.DOutBit_5.value = False
        self.rpi.io.DOutBit_6.value = False
        self.rpi.io.DOutBit_7.value = False
        self.rpi.io.DOutBit_8.value = False

         # checks mains supply
        if self.rpi.io.DInBit_5.value == True:
            # if true turn on mains healthy lamp
            self.rpi.io.DOutBit_7.value = True
        else:
            self.rpi.io.DOutBit_7.value = False

        self.rpi.core.a2green.value = False
        self.rpi.core.a1green.value = False
        self.rpi.core.a2red.value = False
        self.rpi.core.a1red.value = False

        # run clean up process 
        #cleanup_revpi()

        # display that boot is in process
        self.rpi.core.a2red.value = False
        self.rpi.core.a1red.value = True
        time.sleep(0.2)
        self.rpi.core.a2red.value = True
        self.rpi.core.a1red.value = False
        time.sleep(0.2)
        self.rpi.core.a2red.value = False
        self.rpi.core.a1red.value = True
        time.sleep(0.2)
        self.rpi.core.a2red.value = True
        self.rpi.core.a1red.value = False
        time.sleep(0.2)
        self.rpi.core.a2red.value = False
        self.rpi.core.a1red.value = True
        time.sleep(0.2)
        self.rpi.core.a2red.value = True
        self.rpi.core.a1red.value = False
        time.sleep(0.2)
        self.rpi.core.a2red.value = False
        self.rpi.core.a1red.value = True
        time.sleep(0.2)
        self.rpi.core.a2red.value = True
        self.rpi.core.a1red.value = False
        time.sleep(0.2)
        self.rpi.core.a2red.value = False
        self.rpi.core.a1red.value = True
        time.sleep(0.2)
        self.rpi.core.a2red.value = True
        self.rpi.core.a1red.value = True

        
        
        #print("</> ... ... ... ... ... ... ... ... ... ... ... </> ")
        #print("</> ... System Boot Begin ... </>")
        # sending the boot up sms
        #time.sleep(1)
        self.rpi.mainloop(blocking=False)
        # start sceheduled task function - 1 min for testing
        #schedule.every(1).minutes.do(job)
        # try to make connection with the firebase datebase
        try:
            pfr = firebase.get('Telemetry Data/Supply Watchdog/Phase Fail Relay','')
            # if successful print results
            #print("</> ... Connection Successful ... </>")
            #time.sleep(1)
            #print("</> ... Launching Cloud Database ... </>")
            #time.sleep(1)
        except:
            pass
            
            
        # checks if p1 is not tripped
        if self.rpi.io.DInBit_2.value == False:
            self.rpi.io.DOutBit_4.value = False
            #print("</> ... Pump No.1 Healthy ... YES </>")
            #time.sleep(1)
        else:
            self.rpi.io.DOutBit_4.value = True
            #print("</> ... Pump No.1 Healthy ... NO </>")
            #time.sleep(1)

        # checks p2 enabled at panel door switch
        #if self.rpi.io.DInBit_7.value == True:
            
        #############################if self.rpi.io.DInBit_4.value == False:
        #############################    self.rpi.io.DOutBit_6.value = False
            #print("</> ... Pump No.2 Healthy ... YES </>")
            #time.sleep(1)
        #############################else:
            #print("</> ... Pump No.2 Healthy ... NO </>")
            #############################self.rpi.io.DOutBit_6.value = True
            #time.sleep(1)
            
        # takes checks into consideration, if all well at boot p1 will start
        # should p1 not pass checks - p2 will start
        # should p2 also not pass checks - no pumps will start
        # should mains supply fail check - no pumps will start
        if self.rpi.io.DInBit_5.value == True:
            #print("Pump turned on ... YES")
            if self.rpi.io.DInBit_6.value == True:
                if self.rpi.io.DInBit_2.value == False:
                    #print("Pump NOT tripped ... YES")
                    #print('</> ... Starting Pump No.1 ... </> ')
                    #time.sleep(1)
                    self.rpi.io.DOutBit_1.value = True
        else:
            #print("</> ... Pump No.1 Failed check ... </>")
            #time.sleep(1)
            self.rpi.io.DOutBit_1.value = False
            
       ############################# if self.rpi.io.DInBit_5.value == True:
            #print("Pump turned on ... YES")
       #############################    if self.rpi.io.DInBit_7.value == True:
       #############################         if self.rpi.io.DOutBit_1.value == False:
       #############################                 if self.rpi.io.DInBit_4.value == False:
                            #print("Pump NOT tripped ... YES")
                            #print("</> ... Starting Pump No.2 ... </> ")
                            #time.sleep(1)
       #############################                     self.rpi.io.DOutBit_2.value = True
       ############################# else:
            #print("</> ... Pump No.2 Failed check ... </> ")
            #time.sleep(1)
           ############################# self.rpi.io.DOutBit_2.value = False
            
        
        if self.rpi.io.DOutBit_1.value == True:
            try:
                boot_end1_sms(sid=account_sid,token=auth_token,contacts=admin_contact)
            except:
                pass
        elif self.rpi.io.DOutBit_2.value == True:
            try:
                boot_end2_sms(sid=account_sid,token=auth_token,contacts=admin_contact)
            except:
                pass
        else:
            try:
                boot_end3_sms(sid=account_sid,token=auth_token,contacts=admin_contact)
            except:
                pass

        emailFunc()


        #print("</> ... System Boot Complete ... </>")
        #time.sleep(1)
        #print("</> ... Entering Main Execution ... </>")
        #time.sleep(1)
        #print("</> ... ... ... ... ... ... ... ... ... ... ... </> ")

        # display that boot process is finished
        self.rpi.core.a2red.value = False
        self.rpi.core.a1red.value = True
        time.sleep(0.2)
        self.rpi.core.a2red.value = True
        self.rpi.core.a1red.value = False
        time.sleep(0.2)
        self.rpi.core.a2red.value = False
        self.rpi.core.a1red.value = True
        time.sleep(0.2)
        self.rpi.core.a2red.value = True
        self.rpi.core.a1red.value = False
        time.sleep(0.2)
        self.rpi.core.a2red.value = False
        self.rpi.core.a1red.value = True
        time.sleep(0.2)
        self.rpi.core.a2red.value = True
        self.rpi.core.a1red.value = False
        time.sleep(0.2)
        self.rpi.core.a2red.value = False
        self.rpi.core.a1red.value = True
        time.sleep(0.2)
        self.rpi.core.a2red.value = True
        self.rpi.core.a1red.value = False
        time.sleep(0.2)
        self.rpi.core.a2red.value = False
        self.rpi.core.a1red.value = True
        time.sleep(0.2)
        self.rpi.core.a2red.value = False
        self.rpi.core.a1red.value = False

        self.rpi.core.a2green.value = True
        self.rpi.core.a1green.value = False

        # initialise RTU at boot
        RTU_count = 0
        try:
            db = firebase.put('Telemetry Data/Comms Status/','RTU Count',RTU_count)
        except:
            # if connection unsuccsesful print message
            print("Database Connection Failure...")
            pass


        # start cyclictic loop to keep database updated. Loops every 1 second
        while not self.rpi.exitsignal.wait(1):

            AI_1 = (float(self.rpi.io.AIn_1.value)/10000)                    
            AI_2 = (float(self.rpi.io.AIn_2.value)/10000)
            AI_3 = (float(self.rpi.io.AIn_3.value)/10000)

            scaled_AI1 = (10.0*AI_1)
            scaled_AI2 = (4.0*AI_2)
            scaled_AI3 = (3.0*AI_3)

            now = datetime.now()
            time_stamp = now.strftime("%d/%m/%Y %H:%M:%S")
            hour = now.strftime("%H")

            

            #fuel_check()
            try:
                    var = (firebase.get('Telemetry Data/Setpoints/Sump Level SP','')+1)
                    var = var-1
                    
            except:
                pass
            if scaled_AI2 < var:
                self.rpi.io.DOutBit_1.value = False
                self.rpi.io.DOutBit_2.value = False
            elif scaled_AI2 > var:
                if self.rpi.io.DInBit_2.value == False:
                    if self.rpi.io.DInBit_7.value == True:
                        self.rpi.io.DOutBit_2.value = True
                        
                    else:
                        self.rpi.io.DOutBit_2.value = False
                else:
                    self.rpi.io.DOutBit_2.value = False
            

            self.rpi.io.AOut_1.value = self.rpi.io.AIn_1.value
            self.rpi.io.AOut_2.value = self.rpi.io.AIn_1.value

            
            ############################# HOLDING PUMP 2 BITS FALSE UNTIL SECOND PUMP AVAILABLE
            #self.rpi.io.DOutBit_2.value = False
            #self.rpi.io.DOutBit_5.value = False
            #self.rpi.io.DOutBit_6.value = False

            self.rpi.io.DOutBit_3.value = self.rpi.io.DInBit_1.value


            # RTU count value will be incremented by 1 on each cycle i.e every second
            try:
                RTU_count = (firebase.get('Telemetry Data/Comms Status/RTU Count','')+1)
                #print(RTU_count)
            except:
                #print("FAILED")
                pass

            
            #try:
            #    sms_switch = (firebase.get('Telemetry Data/SMS Toggle/Switch',''))
            #
            #except:
                #print("FAILED")
            #    pass

            
            # keep the scheduled task running
            #schedule.run_pending()
            
            # flicker a1 status light on/off each cycle to indicate programrunning inside this loop, waiting for events.
            self.rpi.core.a2green.value = not self.rpi.core.a2green.value
            self.rpi.core.a1green.value = not self.rpi.core.a1green.value

            # push data to firebase database
            try:
                db = firebase.put('Telemetry Data/Comms Status/','RTU Count',RTU_count)
                db = firebase.put('Telemetry Data/Time Data/','Time Stamp',time_stamp)
                db = firebase.put('Telemetry Data/Time Data/','Hour',hour)
                
                

                db = firebase.put('Telemetry Data/Digital Inputs/','DI-0 : Pump No1 Run',self.rpi.io.DInBit_1.value)
                db = firebase.put('Telemetry Data/Digital Inputs/','DI-1 : Pump No1 Trip',self.rpi.io.DInBit_2.value)
                db = firebase.put('Telemetry Data/Digital Inputs/','DI-2 : Pump House Door',self.rpi.io.DInBit_3.value)
                db = firebase.put('Telemetry Data/Digital Inputs/','DI-3 : Generator House Door',self.rpi.io.DInBit_4.value)
                db = firebase.put('Telemetry Data/Digital Inputs/','DI-4 : Phase Fail Relay (true = OK)',self.rpi.io.DInBit_5.value)
                db = firebase.put('Telemetry Data/Digital Inputs/','DI-5 : Pump No1 Enabled',self.rpi.io.DInBit_6.value)
                db = firebase.put('Telemetry Data/Digital Inputs/','DI-6 : Pump No2 Enabled',self.rpi.io.DInBit_7.value)
                db = firebase.put('Telemetry Data/Digital Inputs/','DI-7 : Pump No2 Enabled',self.rpi.io.DInBit_8.value)
                
                db = firebase.put('Telemetry Data/Digital Outputs/','DO-0 : Pump No1 Start',self.rpi.io.DOutBit_1.value)
                db = firebase.put('Telemetry Data/Digital Outputs/','DO-1 : Pump No1 Start',self.rpi.io.DOutBit_2.value)
                db = firebase.put('Telemetry Data/Digital Outputs/','DO-2 : Pump No1 Run Lamp',self.rpi.io.DOutBit_3.value)
                db = firebase.put('Telemetry Data/Digital Outputs/','DO-3 : Pump No1 Trip Lamp',self.rpi.io.DOutBit_4.value)
                db = firebase.put('Telemetry Data/Digital Outputs/','DO-4 : Pump No2 Run Lamp',self.rpi.io.DOutBit_5.value)
                db = firebase.put('Telemetry Data/Digital Outputs/','DO-5 : Pump No2 Trip Lamp',self.rpi.io.DOutBit_6.value)
                db = firebase.put('Telemetry Data/Digital Outputs/','DO-6 : Mains Healthy Lamp',self.rpi.io.DOutBit_7.value)
                db = firebase.put('Telemetry Data/Digital Outputs/','DO-7 : SPARE',self.rpi.io.DOutBit_8.value)


                db = firebase.put('Telemetry Data/Analog Inputs/','AI-0 : Pressure',scaled_AI1)
                db = firebase.put('Telemetry Data/Analog Inputs/','AI-1 : Sump Level',scaled_AI2)
                db = firebase.put('Telemetry Data/Analog Inputs/','AI-2 : Diesel Tank Level',scaled_AI3)


    
                
            except:
                # if connection unsuccsesful print message
                print("Database Connection Failure...")
                pass    

            # when RTU counter hits 60 it is reset back to zero.    
            if RTU_count >= 60:
                RTU_count = 0
                try:
                    db = firebase.put('Telemetry Data/Comms Status/','RTU Count',RTU_count)
            
                except:
                    pass
 

                
                    

            
if __name__ == "__main__":
    root = MyRevPiApp()
    root.start()
          
