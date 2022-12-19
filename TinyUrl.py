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


class URLshortner(ABC):

	@abstractmethod
	def getShortURL(self, longURL):
		pass

	@abstractmethod
	def getLongURL(self, shortURL):
		pass


class BitLy(URLshortner):

	def __init__(self):
		self.shortToLongUrl = {}

	# we can generate 62^7 = 3.5 Trillion
	def getEncodedString(self, uniqueId):
		char = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
		ans = ""

		while uniqueId > 0:
			ans += char[uniqueId % 62]
			uniqueId //= 62

		return ans

	def getShortURL(self, longURL):

		uniqueId = len(self.shortToLongUrl) + 1
		shortURL = self.getEncodedString(uniqueId)

		self.shortToLongUrl[shortURL] = longURL

		return "bit.yl/" + shortURL

	def getLongURL(self, shortURL):

		uniqueString = shortURL.split('/')[1]

		if uniqueString not in self.shortToLongUrl:
			return shortURL

		return self.shortToLongUrl[uniqueString]


shortner = BitLy()
longUrl = "facebook.com"
shortUrl = shortner.getShortURL(longUrl)
print("shortURL = ", shortUrl)
print("longUrl =", shortner.getLongURL(shortUrl))
