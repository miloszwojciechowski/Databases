from astral import LocationInfo
from astral.sun import sun
from astral import zoneinfo
from datetime import datetime
from tqdm import tqdm

def dayOrNight(dataframe):
    dayNight = []
    timezone = zoneinfo.ZoneInfo("Europe/Warsaw")
    stacja = int
    datePrev = datetime.strptime(dataframe["Data"].iloc[0], '%Y-%m-%d %H:%M')  # zmienne do zapisywania daty "poprzedniej" w formacie datetime
    datePrev = datePrev.replace(tzinfo=timezone)
    for index, row in tqdm(dataframe.iterrows(), total=len(dataframe)):
        dateNow = datetime.strptime(row['Data'][:10], '%Y-%m-%d')  # data obecnie sprawdzana w pętli w formacie datetime
        dateNow = dateNow.replace(tzinfo=timezone)
        # kolejne instrukcje wykonają się tylko wtedy, gdy poprzedni indeks stacji jest inny od obecnego, co oznacza zmianę stacji
        if stacja != row['KodSH']:
            long = row['geometry'].x
            lat = row['geometry'].y
            city = LocationInfo(str(row['KodSH']), "Poland", "Europe/Warsaw", lat, long)

        # dane o Słońcu wyliczam tylko dla pierwszego wiersza i jeśli dzień się zmienił
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
    dataframe.insert(len(dataframe.columns), "Dzien/Noc", dayNight)  # dodanie kolumny z wartościami dzień/noc
    return dataframe
