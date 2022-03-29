"""
Pizza Ordering 

1. Requirement gathering and use cases:
    a. User can search a restaurant
    b. User can select a restaurant
    c. User can see the menu of that resturant
    d. Assume all are pizzas in all restaurant
    e. pizza can have type, base size, topping and price depends on the properties --> price is hardcoded, price is calculate based on the propeties
    f. calculate the price of total order


2. Identifying the entities and services

    Entities
    a. restaurant -> location and type and menu // Done
    b. pizza -> base size, topping and price // Done
    c. user -> name, address // Done

    Services
    a. OrderManager -> show menu of a restaurant, show bill for an user 

3. Designing -> can factory be used somewhere? Can we use singleton somewhere?
    >> We can use factory design pattern if we have multiple restaurants to choose from
    >> Services whose not more than one object is needed can be made singleton to memory is not filled with such redundant objects

4. Refine
"""

from abc import ABC, abstractmethod

class Restaurant:

    def __init__(self,name,location,type):
        self.name = name
        self.location = location
        self.type = type
        self.menu = {}

    def getName(self):
        return self.name

    def getLocation(self):
        return self.location

    def getType(self):
        return self.type

    def getMenu(self):
        return self.menu

class Pizza:

    def __init__(self,name,size,topping,price):
        self.name = name
        self.size = size
        self.topping = topping
        self.price = price

    def getName(self):
        return self.name

    def getSize(self):
        return self.size

    def getTopping(self):
        return self.topping

    def getPrice(self):
        return self.price

class User:

    def __init__(self,name,address):
        self.name = name
        self.address = address
        self.order = []

    def getName(self):
        return self.name

    def getAddress(self):
        return self.address

    def addOrder(self,pizza):
        self.order.append(pizza)

    def getOrder(self):
        return self.order

    def checkOut(self):
        self.order = []


class AbstractRestaurantManager(ABC):

    @abstractmethod
    def addRestaurant(self,name,location,type):
        pass

    @abstractmethod
    def addItem(self,restaurantName,ItemName):
        pass

    @abstractmethod
    def getRestaurantObj(self,restaurantName):
        pass

    @abstractmethod
    def viewAllRestaurant(self):
        pass

# this should be singleton
class RestaurantManager(AbstractRestaurantManager):

    __instance = None
    restaurantNameToObject = {}

    def getInstance():
        if RestaurantManager.__instance == None:
            RestaurantManager.__instance = RestaurantManager()

        return RestaurantManager.__instance

    def __init__(self):
        if RestaurantManager.__instance != None:
            raise Exception("Object already exists! Use getInstance method!")
    

    def addRestaurant(self,name,location,type):
        RestaurantManager.restaurantNameToObject[name] = Restaurant(name,location,type)

    def addItem(self,restaurantName,itemName,size,topping,price):
        print("itemName =",itemName)
        restaurantObj = RestaurantManager.restaurantNameToObject[restaurantName]
        restaurantObj.getMenu()[itemName] = Pizza(itemName,size,topping,price)

    def getRestaurantObj(self,restaurantName):
        return RestaurantManager.restaurantNameToObject[restaurantName]

    def viewAllRestaurant(self):

        print("---- AVAILABLE RESTAUNRANTS ARE ----")

        for restaurant in RestaurantManager.restaurantNameToObject:
            print(restaurant)

        print("------------------------------------")


class AbstractOrderManager(ABC):

    @abstractmethod
    def showMenu(self,restaurant):
        pass

    @abstractmethod
    def orderFood(self,restaurant,foodName,user):
        pass

    @abstractmethod
    def showBill(self,user):
        pass



class OrderManager(AbstractOrderManager):

    __instance = None

    @staticmethod
    def getInstance():
        if OrderManager.__instance == None:
            OrderManager.__instance = OrderManager()

        return OrderManager.__instance

    def __init__(self):
        if OrderManager.__instance != None:
            raise Exception("Object already exists! Use getInstance method of class")

    def showMenu(self,restaurant):

        if len(restaurant.getMenu()) == 0:
            print("Sorry no food available at ",restaurant.getName())
            return

        for pizzaName in restaurant.getMenu():
            pizza = restaurant.getMenu()[pizzaName]
            print(pizza.getName(),"with cost = ₹" + str(pizza.getPrice()))

    def orderFood(self,restaurant,foodName,user):

        if foodName not in restaurant.getMenu():
            print(foodName,"is not available at",restaurant.getName())
            return

        foodObj = restaurant.getMenu()[foodName]
        print(foodObj.getName(),"ordered by",user.getName())
        user.addOrder(foodObj)

    def showBill(self,user):

        userOrder = user.getOrder()
        if len(userOrder) == 0:
            print("You order nothing yet!")
            return

        total = 0
        print("--------------------")
        for pizza in userOrder:

            print(pizza.getName(),"with cost = ₹",pizza.getPrice())
            total += pizza.getPrice()

        print("Your total payable amount =",total)
        user.checkOut()
        print("--------------------")


# Processing the resturants
# Creating the restaurant, adding the menu and getting the restaurant object to process further
restaurantManager = RestaurantManager()
restaurantManager.addRestaurant("Pizza Hut","New Delhi","Family")
restaurantManager.addRestaurant("Dominos","New Delhi","Family")
restaurantManager.addRestaurant("Pug 76","New Delhi","Singles")
restaurantManager.addItem("Pizza Hut","Veg Loaded",16,"Paneer",190)
restaurantObj = restaurantManager.getRestaurantObj("Pizza Hut")
restaurantManager.viewAllRestaurant()

# Processing the end user services like ordering the food and checkingout
orderManager = OrderManager()
user = User("Shubham","New Delhi")
orderManager.showMenu(restaurantObj)
orderManager.orderFood(restaurantObj,"Veg Loaded",user)
orderManager.orderFood(restaurantObj,"Non-veg Loaded",user)
orderManager.showBill(user)
orderManager.showBill(user)
