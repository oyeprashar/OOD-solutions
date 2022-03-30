"""
Unix File Search API

1. Requirement gathering and use cases:
	>> Design Unix File Search API to search file with different arguments as "extension", "name", "size" ...
		The design should be maintainable to add new contraints.
	>>Follow up: How would you handle if some contraints should support AND, OR conditionals.

2. Identifying entities and services
	Entities
	1. Directory -> name, children
	2. File -> complete name, fileName, fileExtension, file size

	Services
	1. Filter -> a. minSize b. extension c. fileName // TODO : 1. these filters can be singleton and 2. factory parttern can also be used to get the filters
	2. FileSearcher

3. Design
4. Refinining
"""

from abc import ABC, abstractmethod

class Directory:

	def __init__(self,name):
		self.name = name
		self.children = [] # children can be other directories or files

	def addChild(self,child):
		self.children.append(child)


class File:

	def __init__(self,fullName,size):
		self.fullName = fullName
		self.size = size
		fileName,extension = fullName.split('.')[0],fullName.split('.')[1]
		self.fileName = fileName
		self.extension = extension
		self.children = []

	def getFullName(self):
		return self.fullName

	def getSize(self):
		return self.size

	def getFileName(self):
		return self.fileName

	def getExtention(self):
		return self.extension

# We can have a filterFactory()
class AbstractFilter(ABC):

	@abstractmethod
	def applyFilter(self,file):
		pass

class MinSizeFilter(AbstractFilter):

	def __init__(self,minSize):
		self.minSize = minSize

	def applyFilter(self,file):
		return file.getSize() >= self.minSize

class ExtentionFilter(AbstractFilter):

	def __init__(self,reqExtention):
		self.reqExtention = reqExtention

	def applyFilter(self,file):
		return file.getExtention() == self.reqExtention

class FileNameFilter(AbstractFilter):

	def __init__(self,reqFileName):
		self.reqFileName =reqFileName

	def applyFilter(self,file):
		return file.getFileName() == self.reqFileName

# this is singleton
class FilterFactory:

	__instance = None

	def getInstance():
		if FilterFactory.__instance == None:
			FilterFactory.__instance = FilterFactory()

		return FilterFactory.__instance

	def __init__(self):
		if FilterFactory.__instance != None:
			raise Exception("Object already exists! Use getInstance method!")

		FilterFactory.__instance = self


	def getFilter(self,type,parameter):

		if type == "min size":
			return MinSizeFilter(parameter)

		elif type == "extension":
			return ExtentionFilter(parameter)

		elif type == "file name":
			return FileNameFilter(parameter)

		else:
			print("INVALID TYPE! Select from 1. min size 2. extension 3. file name")
			return

class AbstractFileSearcher(ABC):

	@abstractmethod
	def search(self,rootDir,filterList,operator):
		pass


# this can be singleton
class FileSearcher(AbstractFileSearcher):

	__instance = None

	def getInstance():

		if FileSearcher.__instance == None:
			FileSearcher.__instance = FileSearcher()

		return FileSearcher.__instance

	def __init__(self):
		if FileSearcher.__instance != None:
			raise Exception("Object already exists! Use the getInstance method")

		FileSearcher.__instance = self

	def massFilterApply(self,file,filterList,operator):

		ans = None
		for currFilter in filterList:
			currAns = currFilter.applyFilter(file)

			if ans == None:
				ans = currAns

			if operator == "AND":
				ans = ans and currAns

			elif operator == "OR":
				ans = ans or currAns

		return ans


	def DFS(self,rootDir,filterList,operator,visited,result):

		if isinstance(rootDir,File) and self.massFilterApply(rootDir,filterList,operator) == True:
			result.append(rootDir)
			return

		visited.add(rootDir)

		for children in rootDir.children:
			if children not in visited:
				self.DFS(children,filterList,operator,visited,result)


	def search(self,rootDir,filterList,operator):

		if len(filterList) == 0:
			print("You need to use at least one filter in order to search!")
			return

		if operator != "AND" and operator != "OR":
			print("Invalid operator used!")
			return
		
		result = []
		visited = set()
		self.DFS(rootDir,filterList,operator,visited,result)
		return result


d1 = Directory("Movies")

d2 = Directory("Action")
d3 = Directory("Drama")
d4 = Directory("Comedy")

d5 = Directory("90s")
d6 = Directory("70s")

f1 = File("JamesBond.mp4",1200)
f2 = File("Castaway.mp4",1500)

d1.addChild(d2)
d1.addChild(d3)
d1.addChild(d4)

d2.addChild(d5)
d2.addChild(d6)

d5.addChild(f1)
d6.addChild(f2)

filterFactory = FilterFactory()
filter1 = filterFactory.getFilter("min size",1000)
filter2 = filterFactory.getFilter("file name","JamesBond")
filter3 = filterFactory.getFilter("extension","mp4")

filterList =[MinSizeFilter(1000),ExtentionFilter("mp4"),FileNameFilter("JamesBond")]

filterList =[filter1,filter3]

fileSearcher = FileSearcher()
result = fileSearcher.search(d1,filterList,"AND")

for file in result:
	print(file.getFullName())
