from astral import LocationInfo
from astral.sun import sun
from astral import zoneinfo
from datetime import datetime
from tqdm import tqdm

def dayOrNight(dataframe):
    dayNight = []
    timezone = zoneinfo.ZoneInfo("Europe/Warsaw")
    stacja = int
    datePrev = datetime.strptime(dataframe["Data"].iloc[0], '%Y-%m-%d %H:%M') #zmienne do zapisywania daty "poprzedniej" w formacie datetime
    datePrev = datePrev.replace(tzinfo=timezone)
    print('\n',"Wyliczanie dnia i nocy")
    for index, row in tqdm(dataframe.iterrows(), total=len(dataframe)):
        dateNow = datetime.strptime(row['Data'][:10], '%Y-%m-%d')  #data obecnie sprawdzana w pętli w formacie datetime
        dateNow = dateNow.replace(tzinfo=timezone)
## kolejne instrukcje wykonają się tylko wtedy, gdy poprzedni indeks stacji jest inny od obecnego, co oznacza zmianę stacji
        if stacja != row['KodSH']:
            long = row['geometry'].x
            lat = row['geometry'].y
            city = LocationInfo(str(row['KodSH']), "Poland", "Europe/Warsaw", lat, long)

## dane o Słońcu wyliczam tylko dla pierwszego wiersza i jeśli dzień się zmienił
        if (dateNow - datePrev).days != 0 or index == 0:
            s = sun(city.observer, date=dateNow) # wyliczenie danych na temat słońca na podstawie lokalizacji, daty i strefy

        date = datetime.strptime(row['Data'], '%Y-%m-%d %H:%M')  #pełna data do porównywania z zachodem i wschodem Słońca
        date = date.replace(tzinfo=timezone)
## przypisanie atrybutów dnia i nocy i zapis tych wartości do listy
        if date >= s["sunset"] or date < s["sunrise"]:
            dayNight.append("noc")
        else:
            dayNight.append("dzien")
        stacja = row['KodSH']
        datePrev = dateNow
    dataframe.insert(len(dataframe.columns), "Dzien/Noc", dayNight) #dodanie kolumny z wartościami dzień/noc
    return dataframe

def inWojewodztwo(geodataframe, wojewodztwa):
## tworzymy zmienną do przechowywania współrzędnych stacji oraz listę do przechowywania województw, w których leżą stacje
    coordinates = geodataframe['geometry'][0]
    woj = str
    wojewodztwaLista = []

    print('\n',"Przypisywanie województw")
## iterujemy się przez data frame
    for index, row in tqdm(geodataframe.iterrows(), total=len(geodataframe)):
## geometrię stacji pobieram dla pierwszej stacji i jeśli zmieniły się współrzędne, a zatem też stacja
        if row['geometry'] != coordinates or index == 0:
            coordinates = row['geometry']
## tylko gdy zmieniła się stacja lub jest to pierwsza stacja sprawdzam w jakim województwie leży
            for index1, row1 in wojewodztwa.iterrows():
                if coordinates.within(row1['geometry']):
                    woj = row1['name']
                    break

## jeśli stacja się nie zmieniła to po prostu wpisuje do listy to samo wojewodztwo
        wojewodztwaLista.append(woj)
## dodaję listę z województwami do dataframe
    geodataframe.insert(len(geodataframe.columns), "Województwo", wojewodztwaLista)

    return geodataframe

def inPowiat(geodataframe, powiaty):
## tworzymy zmienną do przechowywania współrzędnych stacji oraz listę do przechowywania powiatów, w których leżą stacje
    coordinates = geodataframe['geometry'][0]
    powiat = str
    powiatyLista = []

    print('\n',"Przypisywanie powiatów")
## iterujemy się przez data frame
    for index, row in tqdm(geodataframe.iterrows(), total=len(geodataframe)):
## geometrię stacji pobieram dla pierwszej stacji i jeśli zmieniły się współrzędne, a zatem też stacja
        if row['geometry'] != coordinates or index == 0:
            coordinates = row['geometry']
## tylko gdy zmieniła się stacja lub jest to pierwsza stacja sprawdzam w jakim powiecie leży
            for index1, row1 in powiaty.iterrows():
                if coordinates.within(row1['geometry']):
                    powiat = row1['name']
                    break

## jeśli stacja się nie zmieniła to po prostu wpisuje do listy ten sam powiat
        powiatyLista.append(powiat)
## dodaję listę z powiatami do dataframe
    geodataframe.insert(len(geodataframe.columns), "Powiat", powiatyLista)

    return geodataframe

def date_splitter(dataframe, dodatkowyPodzial=True):
    dataframe[['Data', 'Godzina']] = dataframe.Data.str.split(expand=True)
    if dodatkowyPodzial:
        dataframe[['Rok', 'Miesiac', 'Dzien']] = dataframe.Data.str.split('-', expand=True)
        dataframe.drop('Data', axis=1, inplace=True)

    return dataframe
