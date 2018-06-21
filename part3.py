# Linying Xie xly
# these should be the only imports you need

import requests
from bs4 import BeautifulSoup

# write your code here
# usage should be python3 part3.py

def main():
	base_url = "http://michigandaily.com"

	html = requests.get(base_url)
	html = html.text

	michigan_soup = BeautifulSoup(html, 'html.parser')
	most_read = michigan_soup.find("div", {"class":"panel-pane pane-mostread"})

	all_titles = most_read.find_all('a')
	urls = [(base_url + url['href']) for url in all_titles]

	authors = []

	for url in urls:
		html = requests.get(url)
		html = html.text

		soup = BeautifulSoup(html, 'html.parser')
		author = soup.find("div", {"class":"link"})

		if author == None:
			no_author = soup.find("div", {"class":"field-item even"})
			no_author = no_author.find("p", {"class":"info"})

			no_author = no_author.text

			authors.append(no_author[3:14])
		else:
			authors.append(author.text)

	print('Michigan Daily -- MOST READ ')

	for i in range(5):
		print(all_titles[i].text)
		print('by ', authors[i])


if __name__=="__main__":
	main()
