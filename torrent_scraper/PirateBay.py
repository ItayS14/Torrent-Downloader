from bs4 import BeautifulSoup
import requests

SOURCE = r'https://piratebays.co/'

def get_torrent_page_links(torrent_name):
    """
        The function will get a list of links to torrent pages for the torrent name 
        :param torrent_name: the torrent to download
        :return: dictionary with torrent option names as keys and as value a tupple or none if no links were found
    """
    torrent_search_page = SOURCE + 's/?q=' + torrent_name.replace(' ', '+') + '&page=0&orderby=99'
    torrent_search_page = requests.get(torrent_search_page).text
    torrent_dict = {}
    soup = BeautifulSoup(torrent_search_page, 'lxml')
    table = soup.find('table')
    if table is None:
        return None
    for tr in table.find_all('tr')[1:]:
        try:
            size = tr.find('font').text.split(',')[1].replace(' Size ', '').replace('GiB', 'Gb').replace('MiB', 'Mb')
        except Exception:
            break
        se_and_le = list(map(lambda object: object.text, tr.find_all('td', align="right")))
        torrent_page_link = tr.find('div').a
        torrent_name = torrent_page_link.text
        href = SOURCE + torrent_page_link['href']
        torrent_dict[torrent_name] = href, size, se_and_le[0], se_and_le[1], 'PirateBay'
    return torrent_dict

def get_magnet_from_url(url):
    """
        The function will get a magnet link from url
        :param url: url to get link from (string)
        :return: magnet link (string)
    """
    torrent_page = BeautifulSoup(requests.get(url).text, 'lxml')
    try:
        magnet_link = torrent_page.find("div", class_='download').a['href']
    except AttributeError:
        return None
    return magnet_link
