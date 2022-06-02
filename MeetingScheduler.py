
"""
1. Requirement gathering and use cases
    - A user can book a room on a specific date for a specific time slot (decided by the user)
    - They either specify a meet room by name or book any random available room
    - We can see history of each room
    - We need to see if a room is available to be booked at that date and time or not

2. Identifying entities and services
    Entities
        a. Room
            + name
            + bookings

    Services
        a. RoomBooker
            + BookRoom()
            - isValidBooking()

3. Designing
4. Refining
"""

# We can use the factory design pattern if we know all the types of the Rooms

from abc import ABC, abstractmethod

class Room:

    def __init__(self,name):
        self.name = name
        self.bookings = {}

    def getBookings(self):
        return self.bookings

    def getName(self):
        return self.name


class RoomBooker(ABC):

    @abstractmethod
    def registerRoom(self,name):
        pass

    @abstractmethod
    def bookRoom(self, date, fromTime, toTime, name = None):
        pass



class MeetingRoomBooker(RoomBooker):

    __instance = None

    def getInstance():

        if MeetingRoomBooker.__instance == None:
            MeetingRoomBooker.__instance = MeetingRoomBooker()

        return MeetingRoomBooker.__instance

    def __init__(self):

        if MeetingRoomBooker.__instance != None:
            raise Exception("Object already exists! Use getInstance() to get that object!")

        self.rooms = {}
        MeetingRoomBooker.__instance = self

    def registerRoom(self,name):
        self.rooms[name] = Room(name)

    def bookAnyAvailableRoom(self,date, fromTime, toTime): # -> return False if cannot book any meeting room

        for room in self.rooms:

            if date in room.getBookings():

                for bookedTime in room.getBookings()[date]:

                    if (fromTime >= bookedTime[0] and fromTime <= bookedTime[1]) or  (toTime >= bookedTime[0] and toTime <= bookedTime[1]):
                        return False

                    else:
                        room.getBookings()[date].append([fromTime,toTime])

                        return True

            else:
                room.getBookings()[date].append([fromTime,toTime])
                return True


    def bookByName(date, fromTime, toTime, name): # -> return False if cannot book this particular meeting room

        if name not in self.rooms:
            print("This room does not exists!")
            return

        room = self.rooms[name]

        if date in room.getBookings():

            for bookedTime in room.getBookings()[date]:

                if (fromTime >= bookedTime[0] and fromTime <= bookedTime[1]) or  (toTime >= bookedTime[0] and toTime <= bookedTime[1]):
                    return False

                else:
                    room.getBookings()[date].append([fromTime,toTime])
                    return True

        else:
            room.getBookings()[date].append([fromTime,toTime])
            return True


    def bookRoom(self, date, fromTime, toTime, name = None):

        if name == None:
            isBooked = self.bookAnyAvailableRoom(date, fromTime, toTime)

        else:
            isBooked = self.bookRoom(date, fromTime, toTime, name)


        if isBooked == False:
            print("Sorry we were unable to room meeting room for you!")

        else:
            print("Meeting room was booked successfully from",fromTime,"to",toTime,"on",date)


    def getHistory(self,name):

        if name not in self.rooms:
            print("This room does not exists!")
            return

        bookings = self.rooms[name].getBookings()
        print(bookings)
