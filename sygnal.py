# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 00:40:44 2020

@author: arkad
"""
""" Moduł przetwarzania sygnałów. """
import numpy as np

def wygladz(sygnal, r):
    """Wygładzanie sygnału filtrem uśredniającym.

       Uwaga! Wartości na brzegach zakresu są wygładzane we fragmencie okna
       znajdującym się nad zakresem, np. dla promienia 1 (długość okna 3):
       [ 1 2 6 4 5]
      [ 1.5 ]
        [ 3 ]
          [ 4 ]
            [ 5 ]
              [ 4.5 ]

       Args:
           sygnal (numpy.array): sygnał
           r (int): promien uśredniania (długość okna = 2 x promien + 1)
       Returns:
           numpy.array: wygładzony sygnał
       Raises:
           ValueError: jeśli podano ujemny promień
    """
    if sygnal.size == 0:
        return sygnal
    if r<0:
        raise ValueError("promień nie może być mniejszy od 0")
    if r>(sygnal.size-1):
        return np.mean(sygnal)

    i=0
    wygladzony = np.zeros(sygnal.size)
    while i <= (sygnal.size-1):
        #dla wartosci brzegowych lewej strony (mniejszych od promienia)
        if i < r:
            prawo = r #z prawej strony zawse bedzie wystarczajaco wartosci do wygladzenia
            war_wygladzona = sygnal[i]
            licznik = 0
            while prawo !=0:
                war_wygladzona = war_wygladzona + sygnal[i+prawo]
                prawo-=1
                licznik+=1
            lewo = i #z lewej strony będzie i wartosci możliwych do wygladzenia
            while lewo!=0:
                war_wygladzona = war_wygladzona + sygnal[i-lewo]
                lewo-=1
                licznik+=1
            war_wygladzona = war_wygladzona/(licznik+1) #dzielimy wartosc wygladzona przez ilosc szumowanych wartosci 
            wygladzony [i] = war_wygladzona
        #dla wartosci brzegowych prawej strony
        elif (sygnal.size-i)<=r:
            lewo = r #z lewej strony mamy wystarczajaco wartosci do wygladzenia
            war_wygladzona = sygnal[i]
            licznik = 0
            while lewo !=0:
                war_wygladzona = war_wygladzona + sygnal[i-lewo]
                licznik+=1
                lewo-=1
            prawo = (sygnal.size-i-1) #z prawej strony bedzie ich (sygnal.size-1)-i wartosci do wygladzenia
            while prawo!=0:
                war_wygladzona = war_wygladzona + sygnal[i+prawo]
                licznik+=1
                prawo-=1
            war_wygladzona = war_wygladzona/(licznik+1)
            wygladzony[i] = war_wygladzona
        #wartosci srodkowe (tzn dla wartosci oddalonych od brzegow o conajmniej promien)
        else:
            a = r
            war_wygladzona = sygnal[i]
            while a !=0:
                war_wygladzona = war_wygladzona + sygnal[i+a]
                war_wygladzona = war_wygladzona + sygnal[i-a]
                a-=1

            war_wygladzona = war_wygladzona/(2*r+1)
            wygladzony[i] = war_wygladzona
        i+=1
    return wygladzony
    """
    plt.plot(x,wygladzony, "blue", label="sin wygladzony")
    plt.plot(x,sygnal, "green", label = "sin")
    plt.title("wykres funkcji trygonometrycznych")
    plt.legend()
    plt.show()"""
def szukaj_pikow(sygnal, promien, brzegi=True):
    """Szukanie pozycji pików (ekstremów) w sygnale
       Args:
           sygnal (numpy.array): sygnał
           promien (int): promien izolacji piku (otoczenie, w którym
                          pik stanowi wartość ekstremalną)
           brzegi (bool): sposób traktowania brzegów zakresu:
                          uwzględniane (True, wartość domyślna)
                          pomijane (False)
       Returns:
           lista_pozycji (list) : lista pozycji pików
       Raises:
           ValueError: jeśli podano ujemny promień
    """
    lista_pozycji = []
    if brzegi is False: #pomijanie wartosci brzegowych
        i = 1
        rozmiar = sygnal.size - 2
    elif brzegi is True: #brak pomijania wartosci brzegowych
        i = 0 
        rozmiar = sygnal.size - 1
        if promien>rozmiar: #promien nie może być większy niż rozmiar danych
            promien = rozmiar-1    
    
        
    while i <= rozmiar:
        #dla wartosci srodkowych (tzn dla wartosci oddalonych od brzegow o conajmniej promien)
        if i>promien and i < rozmiar:
            #maksymalna wartosc
            if sygnal[i] == max(sygnal[i-promien-1:i+promien+1]): #wartosc sygnal[i] musi byc max z okna
                if i not in lista_pozycji: #nie moze znajdowac sie juz w liscie pikow
                    if sygnal[i]>sygnal[i+1] and sygnal[i]>sygnal[i-1]: #musi byc maksymalnym ekstremum lokalnym 
                        lista_pozycji.append(i)
            #minimalna wartosc        
            if sygnal[i] == min(sygnal[i-promien-1:i+promien+1]):#wartosc sygnal[i] misi byc min z okna
                if i not in lista_pozycji: #nie moze znajdowac sie juz w licie pikow
                    if sygnal[i]<sygnal[i+1] and sygnal[i]<sygnal[i-1]: #musi byc minimalnym ekstremum lokalnym
                        lista_pozycji.append(i)
                        
                        
        #dla wartosci brzegowych lewej strony                
        if i<=promien:
            #maximum 
            if i == 0: #jesli uwzględniamy wartosc brzegową
                if sygnal[i] == max(sygnal[:promien+1]): 
                    if i not in lista_pozycji:
                        if sygnal[i]>sygnal[i+1]:
                            lista_pozycji.append(i)
            
            else:
                po_lewej = i
                if sygnal[i] == max(sygnal[i-po_lewej:i+promien+1]):
                    if i not in lista_pozycji:
                        if sygnal[i]>sygnal[i+1] and sygnal[i]>sygnal[i-1]:
                            lista_pozycji.append(i)
            #minumum
            if i == 0:
                if sygnal[i] == min(sygnal[:promien+1]):
                    if i not in lista_pozycji:
                        if sygnal[i]<sygnal[i+1]:
                            lista_pozycji.append(i)
            
            else:
                po_lewej = i
                if sygnal[i] == min(sygnal[i-po_lewej:i+promien+1]):
                    if i not in lista_pozycji:
                        if sygnal[i]<sygnal[i+1] and sygnal[i]<sygnal[i-1]:
                            lista_pozycji.append(i)
                            
                            
        #dla wartosci brzegowych prawej strony     
        if i>=rozmiar:
            if i == rozmiar:
                if sygnal[i] == max(sygnal[i-promien-1:]):
                    if i not in lista_pozycji:
                        if sygnal[i]>sygnal[i-1]:
                            lista_pozycji.append(i)
            
            else:
                po_prawej = rozmiar-i
                if sygnal[i] == max(sygnal[i-promien-1:i+po_prawej]):
                    if i not in lista_pozycji:
                        if sygnal[i]>sygnal[i+1] and sygnal[i]>sygnal[i-1]:
                            lista_pozycji.append(i)
                    
            if i == rozmiar:
                if sygnal[i] == min(sygnal[i-promien-1:]):
                    if i not in lista_pozycji:
                        if sygnal[i]<sygnal[i-1]:
                            lista_pozycji.append(i)
            
            else:
                po_prawej = rozmiar-i
                if sygnal[i] == min(sygnal[i-promien-1:i+po_prawej]):
                    if i not in lista_pozycji:
                        if sygnal[i]<sygnal[i+1] and sygnal[i]<sygnal[i-1]:
                            lista_pozycji.append(i)

        i+=1
    return lista_pozycji
   
