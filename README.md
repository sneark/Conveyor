#Conveyor
1. Temat projektu: 
On the conveyor system moving bricks from the lower end to the upper 
end, laborers are at work. One crew posiƟons bricks onto the conveyor at 
the lower end, and a different crew takes them off at the upper end. The 
bricks come in two varieƟes, weighing either 2 kg or 4 kg, and the 
maximum weight the conveyor can handle is 20 kg. 

2. Techniczne rozwiązania 
Cały projekt napisany został w języku Python. Stworzona jest wizualizacja 
graficzna w aplikacji okienkowej do której użyta została biblioteka Tkinter 
oraz pillow. Do realizacji wątków została użyta biblioteka threading. 

3. Założenia projektowe 
Zadany problem w temacie projektu można rozumieć na parę sposobów. 
W tym projekcie jako wątki przyjęte zostały cegły, które mają 
odpowiednie wagi różne od siebie, zasobem o jakie rywalizują 
poszczególne wątki jest przenośnik, który ma ograniczenie wagowe. 

4. Funkcjonalność 
Projekt został stworzony jako aplikacja okienkowa z graficznym 
interfejsem. 
Możliwa jest zmiana wartości wagowych obu cegieł oraz samo 
ograniczenie wagowe dotyczące przenośnika poprzez wpisanie wartości 
w pola i zastosowania zmian przyciskiem. 
Jako domyślne wartości ustawione są wagi ujęte w temacie projektu. 
Symulacja jest rozpoczęta po naciśnięciu odpowiedniego przycisku, 
możliwe jest również zakończenie i zatrzymanie symulacji. 
W czasie rzeczywistym wyświetlana jest sumaryczna waga cegieł, które 
znajdują się na przenośniku. Pokazany jest także stan kolejki cegieł 
oczekujących na dostęp do przenośnika. 

5. Konstrukcja programu 
 Stworzona została klasa Conveyor która reprezentuje zasób, o który 
rywalizują wątki. W klasie znajdują się zmienne przechowujące wszystkie 
wartości wagowe oraz obiekty służące do synchronizacji wątków. 
 Funkcja add_brick to funkcja sterująca wątkami. W niej przebiega cały 
proces weryfikacji dostępu oraz synchronizacji z innymi wątkami. 
 Funkcja remove_brick odpowiedzialna jest za aktualizację wartości 
wagowych oraz usuwanie cegły z wizualizacji. 
 Funkcja draw_brick oraz move_brick również służą do graficznej 
reprezentacji cegły. Funkcja draw tworzy obiekt cegły natomiast move 
porusza cegłę po przenośniku. 
 Funkcję update_..._label aktualizują wartości wagi i kolejki w wizualizacji. 
 Funkcja simulate_conveyor to funkcja, w której znajduję się pętla 
tworząca wątki (cegły) znajdują się w niej także obsługi zdarzeń. Pętla jest 
także odpowiedzialna za odświeżanie canvasu. 
 Pozostałe funkcję to obsługa przycisków i wywołanie odpowiednich funkcji 
do działania programu. 

6. Synchronizacja pomiędzy wątkami 
Synchronizacja pomiędzy wątkami została zrealizowana przy użyciu 
Semafora oraz Zdarzeń. Semafor jest odpowiedzialny za ustalenie limitu 
ilości wątków które jednocześnie mają dostęp do zasobu. W tym 
projekcie ilość cegieł, które w tym samym momencie mogą znajdować się 
na przenośniku. Wartość semafora jest ustalana jako: 
Maksymalna dozwolona waga // waga lżejszej cegły 
Zastosowane zdarzenia służą do informacji wątków o zmianach w kolejce 
wątków które nie uzyskały dostępu do zasobu przy ich stworzeniu. 
Wątki te nie dostając dostępu do zasobu trafiają do kolejki, są one 
obsługiwane przez zdarzenie isFull na które oczekują, w momencie 
wystąpienia zdarzenia wywoływana jest rekurencyjnie funkcja 
przydzielająca zasób. W takim przypadku wątek jest ponownie 
poddawany weryfikacji przez limit wagowy i semafor które chronią zasób, 
do którego wątek próbuje uzyskać dostęp. 

7. Działanie programu 
 Symulacja rozpoczyna się po naciśnięciu przycisku, wywoływana jest 
wtedy funkcja, która tworzy wątek odpowiedzialny za symulację. 
 Główna pętla tworzy nowe cegły, które w programie są wątkami. Mają 
one losowo przydzielane wagi z wartościami podanymi przez użytkownika. 
Nowe wątki powstają co równą sekundę, jeśli nie zostaną wstrzymane 
przez zdarzenia. 
 Po stworzeniu wątku trafia on do funkcji add_brick która jest 
odpowiedzialna za przydział wątku do zasobu. 
 Sprawdzane jest czy waga cegły nie przekracza podanego limitu, jeśli nie 
przekracza trafia ona do semafora. Aktualizowana jest waga, cegła 
tworzona jest na wizualizacji a następnie usuwana, następnie wątek 
kończy swoją pracę. 
 W przypadku gdy cegła nie spełnia wymagań wagowych jest ona 
przerzucona do drugiej części warunku, gdzie wątek jest wstrzymany i 
oczekuje na zdarzenie isFull, które czeka na informację od innego wątku, 
że odblokowało się miejsce na przenośniku, jest ono zgłaszane w 
momencie usuwania cegły. Po otrzymaniu informacji rekurencyjnie 
wywoływana jest funkcja add_brick i dany wątek ponownie jest 
weryfikowany przez limit wagowy i semafor. 
 Jeśli w kolejce znajduje się co najmniej 5 wątków, aktywowane jest 
zdarzenie, które obsługiwane jest w wątku symulacji. Wstrzymuje ono 
generowanie nowych wątków przez 3 sekund tak aby wstrzymane w 
kolejce wątki uzyskały priorytetowy dostęp do zasobu. Zastosowana jest 
także instrukcja warunkowa która sprawdza czy dany wątek jest pierwszy 
w kolejce, zapobiega to zagłodzeniu wątków znajdujących się w kolejce. 
 W funkcji add_brick aktualizowany jest także licznik kolejki. W momencie, 
w którym w kolejce znajduje się 10 wątków nowe wątki nie są tworzone. 
 Cegła, która uzyska dostęp do przenośnika jest tworzona na wizualizacji 
funkcjami draw_brick oraz move_brick. Funkcja draw_brick w zależności 
od wagi danej cegły przypisuje jej odpowiednią teksturę a następnie 
wywołuje funkcję move_brick. Dzięki tej funkcji cegła porusza się na 
ekranie, cegła, która uzyskała dostęp do zasobu znajduje się na nim 
dokładanie 12,4 sekundy po czym jest zdejmowana z przenośnika. 
 Symulacja w dowolnym momencie może być zatrzymana za pomocą 
przycisku, zatrzymuje on działanie programu na 7 sekund. Program i 
symulację kończy przycisk „Zakończ symulacje” który zamyka okno 
programu i za pomocą .join() zakańcza wątek symulacji.
