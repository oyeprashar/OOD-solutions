"""
Pizza Ordering

Requirement Gathering
	- A user can order a pizza
	- They can pick different type of crust and toppings

Identifying the entities and services:
	How do we support custom pizza with custom topping and crust?

	Entities:

		1. Pizza
			- pizzaId --> primaryKey
			- toppingId --> foreignKey
			- crustId --> foriengKey
			- size
			- isVeg

		2. Crust
			- crustId --> primaryKey
			- name
			- ingredients

		3. Topping
			- toppingId --> primaryKey
			- name
			- ingredients

		4. User
			- userId --> primaryKey
			- firstName
			- lastName
			- address

		5. Order
			- orderId --> primaryKey
			- userId --> foreignKey
			- pizzaId --> foreignKey
			- isCustom
			- status
			- billAmount

		6. CustomPizza
			- userId --> foreignKey
			- customPizzaId --> primaryKey
			- toppingId --> foreignKey
			- crustId --> foreignKey
			- size

	Services:

		PizzaOrderingService
			+ orderPizza(userId, pizzaId, toppingId, crustId)
			+ cancelPizza(userId, orderId)

		API Design
			- End Point: /order-pizza
			- Type: POST
			- Request: {userId, pizzaId, toppingId, crustId}
			- Response: {success, orderId}

			- End Point: /cancel-order
			- Type: PUT
			- Request: {userId, orderId}
			- Response: {success :T/F}
"""
from abc import ABC, abstractmethod


class Pizza:

	def __init__(self, pizzaId):
		self.pizzaId = pizzaId
		self.toppingId = None
		self.crustId = None
		self.size = None
		self.isVeg = None

	# using builder pattern in pizza
	def setToppingId(self, toppingId):
		self.toppingId = toppingId
		return self

	def setCrustId(self, crustId):
		self.crustId = crustId
		return self

	def setSize(self, size):
		self.size = size
		return self

	def setIsVeg(self, isVeg):
		self.isVeg = isVeg
		return self


class AbstractFoodOrderingService(ABC):

	@abstractmethod
	def placeOrder(self, userId, itemId):
		pass

	@abstractmethod
	def cancelOrder(self, userId, orderId):
		pass


class PizzaOrderingService(AbstractFoodOrderingService):

	# using the singleton pattern here
	__instance = None

	@staticmethod
	def getInstance():

		if PizzaOrderingService.__instance is None:
			PizzaOrderingService.__instance = PizzaOrderingService()

		return PizzaOrderingService.__instance

	def __init__(self):

		if PizzaOrderingService.__instance is not None:
			raise Exception("Object already exits!")

		PizzaOrderingService.__instance = self

	def placeOrder(self, userId, itemId):

		"""
		- We will authenticate that the user is logged in or not
		- acquire lock on the database
		- Generate a orderId
		- Write on the DB
		- return the orderId
		"""

		pass

	def placeCustomOrder(self, userId, crustId, toppingId, size):
		"""
		- save the custom pizza in the customPizza table so that user can view his custom pizzas later also
		- place an order
		"""

	def cancelOrder(self, userId, orderId):
		"""
		Acquire lock on the database and update the status of order in order table as canceled
		"""
		pass


overLoadedPizza = Pizza(9818)
overLoadedPizza.setSize(9).setIsVeg(True).setCrustId(102).setToppingId(55)
