from geojson import Feature, Point, FeatureCollection
import json
from os import path, remove
from datetime import datetime
import logging

def createGeoJSON(countryCode: str):
    with open(f'data/gbif/GBIF_{countryCode}_7820753.json', 'r') as read_file:
        observationLists = json.load(read_file)
        xs, ys, eventdates, keys = [], [], [], []

        for observations in observationLists:
            for observation in observations:
                xs.append(observation.get('decimalLongitude'))
                ys.append(observation.get('decimalLatitude'))
                eventdates.append(observation.get('eventDate'))
                keys.append(observation.get('key'))
        
    features = []
    for x, y, eventdate, key in zip(xs, ys, eventdates, keys):
        try:
            features.append(Feature(properties = {'eventdate': eventdate, 'key': key}, geometry=Point((x, y))))
        except:
            logging.exception(f"Failed to convert observation {key} to feature.")
            
    
    filename = f'data/geojson/GBIF_GeoJSON_{countryCode}.json'
    
    if (path.exists(filename)):
        remove(filename)
        logging.info(f'Removed {filename}')

    with open(filename, 'a') as write_file:
        json.dump(FeatureCollection(features), write_file)
        logging.info("Wrote to {filename}")
    
    with open(f'UpdateHistory', 'a') as write_file:
        today = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        write_file.write(f'{today}: Updated {filename} \n')

createGeoJSON('SE')