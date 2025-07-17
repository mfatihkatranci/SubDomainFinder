from tkinter import *
from tkinter import scrolledtext
import requests
import threading
from concurrent.futures import ThreadPoolExecutor

window = Tk()
window.title("Sub Domain Finder")
window.minsize(width=600, height=600)
target_input = "google.com"

lock = threading.Lock()  # Tkinter GUI elemanlarına aynı anda yazmamak için

# GUI temizleme
def clear_outputs():
    find_text.delete("1.0", END)
    unfind_text.delete("1.0", END)

# Subdomain kontrol fonksiyonu
def check_subdomain(word):
    word = word.strip()
    if not word:
        return
    url = "http://" + word + "." + target_input
    try:
        response = requests.get(url, timeout=2)
        with lock:
            if response.status_code == 200:
                find_text.insert(END, f"{url}\n")
            else:
                unfind_text.insert(END, f"{url}\n")
    except requests.RequestException:
        with lock:
            unfind_text.insert(END, f"{url}\n")

# Ana tarama fonksiyonu (ThreadPool içinde)
def start_scanning():
    clear_outputs()
    wordlist = text_list.get("1.0", END).splitlines()

    # Maksimum eşzamanlı thread sayısı (örneğin: 20)
    with ThreadPoolExecutor(max_workers=20) as executor:
        executor.map(check_subdomain, wordlist)

# GUI elemanları
text_list_label = Label(text="Bulmak İstediğiniz Subdomainleri Ekleyiniz:")
text_list_label.pack(pady=10)

text_list = scrolledtext.ScrolledText(width=30, height=10)
text_list.pack()

# Buton bir thread içinde çalışıyor (GUI donmasın diye)
my_button = Button(text="Subdomainleri Tara (ThreadPool)", command=lambda: threading.Thread(target=start_scanning).start())
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
