from functions import *
import geopandas as gp
import pandas as p
from pobieraczIMDW import download_IMDW
import tkinter as tk
from tkinter import filedialog

# KodSH –9-cyfrowy kod stacji pomiarowej, stosowany w IMGW PIB do identyfikacji stacji pomiarowej
# ParametrSH –parametr pomiarowy, stosowany w Systemie Hydrologii
# Data –czas, w którym została zaobserwowana wartość pomiarowa
# Wartość –wartość pomiarowa.

typ = input("Wybierz typ Hydro lub Meteo: ")

def dataframe():
    '''
    rok = input("Podaj rok np. 2002: ")
    miesiac = input("Podaj miesiąc np. 05: ")
    download_IMDW(typ,rok,miesiac)
    '''
    root = tk.Tk()

    path = filedialog.askopenfilename(title="Wybierz plik danych do wczytania")

    # Przypisanie typow danych przechowywanych w kolumnach
    dtypes = {"KodSH":int,"ParametrSH":str,"Data":str,"Wartość":str} #dictionary z nazwami kolumn

    # Wczytanie danych z pliku csv i geojson
    dane = p.read_csv(path, sep=';', header = None, dtype=dtypes, names=["KodSH","ParametrSH","Data","Wartość"], index_col=False)
    stacje = gp.read_file('effacility.geojson')

    # sprecyzowanie układu współrzędnych w pliku geojson
    stacje.crs = 2180

    # Dodanie frame ze współrzędnymi stacji do frame z danymi pomiarowymi
    stacje.rename(columns = {'ifcid':'KodSH'}, inplace = True)

    # polaczenie dataframe ze stacjami z dataframem z wspolrzednymi
    joined = dane.merge(stacje[['KodSH','geometry']], on='KodSH', how = 'inner')

    # dodanie kolumny z województwami do dataframe
    wojewodztwa = gp.read_file('woj.shp')

    pomiary = inWojewodztwo(joined, wojewodztwa)

    # zmiana dataframe na geodataframe oraz układu współrzędnych, aby pasował do biblioteki astral
    pomiary = gp.GeoDataFrame(pomiary, crs = 2180)
    pomiary = pomiary.to_crs(4326)

    pomiary = dayOrNight(pomiary) 


    return pomiary

if __name__ == '__main__':
    df = dataframe()
    df = date_splitter(df)
    p.DataFrame(df).to_csv("dataframe.csv")
