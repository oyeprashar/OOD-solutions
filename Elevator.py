"""
Elevator


Requirements:
	- Elevator can go up or down
	- People can press button from inside and outside

Identifying the entities and services:
	Entities
		1. Elevator
			a. maxCapacity
			b. currentFloor
			c. buttons
			d. door

	Services:
		1. ElevatorService
			+ addRequestedFloor()
				> add the requested floor to the request queue

			+ findNextFloor()
				> return the closed floor from current floor and pop it from request queue
"""
from abc import ABC, abstractmethod


class Elevator:

	def __init__(self, elevatorId):
		self.elevatorId = elevatorId
		self.maxCapacity = None
		self.currentFloor = None
		self.requestQueue = []

	def setMaxCapacity(self, maxCapacity):
		self.maxCapacity = maxCapacity
		return self

	def setCurrentFloor(self, currentFloor):
		self.currentFloor = currentFloor
		return self

	def getCurrentFloor(self):
		return self.currentFloor

	def addToQueue(self, floor):
		self.requestQueue.append(floor)

	def getRequestQueue(self):
		return self.requestQueue


class AbstractElevatorService(ABC):

	@abstractmethod
	def addRequestedFloor(self, elevatorObj, requestedFloor):
		pass

	@abstractmethod
	def getNextFloor(self, elevator):
		pass


class ElevatorService(AbstractElevatorService):

	def addRequestedFloor(self, elevatorObj, requestedFloor):
		elevatorObj.addToQueue(requestedFloor)

	def findClosetFloor(self, elevatorObj):

		requestQueue = elevatorObj.getRequestQueue()

		if len(requestQueue) == 0:
			return

		closetFloorIndex = None

		for i in range(len(requestQueue)):

			if closetFloorIndex is None:
				closetFloorIndex = i

			elif requestQueue[i] < requestQueue[closetFloorIndex]:
				closetFloorIndex = i

		closetFloor = requestQueue[closetFloorIndex]
		requestQueue.pop(closetFloorIndex)

		return closetFloor

	def getNextFloor(self, elevatorObj):
		return self.findClosetFloor(elevatorObj)
