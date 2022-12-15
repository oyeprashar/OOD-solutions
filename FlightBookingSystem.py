"""
Flight Booking System

Requirement Gathering
	- We can add a flight from a source to destination and time
	- A user can view flights using source and destionation
	- A user can view the occupied and free seats
	- A user can book multiple tickets
	- A user can cancel multiple ticket
	- The system should generate the bill and refund the amount on booking and cancellations

Identifying the Entities and Services:

	- Database Tables
		1. User
			a. userId --> primaryKey, foreignKey
			b. name
			c. phoneNumber

		2. Booking
			a. bookingId --> primaryKey
			b. userId --> foreignKey
			c. flightId --> foreignKey
			d. seatId --> foreignKey
			e. amount
			f. status

		3. Flight
			a. flightId --> primaryKey
			c. source
			d. destination
			f. date

		4. Seat
			a. class
			b. seatId --> primaryKey
			c. flightId
			d. status
			e. cost

	- Services
		1. FlightTicketBookingService
			+ viewFlights(src, dest, date)
				> use (src, dest, date) and find the flightIds
				> use the flightIds to find all the seats associated with it
				> return {flightId, {seat : status}, flightId, {seat : status} ... }

			+ bookFlight(userId, flightId, seatIdsArr)
				> Authenticate if the userId is logged in or not
				> check if the flightId is valid
				> for each seat
					-> If status of seat is True, we create a bookingId, and add an entry to Booking table
						with all the relevant information
					-> Change the status of the seat to False
						
			+ cancelFlight(userId, bookingId)
				> Authenticate if the userId is logged in or not
				> Check if bookingId is made by the userId
				> Change the status of booking in the Booking table to False
				> Set the status of the seat True
"""
