'''
    I2C LCD1602 demo

    Author: shaoziyang
    Date:   2018.2

    http://www.micropython.org.cn

'''
from machine import I2C, Pin
from mp_i2c_lcd1602 import LCD1602
from time import sleep_ms

i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000) 

LCD = LCD1602(i2c, addr=39)

LCD.puts("I2C LCD2004",0,0)
LCD.puts("Whatsup SLAPPERS",2,1)
LCD.puts("Slap Like NOW",4,2)
LCD.puts("Sacrilegious",8,3)
n = 0
while 1:
    LCD.puts(n, 0, 3)
    n += 1
    LCD.backlight(n&1)
    sleep_ms(1000)

