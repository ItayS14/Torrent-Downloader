from ftfy import fix_encoding
import os
from beautifultable import BeautifulTable
import PirateBay
import x1337
from unidecode import unidecode

def print_data(resualt_pages, resualt_pages_keys):
    """
        The function will print the data
        :param resualt_pages: the data scraped from the torrent sites
        :param resualt_pages_keys: sorted by seeders dict keys
    """
    table = BeautifulTable()
    table.column_headers = ["Index", "Name", "Size", "Seeders", "Leechers"]
    [table.append_row([i, fix_encoding(resualt_pages_keys[i]), resualt_pages[resualt_pages_keys[i]][1], resualt_pages[resualt_pages_keys[i]][2], resualt_pages[resualt_pages_keys[i]][3]]) for i in range(len(resualt_pages.keys()))]
    print(table)



def main():
    search_torrent = input('Enter torrent name to search: ')
    resualt_pages = {}
    tpb_resualts = PirateBay.get_torrent_page_links(search_torrent)
    x1337_resualts = x1337.get_torrent_page_links(search_torrent)
    if tpb_resualts:
        resualt_pages.update(tpb_resualts)
    if x1337_resualts:
        resualt_pages.update(x1337_resualts)
    if resualt_pages:
        resualt_pages_keys = sorted(resualt_pages.keys(), key=lambda x: int(resualt_pages[x][2]))[::-1]
        print_data(resualt_pages, resualt_pages_keys)
        while True:
	        index = input("Choose torrent link by index: ")
	        if index.isnumeric() and 0 <= int(index) < len(resualt_pages_keys):
	        	index = int(index)
	        	break
	        print('Invalid index.')
        magnet_link = PirateBay.get_magnet_from_url(resualt_pages[resualt_pages_keys[index]][0]) if resualt_pages[resualt_pages_keys[index]][-1] == 'PirateBay' else x1337.get_magnet_from_url(resualt_pages[resualt_pages_keys[index]][0])
        os.startfile(magnet_link)
    else:
        print("Sorry, no reasults were found.")

if __name__ == '__main__':
    main()
