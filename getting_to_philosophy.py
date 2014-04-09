import sys
import requests
from bs4 import BeautifulSoup

class WikiURL(object):
	MAX_HOPS = 100

	def __init__(self, url):
		self.url = url
		self.curr_hops = 0
		self.visited = []
		self.root = "http://en.wikipedia.org"
		self.target = "http://en.wikipedia.org/wiki/Philosophy"
		if self.testURL(url):
			self.goToURL(url)
		else:
			print "Invalid URL. Please run script with a valid Wikipedia URL"

	def goToURL(self, url):
		if self.curr_hops == self.MAX_HOPS:
			print self.MAX_HOPS, "attempts tried without finding Philosophy page. Please try again"
			return

		# If we've visited it, we're stuck and need to start over
		if url in self.visited:
			print "Got stuck in a loop at", url, "! Please try again"
			return
		else:
			self.visited.append(url)

		# Hooray recursion
		if url == self.target:
			print "Page found! Took", self.curr_hops, "hops"
			return
		else:
			self.curr_hops += 1
			newURL = self.findURL(url)
			if not newURL:
				print "No links found on page! Please try again"
				return
			self.goToURL(newURL)

	# Parse the wiki page and grab the first URL we see in a <p> tag
	def findURL(self, url):
		print "Going to", url
		page = requests.get(url).text
		url = self.parsePage(page)
		return url

	def parsePage(self, page):
		soup = BeautifulSoup(page)
		text = soup.find(id = "mw-content-text")
		p_tags = text.find_all('p')
		for tags in p_tags:
			a_tags = tags.find_all('a', href = True)
			for next_a_tag in a_tags:
				curr_tag = next_a_tag['href']
				is_new_page = self.isNewPage(curr_tag)
				if next_a_tag['href'] and is_new_page:
					return str(self.root) + str(next_a_tag['href'])

	# Make sure the URL we see is a wiki URL and not some audo file or bad link
	def testURL(self, url):
		if url.find("http://en.wikipedia.org/wiki/") < 0:
			return False
		return True

	# Ensure we are not clicking on citations
	def isNewPage(self, url):
		is_file = url.find("File:") >= 0
		is_wiki_page = url.find("/wiki/") >= 0
		if url.find("#") == 0 and url.find("/") < 0 or not is_wiki_page or is_file:
			return False
		return True

if len(sys.argv) < 2:
	print "Please insert a starting URL"
else:
	init_url = sys.argv[1]
	print "Starting at", init_url
	WikiURL(init_url)