"""
1. Requirement Gathering

	The system should be able to list down cities where its cinemas are located.
	Upon selecting the city, the system should display the movies released in that particular city to that user.
	Once the user makes his choice of the movie, the system should display the cinemas running that movie and its available shows.
	The user should be able to select the show from a cinema and book their tickets.
	The system should be able to show the user the seating arrangement of the cinema hall.
	The user should be able to select multiple seats according to their choice.
	The user should be able to distinguish between available seats from the booked ones.
	Users should be able to put a hold on the seats for 5/10 minutes before they make a payment to finalize the booking.
	The system should serve the tickets First In First Out manner

2. Identifying the entities and services

	Enities:
		1. MovieHall
			a. Number of rows
			b. Number of columns
			c. grid

		2. CinemaComplex
			a. hashMap : key = timing and value movieHall
			b. city

	After identifying the entities and services, look at the requirements and create a flow on pen and paper before coding

	Services
		1. TicketBookingService
			+ getCities()
			+ getReleasedMovieForCity()
			+ viewSeatingForCinema()
			+ bookTickets()

3. Designing
4. Refining
"""

from abc import ABC, abstractmethod
from collections import defaultdict
import threading


class MovieHall:

	def __init__(self, rows, columns):
		self.rows = rows
		self.columns = columns
		self.grid = []
		self.initializeGrid()

	def getRowsCount(self):
		return self.rows

	def getColumnsCount(self):
		return self.columns

	def initializeGrid(self):
		for i in range(self.rows):
			currRow = []
			for j in range(self.columns):
				currRow.append("empty")
			self.grid.append(currRow)

	def getGrid(self):
		return self.grid

	def printMovieHallSeats(self):

		for row in self.grid:
			print(row)
		print("--------------------------------")


class CinemaComplex:

	def __init__(self, city):
		self.city = city
		self.movies = []
		self.movieAndMovieHallMap = defaultdict(list)

	def addMovieHall(self, movieName, timing, movieHallObj):
		self.movieAndMovieHallMap[movieName].append([timing, movieHallObj])
		self.movies.append(movieName)

	def getTimingAndHallObj(self, movieName):
		return self.movieAndMovieHallMap[movieName]

	def displayTimings(self):
		print("---- Available timings are ----")
		for key in self.movieAndMovieHallMap.keys():
			print(key)
		print("-------------------------------")


class AbstractTicketBookingService(ABC):

	@abstractmethod
	def getCities(self):
		pass

	@abstractmethod
	def bookTicket(self, city, target, timing):
		pass

	@abstractmethod
	def viewAvailableTickets(self, target, city):
		pass


class MovieTicketBookingService(AbstractTicketBookingService):

	def __init__(self):
		self.cityToCinemaComplexMap = {}
		self.cityToMovies = defaultdict(list)
		self.ticketBookingLock = threading.Lock()

	def addCinemaComplex(self, city, cinemaObj):
		self.cityToCinemaComplexMap[city] = cinemaObj

	def getCities(self):

		print("--- Viewing available cities ---")
		for city in self.cityToCinemaComplexMap.keys():
			print(city)
		print("--------------------------------")

	def addReleasedMovie(self, city, movieName):
		self.cityToMovies[city].append(movieName)

	def getReleasedMovies(self, city):

		if city not in self.cityToMovies:
			print("We are not operations in ",city)
			return

		releasedMovies = self.cityToMovies[city]
		print("released movies in", city, "are", releasedMovies)

	def viewAvailableTickets(self, city, movie):

		if city not in self.cityToCinemaComplexMap:
			print("We are not serving in",city)
			return

		complexForCity = self.cityToCinemaComplexMap[city]
		hallId = 0
		timingAndHallObjArr = complexForCity.getTimingAndHallObj(movie)

		for timing, hall in timingAndHallObjArr:

			print("---- HALL ID :", hallId, "TIME SLOT :", timing, " ----")
			hall.printMovieHallSeats()
			hallId += 1

	def bookTicket(self, location, movie, timing):

		self.ticketBookingLock.acquire()
		if location not in self.cityToCinemaComplexMap:
			print("Sorry we are currently not operational at",location)
			return

		if movie not in self.cityToMovies[location]:
			print("Sorry we are not having shows for",movie,"at",location)
			return

		movieComplex = self.cityToCinemaComplexMap[location]
		timingAndHalls = movieComplex.getTimingAndHallObj(movie)
		allHalls = []
		hallId = 0

		for currTiming, currHall in timingAndHalls:
			if currTiming == timing:
				print("--- Showing hall with id =", hallId, "---")
				currHall.printMovieHallSeats()
				allHalls.append(currHall)
				hallId += 1

		targetHallId = int(input("Please enter the hall id in which you would like to make the booking : "))

		if targetHallId < 0 or targetHallId >= len(allHalls):
			print("Invalid input")
			return

		numberOfSeats = int(input("Enter the number of seats you wanna book :"))
		print("Enter", numberOfSeats, "row and cols")
		seats = []

		for _ in range(numberOfSeats):
			i, j = map(int, input().split())
			seats.append([i, j])

		targetHall = allHalls[targetHallId]
		self.blockSeats(seats, targetHall)
		self.ticketBookingLock.release()

	def blockSeats(self, seats, targetHall):
		movieHallGrid = targetHall.getGrid()
		for seat in seats:
			i = seat[0]
			j = seat[1]

			if i < 0 or i >= targetHall.getRowsCount() or j < 0 or j >= targetHall.getColumnsCount():
				print("Invalid seat input")

			elif movieHallGrid[i][j] == "empty":
				movieHallGrid[i][j] = "X"
				print("Ticket booked for seat", seat)
			else:
				print("Seat not available at", seat)


DLF = CinemaComplex("New Delhi")
movieHall1DLF = MovieHall(10, 10)
movieHall2DLF = MovieHall(10, 10)
DLF.addMovieHall("FF8", "6-7", movieHall1DLF)
DLF.addMovieHall("KKRH", "6-7", movieHall2DLF)

Ambience = CinemaComplex("Gurgaon")
movieHall1Ambience = MovieHall(2, 10)
Ambience.addMovieHall("MIB3", "6-7", movieHall1Ambience)


ticketBookingService = MovieTicketBookingService()
ticketBookingService.addReleasedMovie("New Delhi", "FF8")
ticketBookingService.addReleasedMovie("New Delhi", "KKRH")
ticketBookingService.addReleasedMovie("Gurgaon", "MIB3")
ticketBookingService.addCinemaComplex("New Delhi", DLF)
ticketBookingService.addCinemaComplex("Gurgaon", Ambience)

ticketBookingService.bookTicket("New Delhi", "KKRH", "6-7")
# ticketBookingService.getCities()
# ticketBookingService.getReleasedMovies("New Delhi")
# ticketBookingService.getReleasedMovies("Gurgaon")

# ticketBookingService.viewAvailableTickets("New Delhi", "KKRH")































