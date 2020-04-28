from bs4 import BeautifulSoup
import requests
from scrappers.GeneralScrapper import TorrentScrapper, Torrent


class PirateBay(TorrentScrapper):
    def __init__(self, source):
        super().__init__(source)

    def get_links(self, torrent_name):
        response = requests.get(f'{self._source}search/{torrent_name}').text # For now not veryfing the ssl certificate
        soup = BeautifulSoup(response, 'lxml')
        
        table = soup.find('table')
        if not table:
            raise TorrentScrapper.NoResultsFound
        
        return [PirateBayTorrent.from_tr(tr) for tr in table.find_all('tr')[1:-1]]

class PirateBayTorrent(Torrent):
    def __init__(self, name, size, link, se, le):
        super().__init__(name, size, link, se, le, 'PirateBay')

    @classmethod
    def from_tr(cls, tr):
        link = tr.find('div').a
        return PirateBayTorrent(
            link.text,
            tr.find('font').text.split(',')[1].replace(' Size ', '').replace('GiB', 'Gb').replace('MiB', 'Mb'),
            link['href'],
            *[int(obj.text) for obj in tr.find_all('td', align='right')]
        )
        
    @property
    def magnet(self):
        page = BeautifulSoup(requests.get(self._link).text, 'lxml')
        return page.find('div', class_= 'download').a['href']
