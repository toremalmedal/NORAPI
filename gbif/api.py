import requests
import json
import logging
from datetime import datetime
from os import path, remove

urlGBIF = "https://api.gbif.org/v1/occurrence/search"
urlArtsdatabanken = "https://artskart.artsdatabanken.no/publicapi/"

def getObservationsGBIF(countryCode: str, speciesKey: str, limit = 100):
    
    endOfRecords = False
    offset = 0
    results = []
    filename = (f'data/gbif/GBIF_{countryCode}_{speciesKey}.json')

    while endOfRecords is False:
        payload = {'country': countryCode, 'specieskey': speciesKey, 'limit': limit, 'offset': offset}
        r = requests.get(f'{urlGBIF}', params=payload)
        
        logging.warning(f'Get request for {r.url} got status code {r.status_code}')
        
        r = r.json()
        results.append(r['results'])
        endOfRecords = r['endOfRecords']
        offset = offset+limit
    
    if (path.exists(filename)):
        remove(filename)
        logging.info(f'Removed {filename}')

    with open(filename, 'a') as write_file:
        json.dump(results, write_file)
        logging.info("Wrote to {filename}")
    
    with open(f'UpdateHistory', 'a') as write_file:
        today = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        write_file.write(f'{today}: Updated GBIF_{countryCode}_{speciesKey}.json \n')

for country in ['NO', 'SE', 'DK']:
    getObservationsGBIF(country, '7820753')

# https://artskart.artsdatabanken.no/publicapi/api/taxon?term=stillehavs%C3%B8sters
# TaxonId: 190349