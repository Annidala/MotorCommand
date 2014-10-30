#!/usr/bin/python
# -*- coding: utf-8 -*-

import serial


#import convertfrombyte
#import converttobyte

from conversion_MAC140 import *

from  classe_getmotorinfo_v2 import *
from classe_setcommand import *

import time
import datetime


    
#a=In(2).set_mode()
#print a
""" Access to serial port"""
ser=serial.Serial('/dev/ttyUSB1', 19200, timeout=0.1)


""" Initial configuration : """

measuredeffort=[]
measureddistance=[]
measuredtime=[]


''' Reset errors '''
clear_err=In(0).clear_initial_error()
ser.write(clear_err)



'''Set test parameters : velocity, security stops'''
#Displacement rate in mm/min

v=Conversion(5).V_SOLL() # converts displacement rate in mm/min in dimensionless value for the motor 
v_ang=In(v).set_requiredvelocity() # 
ser.write(v_ang) # set the value of the displacement rate in the motor register



''' Test commands'''
#mode position
control_mode=In(2).set_mode()
ser.write(control_mode)

#Test launch
pfinale_=Conversion(80000).displacement_in_counts()
pfinale=In(pfinale_).set_requiredposition()
ser.write(pfinale)
t0_=datetime.datetime.now()
t0=(((((((t0_.year*12)+t0_.month)*30+t0_.day)*24+t0_.hour)*60+t0_.minute)*60+t0_.second)*1000000)+t0_.microsecond


t=0
dt=1

while t<180:
  
  position_= Out(10).get_command() #command sequence for reading register 10 = actual position
  position=ser.write(position_)
  position2=ser.read(100)
  
  t1_=datetime.datetime.now()
  t1=(((((((t1_.year*12)+t1_.month)*30+t1_.day)*24+t1_.hour)*60+t1_.minute)*60+t1_.second)*1000000)+t1_.microsecond
  t=(t1-t0)/1000000.
  measureddistance.append(GetAnswer(position2).get_answer())
  measuredtime.append(t)
  time.sleep(dt)


#test stop
stop= In(0).set_mode()
ser.write(stop)

#results
print measureddistance
print measuredtime
ser.close()
