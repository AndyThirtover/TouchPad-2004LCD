# MicroPython TouchPad and 2004LCD

## simple_main.py

This project has a simplified version of an LCD library to drive the 20x4 LCDs with I2C backpacks.

It defined four touch pads and shows the no-touch calibrated value for each, and the current value.  With a line for each pad.

It uses uasyncio in a naive way.  Here's initialising the LCD:

`i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)` 
`lcd = LCD2004(i2c, addr=39)`

and here's writing some text of values to the LCD:

`lcd.puts(some_variable,x_pos,y_or_line_number)`

## lcd2004.py

This is the simplified version of the Chinese LCD1602 library.   It has a reduced number of 'if' statements and is generally faster.

## Driving NeoPixels

Turns out the standard import module for MicroPython is a poor implementation giving rise to erroneous colours and flashes.

I used: https://github.com/nickovs/ws2812-SPI as an alternative.  It uses the hardware SPI and drives pin IO13 - Silky Smooth.

## main.py + classes.py

This is what I wanted to do in the first place.  It has better examples of how to use uasyncio with tasks and run_forever.

Essentially, TouchPads become a class of TouchUI with all the plumbing for updating the NeoPixel rings, the LCD and associated circuit actions.
