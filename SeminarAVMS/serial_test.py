import serial


serialInst = serial.Serial()

serialInst.baudrate = 9600
serialInst.port = 'COM3'
serialInst.open()

while True:
	if serialInst.in_waiting:
		packet = serialInst.readline()
		packet = packet.decode('utf8').rstrip()
		packet = packet.split(' ')

		try: 
			red = int(packet[0])
			IR = int(packet[1])
			# print(packet)
			# print(red, type(IR))
			SpO2 = 110 - 25 * red / IR
			print(SpO2)

		except:
			red = packet[0]
			IR = (packet[1])
			print(packet)
			print(red, type(IR))

		

