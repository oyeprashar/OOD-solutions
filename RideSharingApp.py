"""
Identifying entities and services

	Entities:
		1. User
			a. Name
			b. Location
		2. Driver extends User
		3. Rider extends User

	Services
		1. AbstractRideSharingService
		1. RideSharingService implements AbstractRideSharingService
			+ shareCar()
			+ getRide()
			- matchDriverRider()
"""

from abc import ABC, abstractmethod
import threading


class User:

	def __init__(self, name, xCoordinate, yCoordinate):
		self.name = name
		self.location = [xCoordinate, yCoordinate]

	def getName(self):
		return self.name

	def getLocation(self):
		return self.location


class Driver(User):

	def __init__(self, name, xCoordinate, yCoordinate):
		User.__init__(self, name, xCoordinate, yCoordinate)


class Rider(User):

	def __init__(self, name, xCoordinate, yCoordinate):
		User.__init__(self, name, xCoordinate, yCoordinate)


class AbstractRideSharingService(ABC):

	@abstractmethod
	def shareCar(self, driveObj):
		pass

	@abstractmethod
	def getRide(self, riderObj):
		pass

	@abstractmethod
	def matchRide(self, riderObj):
		pass


class RideSharingSevice(AbstractRideSharingService):

	def __init__(self):
		# Alot of work can be done on this structure to make it efficient
		# We can have multiple queues based on location so that we don't have one big queue which is being iterated again
		# and again
		# sorting can be done based on location and then based on time stamp so that TAT is minimized
		self.activeDrivers = []
		self.getRideLock = threading.Lock()

	def shareCar(self, driverObj):
		# this adds the driver to matching queue
		self.activeDrivers.append(driverObj)

	def getRide(self, riderObj):

		with self.getRideLock:
			return self.matchRide(riderObj)


	def matchRide(self, riderObj):

		# Find the closet active driver from the active driver list
		# Removes the driver from the waiting queue
		# Returns the driver details
		pass






