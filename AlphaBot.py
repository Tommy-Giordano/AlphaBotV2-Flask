import RPi.GPIO as GPIO
import time

class AlphaBot(object):
	
	def __init__(self,in1=12,in2=13,ena=6,in3=20,in4=21,enb=26):
		self.IN1 = in1
		self.IN2 = in2
		self.IN3 = in3
		self.IN4 = in4
		self.ENA = ena
		self.ENB = enb
  
		self.moving = False
		self.canMoveForward = True
  
		self.DL = 19
		self.DR = 16
  
		self.speed = [50, 50]
  
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		GPIO.setup(self.IN1,GPIO.OUT)
		GPIO.setup(self.IN2,GPIO.OUT)
		GPIO.setup(self.IN3,GPIO.OUT)
		GPIO.setup(self.IN4,GPIO.OUT)
		GPIO.setup(self.ENA,GPIO.OUT)
		GPIO.setup(self.ENB,GPIO.OUT)
  
		# Sesonri Left e Right di luce
		GPIO.setup(self.DL, GPIO.IN, GPIO.PUD_UP)
		GPIO.setup(self.DR, GPIO.IN, GPIO.PUD_UP)
  
		# GPIO.input(DR)
  
		self.PWMA = GPIO.PWM(self.ENA,500)
		self.PWMB = GPIO.PWM(self.ENB,500)
		self.PWMA.start(50)
		self.PWMB.start(50)
		self.stop()
  
	def getSensors(self):
		return (GPIO.input(self.DL),GPIO.input(self.DR)) 
	
	def stop(self):
		print("im STOPPING")
		GPIO.output(self.IN1,GPIO.LOW)
		GPIO.output(self.IN2,GPIO.LOW)
		GPIO.output(self.IN3,GPIO.LOW)
		GPIO.output(self.IN4,GPIO.LOW)
		self.moving = False

	def forwardTime(self, seconds = 0):
		if not self.canMoveForward:
			self.stop()
			return
		print("im moving forward")
		self.setMotor(-self.speed[0], self.speed[1])
		time.sleep(seconds)
		self.stop()
	
	def backwardTime(self, seconds = 0):
		print("im moving forward")
		self.setMotor(self.speed[0], -self.speed[1])
		time.sleep(seconds)
		self.stop()

	def leftTime(self, seconds = 0):
		print("im moving forward")
		self.setMotor(-self.speed[0], -self.speed[1])
		time.sleep(seconds)
		self.stop()

	def rightTime(self, seconds = 0):
		print("im moving forward")
		self.setMotor(self.speed[0], self.speed[1])
		time.sleep(seconds)
		self.stop()

	def forward(self, seconds = 0):
		if not self.canMoveForward:
			self.stop()
			return
		
		if self.moving:
			return
		
		if self.getSensors()[0] == 0 or self.getSensors()[1] == 0:
			return
		
		print("im moving forward")
		# GPIO.output(self.IN1,GPIO.HIGH)
		# GPIO.output(self.IN2,GPIO.LOW)
		# GPIO.output(self.IN3,GPIO.LOW)
		# GPIO.output(self.IN4,GPIO.HIGH)
		self.setMotor(-self.speed[0], self.speed[1])
		self.moving = True
  		# time.sleep(seconds)
		# self.stop()


	def backward(self, seconds = 0):
		if(self.moving):
			return
		print("im moving backward")
		# GPIO.output(self.IN1,GPIO.LOW)
		# GPIO.output(self.IN2,GPIO.HIGH)
		# GPIO.output(self.IN3,GPIO.HIGH)
		# GPIO.output(self.IN4,GPIO.LOW)
		self.setMotor(self.speed[0], -self.speed[1])
		self.moving = True
		# time.sleep(seconds)
		# self.stop()

	def left(self, seconds = 0):
		if(self.moving):
			return
		print("im moving left")
		# GPIO.output(self.IN1,GPIO.LOW)
		# GPIO.output(self.IN2,GPIO.LOW)
		# GPIO.output(self.IN3,GPIO.LOW)
		# GPIO.output(self.IN4,GPIO.HIGH)
		self.setMotor(-self.speed[0], -self.speed[1])
		self.moving = True
  		# time.sleep(seconds)
		# self.stop()

	def right(self, seconds = 0):
		if(self.moving):
			return
		print("im moving right")
		# GPIO.output(self.IN1,GPIO.HIGH)
		# GPIO.output(self.IN2,GPIO.LOW)
		# GPIO.output(self.IN3,GPIO.LOW)
		# GPIO.output(self.IN4,GPIO.LOW)
		self.setMotor(self.speed[0], self.speed[1])
		self.moving = True
		# time.sleep(seconds)
		# self.stop()

				
	def forwardLeft(self):
		if not self.canMoveForward:
			self.stop()
			return
		if self.moving:
			return
		if self.getSensors()[0] == 0 or self.getSensors()[1] == 0:
			return
				
		print("im moving forward TO THE LEFT")
		self.setMotor(self.curvedSpeed[0], self.speed[1])
		self.moving = True
	
	def forwardRight(self):
		if not self.canMoveForward:
			self.stop()
			return
		if self.moving:
			return
		if self.getSensors()[0] == 0 or self.getSensors()[1] == 0:
			return
				
		print("im moving forward TO THE RIGHT")
		self.setMotor(self.speed[0], self.curvedSpeed[1])
		self.moving = True
	
	def backwardLeft(self):
		if self.moving:
			return
		print("im moving backward TO THE LEFT")
		self.setMotor(-self.speed[0], -self.curvedSpeed[1])
		self.moving = True
	
	def backwardRight(self):
		if self.moving:
			return
		print("im moving backward TO THE RIGHT")
		self.setMotor(-self.curvedSpeed[0], -self.speed[1])
		self.moving = True
		

		
	def setPWMA(self,value):
		self.PWMA.ChangeDutyCycle(value)

	def setPWMB(self,value):
		self.PWMB.ChangeDutyCycle(value)	
		
	def setMotor(self, left, right):
		if((right >= 0) and (right <= 100)):
			GPIO.output(self.IN1,GPIO.HIGH)
			GPIO.output(self.IN2,GPIO.LOW)
			self.PWMA.ChangeDutyCycle(right)
		elif((right < 0) and (right >= -100)):
			GPIO.output(self.IN1,GPIO.LOW)
			GPIO.output(self.IN2,GPIO.HIGH)
			self.PWMA.ChangeDutyCycle(0 - right)
		if((left >= 0) and (left <= 100)):
			GPIO.output(self.IN3,GPIO.HIGH)
			GPIO.output(self.IN4,GPIO.LOW)
			self.PWMB.ChangeDutyCycle(left)
		elif((left < 0) and (left >= -100)):
			GPIO.output(self.IN3,GPIO.LOW)
			GPIO.output(self.IN4,GPIO.HIGH)
			self.PWMB.ChangeDutyCycle(0 - left)
	
	def changeSpeed(self, speed):
		self.speed[0] += speed 
		self.speed[1] += speed
  
		self.speed[0] = max(0, min(100, self.speed[0]))
		self.speed[1] = max(0, min(100, self.speed[1]))

class ChillBot(object):
	
	# def __init__(self,in1=7,in2=16,ena=8,in3=14,in4=15,enb=18):
	def __init__(self,in1=26,in2=36,ena=24,in3=8,in4=10,enb=12):
		self.IN1 = in1
		self.IN2 = in2
		self.IN3 = in3
		self.IN4 = in4
		self.ENA = ena
		self.ENB = enb
  
		self.moving = False
		self.canMoveForward = True
  
		self.DL = 19
		self.DR = 16
  
		self.speed = [50, 50]
		self.curvedSpeed = [self.speed[0] * 0.75, self.speed[1] * 0.75]
  
		GPIO.setmode(GPIO.BOARD) #BOARD
		GPIO.setwarnings(True)
		GPIO.setup(self.IN1,GPIO.OUT)
		GPIO.setup(self.IN2,GPIO.OUT)
		GPIO.setup(self.IN3,GPIO.OUT)
		GPIO.setup(self.IN4,GPIO.OUT)
		GPIO.setup(self.ENA,GPIO.OUT)
		GPIO.setup(self.ENB,GPIO.OUT)
  
		# Sesonri Left e Right di luce
		GPIO.setup(self.DL, GPIO.IN, GPIO.PUD_UP)
		GPIO.setup(self.DR, GPIO.IN, GPIO.PUD_UP)
  
		# GPIO.input(DR)
  
		self.PWMA = GPIO.PWM(self.ENA,500)
		self.PWMB = GPIO.PWM(self.ENB,500)
		self.PWMA.start(50)
		self.PWMB.start(50)
		self.stop()
  
	def getSensors(self):
		return (GPIO.input(self.DL),GPIO.input(self.DR)) 
	
	def stop(self):
		print("im STOPPING")
		GPIO.output(self.IN1,GPIO.LOW)
		GPIO.output(self.IN2,GPIO.LOW)
		GPIO.output(self.IN3,GPIO.LOW)
		GPIO.output(self.IN4,GPIO.LOW)
		self.moving = False

	def forwardTime(self, seconds = 0):
		if not self.canMoveForward:
			self.stop()
			return
		print("im moving forward")
		self.setMotor(self.speed[0], self.speed[1])
		time.sleep(seconds)
		self.stop()
	
	def backwardTime(self, seconds = 0):
		print("im moving forward")
		self.setMotor(-self.speed[0], -self.speed[1])
		time.sleep(seconds)
		self.stop()

	def leftTime(self, seconds = 0):
		print("im moving forward")
		self.setMotor(-self.speed[0], self.speed[1])
		time.sleep(seconds)
		self.stop()

	def rightTime(self, seconds = 0):
		print("im moving forward")
		self.setMotor(self.speed[0], -self.speed[1])
		time.sleep(seconds)
		self.stop()

	def forward(self, seconds = 0):
		if not self.canMoveForward:
			self.stop()
			return
		if self.moving:
			return
		if self.getSensors()[0] == 0 or self.getSensors()[1] == 0:
			return
				
		print("im moving forward")
		self.setMotor(self.speed[0], self.speed[1])
		self.moving = True
  		

	def backward(self, seconds = 0):
		if self.moving:
			return
		print("im moving backward")
		self.setMotor(-self.speed[0], -self.speed[1])
		self.moving = True
		

	def left(self, seconds = 0):
		if self.moving:
			return
		print("im moving left")
		self.setMotor(-self.speed[0], self.speed[1])
		self.moving = True
  		
	def right(self, seconds = 0):
		if self.moving:
			return
		print("im moving right")
		self.setMotor(self.speed[0], -self.speed[1])
		self.moving = True
		
	def forwardLeft(self):
		if not self.canMoveForward:
			self.stop()
			return
		if self.moving:
			return
		if self.getSensors()[0] == 0 or self.getSensors()[1] == 0:
			return
				
		print("im moving forward TO THE LEFT")
		self.setMotor(self.curvedSpeed[0], self.speed[1])
		self.moving = True
	
	def forwardRight(self):
		if not self.canMoveForward:
			self.stop()
			return
		if self.moving:
			return
		if self.getSensors()[0] == 0 or self.getSensors()[1] == 0:
			return
				
		print("im moving forward TO THE RIGHT")
		self.setMotor(self.speed[0], self.curvedSpeed[1])
		self.moving = True
	
	def backwardLeft(self):
		if self.moving:
			return
		print("im moving backward TO THE LEFT")
		self.setMotor(-self.speed[0], -self.curvedSpeed[1])
		self.moving = True
	
	def backwardRight(self):
		if self.moving:
			return
		print("im moving backward TO THE RIGHT")
		self.setMotor(-self.curvedSpeed[0], -self.speed[1])
		self.moving = True
		
	def setPWMA(self,value):
		self.PWMA.ChangeDutyCycle(value)

	def setPWMB(self,value):
		self.PWMB.ChangeDutyCycle(value)	
		
	def setMotor(self, left, right):
		if((right >= 0) and (right <= 100)):
			GPIO.output(self.IN1,GPIO.HIGH)
			GPIO.output(self.IN2,GPIO.LOW)
			self.PWMA.ChangeDutyCycle(right)
		elif((right < 0) and (right >= -100)):
			GPIO.output(self.IN1,GPIO.LOW)
			GPIO.output(self.IN2,GPIO.HIGH)
			self.PWMA.ChangeDutyCycle(0 - right)
		if((left >= 0) and (left <= 100)):
			GPIO.output(self.IN3,GPIO.HIGH)
			GPIO.output(self.IN4,GPIO.LOW)
			self.PWMB.ChangeDutyCycle(left)
		elif((left < 0) and (left >= -100)):
			GPIO.output(self.IN3,GPIO.LOW)
			GPIO.output(self.IN4,GPIO.HIGH)
			self.PWMB.ChangeDutyCycle(0 - left)
	
	def changeSpeed(self, speed):
		self.speed[0] += speed 
		self.speed[1] += speed
  
		self.speed[0] = max(0, min(100, self.speed[0]))
		self.speed[1] = max(0, min(100, self.speed[1]))

		self.curvedSpeed = [self.speed[0] * 0.75, self.speed[1] * 0.75]
