from dataframe import dataframe, typ
from neo4j import GraphDatabase
from tqdm import tqdm
from functions import date_splitter

df = dataframe()
df = date_splitter(df, False)

driver = GraphDatabase.driver("bolt://localhost:7687", auth=('neo4j', 'haslo'))
session = driver.session()

unq_dat = df.Data.unique()
print('unikatowe daty')
for date in tqdm(unq_dat):
    # stworzyc date w neo4j
    query = 'create(d:dzien {date: "' + date + '"})'
    session.run(query)

wiersz0 = df.iloc[0]
idStacji = wiersz0['KodSH']

print('Transfer danych do neo4j')
for index, row in tqdm(df.iterrows(), total=len(df)):
    if idStacji != row['KodSH']:  # nowa stacja
        # stworzyc stacje w neo4j
        query = 'create(s:stacja {KodSH: "' + str(idStacji) + '"})'
        session.run(query)

    pomiar = f"Typ: '{typ}', value: {(row['Wartość'].replace(',', '.'))}, Dzien_Noc: {row['Dzien/Noc']}" \
             f"date: '{row['Data']}', stacja: '{row['KodSH']}'"
    # stworzyc pomiar w neo4j
    query = 'create(p:pomiar {'+pomiar+'})'
    session.run(query)

    idStacji = row['KodSH']

# stworzyc strzalki od pomiarow do stacji w neo4j
# stworzyc strzalki od pomiarow do dat w neo4j

query = 'match (p:pomiar), (d:dzien) where p.date = d.date create (p)-[:wykonano_dnia]->(d)'
session.run(query)
query = 'match (p:pomiar), (s:stacja) where p.date = s.date create (p)-[:wykonano_w]->(s)'
session.run(query)

session.close()
