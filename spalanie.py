# -*- coding: utf-8 -*-
"""
Created on Sun May 17 19:00:00 2026

@author: Gemini
"""

import csv
from datetime import datetime
import os
import matplotlib.pyplot as plt

# Nazwy plików
CSV_FILE = "historia_spalania.csv"
CHART_FILE = "wykres_spalania.png"


def pobierz_liczbe(komunikat):
    """
    Pomocnicza funkcja do pobierania poprawnych liczb od użytkownika.

    Funkcja działa w pętli do momentu, aż użytkownik wprowadzi poprawną
    wartość liczbową. Automatycznie zamienia przecinki na kropki, aby
    zapobiec błędom formatowania.

    Parameters
    ----------
    komunikat : str
        Tekst wyświetlany użytkownikowi jako prośba o wprowadzenie danych.

    Returns
    -------
    float
        Wprowadzona przez użytkownika i poprawnie skonwertowana liczba zmiennoprzecinkowa.
    """
    while True:
        try:
            return float(input(komunikat).replace(",", "."))
        except ValueError:
            print("To nie jest poprawna liczba. Spróbuj ponownie.")


def glowny_program():
    """
    Główna funkcja sterująca działaniem aplikacji kalkulatora spalania.

    Funkcja odpowiada za interakcję z użytkownikiem, obliczenie średniego 
    spalania na 100 km, zapis danych oraz historii tankowania do pliku CSV, 
    wypisanie podsumowania w oknie konsoli oraz wygenerowanie dwuosiowego 
    wykresu liniowego (.png).

    Parameters
    ----------
    Brak parametrów.

    Returns
    -------
    None
        Funkcja nie zwraca żadnej wartości, wykonuje operacje wejścia/wyjścia.
    """
    print("--- KALKULATOR SPALANIA ---")

    # 1. Pobieranie danych od użytkownika
    paliwo = pobierz_liczbe("Podaj ilość zatankowanego paliwa (w litrach): ")
    przebieg_obecny = pobierz_liczbe("Podaj obecny stan licznika (km): ")
    przebieg_poprzedni = pobierz_liczbe("Podaj poprzedni stan licznika (km): ")
    cena = pobierz_liczbe("Podaj łączny koszt tankowania (zł): ")

    # 2. Obliczenia
    dystans = przebieg_obecny - przebieg_poprzedni
    if dystans <= 0:
        print(
            "Błąd: Obecny przebieg musi być większy niż poprzedni! Przerywam."
        )
        return

    spalanie = (paliwo / dystans) * 100
    
    # 3. Obliczenia i ustalanie daty
    dystans = przebieg_obecny - przebieg_poprzedni
    if dystans <= 0:
        print("Błąd: Obecny przebieg musi być większy niż poprzedni! Przerywam.")
        return

    spalanie = (paliwo / dystans) * 100
    
    # --- NOWY FRAGMENT: WYBÓR DATY ---
    domyslna_data = datetime.now().strftime("%Y-%m-%d")
    print(f"\nDomyślna data to dzisiaj: {domyslna_data}")
    data_input = input("Wciśnij ENTER, aby użyć domyślnej, lub wpisz własną datę (RRRR-MM-DD): ").strip()
    
    if data_input == "":
        dzisiejsza_data = domyslna_data
    else:
        # Walidacja, czy użytkownik wpisał datę w dobrym formacie
        try:
            datetime.strptime(data_input, "%Y-%m-%d")
            dzisiejsza_data = data_input
        except ValueError:
            print("Niepoprawny format daty! Używam daty dzisiejszej.")
            dzisiejsza_data = domyslna_data
    # ----------------------------------

    print(f"\nWynik: Twoje spalanie to {spalanie:.2f} L/100km (Data: {dzisiejsza_data})")

    print(f"\nWynik: Twoje spalanie to {spalanie:.2f} L/100km")

    # 4. Zapis do pliku CSV
    file_exists = os.path.isfile(CSV_FILE)

    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as plik:
        writer = csv.writer(plik)
        # Jeśli plik nie istnieje, dodajemy nagłówek
        if not file_exists:
            writer.writerow(
                [
                    "Data",
                    "Ilosc_paliwa",
                    "Dystans",
                    "Koszt",
                    "Spalanie_L_100km",
                ]
            )
        writer.writerow(
            [
                dzisiejsza_data,
                round(paliwo, 2),
                round(dystans, 2),
                round(cena, 2),
                round(spalanie, 2),
            ]
        )

    # 4. Odczyt i wypisanie zawartości pliku CSV w konsoli
    print("\n--- HISTORIA TANKOWAŃ ---")
    daty = []
    spalania = []
    koszty = []

    with open(CSV_FILE, mode="r", encoding="utf-8") as plik:
        reader = csv.reader(plik)
        next(reader)  # Pomijamy nagłówek

        for wiersz in reader:
            if not wiersz:
                continue
            data_t, paliwo_t, dystans_t, koszt_t, spalanie_t = wiersz
            print(
                f"Tankowałeś w dniu {data_t}, nalałeś {paliwo_t} L, "
                f"przejechałeś {dystans_t} km i koszt: {koszt_t} zł."
            )

            # Zbieramy dane do wykresu
            daty.append(data_t)
            spalania.append(float(spalanie_t))
            koszty.append(float(koszt_t))

    # 6. Generowanie wykresu
    if len(daty) > 0:
        plt.figure(figsize=(10, 5))

        # Wykres spalania (oś lewa)
        fig, ax1 = plt.subplots(figsize=(10, 5))
        kolor_spalania = "tab:blue"
        ax1.set_xlabel("Data tankowania")
        ax1.set_ylabel("Spalanie (L/100km)", color=kolor_spalania)
        linia1 = ax1.plot(
            daty,
            spalania,
            color=kolor_spalania,
            marker="o",
            linewidth=2,
            label="Spalanie (L/100km)",
        )
        ax1.tick_params(axis="y", labelcolor=kolor_spalania)
        ax1.grid(True, linestyle="--", alpha=0.5)

        # Druga oś dla kosztów (oś prawa)
        ax2 = ax1.twinx()
        kolor_kosztow = "tab:green"
        ax2.set_ylabel("Koszt tankowania (zł)", color=kolor_kosztow)
        linia2 = ax2.plot(
            daty,
            koszty,
            color=kolor_kosztow,
            marker="s",
            linewidth=2,
            linestyle=":",
            label="Koszt (zł)",
        )
        ax2.tick_params(axis="y", labelcolor=kolor_kosztow)

        # Połączenie legend z obu osi
        linie = linia1 + linia2
        etykiety = [l.get_label() for l in linie]
        ax1.legend(linie, etykiety, loc="upper left")

        plt.title("Historia Spalania i Kosztów Tankowania")
        fig.tight_layout()

        # Zapis do pliku
        plt.savefig(CHART_FILE)
        plt.close()
        print(f"\n[INFO] Zaktualizowano wykres i zapisano do pliku: {CHART_FILE}")


if __name__ == "__main__":
    glowny_program()