import argparse
from datetime import date, timedelta, datetime
from google.cloud import storage
from config_params import stores
from audit.file_audit import MuffatoFileAudit

import BenderBot

def exceptions_list(dt: date, store_name: str):
    dt = datetime.strptime(dt, "%Y-%m-%d")
    if store_name.startswith('9_') and dt < datetime(2020, 11, 5):
        return True
    if store_name == '94_MAX-TITO-MUFFATO' and dt < datetime(2020, 8, 3):
        return True
    if store_name == '99_SJRP-DAHMA' and dt < datetime(2020, 10, 12):
        return True
    if store_name == '100_CATANDUVA' and dt < datetime(2020, 8, 21):
        return True


# Compara cada nome de arquivo com os da lista passada
def check_list(item: str, items_list: [], dt: date):
    for item_name in items_list:
        if item.__contains__(item_name):
            items_list.remove(item_name)
            return

    print(f'{dt}: {item} não esta na lista de lojas!')


# Lista todos os diretorios e arquivos do 'bucket/folder'
def list_items(bucket: str, folder: str, filter=None):
    storage_client = storage.Client('mediar-painel')
    items = storage_client.list_blobs(bucket, prefix=folder + filter)

    return items


def verify(dt: date, bucket: str, folder: str, filter=''):
    items = list_items(bucket, folder, filter)
    # Caso para sales-raw
    if filter.__contains__('sales-raw'):
        items_list = stores['mediar-ftp'][folder].copy()
    else:
        items_list = stores[bucket][folder].copy()

    for item in items:
        if item.name.__contains__(f'{dt}'):
            check_list(item.name, items_list, dt)

    for store_name in items_list:
        if not exceptions_list(dt, store_name):
            print(f'{dt} falta {store_name} em {bucket}/{folder}{filter}')


def compara_quantidade(attributes: dict, tipo: str):
    dt = attributes['date']
    contador1 = 0
    contador2 = 0
    contador3 = 0
    storage_client = storage.Client('mediar-painel')
    items1 = storage_client.list_blobs('mediar-ftp', prefix=f'muffato/{tipo}')
    items2 = storage_client.list_blobs(
        'mediar-data', prefix=f'muffato/sales-raw/{tipo}')
    items3 = storage_client.list_blobs(
        'mediar-data', prefix=f'muffato/transactions/')

    for item in items1:
        if item.name.__contains__(f'{dt}'):
            contador1 += 1
    for item in items2:
        if item.name.__contains__(f'{dt}'):
            contador2 += 1
    for item in items3:
        if item.name.__contains__(f'{dt}'):
            contador3 += 1

    if contador1 > contador2:
        print(f'{dt} - {tipo} - ERRO: GZIP Muffato faltou {contador1 - contador2}')
    if contador2 > contador3:
        print(f'{dt} - {tipo} - ERRO: Sales Processing faltou {contador2 - contador3}')


def daterange(start_date, end_date):
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    for n in range(int((end_date - start_date).days)+1):
        yield (start_date + timedelta(n)).strftime('%Y-%m-%d')


def is_date(x):
    try:
        datetime.strptime(x, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def is_int(x):
    try:
        int(x)
        return True
    except ValueError:
        return False

# if __name__ == '__main__':
#     parser = argparse.ArgumentParser()
#     parser.add_argument('--start_date')
#     parser.add_argument('--end_date')
#     parser.add_argument('--store_ids')
#     parser.add_argument('--sleeptime')
#     args = parser.parse_args()
#     if not is_date(args['start_date']):
#         if is_int(args['start_date']):
#             args['start_date'] = (datetime.now() + timedelta(int(args['start_date']))).strftime('%Y-%m-%d')
#         else:
#             raise ValueError('--start_date is not a date or int')
#     try:
#         if not is_date(args['end_date']):
#             if is_int(args['end_date']):
#                 args['end_date'] = (datetime.now() + timedelta(int(args['end_date']))).strftime('%Y-%m-%d')
#             else:
#                 raise ValueError('--end_date is not a date or int')
#         assert args['end_date'] >= args['start_date'], '--end_date is not >= --start_date'
#     except:
#         args['end_date'] = args['start_date']

#     for date in daterange(args['start_date'], args['end_date']):
#         file_check = MuffatoFileAudit('mediar-data', date)
#         file_check.exists('mediar-data', )
#         #verify(date, 'mediar-ftp', 'muffato', filter='/ASSORTMENT')
#         #verify(date, 'mediar-data', 'muffato', filter='/sales-raw/ASSORTMENT')
#         #verify(date, 'mediar-ftp', 'muffato', filter='/SALES')
#         #verify(date, 'mediar-data', 'muffato', filter='/sales-raw/SALES')
#         #verify(date, 'mediar-data', 'muffato', filter=f'/transactions/dt={attributes["date"]}')
#         #verify(date, 'mediar-data', 'muffato', filter=f'/assortment/dt={attributes["date"]}')
#         #verify(date, 'mediar-ftp', 'sva')
#         #verify(date, 'mediar-data', 'sva', filter='/video-raw')
#         #verify(date, 'mediar-data', 'sva', filter='/video-metrics')
#         #verify(date, 'mediar-data', 'sva', filter='/video-filtered')
#         #compara_quantidade(attributes, 'SALES')

bot = BenderBot.BenderBot()

bot.postMessageToChannel("All good.")
