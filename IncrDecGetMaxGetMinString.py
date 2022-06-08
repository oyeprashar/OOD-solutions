"""
1. Requirement gathering and use cases

	Design data-structure(s) to implement these functions in most efficient way:
	Class Solution {
	void incr(String s) {} //increment frequency of a string
	void decr(String s) {} //decrement frequency of a string
	String getMax() {} //return string with maximum frequency
	String getMin() {} //return string with minimum frequency
	}

	Eg.
	incr(“hello”)
	getMax() -> “hello”
	incr(“world”)
	incr(“world”)
	getMax() -> “world”
	decr(“hello”)
	getMin() -> “world”

	The Data structures that we can use
		Hashmap - increment/decrement freq : O(1) | get max/min freq : O(n)


	Question: Can the freq be 0 and stay in dictionary?
		ans: Lets say when the freq touches 0 we remove it from our dictionary

	

2. Identifying the entities and services
3. Designing
4. Refinement

"""

from abc import ABC, abstractmethod
import heapq


class MinItem:

	def __init__(self,value):
		self.value = value
		self.freq = 1

	def incrementFreq(self):
		self.freq += 1

	def decrementFreq(self):
		self.freq -= 1

	def getValue(self):
		return self.value

	def getFreq(self):
		return self.freq

	def __lt__(self,otherObj):
		return self.freq <= otherObj.freq

class MaxItem:

	def __init__(self,value):
		self.value = value
		self.freq = 1

	def incrementFreq(self):
		self.freq += 1

	def decrementFreq(self):
		self.freq -= 1

	def getValue(self):
		return self.value

	def getFreq(self):
		return self.freq

	def __lt__(self,otherObj):
		return self.freq >= otherObj.freq

class AbstractCustomDS:

	@abstractmethod
	def incr(self,string):
		pass

	@abstractmethod
	def decr(self,string):
		pass

	@abstractmethod
	def getMax(self):
		pass

	@abstractmethod
	def getMin(self):
		pass

class CustomDS(AbstractCustomDS):

	def __init__(self):
		self.stringFreq = {}

	# O(1)
	def incr(self,string):

		if string not in self.stringFreq:
			self.stringFreq[string] = 1

		else:
			self.stringFreq[string] += 1

		print("The freq of",string,"is",self.stringFreq[string])

	# O(1)
	def decr(self,string):

		if string not in self.stringFreq:
			print("404")
			return

		self.stringFreq[string] -= 1
		newFreq = self.stringFreq[string]

		if self.stringFreq[string] == 0:
			self.stringFreq.remove(string)

		print("The freq of",string,"is",newFreq)

	# O(n)
	def getMax(self):

		maxFreq = -3**38
		maxString = None

		for string in self.stringFreq:

			if self.stringFreq[string] > maxFreq:
				maxFreq = self.stringFreq[string]
				maxString = string

		return maxString,maxFreq

	# O(n)
	def getMin(self):

	 	minFreq = 3**38
	 	minString = None

	 	for string in self.stringFreq:

	 		if self.stringFreq[string] < minFreq:
	 			minFreq = self.stringFreq[string]
	 			minString = string

	 	return minString,minFreq


dataStructure = CustomDS()
dataStructure.incr("apple")
dataStructure.incr("apple")
dataStructure.incr("apple")
dataStructure.incr("apple")
dataStructure.incr("banana")
dataStructure.incr("banana")
dataStructure.incr("watermelon")
dataStructure.decr("apple")

print(dataStructure.getMax())
print(dataStructure.getMin())
