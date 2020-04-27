import tkinter
from tkinter import ttk
import os
from scrappers import providers
from scrappers.GeneralScrapper import TorrentScrapper


def popup_msg(msg):
    """
    The function will display popup msg
    :param msg: the text to display in the msg
    """
    popup = tkinter.Tk()
    popup.geometry('200x70')
    popup.wm_title("Error")
    label = tkinter.Label(popup, text=msg)
    label.pack(side='top', fill='x', pady=10)
    button = tkinter.Button(popup, text='Ok', command=lambda : popup.destroy(), width=5, height=1)
    button.pack()
    popup.mainloop()

def search_for_torrents(torrent_name):
    """
    The function will search for torrents and update the gui base on that
    :param torrent_name: the torrent to search
    """   
    # Running over results from all sources
    torrents = []
    try: 
        for provider in providers:
            torrents += provider.get_links(torrent_name)
    except TorrentScrapper.NoResultsFound: # TODO: Change it later to only when execption was thrown in all the providers
        popup_msg('Sorry, no results were found!') 

    global results
    global treeview
    treeview.delete(*treeview.get_children())
    results = sorted(torrents, key= lambda x: x.seeders, reverse=True)
    for torrent in results:
        treeview.insert('', 'end', values=torrent.to_list)


def on_double_click(event):
    """
    the function will handle double clicking
    :param event: this is not being used thats only because it have to be given
    """
    item = treeview.selection()
    if item:
        index = treeview.index(item)
        global results
        os.system(f'start {results[index].info}')


def download_torrent(item):
    """
    The function will download torrent
    :param items: the items chosen on the treeview
    """
    if item:
        index = treeview.index(item[0])
        global results
        os.startfile(results[index].magnet)
    else:
        popup_msg('No item was chosen')

if __name__ == '__main__':
    window = tkinter.Tk()
    window.title('Torrent Downloader')
    window.wm_iconbitmap('icon.ico')
    window.geometry("760x450")
    img = tkinter.PhotoImage(file = 'title.gif')
    img_lbl = tkinter.Label(window, image=img)
    img_lbl.image = img
    img_lbl.pack()
    results =  []
    entry_lbl = tkinter.Label(window, text='Enter name to search:')
    entry = tkinter.Entry(window)
    search_btn = tkinter.Button(window, text='Search', command=lambda:search_for_torrents(entry.get()), height=2, width=10)
    treeview_label = tkinter.Label(window, text='Results:')
    treeview = ttk.Treeview(window, columns=('Name', 'Size', 'Seeders', 'Leechers'), selectmode='browse')
    treeview.bind("<Double-1>", on_double_click) #oppening the link in defult browser when double click on the row in the treeview
    treeview.column('Name', width=500)
    treeview.column('Size', width=70)
    treeview.column('Seeders', width=70)
    treeview.column('Leechers', width=70)
    treeview.heading('Name', text='Name')
    treeview.heading('Size', text='Size')
    treeview.heading('Seeders', text='Seeders')
    treeview.heading('Leechers', text='Leechers')
    treeview['show'] = 'headings'
    download_btn = tkinter.Button(window, text='Download', command=lambda :download_torrent(treeview.selection()), height=2, width=10)
    download_btn.place(x=13, y=400)
    search_btn.place(x=230, y=100)
    entry.place(x=14, y=120, width=200)
    entry_lbl.place(x=10, y=95)
    treeview_label.place(x=10, y=140)
    treeview.place(x=13, y=165)
    window.mainloop()
