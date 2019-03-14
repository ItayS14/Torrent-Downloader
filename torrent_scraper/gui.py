import tkinter
from tkinter import ttk
import os
import PirateBay
import x1337

def popup_msg(msg):
    """
    The function will display popup msg
    :param msg: the text to display in the msg
    """
    print('trying')
    popup = tkinter.Tk()
    popup.geometry('200x70')
    popup.wm_title("Error")
    label = tkinter.Label(popup, text=msg)
    label.pack(side='top', fill='x', pady=10)
    button = tkinter.Button(popup, text='Ok', command=lambda : popup.destroy(), width=5, height=1)
    button.pack()
    popup.mainloop()

def search_for_torrents(search_torrent):
    """
    The function will search for torrents and update the gui base on that
    :param search_torrent: the torrent to search
    """
    global result_pages
    result_pages = {}
    tpb_resualts = PirateBay.get_torrent_page_links(search_torrent)
    x1337_resualts = x1337.get_torrent_page_links(search_torrent)
    if tpb_resualts:
        result_pages.update(tpb_resualts)
    if x1337_resualts:
        result_pages.update(x1337_resualts)
    global results
    results.delete(*results.get_children())
    if result_pages:
        result_pages_keys = sorted(result_pages.keys(), key=lambda x: int(result_pages[x][2]))[::-1]
        for key in result_pages_keys:
            results.insert('', 'end', values=(key, result_pages[key][1], result_pages[key][2], result_pages[key][3]))
    else:
        popup_msg("No results were found")

def on_double_click(event):
    """
    the function will handle double clicking
    :param event: this is not being used thats only because it have to be given
    """
    for item in results.selection():
        item = results.item(item, 'values')
        if item:
            os.system("start " + result_pages[item[0]][0])
        else:
            popup_msg('Link is invalid')

def download_torrent(items):
    """
    The function will download torrent
    :param items: the items chosen on the treeview
    """
    if items:
        for item in items:
            if not item:
                break
            item = results.item(item, "values")
            magnet_link = PirateBay.get_magnet_from_url(result_pages[item[0]][0]) if result_pages[item[0]][-1] == 'PirateBay' else x1337.get_magnet_from_url(result_pages[item[0]][0])
            if magnet_link:
                os.startfile(magnet_link)
            else:
                popup_msg('Download link is invalid')
    else:
        popup_msg('No item is chosen')

if __name__ == '__main__':
    window = tkinter.Tk()
    window.title('Torrent Downloader')
    window.wm_iconbitmap('icon.ico')
    window.geometry("760x450")
    img = tkinter.PhotoImage(file = 'title.gif')
    img_lbl = tkinter.Label(window, image=img)
    img_lbl.image = img
    img_lbl.pack()
    result_pages = {}
    entry_lbl = tkinter.Label(window, text='Enter name to search:')
    entry = tkinter.Entry(window)
    search_btn = tkinter.Button(window, text='Search', command=lambda:search_for_torrents(entry.get()), height=2, width=10)
    results_label = tkinter.Label(window, text='Results:')
    results = ttk.Treeview(window, columns=('Name', 'Size', 'Seeders', 'Leechers'))
    results.bind("<Double-1>", on_double_click) #oppening the link in defult browser when double click on the row in the treeview
    results.column('Name', width=500)
    results.column('Size', width=70)
    results.column('Seeders', width=70)
    results.column('Leechers', width=70)
    results.heading('Name', text='Name')
    results.heading('Size', text='Size')
    results.heading('Seeders', text='Seeders')
    results.heading('Leechers', text='Leechers')
    results['show'] = 'headings'
    download_btn = tkinter.Button(window, text='Download', command=lambda :download_torrent(results.selection()), height=2, width=10)
    download_btn.place(x=13, y=400)
    search_btn.place(x=230, y=100)
    entry.place(x=14, y=120, width=200)
    entry_lbl.place(x=10, y=95)
    results_label.place(x=10, y=140)
    results.place(x=13, y=165)
    window.mainloop()
