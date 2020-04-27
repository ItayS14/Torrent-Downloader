
# Any scrapper that is in the project wil be derived from those base classes

#Class That represent a scrapper for a website
class TorrentScrapper:

    # Raised when there are no results at get links function
    class NoResultsFound(Exception): 
        pass

    def __init__(self, source):
        self._source = source

    def get_links(self, torrent_name):
        """
        The function will get links for magnet link pages from a torrent website
        :param torrent_name: the torrent to serch (str)
        :return: list of Torrent for every link 
        """
        raise NotImplementedError


# Class that represnt torrent page
class Torrent:
    def __init__(self, name, size, link, se, le, source):
        self._name = name
        self._size = size
        self._link = link
        self._se = se
        self._le = le
        self._source = source
    
    @property
    def magnet(self):
        """
        The property will fetch the magnet link from the torrent page of the websites
        """
        raise NotImplementedError
