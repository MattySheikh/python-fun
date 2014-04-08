import sys
import urllib2
from bs4 import BeautifulSoup
init_url = sys.argv[1]
target = "http://en.wikipedia.org/wiki/Philosophy"
print "Starting at", init_url

class WikiURL(object):
	MAX_HOPS = 100

	def __init__(self, url):
		self.url = url
		self.curr_hops = 0
		self.visited = []
		self.root = "http://en.wikipedia.org"
		if self.testURL(url):
			self.goToURL(url)
		else:
			print "Invalid URL. Please run script with a valid URL"

	def goToURL(self, url):
		if self.curr_hops == self.MAX_HOPS:
			print self.MAX_HOPS, "attempts tried without finding Philosophy page. Please try again"
			return
		self.curr_hops += 1

		# If we've visited it, we're stuck and need to start over
		if url in self.visited:
			print "Got stuck in a loop at", url, "! Please try again"
			return
		else:
			self.visited.append(url)

		# Hooray recursion
		if url == "http://en.wikipedia.org/wiki/Philosophy":
			print "Page found! Took", self.curr_hops, "hops"
			return
		else:
			newURL = self.findURL(url)
			self.goToURL(newURL)

	# Parse the wiki page and grab the first URL we see in a <p> tag
	def findURL(self, url):
		print "Going to", url
		page = urllib2.urlopen(url)
		url = self.parsePage(page)
		return url

	def parsePage(self, page):
		soup = BeautifulSoup(page)
		text = soup.find(id = "mw-content-text")
		p_tags = text.find_all('p')
		for tags in p_tags:
			a_tags = tags.find_all('a', href = True)
			if a_tags[0]['href']:
				return str(self.root) +  str(a_tags[0]['href'])

	# Make sure the first URL we see is a wiki URL
	def testURL(self, url):
		return url.find("http://en.wikipedia.org/wiki/") >= 0

WikiURL(init_url)
