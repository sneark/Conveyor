import tkinter as tk
import threading
import time
import random
from PIL import Image, ImageTk  # wymaga ręcznej instalacji bibloteki "pillow" w interpreterze projektu


# Klasa Przenośnika czyli zasób o który rywalizują wątki(cegły)
class Conveyor:
    def __init__(self, canvas, weight_label, threads_label):
        self.brick1weight = 2  # waga lżejszej cegły
        self.brick2weight = 4  # waga cięższej cegły
        self.current_weight = 0  # aktualna waga
        self.weight_limit = 20  # limit wagowy
        self.weight = 0  # waga poczególnej cegły
        self.semaphore = threading.Semaphore(10)  # semafor
        self.canvas = canvas  # canvas [GUI]
        self.weight_label = weight_label  # label wagi [GUI]
        self.threads_label = threads_label  # label wątków [GUI]
        self.is_running = False  # bool do wątku symulacji
        self.isFull = threading.Event()  # Zdarzenie które służy do sprawdzania czy wątek zablokowany przez limit wagowy może już uzsykać dostęp do przenośnika
        self.priority = threading.Event()  # Zdarzenie zwiększające priorytet wstrzymanym wątkom
        self.width = 50  # zmienna potrzebna do wizualizacji [GUI]
        self.maxOfThreads = 10  # maksymalna liczba zatrzymanych wątków
        self.currentNumofThreads = 0  # aktulana liczba wstrzymanych wątków
        self.queue = [1000]  # tablica ID do zniwelowania zagłodzenia

    # Metoda add_brick wywoływana przy tworzenia wątku cegły. Sprawdza limit wagowy dodaje wage do licznika odpala metody rysowania a później usuwania
    # Jak nie spełnia limitu wagowego to wątek czeka aż będzie miejsce po czym rekurencyjnie wywołuje funkcje
    def add_brick(self, weight, ID, check):
        # print(self.queue)
        if self.queue:
            if ID != min(self.queue) and check == 1:  # zapobiega zagłodzeniu wątków w kolejce
                if self.queue[0] == 1000:
                    self.queue.remove(1000)
                if ID in self.queue[1:3]:
                    time.sleep(1)
                else:
                    time.sleep(2)
        if self.currentNumofThreads >= 5 and check == 1:
            self.priority.set()
        if self.current_weight + weight <= self.weight_limit:
            with self.semaphore:
                if check == 1:
                    self.queue.remove(ID)
                    self.currentNumofThreads -= 1
                    self.update_threads_label()
                self.current_weight += weight
                self.update_weight_label()
                print(f'Dodano cegle {ID} o wadze {weight}\n')
                brick_id = self.draw_brick(weight, check)
                self.remove_brick(brick_id, weight, ID)
        elif self.current_weight + weight > self.weight_limit:
            if check == 0:
                self.queue.append(ID)
                self.currentNumofThreads += 1
                # print(f"CEGŁA NR: {ID} Z WAGĄ: {weight} jest wstrzymana\n")
                self.update_threads_label()
            local_weight = weight
            self.weight = weight
            local_ID = ID
            self.isFull.wait()
            self.isFull.clear()
            time.sleep(random.uniform(0.1, 1))
            self.add_brick(local_weight, local_ID, 1)

    # Usuwa cegłe i odejmuje wagę z licznika
    def remove_brick(self, brick_id, weight, ID):
        print(f'Usunieto cegle {ID} o wadze {weight}\n')
        self.current_weight -= weight
        self.update_weight_label()
        brick_id.destroy()
        self.isFull.set()

    # [GUI] Cegły są rysowane obok siebie co 75px, tworzone labela z odpowiednim .png wywołanie funkcji move_brick
    def draw_brick(self, weight, check):
        if self.width <= 800:
            self.width += 75
        else:
            self.width = 50

        if weight == self.brick1weight:
            brick_id = tk.Label(image=brick2kg, borderwidth=0)
        else:
            brick_id = tk.Label(image=brick4kg, borderwidth=0)
        self.move_brick(brick_id, weight, check)
        return brick_id

    # [GUI] Ruch cegieł
    def move_brick(self, brick_id, weight, check):
        height = 700
        width = self.width
        for i in range(0, 640):
            brick_id.place_configure(x=width, y=height)
            height -= 1
            time.sleep(0.02)

    # [GUI] funkcje do updatu labela który wyświetla wagę
    def update_weight_label(self):
        # print(f"AKTUALNA WAGA: {self.current_weight} kg")
        self.weight_label.config(text=f"Aktualna waga: {self.current_weight} kg\n")

    def update_threads_label(self):
        self.threads_label.config(text=f"Kolejka: {self.currentNumofThreads}")

    # Funkcją w której tworzone są wątki cegieł
    def simulate_conveyor(self):
        i = 1
        while self.is_running:
            self.update_threads_label()
            self.update_weight_label()
            self.canvas.update()
            if self.priority.is_set():
                time.sleep(3)
                self.priority.clear()
            if self.currentNumofThreads < 10:
                brick_weight = random.choice([self.brick1weight, self.brick2weight])
                threading.Thread(target=self.add_brick, args=[brick_weight, i, 0]).start()
                i += 1
                time.sleep(1)


# Start symulacji po naciśnieciu przycisku, tworzony wątek symulacji
def start_simulation(conveyor, max, sbrick, bbrick, check):
    try:
        conveyor.weight_limit = int(max)
        conveyor.brick1weight = int(sbrick)
        conveyor.brick2weight = int(bbrick)
        conveyor.semaphore = threading.Semaphore(int(max) // int(sbrick))
    except ValueError:
        print("Podaj poprawne wartości!")
    if not conveyor.is_running and check == 1:
        canvas.delete("all")  # Czyszczenie canvas przed rozpoczęciem nowej symulacji
        conveyor.is_running = True
        conveyor.simulation_thread = threading.Thread(target=conveyor.simulate_conveyor, daemon=True)
        conveyor.simulation_thread.start()


def delete_simulation(conveyor):
    if conveyor.is_running:
        conveyor.is_running = False
        conveyor.simulation_thread.join()
        root.destroy()


def freeze_simulation():
    time.sleep(7)


# [GUI] tworzenia okna, labelów, przycisków, dodawanie zdjęć itd.
root = tk.Tk()
root.geometry("1000x1000")
root.title("Conveyor")
root.config(background="black")
canvas = tk.Canvas(root, width=1000, height=1000, bg='black', bd=2, highlightthickness=0)
canvas.pack()

start_button = tk.Button(root, text="ZACZNIJ SYMULACJE",
                         command=lambda: start_simulation(conveyor, e1.get(), e2.get(), e3.get(), 1))
start_button.config(activebackground="green", bd=4, font=('Cooper Black', 14), background="black", foreground="green",
                    borderwidth=0)
start_button.place_configure(x=10, y=800)

stop_button = tk.Button(root, text="ZATRZYMAJ SYMULACJE", command=lambda: freeze_simulation())
stop_button.config(activebackground="green", bd=4, font=('Cooper Black', 12), background="black", foreground="white",
                   borderwidth=0)
stop_button.place_configure(x=400, y=950)

freeze_button = tk.Button(root, text="ZAKONCZ SYMULACJE", command=lambda: delete_simulation(conveyor))
freeze_button.config(activebackground="green", bd=4, font=('Cooper Black', 14), background="black", foreground="red",
                     borderwidth=0)
freeze_button.place_configure(x=740, y=800)

brick2kg = ImageTk.PhotoImage(Image.open('./Textures/brick2.png'))
brick4kg = ImageTk.PhotoImage(Image.open("./Textures/brick4.png"))
convimg = ImageTk.PhotoImage(Image.open("./Textures/conveyor.png"))

conv = tk.Label(image=convimg, borderwidth=0)
conv.place_configure(x=0, y=0)

weight_label = tk.Label(root, text="AKTUALNA WAGA: 0 kg", font=('Cooper Black', 18), background="black",
                        foreground="white")
weight_label.place_configure(x=370, y=10)

threads_label = tk.Label(root, text="Kolejka: 0 ", font=('Cooper Black', 18), background="black", foreground="white")
threads_label.place_configure(x=800, y=10)

maxweight = tk.Label(root, text="Podaj maksymalna wage:", font=('Cooper Black', 14), background="black",
                     foreground="white")
maxweight.place_configure(x=370, y=800)

e1 = tk.Entry(root, font=('Cooper Black', 14), width=2)
e1.place_configure(x=650, y=800)

smaller = tk.Label(root, text="Podaj wage mniejszej cegly:", font=('Cooper Black', 14), background="black",
                   foreground="white")
smaller.place_configure(x=370, y=825)

e2 = tk.Entry(root, font=('Cooper Black', 14), width=2)
e2.place_configure(x=650, y=825)

bigger = tk.Label(root, text="Podaj wage wiekszej cegly:", font=('Cooper Black', 14), background="black",
                  foreground="white")
bigger.place_configure(x=370, y=850)

e3 = tk.Entry(root, font=('Cooper Black', 14), width=2)
e3.place_configure(x=650, y=850)

set = tk.Button(root, text="Zastosuj", command=lambda: start_simulation(conveyor, e1.get(), e2.get(), e3.get(), 0))
set.config(activebackground="green", bd=4, font=('Cooper Black', 16), background="black", foreground="green",
           borderwidth=0)
set.place_configure(x=460, y=880)

e1.insert(10, "20")
e2.insert(10, "2")
e3.insert(10, "4")

conveyor = Conveyor(canvas, weight_label, threads_label)
root.mainloop()
