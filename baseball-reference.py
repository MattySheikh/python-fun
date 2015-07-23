import sys
import requests
from bs4 import BeautifulSoup

class TGwynn(object):
	def __init__(self):
		url = "http://www.baseball-reference.com/players/g/gwynnto01.shtml"
		print "Going to", url
		page = requests.get(url).text
		soup = BeautifulSoup(page, "html.parser")
		standardBattingTable = soup.find("table", { "id": "batting_standard" })
		tableHeader = standardBattingTable.find("thead").findAll("th")

		for index, result in enumerate(tableHeader):
			if "data-stat" in result.attrs and result.attrs["data-stat"] == "G":
				gameLogIndex = index

		tableBody = standardBattingTable.find("tbody").findAll("tr", { "class": "full" })

		for index, tableRow in enumerate(tableBody):
			tableCells = tableRow.findAll("td")
			print "Played", tableCells[gameLogIndex].text, "games in year", (index + 1)


TGwynn()