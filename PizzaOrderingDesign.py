"""
Pizza Ordering

Requirement Gathering
	- A user can order a pizza
	- They can pick different type of crust and toppings

Identifying the entities and services:

	Entities:

		1. Pizza
			- pizzaId --> primaryKey
			- toppingId --> foreignKey
			- crustId --> foriengKey
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
			- status
			- billAmount

	Services:

		PizzaOrderingService
			+ orderPizza(userId, pizzaId, toppingId, crustId)
			+ cancelPizza(userId, orderId)

"""
