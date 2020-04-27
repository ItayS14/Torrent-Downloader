
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
    
    def __repr__(self):
        return f'TorrentScrapper({self._source})'

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
        :return: a magnet link for the torrent (str)
        """
        raise NotImplementedError

    @property
    def to_list(self):
        """
        Returns tupple with inforamtion about the Torrent to display in the GUI
        """
        return (self._name, self._size, self._se, self._le)

    @property 
    def seeders(self):
        return self._se

    @property
    def info(self):
        return self._link

    def __repr__(self):
        return f'Torrent({self._name}, {self._size}, {self._link}, {self._se}, {self._le}, {self._source})'