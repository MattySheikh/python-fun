import sys
import requests
from bs4 import BeautifulSoup

class TGwynn(object):
	def __init__(self):
		url = "http://www.baseball-reference.com/players/g/gwynnto01.shtml"
		print "Going to", url
		page = requests.get(url).text
		soup = BeautifulSoup(page, "html.parser")

		# Find the standard batting table
		standardBattingTable = soup.find("table", { "id": "batting_standard" })

		# Find the table header and all the header names
		tableHeader = standardBattingTable.find("thead").findAll("th")

		# Iterate over each table hearder name
		for index, result in enumerate(tableHeader):
			# Find where the data stat is "G" for games played
			if "data-stat" in result.attrs and result.attrs["data-stat"] == "G":
				# Set at which index we need to look at in each row as that should be where the games are
				gameLogIndex = index

		# Get the actual data in the table now. Since there are hidden minor league rows, we want to
		# look at only the "full" rows
		tableBody = standardBattingTable.find("tbody").findAll("tr", { "class": "full" })

		# Iterate over each non-header row
		for index, tableRow in enumerate(tableBody):
			tableCells = tableRow.findAll("td")
			print "Played", tableCells[gameLogIndex].text, "games in year", (index + 1)


TGwynn()