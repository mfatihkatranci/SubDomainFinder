from tkinter import *
from tkinter import scrolledtext
import requests
import threading

window = Tk()
window.title("Sub Domain Finder")
window.minsize(width=600, height=600)
target_input = "google.com"


# GUI'deki text alanlarını temizle ve güncelle
def clear_outputs():
    find_text.delete("1.0", END)
    unfind_text.delete("1.0", END)


# Subdomain kontrol fonksiyonu (her thread için)
def check_subdomain(word):
    word = word.strip()
    if not word:
        return
    url = "http://" + word + "." + target_input
    try:
        response = requests.get(url, timeout=2)
        if response.status_code == 200:
            find_text.insert(END, f"{url}\n")
        else:
            unfind_text.insert(END, f"{url}\n")
    except requests.RequestException:
        unfind_text.insert(END, f"{url}\n")


# Ana thread fonksiyonu (kullanıcı butona bastığında)
def start_scanning():
    clear_outputs()
    wordlist = text_list.get("1.0", END).splitlines()

    threads = []
    for word in wordlist:
        t = threading.Thread(target=check_subdomain, args=(word,))
        t.start()
        threads.append(t)

    # Tüm threadlerin bitmesini bekle (isteğe bağlı)
    for t in threads:
        t.join()


# GUI elemanları
text_list_label = Label(text="Bulmak İstediğiniz Subdomainleri Ekleyiniz:")
text_list_label.pack(pady=10)

text_list = scrolledtext.ScrolledText(width=30, height=10)
text_list.pack()

my_button = Button(text="Subdomainleri Tara (Threading)",
                   command=lambda: threading.Thread(target=start_scanning).start())
my_button.pack(pady=10)

find_label = Label(text="Bulunan Subdomainler")
find_label.place(x=80, y=250)
find_text = Text(width=30, height=10)
find_text.place(x=30, y=270)

unfind_label = Label(text="Bulunamayan Subdomainler")
unfind_label.place(x=380, y=250)
unfind_text = Text(width=30, height=10)
unfind_text.place(x=330, y=270)

window.mainloop()
