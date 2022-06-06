"""
1. Requirement gathering and use cases
	- The system should support the booking of different room types like standard, deluxe, family suite, etc.
	- Guests should be able to search room inventory and book any available room.
	- The system should be able to retrieve information like who book a particular room or what are the rooms booked by a specific customer.
	- The system should allow customers to cancel their booking. Full refund if the cancelation is done before 24 hours of check-in date.
	- The system should be able to send notifications whenever the booking is near check-in or check-out date.
	- The system should maintain a room housekeeping log to keep track of all housekeeping tasks.
	- Any customer should be able to add room services and food items.
	- Customers can ask for different amenities.
	- The customers should be able to pay their bills through credit card, check or cash.

2. Identifying the entities and services
	
	Entities
		a. Room
			+ price
			+ bookingHistory (should store the dates)
			+ currentBooking
			+ roomServiceLog
			+ servicesRequested

		b. Hotel
			+ roomTypeToObject

		c. Customer
			+ name
			+ phoneNumber
			+ bookedRoom

	Services
		a. HotelBooker
			+ customerNumberToRoomDict
			+ viewAllHotels()
			+ viewAllRooms(hotelName)
			+ bookRoom(hotelName,roomType,customerObj,checkin,checkout)
			+ requestSpecialService(customerObj)
			+ getHistoryOfRoom(hotelName,roomType)
			+ getHistoryOfCustomer(customerObj)
			+ cancelBooking(customerObj) -> Full refund if the cancelation is done before 24 hours of check-in date
			+ sendNotification(cutomerObj) -> send notifications whenever the booking is near check-in or check-out date
			+ checkOut(cutomerObj) -> pay bills through credit card, check or cash. 

3. Designing
4. Refinement
"""

from abc import ABC, abstractmethod

class Room:

	def __init__(self,price):
		self.price = price
		self.bookingHistory = []
		self.currentBooking = []
		self.roomServiceLog = []
		self.requestedServices = []

	def getPrice(self):
		return self.price

	def getBookingHistory(self):
		return self.bookingHistory

	def getCurrentBooking(self):
		return self.currentBooking

	def getRoomServiceLog(self):
		return self.roomServiceLog

	def getRequestedServices(self):
		return self.requestedServices

	def addRequestedServices(self,message):
		self.requestedServices.append(message)

class Standard:

	def __init__(self,price):
		Room.__init__(self,price)

class Deluxe:

	def __init__(self,price):
		Room.__init__(self,price)
		
class FamilySuite:

	def __init__(self,price):
		Room.__init__(self,price)

class RoomFactory:

	def __init__(self,roomType,price):

		roomType = roomType.lower()

		if roomType == "standard":
			return Standard(price)

		elif roomType == "deluxe":
			return Deluxe(price)

		elif roomType == "familysuite":
			return FamilySuite(price)

		else:
			raise Exception("Invalid room type!")

class Hotel:

	def __init__(self,name):
		self.name = name
		self.roomTypeToObject {}

	def getName(self):
		return self.name

	def addRoom(self,roomType,roomObj):
		self.roomTypeToObject[roomType].append(roomObj)

	def getRooms(self):
		return self.roomTypeToObject

class AbtractRoomBooker(ABC):

	@abstractmethod
	def viewAllHotels(self):
		pass

	@abstractmethod
	def viewAllRooms(self,hotelName):
		pass

	@abstractmethod
	def bookRoom(self,hotelName,roomType,customerObj,checkin,checkout):
		pass

	@abstractmethod
	def cancelBooking(self,customerObj):
		pass

	@abstractmethod
	def requestSpecialService(self,phoneNumber,message):
		pass

	@abstractmethod
	def getHistoryOfRoom(self,hotelName,roomType):
		pass

	@abstractmethod
	def checkout(self,customerObj):
		pass

class Booking:

	def __init__(self,checkin,checkout,hotelObject,roomObject,customerObj):
		self.checkin = checkin
		self.checkout = checkout
		self.hotelObject = hotelObject
		self.roomObject = roomObject
		self.customerObj = customerObj

	def getCheckinCheckout(self):
		return checkin,checkout

	def getHotelObject(self):
		return self.hotelObject

	def getRoomObject(self):
		return self.roomObject

	def getCustomerObj(self):
		return self.customerObj

class Customer:

	def __init__(self,name,phoneNumber):
		self.name = name
		self.phoneNumber = phoneNumber
		self.currentBooking = None
		self.bookingHistory = []

	def getName(self):
		return self.name

	def getPhoneNumber(self):
		return self.phoneNumber

	def setCurrentBooking(self,bookingObj):

		if self.currentBooking != None:
			self.bookingHistory.append(self.currentBooking)

		self.currentBooking = bookRoom

	def addBookingToHistory(self,bookingObj):
		self.bookingHistory.append(bookingObj)


class RoomBooker(AbstractRoomBooker):

	__instance = None
	hotelNameToObject = {}
	phoneNumberToCustomer = {} # dictionary of customers having active bookings

	def __init__(self):

		if RoomBooker.__instance != None:
			raise Exception("Object already exists! Use getInstance()")

		RoomBooker.__instance = self

	def getInstance():
		if RoomBooker.__instance == None:
			RoomBooker.__instance = RoomBooker()

		return RoomBooker.__instance

	def registerHotel(self,hotelName):
		RoomBooker.hotelNameToObject[hotelName] = Hotel(hotelName)


	def viewAllHotels(self):
		if len(RoomBooker.hotelNameToObject) == 0:
			print("No hotel available")
			return

		for hotelName in RoomBooker.hotelNameToObject:
			print(hotelName)

	def viewAllRooms(self,hotelName):
		
		if hotelName not in RoomBooker.hotelNameToObject:
			print(hotelName,"doesn't not exists!")
			return

		hotelObject = RoomBooker.hotelNameToObject[hotelName]
		rooms = hotelObject.getRooms()

		print(hotelName,"has following rooms with following quanity")
		for room in rooms:
			print("room name:",room.getName(),"quanity :",len(rooms[room]))

	def isClashing(self,checkin,checkout,bookedFrom,bookedTo):

		if (checkin >= bookedFrom and checkin <= bookedTo) or (checkout >= bookedFrom and checkout <= bookedTo):
			return True

		return False

	def bookRoom(self,hotelName,roomType,customerObj,checkin,checkout):
		
		if hotelName not in RoomBooker.hotelNameToObject:
			print(hotelName,"doesn't not exists!")
			return

		hotelObject = RoomBooker.hotelNameToObject[hotelName]
		rooms = hotelObject.getRooms()

		if roomType not in rooms:
			print(roomType,"doesn't exists!")
			return

		roomObject = rooms[roomType]

		if len(roomObject.getCurrentBooking()) > 0:
			for booking in roomObject.getCurrentBooking():
				bookedFrom,bookedTo = booking.getCheckinCheckout

				if self.isClashing(checkin,checkout,bookedFrom,bookedTo) == True:
					print(roomType,"not available in",hotelName,"from",checkin,"to",checkout)
					return

		bookingObj = Booking(checkin,checkout,hotelObject,roomObject,customerObj)
		RoomBooker.phoneNumberToCustomer[customerObj.getPhoneNumber()] = customerObj
		customerObj.setCurrentBooking(bookingObj)

	def cancelBooking(self,phoneNumber):
		
		if phoneNumber not in RoomBooker.phoneNumberToCustomer:
			print("Invalid customer number")
			return

		customerObj = RoomBooker.phoneNumberToCustomer[phoneNumber]
		name = customerObj.getName()
		customerObj.setCurrentBooking(None)
		RoomBooker.phoneNumberToCustomer.remove(phoneNumber)
		print("Canceled successfully for",name)

	def requestSpecialService(self,phoneNumber,message):

		if phoneNumber not in RoomBooker.phoneNumberToCustomer:
			print("Invalid customer number")
			return

		# if customer object is found then there must be a booking for them
		customerObj = RoomBooker.phoneNumberToCustomer[phoneNumber]

		bookingObj = customerObj.getCurrentBooking()[-1]
		roomObj = bookingObj.getRoomObject()
		roomObj.addRequestedServices(message)


	def getHistoryOfRoom(self,hotelName,roomType):
		if hotelName not in RoomBooker.hotelNameToObject:
			print(hotelName,"doesn't not exists!")
			return

		hotelObject = RoomBooker.hotelNameToObject[hotelName]
		rooms = hotelObject.getRooms()

		if roomType not in rooms:
			print(roomType,"doesn't exists!")
			return

		roomObject = rooms[roomType]

		print(roomObject.getName(),"has following active bookings")

		for booking in roomObject.getCurrentBooking:
			checkin,checkout = booking.getCheckinCheckout()
			print("from",checkin,"to",checkout)

		print(roomObject.getName(),"has following old bookings")

		for booking in roomObject.getCurrentBooking:
			checkin,checkout = booking.getBookingHistory()
			print("from",checkin,"to",checkout)


	def checkout(self,customerObj):

		if phoneNumber not in RoomBooker.phoneNumberToCustomer:
			print("Invalid customer number")
			return

		customerObj = RoomBooker.phoneNumberToCustomer[phoneNumber]
		name = customerObj.getName()
		price = customerObj.getCurrentBooking()[-1].getRoomObject().getPrice()
		checkin,checkout = customerObj.getCurrentBooking()[-1].getRoomObject().getCheckinCheckout()
		customerObj.setCurrentBooking(None)
		RoomBooker.phoneNumberToCustomer.remove(phoneNumber)
		days = checkout - checkin
		print("Please pay =",price*days)
