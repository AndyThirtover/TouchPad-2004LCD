# Classes for the TouchPad
import uasyncio

RED = (128,0,0)
GREEN = (0,32,0)
BLUE = (0,0,32)
segment_wait = const(30)


class TouchUI():
	def __init__ (self, touch_pad, line_number, no_touch, np, start_pixel, lcd, action):
		self.touch_pad = touch_pad
		self.line_number = line_number
		self.no_touch = no_touch
		self.trigger = no_touch - 30
		self.np = np
		self.start_pixel = start_pixel
		self.lcd = lcd
		self.action = action
		self.last_state = None
		self.state = False
		print("TouchUI {}, Calibrate: {}  Trigger: {} Start: {}".format(self.line_number, self.no_touch, self.trigger, self.start_pixel))

	def trace(self,ind):
		print("Trace from: {}".format(ind))

	def do_np(self, show_state):
		print("Display: {}".format(True))
		for i in range(12):
			if show_state:
				self.np[self.start_pixel+i] = RED
			else:
				self.np[self.start_pixel+i] = GREEN
			self.np.write()
			await uasyncio.sleep_ms(segment_wait)


	async def run(self):
		# Initial State
		for i in range(12):
			self.np[self.start_pixel+i] = GREEN
		self.np.write()

		while True:
			current = self.touch_pad.read()
			#self.lcd.puts(current,4,self.line_number)  # hardware debug only
			if current < self.trigger:
				if self.state == False:
					self.state = True
					for i in range(12):
						self.np[self.start_pixel+i] = RED
						self.np.write()
						await uasyncio.sleep_ms(segment_wait)
					self.action("Called from: {}".format(self.line_number))
			else:
				if self.state == True:
					self.state = False
					for i in range(12):
						self.np[self.start_pixel+i] = GREEN
						self.np.write()
						await uasyncio.sleep_ms(segment_wait)
			self.last_state = self.state
			await uasyncio.sleep_ms(10)



