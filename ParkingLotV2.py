"""
1. Requirement gathering and uses cases

	-> We will assume that the first slot on each floor will be for a truck, the next 2 for bikes, and all the other slots for cars.
	-> The ticket id would be of the following format: <parking_lot_id>_<floor_no>_<slot_no> PR1234_2_5 (denotes 5th slot of 2nd floor of parking lot PR1234)
	1. create_parking_lot
	    Created parking lot with <no_of_floors> floors and <no_of_slots_per_floor> slots per floor
	2. park_vehicle
	    Parked vehicle. Ticket ID: <ticket_id>
	    Print "Parking Lot Full" if slot is not available for that vehicle type.
	3. unpark_vehicle
	    Unparked vehicle with Registration Number: <reg_no> and Color: <color>
	    Print "Invalid Ticket" if ticket is invalid or parking slot is not occupied.
	4. display free_count <vehicle_type>
	    No. of free slots for <vehicle_type> on Floor <floor_no>: <no_of_free_slots>
	    The above will be printed for each floor.
	5. display free_slots <vehicle_type>
	    Free slots for <vehicle_type> on Floor <floor_no>: <comma_separated_values_of_slot_nos>
	    The above will be printed for each floor.
	6. display occupied_slots <vehicle_type>
	    Occupied slots for <vehicle_type> on Floor <floor_no>: <comma_separated_values_of_slot_nos>
	    The above will be printed for each floor.

2. Identifying the entities and services
	
	Enities:
		a. Vehicle
			+ license plate
			+ color

		b. Ticket
			+ id
			+ VehicleObj

		c. ParkingLot
			+ id
			+ grid (levels X slots)

	Services
		a. ParkingLotProcessor
			+ registerParkingLot(self,parkingLotObj)
			+ parkCar(self,VehicleObj) -> puts ticket at that slot and shows the ticket id
			+ unpark(self,regNum)
			+ displayFreeCount(self,VehicleType) --> tells the number of slots available for this type of vehicle at each level
			+ displayFreeSlots(self,VehicleType) --> tells what slots are free for this type of vehicle
			+ displayOccupiedSlots(self,VehicleType) 

3. Designing
4. Refinement
"""

from abc import ABC, abstractmethod

class Vehicle:

	def __init__(self,numberPlate,color):
		self.numberPlate = numberPlate
		self.color = color

	def getNumberPlate(self):
		return self.numberPlate

	def getColor(self):
		return self.color


class Truck(Vehicle):

	def __init__(self,numberPlate,color):
		Vehicle.__init__(self,numberPlate,color)


class Bike(Vehicle):

	def __init__(self,numberPlate,color):
		Vehicle.__init__(self,numberPlate,color)

class Car(Vehicle):

	def __init__(self,numberPlate,color):
		Vehicle.__init__(self,numberPlate,color)


class VehicleFactory:

	def getVehicle(vehicleType,numberPlate,color):

		vehicleType = vehicleType.lower()

		if vehicleType == "truck":
			return Truck(numberPlate,color)

		elif vehicleType == "car":
			return Car(numberPlate,color)
		
		elif vehicleType == "bike":
			return Bike(numberPlate,color)
		
		else:
			raise Exception("Invalid vehicle type")


class Ticket: #  <parking_lot_id>_<floor_no>_<slot_no>

	def __init__(self,ticketId,vehicleObj,level,slot):
		self.ticketId = ticketId
		self.vehicleObj = vehicleObj
		self.level = level
		self.slot = slot

	def getLevelAndSlot(self):
		return self.level,self.slot

	def getTicketId(self):
		return self.ticketId

	def getVehicleObj(self):
		return self.vehicleObj


class ParkingLot:


	def __init__(self,parkingLotId,levels,slots):

		self.parkingLotId = parkingLotId
		self.levels = levels
		self.slots = slots
		self.grid = []
		self.initializeGrid()

	def getParkingLotId(self):
		return self.parkingLotId

	def getGrid(self):
		return self.grid

	def getLevels(self):
		return self.levels

	def getSlots(self):
		return self.slots

	def initializeGrid(self):

		for row in range(self.levels):
			currRow = []

			for col in range(self.slots):
				currRow.append(None)

			self.grid.append(currRow)

class AbstractParkingProcessor(ABC):

	@abstractmethod
	def registerParkingLot(self,parkingLotObj):
		pass

	@abstractmethod
	def parkCar(self,vehicleObj):
		pass

	@abstractmethod
	def unpark(self,regNum):
		pass

	@abstractmethod
	def displayFreeCount(self,VehicleType):
		pass

	@abstractmethod
	def displayFreeSlots(self,VehicleType):
		pass

	@abstractmethod
	def displayOccupiedSlots(self,VehicleType):
		pass


class ParkingProcessor():

	__instance = None
	parkingLotObj = None
	parkedVehiclesDict = {}

	def getInstance():

		if ParkingProcessor.__instance == None:
			ParkingProcessor.__instance = ParkingProcessor()

		return ParkingProcessor.__instance

	def __init__(self):

		if ParkingProcessor.__instance != None:
			raise Exception("The object already exists! Use getInstance() to get the object!")

		ParkingProcessor.__instance = self


	def registerParkingLot(self,parkingLotObj):
		ParkingProcessor.parkingLotObj = parkingLotObj

	def findSpots(self,vehicleType):

		# first slot on each floor will be for a truck, the next 2 for bikes, and all the other slots for cars.
		low = -1
		high = -1

		if vehicleType == "truck":
			low = 0
			high = 0

		elif vehicleType == "bike":
			low = 1
			high = 2

		elif vehicleType == "car":
			low = 3
			high = 3**38

		availableSpots = []

		if low == -1 or high == -1:
			return availableSpots

		availableSpots = []

		grid = ParkingProcessor.parkingLotObj.getGrid()

		for level in range(len(grid)): # we have no condition on the level
			for slot in range(len(grid[0])): # we only have condition on the slot number

				if slot >= low and slot <= high and grid[level][slot] == None:
					availableSpots.append([level,slot])

		return availableSpots

	def isParkingLotRegistered(self):
		return ParkingProcessor.parkingLotObj != None


	def getVehicleType(self,vehicleObj):

		vehicleType = None

		if isinstance(vehicleObj,Truck):
			vehicleType = "truck"

		elif isinstance(vehicleObj,Bike):
			vehicleType = "bike"

		elif isinstance(vehicleObj,Car):
			vehicleType = "Car"

		return vehicleType


	def parkCar(self,vehicleObj):

		"""
		1. Find the first available slot to park the vehicle at
		2. Create a ticket
		3. put ticket at that slot in the grid
		4. put key = regNum value = ticket in parkedVehiclesDict
		"""

		if self.isParkingLotRegistered == False:
			print("No parking lot registered!")
			return

		vehicleType = self.getVehicleType(vehicleObj)

		if vehicleType == None:
			print("Invalid vehcile type")
			return

		availableSpots = self.findSpots(vehicleType)

		if len(availableSpots) == 0:
			print("Parking Lot Full")
			return

		i = availableSpots[0][0]
		j = availableSpots[0][1]

		ticketId = ParkingProcessor.parkingLotObj.getParkingLotId() + "_" + str(i) + "_" + str(j) # <parking_lot_id>_<floor_no>_<slot_no>
		ticket = Ticket(ticketId,vehicleObj,i,j)
		ParkingProcessor.parkingLotObj.getGrid()[i][j] = ticket
		ParkingProcessor.parkedVehiclesDict[vehicleObj.getNumberPlate()] = ticket
		print("Parked vehicle. Ticket ID:",ticketId)


	def unpark(self,regNum):

		if self.isParkingLotRegistered == False:
			print("No parking lot registered!")
			return

		if regNum not in ParkingProcessor.parkedVehiclesDict:
			print("Vehicle with number",regNum,"is not parked with us!")
			return

		ticket = ParkingProcessor.parkedVehiclesDict[regNum]
		i,j = ticket.getLevelAndSlot()
		ParkingProcessor.parkingLotObj.getGrid()[i][j] = None
		ParkingProcessor.parkedVehiclesDict.remove(regNum)
		print("Unparked vehicle with Registration Number:",ticket.getVehicleObj().getNumberPlate(),"and color:",ticket.getVehicleObj().getColor())


	"""
	6. display occupied_slots <vehicle_type>
	    Occupied slots for <vehicle_type> on Floor <floor_no>: <comma_separated_values_of_slot_nos>
	    The above will be printed for each floor.

	@abstractmethod
	def displayFreeCount(self,VehicleType):
		pass

	@abstractmethod
	def displayFreeSlots(self,VehicleType):
		pass

	@abstractmethod
	def displayOccupiedSlots(self,VehicleType):
		pass
	"""

	def displayFreeCount(self,vehicleType):

		availableSpots = self.findSpots(vehicleType)
		for level in range(len(availableSpots)):
			print("No. of free slots for",vehicleType, "on Floor",level,"are =",len(availableSpots[level]))


	def displayFreeSlots(self,vehicleType):
		availableSpots = self.findSpots(vehicleType)

		for level in range(len(availableSpots)):
			print("Free slots for",vehicleType, "on Floor",level,"are =",availableSpots[level])

	def displayOccupiedSlots(self,vehicleType):

		availableSpots = self.findSpots(vehicleType)

		freeLevel = set()
		freeSlot = set()

		for spot in availableSpots:
			freeLevel.add(spot[0])
			freeSlot.add(spot[1])

		grid = ParkingProcessor.parkingLotObj.getGrid()

		for level in range(len(grid)):
			for slot in range(len(grid[0])):

				occupiedSlots = []

				if level not in freeLevel and slot not in freeSlot:
					occupiedSlots.append(slot)

				print("Occupied slots for", vehicleType, "on Floor",level, occupiedSlots)
