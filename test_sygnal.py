# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 13:58:10 2020

@author: arkad
"""
import sygnal
import numpy as np
import pytest

@pytest.fixture
def prosty_sygnal():
    """Prosty przykład sygnału 1d typu zmiennoprzecinkowego."""
    return np.array([1, -1, -3, 0, 4, 6, 5, 2], dtype='float_')

def test_lekko_wygladz_sygnal(prosty_sygnal):
    """Test wygładzania filtrem uśredniającym o dł. okna 3 (promień 1)."""
    wygladzony_sygnal = sygnal.wygladz(prosty_sygnal, 1)
    wartosc_oczekiwana = np.array([0, -1, -4/3, 1/3, 10/3, 5, 13/3, 7/2],
                                  dtype='float_')
    assert np.allclose(wygladzony_sygnal, wartosc_oczekiwana)


def test_mocno_wygladz_sygnal(prosty_sygnal):
    """Test wygładzania filtrem uśredniającym o dł. okna 7 (promień 3)."""
    wygladzony_sygnal = sygnal.wygladz(prosty_sygnal, 3)
    wartosc_oczekiwana = np.array([-3/4, 1/5, 7/6, 12/7, 13/7, 14/6, 17/5, 17/4],
                                  dtype='float_')
    assert np.allclose(wygladzony_sygnal, wartosc_oczekiwana)


def test_wygladz_sygnal_za_duze_okno(prosty_sygnal):
    """Test wygładzania filtrem uśredniającym o dł. okna 17 (promień 8),
       czyli większej niż długość sygnału.
    """
    wygladzony_sygnal = sygnal.wygladz(prosty_sygnal, 8)
    assert (wygladzony_sygnal == np.mean(prosty_sygnal)).any()


def test_wygladz_sygnal_okno_jeden(prosty_sygnal):
    """Test wygładzania filtrem uśredniającym o dł. okna 1 (promień 0).
       Oczekiwany brak efektu.
    """
    wygladzony_sygnal = sygnal.wygladz(prosty_sygnal, 0)
    assert np.array_equal(wygladzony_sygnal, prosty_sygnal)


def test_wygladz_nie_in_situ(prosty_sygnal):
    """Weryfikacja, czy wygładzanie nie modyfikuje argumentu wejściowego."""
    kopia_zapasowa = prosty_sygnal.copy()
    sygnal.wygladz(prosty_sygnal, 1)
    assert np.array_equal(prosty_sygnal, kopia_zapasowa)


def test_wygladz_pusty_sygnal():
    """Test wygładzania sygnału o długości zero. Oczekiwany brak efektu."""
    pusty_sygnal = np.array([])
    wygladzony_sygnal = sygnal.wygladz(pusty_sygnal, 1)
    assert np.array_equal(wygladzony_sygnal, pusty_sygnal)


def test_wygladz_sygnal_okno_ujemne(prosty_sygnal):
    """Test zachowania dla ujemnego promienia."""
    with pytest.raises(ValueError):
        sygnal.wygladz(prosty_sygnal, -1)

@pytest.fixture
def sygnal_z_pikami():
    """Prosty przykład sygnału 1d typu zmiennoprzecinkowego z wieloma pikami."""
    return np.array([1, -1, 1, 2, 4, 3, 5, 2, 1, -3, -2, -3], dtype='float_')


def test_szukaj_pikow_w_otoczeniu_0(sygnal_z_pikami):
    """Test szukania pozycji ekstremów lokalnych sygnału.
       Uwzględnione wartości na brzegu zakresu.
    """
    pozycje = sygnal.szukaj_pikow(sygnal_z_pikami, 0)
    assert np.array_equal(pozycje, [0, 1, 4, 5, 6, 9, 10, 11])

def test_szukaj_pikow_w_otoczeniu_2(sygnal_z_pikami):
    """Test szukania pozycji ekstremów sygnału o promieniu izolacji 2,
       tj. uwzględnia tylko ekstrema dominujące w otoczenia +/-2 pozycje.
       Uwzględnione wartości na brzegu zakresu.
    """
    pozycje = sygnal.szukaj_pikow(sygnal_z_pikami, 2)
    assert np.array_equal(pozycje, [0, 1, 6, 9, 11])


def test_szukaj_pikow_w_otoczeniu_20(sygnal_z_pikami):
    """Test szukania ekstremów sygnału o promieniu izolacji większym niż
       długość sygnału. Znajduje tylko pozycje ekstremów globalnych.
       Uwzględnione wartości na brzegu zakresu.
    """
    pozycje = sygnal.szukaj_pikow(sygnal_z_pikami, 20)
    assert np.array_equal(pozycje, [6, 9, 11])


def test_szukaj_pikow_w_pustym():
    """Test szukania pozycji ekstremów dla sygnału o długości zero."""
    pusty_sygnal = np.array([])
    pozycje = sygnal.szukaj_pikow(pusty_sygnal, 0)
    assert np.array_equal(pozycje, [])


def test_szukaj_pikow_w_otoczeniu_0_bez_brzegow(sygnal_z_pikami):
    """Test szukania pozycji ekstremów lokalnych sygnału.
       Pomija wartości na brzegu zakresu.
    """
    pozycje = sygnal.szukaj_pikow(sygnal_z_pikami, 0, brzegi=False)
    assert np.array_equal(pozycje, [1, 4, 5, 6, 9, 10])


def test_szukaj_pikow_w_otoczeniu_2_bez_brzegow(sygnal_z_pikami):
    """Test szukania pozycji ekstremów sygnału o promieniu izolacji 2,
       tj. uwzględnia tylko ekstrema dominujące w otoczenia +/-2 pozycje.
       Pomija wartości na brzegu zakresu.
    """
    pozycje = sygnal.szukaj_pikow(sygnal_z_pikami, 2, brzegi=False)
    assert np.array_equal(pozycje, [1, 6, 9])


def test_szukaj_pikow_w_otoczeniu_20_bez_brzegow(sygnal_z_pikami):
    """Test szukania ekstremów sygnału o promieniu izolacji większym niż
       długość sygnału. Znajduje tylko pozycje ekstremów globalnych.
       Pomija wartości na brzegu zakresu.
    """
    pozycje = sygnal.szukaj_pikow(sygnal_z_pikami, 20, brzegi=False)
    assert np.array_equal(pozycje, [6, 9])


def test_szukaj_pikow_w_pustym_bez_brzegow():
    """Test szukania pozycji ekstremów dla sygnału o długości zero."""
    pusty_sygnal = np.array([])
    pozycje = sygnal.szukaj_pikow(pusty_sygnal, 0, brzegi=False)
    assert np.array_equal(pozycje, [])


def test_szukaj_pikow_promien_ujemny(sygnal_z_pikami):
    """Test zachowania dla ujemnego promienia."""
    with pytest.raises(ValueError):
        sygnal.szukaj_pikow(sygnal_z_pikami, -1)