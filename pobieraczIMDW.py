# author: Antoni Pytkowski
# date: 2022-11-19
# ver: 1.0.2
# disclaimer: funkcja sie wywali jezeli jakis jelop inaczej sformatowal nazwe archiwum
# niz tak jak jest w linii 55, ale to nie moja wina ze niektorzy sa glupi

import io
import requests
import tarfile
import time
import urllib.error
import zipfile


# user input
# hydroMeteo expected to be string like 'Hydro' or 'Meteo'
# year  expected to be string like '2022' or another year
# month  expected to be string like '01' or another month

def save_tar(link):
    start_time = time.time()
    print('started downloading .tar')
    link += '.tar'
    req = requests.get(link)
    with open('tfile.tar', 'wb') as f:
        f.write(req.content)
    archive = tarfile.open('tfile.tar')
    archive.extractall('data/')
    print(f'downloaded in {round(time.time() - start_time, 3)} seconds')
    return

def save_zip(link):
    start_time = time.time()
    print('started downloading .zip')
    link += '.zip'
    req = requests.get(link)
    archive = zipfile.ZipFile(io.BytesIO(req.content))
    archive.extractall('data/')
    print(f'downloaded in {round(time.time() - start_time, 3)} seconds')
    return

def download_IMDW(hydroMeteo, year, month):
    if type(hydroMeteo) != str:
        print("variable hm expected to be string eg. 'Meteo'")
        return
    if not hydroMeteo in ['Hydro', 'Meteo']:
        print("variable hm has to be 'Hydro' or 'Meteo'")
    if type(year) != str:
        print("variable y expected to be string eg. '2022'")
        return
    if type(month) != str:
        print("variable hm expected to be string eg. '01'")
        return

    http_datastore = f'https://dane.imgw.pl/datastore/getfiledown/Arch/Telemetria/{hydroMeteo}/{year}/{hydroMeteo}_{year}-{month}'

    try:
        save_tar(http_datastore)
    except urllib.error.HTTPError:
        print('cannot get .tar, file extension is .zip')
        try:
            save_zip(http_datastore)
        except urllib.error.HTTPError:
            print('ERROR: cannot get .zip nor .tar')
    finally:
        print(http_datastore)
    return
