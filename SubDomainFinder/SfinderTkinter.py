from tkinter import *
from tkinter import scrolledtext
import requests

window = Tk()
window.title("Sub Domain Finder")
window.minsize(width=600, height=600)
target_input = "google.com"

# functions
def write_result():
    result_string = text_list.get(1.0, END)
    return result_string

def make_request(url):
    try:
        return requests.get(url)
    except requests.exceptions.ConnectionError:
        pass

    for word in result_string:
        # strip komutu boslukları ve gereksiz karakterleri temizlemek icin kullanılır.
        word = word.strip()
        url = "http://" + word + "." + target_input
        response = make_request(url)
        if response:
            print("Found subdomain --> " + url)





text_list_label = Label(text="Bulmak İstediğiniz Sub domainleri Ekleyiniz")
text_list_label.pack()
text_list_label.config(padx=10, pady=10)
text_list = scrolledtext.ScrolledText(width=30, height=10)
text_list.pack()

result_string = text_list.get(1.0, END)

my_button = Button(text="Ekle", command=write_result)
my_button.pack()
my_button.config(padx=10)

find_label = Label(text="Bulunan Subdomainler")
#find_label.pack(side="left")
find_label.place(x=80, y=250)
find_text = Text(width=30, height=10)
#find_text.insert()
find_text.place(x=30, y=270)

unfind_label = Label(text="Bulunamayan Subdomainler")
#find_label.pack(side="left")
unfind_label.place(x=380, y=250)

unfind_text = Text(width=30, height=10)
unfind_text.place(x=330, y=270)

#subdomain_list = text_list.get(1.0, END)


window.mainloop()
