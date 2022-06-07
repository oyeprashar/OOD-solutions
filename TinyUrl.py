"""
1. Requirement gathering and use cases
	
	- The user can do two things
		a. Give the long url and ask for the tiny url
		b. Give the short url and expect to receive the longer one



	Approach
		1. if we have already generated a short url for the input long url then we return that
		2. id = len(shortUrlToLong)
		3. use the id to generate the shortURL and map the longURL to shortURL
		4. Use shortURL and return the longURL


2. Identifying the entities and services
			

	Services
		a. LinkShortner
			+ getShortURL(self,websiteObject)	
			+ getLongURL(self,websiteObject)

3. Designing
4. Refinement
"""

from abc import ABC, abstractmethod

class AbstractLinkShortner(ABC):

	@abstractmethod
	def getShortURL(self,longUrl):
		pass

	@abstractmethod
	def getLongUrl(self,shortUrl):
		pass


class LinkShortner(AbstractLinkShortner):

	__instance = None
	longToShortUrl = {}
	shortToLongUrl = {}
	baseUrl = "tinyUrl.com/"

	def getInstance():

		if LinkShortner.__instance == None:
			LinkShortner.__instance = LinkShortner()

		return LinkShortner.__instance

	def __init__(self):

		if LinkShortner.__instance != None:
			raise Exception("Object already exists! Please use getInstance() to get the object!")

		LinkShortner.__instance = self

	def getShortURL(self,longUrl):

		if longUrl in LinkShortner.longToShortUrl:
			return self.baseUrl + LinkShortner.longToShortUrl[longUrl]

		chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
		uniqueId = len(LinkShortner.longToShortUrl) + 1 # Cannot be zero since the below function stops when this id becomes 0
		shortUrl = ""

		while uniqueId > 0:
			shortUrl += chars[uniqueId%62]
			uniqueId //= 62

		LinkShortner.longToShortUrl[longUrl] = shortUrl
		LinkShortner.shortToLongUrl[shortUrl] = longUrl

		return LinkShortner.baseUrl + shortUrl

	def getLongUrl(self,shortUrl):

		if len(shortUrl) == 0:
			return "Invalid URL"

		domainParts = shortUrl.split('/')

		if len(domainParts) == 1:
			return "Invalid URL"

		shortCode = domainParts[1]

		if shortCode not in LinkShortner.shortToLongUrl:
			return "404"

		return LinkShortner.shortToLongUrl[shortCode]


shortner = LinkShortner()
print(shortner.getShortURL("google.com"))
print(shortner.getLongUrl("tinyUrl.com/b"))
