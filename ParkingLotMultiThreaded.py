"""
1. Requirment gathering

    ~ MULTI-THREADING USED ~

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
   
    Also: How to send notifications to users who have parked car - 1 hour later since they entered the parking lot (redis)


2. Identifying entities and services
    Entities:
        1. Parking Lot
            - n * m grid
            - parking lot id

        2. Vehicle
            - ticket 
            - license plate

        3. Ticket
            - floor
            - slot
            - car

    Services:
        1. ParkingLotService

3. Design
4. Refine : usage of factory pattern and singleton
    - Singleton ✅
    - Factory ✅
    - multithreading ✅
"""
from abc import ABC, abstractmethod
import threading

class ParkingLot:

    def __init__(self, numOfSlots, numOfFloors, id):
        self.grid = []
        self.numOfSlots = numOfSlots
        self.numOfFloors = numOfFloors
        self.id = id
        self.parkedVehicles = {}

        for i in range(self.numOfFloors):
            currRow = []
            for j in range(self.numOfSlots):
                currRow.append(-1)
            self.grid.append(currRow)

    def removeVehicle(self, licensePlate):
        self.parkedVehicles.pop(licensePlate, None)

    def addVehicle(self, licensePlate, ticketObj):
        self.parkedVehicles[licensePlate] = ticketObj

    def getParkedVehicle(self):
        return self.parkedVehicles

    def getGrid(self):
        return self.grid

    def getNumOfSlots(self):
        return self.numOfSlots

    def getNumOfFloors(self):
        return self.numOfFloors

    def getId(self):
        return self.id

class Vehicle:

    def __init__(self, color, licensePlate):

        self.color = color 
        self.licensePlate = licensePlate

    def getLicensePlate(self):
        return self.licensePlate

    def getColor(self):
        return self.color

class Car(Vehicle):

    def __init__(self, color, licensePlate):
        Vehicle.__init__(self, color, licensePlate)

class Bike(Vehicle):

    def __init__(self, color, licensePlate):
        Vehicle.__init__(self, color, licensePlate)

class Truck(Vehicle):

    def __init__(self, color, licensePlate):
        Vehicle.__init__(self, color, licensePlate)

class Ticket:
    def __init__(self, floor, slot, vehicleObj):
        self.floor = floor
        self.slot = slot
        self.vehicleObj = vehicleObj
        self.ticketId = ""

    def setTicketId(self, parkingLotId):
        self.ticketId = parkingLotId + "_" + str(self.floor) + "_" + str(self.slot)

    def getFloor(self):
        return self.floor

    def getSlot(self):
        return self.slot

    def getVehicleObj(self):
        return self.vehicleObj

    def getTicketId(self):
        return self.ticketId

class AbstractParkingLotService(ABC):

    @abstractmethod
    def parkVehicle(self, vehicleObj, parkingLotObj):
        pass

    @abstractmethod
    def unparkVehicle(self, licensePlate,parkingLotObj):
        pass

class ParkingLotService(AbstractParkingLotService):

    __instance = None
    __parkingLock = threading.Lock()
    __unparkingLock = threading.Lock()

    @staticmethod
    def getInstance():

        if ParkingLotService.__instance == None:
            ParkingLotService.__instance = ParkingLotService()

        return ParkingLotService.__instance

    def __init__(self):

        if ParkingLotService.__instance != None:
            raise Exception("Object already exists! Use getInstance() to retrieve the method")

        ParkingLotService.__instance = self


    def getRangeByVehicleType(self, vehicleObj):

        if isinstance(vehicleObj, Truck):
            return 0,1
        elif isinstance(vehicleObj, Bike):
            return 1,2
        elif isinstance(vehicleObj, Car):
            return 3,3**38

        return -1,-1

    def findFirstEmptySpotForVehicle(self, vehicleObj, parkingLotObj):
        start, end = self.getRangeByVehicleType(vehicleObj)

        if start == -1 or end == -1:
            raise Exception("Invalid vehicle given!")

        for floor in range(parkingLotObj.getNumOfFloors()):
            for slot in range(parkingLotObj.getNumOfSlots()):

                if parkingLotObj.getGrid()[floor][slot] == -1 and slot >= start and slot <= end:
                    return floor,slot


        return -1,-1

    def parkVehicle(self, vehicleObj, parkingLotObj):

        
        ParkingLotService.__parkingLock.acquire()
        floor,slot = self.findFirstEmptySpotForVehicle(vehicleObj, parkingLotObj)

        if floor == -1 or slot == -1:
            print("No slots are empty!")
            return

        ticket = Ticket(floor, slot, vehicleObj)
        ticket.setTicketId(parkingLotObj.getId())
        parkingLotObj.addVehicle(vehicleObj.getLicensePlate(), ticket)
        print("Parked vehicle. Ticket ID :",ticket.getTicketId())

        ParkingLotService.__parkingLock.release()

    def unparkVehicle(self, licensePlate, parkingLotObj):

        ParkingLotService.__unparkingLock.acquire()

        if licensePlate not in parkingLotObj.getParkedVehicle():
            return "Invalid ticket"

        ticket = parkingLotObj.getParkedVehicle()[licensePlate]
        vehicleObj = ticket.getVehicleObj()
        floor = ticket.getFloor()
        slot = ticket.getSlot()
        parkingLotObj.getGrid()[floor][slot] = -1
        parkingLotObj.removeVehicle(licensePlate)
        print("Park unparked with reg number =",licensePlate,"and color :",vehicleObj.getColor())

        ParkingLotService.__unparkingLock.release()

class VehicleFactory:

    @staticmethod
    def getVehicleObj(vehicleType, licensePlate, color):

        if vehicleType == "car":
            return Car(color, licensePlate)
        elif vehicleType == "bike":
            return Bike(color, licensePlate)
        elif vehicleType == "truck":
            return Truck(color, licensePlate)
        else:
            return None


vehicleObj = VehicleFactory.getVehicleObj("car", "DL-5CE-8980", "Silky Silver")
ambienceMallParkingLot = ParkingLot(5, 5, "HR26")
parkingLotService = ParkingLotService()
parkingLotService.parkVehicle(vehicleObj, ambienceMallParkingLot)
parkingLotService.unparkVehicle("DL-5CE-8980", ambienceMallParkingLot)









