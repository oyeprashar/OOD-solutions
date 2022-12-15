"""
Design ATM

Requirement Gathering:
	- Person can have multiple bank account associated with their userId
	- A person can withdraw money from any one of their account
	- Each account will have a pin associated with it
	- A user cannot withdraw more than Rs. 10,000
	- A user cannot withdraw money more than they have in their account

Identifying the entities and services:
	Database Tables:
		1. User
			a. name
			b. phoneNumber
			c. userId (Primary Key)

		2. BankAccount
			a. userId
			b. accountId
			c. bankName
			d. amount

	Services:

		1. AbstractBankingService
			+ withdrawCash(userId, accountNumber, amount)
"""
from abc import ABC, abstractmethod


class AbstractBankingService(ABC):

	@abstractmethod
	def withdrawCash(self, userId, accountNumber, amount):
		pass


class BankingService(AbstractBankingService):

	def __int__(self):
		self.notes = [[500, 10], [2000, 5]]

	def addNote(self, note, count):
		self.notes.append([note, count])

	def getNotesCount(self, amount):

		requiredNotes = {}

		for note in self.notes:
			requiredNotes[note] = 0

		while amount > 0:

			for i in range(len(self.notes)):

				note = self.notes[i][0]
				availableCount = self.notes[i][1]
				requiredCount = min(amount // note, availableCount)
				self.notes[i][1] -= requiredCount
				requiredNotes[note] = requiredCount
				amount -= (requiredCount * note)

			if amount > 0:
				return False, {}

		return True, requiredNotes
	
	def isAccountAssociated(self, userId, accountId):  # checks if bank account is associated and returns the balance

		"""
		- Use (userId, accountId) to find the row in the `BankAccount` table
		- If row is not found then we will return False, 0
		- If row is found then return True, accountBalance
		"""

	def withdrawCash(self, userId, accountNumber, amount):  # returns the dominations and count that machine will give
		"""
		step1: Check if the accountNumber is associated with this user or not, return 4xx, False
		step2: Check if amount <= 10,000 or user has the input amount in the bank or not, return 4xx, False
		step3: Update the amount in the `BankAccount` table after acquiring the lock to avoid race condition, return 200, True
		"""
