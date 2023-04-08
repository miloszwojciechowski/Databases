from dataframe import dataframe, typ
from functions import date_splitter
import pymongo
from tqdm import tqdm

stacjeDf = dataframe()
stacjeDf = date_splitter(stacjeDf)

connection = pymongo.MongoClient(r'mongodb+srv://PAG:database@cluster0.wdzyage.mongodb.net/test')
db = connection.baza
stacje = db.stacje

## ustawiamy dane pierwszej stacji do jsona
wiersz0 = stacjeDf.iloc[0]
stacja = {'KodSH': int(wiersz0['KodSH']),
        'Lokalizacja': wiersz0['Województwo'],
        'Rok': wiersz0['Rok'],
        'Miesiac': wiersz0['Miesiac'],
        'Typ': typ,
        'pomiary': []
        }
idStacji = wiersz0['KodSH']

print('\n',"Transfer danych do MongoDB")
## iterujemy się po całym dataframe i zbieramy dane z pomiarów
for index, row in tqdm(stacjeDf.iterrows(), total=len(stacjeDf)):
## gdy stacja się zmieni, jsona z pomiarami z poprzedniej oddajemy do bazy danych i tworzymy nowego dla nowej stacji
    if idStacji != row['KodSH']:
        db.stacje.insert_one(stacja)
        stacja = {'KodSH': int(row['KodSH']),
                'Lokalizacja': row['Województwo'],
                'Rok': row['Rok'],
                'Miesiac': row['Miesiac'],
                'Typ': typ,
                'pomiary': []
                }
## zapisujemy kodSH do zmiennej, do której będziemy porównywać następny wiersz
    idStacji = row['KodSH']
## zapis danych pomiarowych do mini-jsona wewnątrz jsona stacji, DODAJ ATRYBUT DZIEN/NOC
    stacja['pomiary'].append({'id': int(len(stacja['pomiary'])+1), 'value': float(row['Wartość'].replace(',','.')),
                              'dzien': str(row['Dzien']), 'godzina': str(row['Godzina']), 'dzien/noc': row['Dzien/Noc']})

connection.close()
