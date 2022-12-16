"""
Library Management System

Requirements Gathering

	Books have the following information:
		Unique id
		Title
		Author
		Publication Date
		There can be multiple copies of the same book (book items). Each book item has a unique barcode.

	There can be 2 types of users:

		1. Librarians - Can add and remove books, book items and users, search the catalog
		 	(by title, author or publication date). Can also check out, renew and return books.
		2. General members - can search the catalog (by title, author or publication date), as well as check-out,
		 renew, and return a book.

		Common to all: search by title and publication, checkout, renew, return
		ADMIN: add, remove books and users

		Each user has a unique barcode and a name.

	Also, we have the following limitations:

		1. A member can check out at most 3 books (assume at a simple time)
		2. A member can keep a book at most 20 days.

	The system should be able to calculate the fine for the users who return the books after the expected deadline.

Identifying the entities and services

	Database Models:
		1. Library
			bookId --> primary key
			libraryId
			title
			authorName
			publicationDate
			barCode
			status

		2. User
			userId --> primary key
			name
			isLibrarian
			barCode

		3. IssuedBooks
			bookingId --> primary key
			userId --> foriegn key
			bookId --> foriegn key
			expectedReturnDate
			actualReturnDate
			status (false by default, turns true when we return the book)
			perDayPenality
			paidPenality (0 by default)

	FRONTEND:
		Home page -> lib1, lib2, lib3 options to select a library
		After lib selection -> we show them all the books available to be issued

	Services:

		LibraryManagementSystem
			+ viewBook(libraryId, bookIds)
				-> Since a user can only view 3 books at a time
				-> We pick first 3 books from input array booksIds
				-> For each one of these 3 book Ids
					-> find the details of this bookId in `Library` and save them in array
				-> return these details to the frontend

			+ issueBook(userid, bookId, libraryId)
				-> First we need to authenticate the userId
				-> validate if bookId is there in libraryId
				-> Check status of bookId in `library` and if it is false then return right here
				-> If book is available then change its status to false
				-> Create a bookingId, expectedDate is currDate + 20 days and add entry in `IssuedBooks` table
				-> return the bookingId

			+ returnBook(userId, bookingId)
				-> authenticate the userId
				-> validate that bookingId is associated with this userId (SKIP THIS CHECK IF `isLibrarian` is True)
				-> find the row in `IssuedBooks`
				-> if current date > `expectedReturnDate`, find the difference of days
				-> compute penality by daysDiff * `perDayPenality`
				-> takeThePayment and if the status of this payment is true we proceed forward
				-> Update the status = True, actualReturnDate as today's date, paidPenality with amount paid by user

			+ addBook(userId, bookId, libraryId)
				-> Authenticate that userId has `isLibrarian` True in `User` table
				-> If user is not librarian we return and don't execute

			+ removeBook(userId, bookId, libraryId)
				-> Authenticate that userId has `isLibrarian` True in `User` table
				-> If user is not librarian we return and don't execute

			// search the catalog (by title, author or publication date). Can also check out, renew and return books.

			+ searchByTitle()
			+ searchByPublicationDate()	
			+ renewBook()

"""
