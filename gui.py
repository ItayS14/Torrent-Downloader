import tkinter
from tkinter import ttk, messagebox
import os
from scrappers import providers
from scrappers.GeneralScrapper import TorrentScrapper


# The class represnt the main windows of the app
class Application(tkinter.Frame):
    def __init__(self, master):
        super().__init__(master)
        master.title('Torrent Downloader')
        master.wm_iconbitmap('Data/icon.ico')
        master.geometry('760x450')
    
        img = tkinter.PhotoImage(file= 'Data/title.gif')
        img_lbl = tkinter.Label(master, image=img)
        img_lbl.image = img
        img_lbl.pack()            

        entry_lbl = tkinter.Label(master, text='Enter name to search:')
        entry_lbl.place(x=10, y=95)
        
        self._entry = tkinter.Entry(master)
        self._entry.place(x=14, y=120, width=200)
       
        # Search button that searches for torrents using the providers
        search_btn = tkinter.Button(master, text='Search', command=lambda:self.search_torrents(self._entry.get()), height=2, width=10)
        search_btn.place(x=230, y=100)
        
        treeview_label = tkinter.Label(master, text='Results:')
        treeview_label.place(x=10, y=140)
       
        # Packing the torrent list treeview
        self._treeview = ttk.Treeview(master, columns=('Name', 'Size', 'Seeders', 'Leechers'), selectmode='browse')
        self._treeview.bind("<Double-1>", self.on_double_click) #oppening the link in defult browser when double click on the row in the treeview
        self._treeview.column('Name', width=500)
        self._treeview.column('Size', width=70)
        self._treeview.column('Seeders', width=70)
        self._treeview.column('Leechers', width=70)
        self._treeview.heading('Name', text='Name')
        self._treeview.heading('Size', text='Size')
        self._treeview.heading('Seeders', text='Seeders')
        self._treeview.heading('Leechers', text='Leechers')
        self._treeview['show'] = 'headings'
        self._treeview.place(x=13, y=165)
        
        # The download button, with lambda that downloads the select torrent from the treeview
        download_btn = tkinter.Button(master, text='Download', command= self.download_torrent, height=2, width=10)
        download_btn.place(x=13, y=400)

        # List that holds the current search result list
        self._torrents = []

    def search_torrents(self, torrent_name):
        """
        The function will search for torrents and update the gui base on that
        :param torrent_name: the torrent to search
        """   
        if not torrent_name:
            return
            
        # Running over results from all sources
        self._torrents = []
        try: 
            for provider in providers:
                self._torrents += provider.get_links(torrent_name)
        except TorrentScrapper.NoResultsFound: # TODO: Change it later to only when execption was thrown in all the providers
            messagebox.showerror('Error','Sorry, no results were found!') 

        self._treeview.delete(*self._treeview.get_children())
        self._torrents = sorted(self._torrents, key= lambda x: x.seeders, reverse=True)
        for torrent in self._torrents:
            self._treeview.insert('', 'end', values=torrent.to_list)
    

    def on_double_click(self, _):
        """
        The function will open the webpage of the selected torrent in case of double clicking
        """
        item = self._treeview.selection()
        if item:
            index = self._treeview.index(item)
            os.system(f'start {self._torrents[index].info}')

    def download_torrent(self):
        """
        The function will download the selected torrent
        """
        item = self._treeview.selection()
        if item:
            index = self._treeview.index(item[0])
            os.startfile(self._torrents[index].magnet)


def main():
    root = tkinter.Tk()
    Application(root).pack()
    root.mainloop() 

if __name__ == '__main__':
    main()