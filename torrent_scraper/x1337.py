from bs4 import BeautifulSoup
import requests

SOURCE = r'https://1337x.to'
HEADERS = {'User-Agent': 'My User Agent 1.0', 'From': 'youremail@domain.com'} #those are fake user agent becuase the site requries them

def get_torrent_page_links(torrent_name):
    """
        The function will get a list of links to torrent pages for the torrent name 
        :param torrent_name: the torrent to download
        :return: dictionary with torrent option names as keys and as value a tupple or none of no links were found
    """
    torrent_search_page = SOURCE + '/sort-search/' + torrent_name.replace(' ', '+') + '/seeders/desc/1/'
    torrent_search_page = requests.get(torrent_search_page, headers=HEADERS).text
    torrent_dict = {}
    soup = BeautifulSoup(torrent_search_page, 'lxml')
    table = soup.find('table')
    if table is None:
        return None
    for tr in table.find_all('tr')[1:]:
        cols = tr.find_all('td')
        torrent_page_link = cols[0].find_all('a')[1]
        torrent_name = torrent_page_link.text
        href = SOURCE + torrent_page_link['href']
        size = cols[4].text[:cols[4].text.index(' ') + 3].replace('MB', 'Mb').replace('GB', 'Gb')
        torrent_dict[torrent_name] = href, size, cols[1].text, cols[2].text, '1337x'
    return torrent_dict

def get_magnet_from_url(url):
    """
        The function will get a magnet link from url
        :param url: url to get link from (string)
        :return: magnet link (string)
    """
    soup = BeautifulSoup(requests.get(url, headers=HEADERS).text, 'lxml')
    try:
        magnet = soup.find('ul', 'download-links-dontblock btn-wrap-list').find('a')['href']
    except AttributeError:
        return None
    return magnet

