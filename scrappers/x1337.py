from bs4 import BeautifulSoup
import requests
from scrappers.GeneralScrapper import TorrentScrapper, Torrent


class X1337(TorrentScrapper):
    def __init__(self, source):
        super().__init__(source)
    
    def get_links(self, torrent_name):
        """
            The function will get a list of links to torrent pages for the torrent name 
            :param torrent_name: the torrent to download
            :return: dictionary with torrent option names as keys and as value a tupple or none of no links were found
        """
        res = requests.get(f'{self._source}search/{torrent_name}/1/').text
        soup = BeautifulSoup(res, 'lxml')
        
        table = soup.find('table')
        if not table:
            raise TorrentScrapper.NoResultsFound

        return [X1337Torrent.from_tr(tr, self._source) for tr in table.find_all('tr')[1:]]


class X1337Torrent(Torrent):
    def __init__(self, name, size, link, se, le):
        super().__init__(name, size, link, se, le, '1337X')
    
    @classmethod
    def from_tr(cls, tr, source):
        cols = tr.find_all('td')
        link = cols[0].find_all('a')[1]
        return X1337Torrent(
            link.text,
            cols[4].text[:cols[4].text.index(' ') + 3].replace('MB', 'Mb').replace('GB', 'Gb'),
            source[:-1] + link['href'],
            int(cols[1].text),
            int(cols[2].text)
        )

    @property
    def magnet(self):
        soup = BeautifulSoup(requests.get(self._link).text, 'lxml')
        return soup.select_one("a[href*=magnet]")['href']