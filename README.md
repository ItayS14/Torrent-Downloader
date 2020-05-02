# Torrent Downloader

Python program that scrapes the internet for magnet links for a torrent



![Screenshot](Data/screenshot.jpg)



### Using

In order to use the program, just enter the torrent name (movie or tv show), i.e - Game of thrones, and the program will take care of the rest.

Once you found the torrent to download from the list, just click download and the download will automatically start with your default Torrent Client.

To use the subtitles script on already downloaded files just type in CMD:

```cmd
python subs.py {path_to_the_file_or_directory}
```

### Installing 

Clone the repository and install the dependencies

```cmd
git clone https://gitlab.com/ItayS14/torrent-downloader
```

Also, make sure that you have a torrent client on your computer.

#### Project dependencies

can be installed via pip.

* beautifulsoup4
* subliminal

#### Additional recommended settings

In some torrent clients it is possible to setup a script to run automatically after download is finished. It is recommended to make the subtitles script run automatically.

**For example** in qBittorrent this setting can be done by:

Settings -> Downloads -> Run external program on torrent completion 

> python {path_to_subs.py}"%F"

