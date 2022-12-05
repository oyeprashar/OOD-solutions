"""
1. Requirement gathering

	Restaurant can register themselves.
	User can create, update, delete, get their profiles.
	User can search for the restaurant using restaurant name, city name.
	Restaurant can add, update foodmenu.
	User can see the foodmenu. User can get the food items based on Meal type or Cuisine type.
	User can add/remove items to/from the cart. User can get all the items of the cart.
	User can place or cancel the order. User can get all the orders ordered by him/her.
	User can apply the coupons. User can get the detailed bill containing tax details.
	User can make a payment using different modes of payment - credit card, wallet, etc.
	Delivery boy can get all the deliveries made by him using his ID.
	User can get the order status anytime. Success, Out for Delivery, Delivered, etc.

2. Identifying the entities and services

	Entities
		1. Restaurant
			a. name
			b. menu

		2. Order
			a. orderId
			b. itemList
			c. status (preparing, delivered, onTheWay)

		3. User
			a. name
			b. id
			c. cart

		4. Cart
			a. userId
			b. orderList

		5. FoodItem
			a. name
			b. price
			c. resId

		6. Customer extends User
		7. DeliveryExecutive extends User

	Services:
		RestaurantService
		- Restaurant can register themselves.
		- Restaurant can add, update foodmenu.
		- User can search for the restaurant using restaurant name, city name.
		- User can see the foodmenu. Display food items based on Meal type or Cuisine type.

		ProfileService
			- User can create, update, delete, get their profiles.
			- Delivery boy or user can can get all the deliveries or orders made by him using his Id.

		CartService
			- User can add/remove items to/from the cart. User can get all the items of the cart.
			- User can place or cancel the order. User can get all the orders ordered by him/her.
			- User can apply the coupons. User can get the detailed bill containing tax details.
			- User can get the order status anytime. Success, Out for Delivery, Delivered, etc.

		PaymentService
			- User can make a payment using different modes of payment - credit card, wallet, etc.

3. Design
4. Refine : Patterns and refactoring
"""