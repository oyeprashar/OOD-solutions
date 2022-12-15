"""
Design API rate limiter

Why do we need a rate limiter?
	- If a bot comes and starts calling the API in an infite loop, the server will be bombarded with request and
	 	will get busy serving this bot and all the resources will get occupied so when a genuine user comes, 
	 	they won't be able to use our service.

	- Cost is saved if everything is on cloud and paid per used resource

Approach to design rate limiter:

	- we create queue for users of size N
	- new requests are added to queue only if there is space in this queue
	- FCFS Algo will be implemented on this


Entities:
	User
		- userId

	APIRateLimiter
		- addRequest(userId, request) : returns True/False
		- popRequest(userId): returns the request on basis of FCFS

"""
from abc import ABC, abstractmethod
from collections import defaultdict


class AbstractAPIRateLimiter(ABC):

	@abstractmethod
	def addRequest(self, userId, request):
		pass
	
	@abstractmethod
	def popRequest(self, userId):
		pass


class APIRateLimiter(AbstractAPIRateLimiter):

	def __int__(self, rateLimit):
		self.userIdToQueue = defaultdict(list)
		self.rateLimit = rateLimit

	def addRequest(self, userId, requestObj):

		userQueue = self.userIdToQueue[userId]

		if len(userQueue) < self.rateLimit:
			userQueue.append(requestObj)
			return True

		return False
	
	def popRequest(self, userId):
		userQueue = self.userIdToQueue[userId]
		
		if len(userQueue) == 0:
			return None
		
		return userQueue.pop(0)
		
