import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool
from multiprocessing import cpu_count


"""
def compilePapers():
    error = "The abstract you requested was not found"
    for i in range(1000, 2000):
        url = "https://papers.ssrn.com/sol3/papers.cfm?abstract_id=" + str(i)
        article = quickSoup(url)

        if error not in article.get_text() and article.find('h1') is not None:
            title = article.find('h1').get_text()
            paperList.append(url + "," + title)

"""

linkList = []
for x in range(35000, 1000000):
    linkList.append("https://papers.ssrn.com/sol3/papers.cfm?abstract_id=" + str(x))

paperList = []


def quickSoup(url):
    header = {}
    header['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
    page = requests.get(url, headers=header)
    soup = BeautifulSoup(page.content, 'html.parser')
    return(soup)


def getPaper(url):
    try:
        error = "The abstract you requested was not found"
        article = quickSoup(url)
        if error not in article.get_text() and article.find('h1') is not None:
            title = article.find('h1').get_text()
            paperList.append(url + "," + title)
            return(url + "," + title)
    except Exception as e:
        return(None)


if __name__ == "__main__":
    numWorkers = cpu_count() * 8
    print(numWorkers)
    p = Pool(numWorkers)

    papers = p.map(getPaper, linkList)
    p.terminate()
    p.join()
    writePapers = []
    for paper in papers:
        if paper is not None:
            writePapers.append(paper)
    writeString = "\n".join(writePapers)
    f = open('threadedData.csv', 'a')
    f.write(writeString)
    f.close()

    print("Whew! Done with that!")

# for 3500: 560 seconds with 8 workers, 287 with 32, 309 with 40, 325 with 64