from abc import ABC, abstractmethod

class Node:
    def __init__(self,key,value):
        self.key = key
        self.value = value
        self.next = None
        self.prev = None

class Cache(ABC):

    @abstractmethod
    def get(self,key):
        pass

    @abstractmethod
    def insert(self,key,value):
        pass


class LRUCache(Cache):

    __instance = None

    @staticmethod
    def getInstance(capacity):

        if self.__instance == None:
            LRUCache.__instance = LRUCache(capacity)

        return LRUCache.__instance


    def __init__(self, capacity: int):

        if LRUCache.__instance != None:
            raise Exception("Object already exists! Use getInstance method to get the object!")

        self.capacity = capacity
        self.dictionary = {}
        self.head = Node(None,None)
        self.tail = Node(None,None)
        self.head.next = self.tail
        self.tail.prev = self.head

        LRUCache.__instance = self
        
    def moveToFront(self,key):
        
        currNode = self.dictionary[key]
        
        # step1 : remove from the old place
        currNode.prev.next = currNode.next
        currNode.next.prev = currNode.prev
        
        # step2 : add in the front
        currNode.next = self.head.next
        self.head.next.prev = currNode
        self.head.next = currNode
        currNode.prev = self.head
        
    def insert(self,key,value):
        
        currNode = Node(key,value)
        self.dictionary[key] = currNode
        
        currNode.next = self.head.next
        self.head.next.prev = currNode
        self.head.next = currNode
        currNode.prev = self.head
        
    def removeFromLast(self):
        
        currNode = self.tail.prev
        self.dictionary.pop(currNode.key)
        
        currNode.prev.next = currNode.next
        currNode.next.prev = currNode.prev
        
        
    
    def get(self, key: int) -> int:
        
        if key not in self.dictionary:
            return -1
        
        else:
            self.moveToFront(key)
            return self.dictionary[key].value

    def put(self, key: int, value: int) -> None:
        
        if key in self.dictionary:
            self.moveToFront(key)
        
        elif len(self.dictionary) < self.capacity:
            self.insert(key,value)
        
        else:
            self.removeFromLast()
            self.insert(key,value)
       
