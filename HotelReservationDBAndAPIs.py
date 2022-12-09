"""
Let’s design a hotel reservation system similar to Expedia, Kayak, or Booking.com.
We will talk about suitable databases, data modeling, double booking issue, and different ways we can scale the application.

End points that we will be needing
	GET /get-reservation
	POST /make-reservation
	DELETE /cancel-reservation

What all entities will I be needing?
	1. Hotel
	2. Room
	3. User
	4. Reservations

Data Model
	1. Hotel
		hotel_id
		address
		ph_number

	2. Room
		hotel_id
		room_id  # lets assume we have 3 major type of rooms (small, medium and big with id 0, 1, 2)
		room_count

	3. User
		user_id
		first_name
		last_name
		ph_number

	4. Reservations
		user_id (foreign key to access `User` table)
		reservation_id (primary key)
		hotel_id (hotel_id, room_id) foreign key to access `Room` table | hotel_id foreign key to access `Hotel` table
		room_id
		from_date
		to_date

Flow for `POST /make-reservation`:

	REQUEST :
	 	user_id, hotel_id, room_id, from_date, to_date

	FLOW:
		- performs validation checks to see if the input data is valid or not
		- authentication check to see if user_id is logged in or not

		These two are one transaction, and we will lock the row so achieve concurrency and avoid race condition in DB
			- updates the `room_count`
			- makes entry in `reservations` table

	RESPONSE:
		reservation_id


Flow for `DELETE /cancel-reservation`

	REQUEST:
		user_id, reservation_id

	FLOW:
		- performs input validation
		- authentication check to see if user_id is logged in or not

		These are one transactiona, and we take lock on the row to perform them to ensure concurrency
			- find the room_id from the `reservations` table using reservation_id
			- we use (hotel_id, room_id) as foreign key and access room table, increment the count by 1
			- remove the reservation entry from Reservations

	RESPONSE
		True/False

"""

