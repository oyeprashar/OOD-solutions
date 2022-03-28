"""
----------------
PARKING LOT OOD
----------------
https://workat.tech/machine-coding/practice/design-parking-lot-qm6hwq4wkhp8
https://www.educative.io/courses/grokking-the-object-oriented-design-interview/gxM3gRxmr8Z
https://leetcode.com/discuss/interview-question/124739/Parking-Lot-Design-Using-OO-Design

1. Requirement (what and why) gathering and use cases:
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


2. Identifying the entities and services:
    Entities:
        a. Parking-lot -> the lot itself
        b. Vehicle -> registration number, color
        c. Ticket

    Services:
        a. ParkinglotManager

3. Designing
4. Refinement
"""

from abc import ABC, abstractmethod,abstractproperty

class Vehicle(ABC):


    @property
    @abstractmethod
    def color(self):
        pass

    @property
    @abstractmethod
    def regNum(self):
        pass


    @property
    @abstractmethod
    def type(self):
        pass


class Car(Vehicle):


    def __init__(self,_color,_regNum,_type):
        self._color = _color
        self._regNum = _regNum
        self._type = _type

    def getColor(self):
        return self.color

    def getRegNum(self):
        return self.regNum

    def getType(self):
        return self.type

    @property
    def color(self):
        return self._color

    @property
    def regNum(self):
        return self._regNum


    @property
    def type(self):
        return self._type


class Bike(Vehicle):

    def __init__(self,_color,_regNum,_type):
        self._color = _color
        self._regNum = _regNum
        self._type = _type

    def getColor(self):
        return self.color

    def getRegNum(self):
        return self.regNum

    def getType(self):
        return self.type


    @property
    def color(self):
        return self._color

    @property
    def regNum(self):
        return self._regNum


    @property
    def type(self):
        return self._type

def Truck(Vehicle):

    def __init__(self,_color,_regNum,_type):
        self._color = _color
        self._regNum = _regNum
        self._type = _type

    def getColor(self):
        return self.color

    def getRegNum(self):
        return self.regNum

    def getType(self):
        return self.type


    @property
    def color(self):
        return self._color

    @property
    def regNum(self):
        return self._regNum


    @property
    def type(self):
        return self._type

# this should be singleton pattern
# Factory parttern used
class VehicleFactory:

    __instance = None

    def __init__(self):

        if VehicleFactory.__instance != None:
            raise Exception("Object already exists")

        VehicleFactory.__instance = self

    def getInstance():
        if VehicleFactory.__instance == None:
            VehicleFactory.__instance = VehicleFactory()

        return VehicleFactory.__instance

    def getVehicle(self,type,color,regNum):

        if type == "car":
            return Car(color,regNum,type)

        elif type == "bike":
            return Bike(color,regNum,type)

        elif type == "truck":
            return Truck(color,regNum,type)

        else:
            return None


class ParkingLot:

    parkingLotId = "P1234"

    def __init__(self,numOfFloors,numOfSlots):
        self.numOfSlots = numOfSlots
        self.numOfFloors = numOfFloors
        self.lot = []

        for x in range(numOfFloors):
            currFloor = []
            for y in range(numOfSlots):
                currFloor.append(-1)
            self.lot.append(currFloor)


    def getId(self):
        return self.parkingLotId        

class Ticket:

    def __init__(self,parkingLotId,parkedVehicle,floorIndex,slotIndex):
        self.parkedVehicle = parkedVehicle
        self.floorIndex = floorIndex
        self.slotIndex = slotIndex
        self.id = parkingLotId + '_' + str(floorIndex+1) + '_' + str(slotIndex+1)

    def getId(self):
        return self.id

    def getFloorIndex(self):
        return self.floorIndex

    def getSlotIndex(self):
        return self.slotIndex

class IParkinglotManager(ABC):

    @abstractmethod
    def parkVehicle(self,vehicle,parkingLot):
        pass


    @abstractmethod
    def unparkVehicle(self,ticket,parkingLot):
        pass


    @abstractmethod
    def printFreeSlots(self,parkingLot):
        pass

# this is singleton as parkinglot is an argument and we are not tightly coupled with that class


class ParkinglotManager(IParkinglotManager):

    __instance = None

    def getInstance():
        if ParkinglotManager.__instance == None:
            ParkinglotManager.__instance = ParkinglotManager()

        return ParkinglotManager.__instance


    def __init__(self):

        if ParkinglotManager.__instance != None:
            raise Exception("Object already exists! Use getInstance method to get that Object!")

        self.ticketIdToTicketObj = {}

    def findSpot(self,type,parkingLot):

        for i in range(len(parkingLot.lot)):
            for j in range(len(parkingLot.lot[0])):

                if parkingLot.lot[i][j] == -1:

                    if type == "truck" and j == 0:
                        return True, [i,j]

                    elif type == "bike" and (j == 1 or j == 2):
                        return True, [i,j]

                    elif type == "Car" and j > 2:
                        return True, [i,j]


        return False, [-1,-1]


    def parkVehicle(self,vehicle,parkingLot):

        possible,index = self.findSpot(vehicle.getType(),parkingLot)

        if possible == False:
            print("Sorry! No slot available for vehicle type =",vehicle.getType())
            return

        i = index[0]
        j = index[1]
        ticket = Ticket(parkingLot.getId(),vehicle,i,j)
        parkingLot.lot[i][j] = ticket
        self.ticketIdToTicketObj[ticket.getId()] = ticket

        print("Vehicle successfully parked at floor =",i+1,"slot =",j+1,"with ticked id",ticket.getId())

    def unparkVehicle(self,ticketid,parkingLot):

        if ticketid not in self.ticketIdToTicketObj:
            print("Invalid ticket id")
            return

        ticket = self.ticketIdToTicketObj[ticketid]
        i = ticket.getFloorIndex()
        j = ticket.getSlotIndex()
        parkingLot.lot[i][j] = -1

        print("Vehicle successfully unparked at floor =",i+1,"slot =",j+1,"with ticked id",ticket.getId())


    def printFreeSlots(self,parkingLot):

        for i in range(len(parkingLot.lot)):
            for j in range(len(parkingLot.lot[0])):

                if parkingLot.lot[i][j] == -1:

                    if j == 0:
                        print("Free truck slot at",i,j)

                    elif j == 1 or j == 2:
                        print("Free bike slot at",i,j)

                    elif j > 2:
                        print("Free car slot at",i,j)


parkingLot = ParkingLot(5,5)
parkinglotManager = ParkinglotManager()
vehicleFactory = VehicleFactory()
vehicle = vehicleFactory.getVehicle("bike","red","EX9890")
parkinglotManager.parkVehicle(vehicle,parkingLot)
parkinglotManager.unparkVehicle("P1234_1_2",parkingLot)
parkinglotManager.printFreeSlots(parkingLot)    
