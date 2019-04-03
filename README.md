# RaceResults

## Requirements
- Python
    - Scrapy
    - Arrow
    - PyMongo
- MongoDB Database

## Run Spider

```console
# Run br_timing spider
foo@bar:~$ python -m scrapy runspider raceresults/spiders/br_timing.py
```


Example Document:
```json
{
    "_id": "119f835e0d54e916eadd489d8f8be9275d8ff67a39b9a2c41e526c8479a9ba7b", 
    "ageclass": "M20", 
    "bib_number": "1234", 
    "birth": 1991, 
    "collection": "race_results", 
    "competition": "Marathon (42.2km)", 
    "distance": 42.2, 
    "event_date": "Sun, 1 Mar 2018 00:00:00 GMT", 
    "event_date_str": "01.03.2018", 
    "event_name": "Example Marathon", 
    "event_year": 2018, 
    "firstname": "Max", 
    "identityhash": "119f835e0d54e916eadd489d8f8be9275d8ff67a39b9a2c41e526c8479a9ba7b", 
    "laps": null, 
    "lastname": "Mustermann", 
    "list_url": "https://coderesearch.com/sts/services/10050/0000/m", 
    "name": "Mustermann, Max", 
    "nationality": "GER", 
    "place_ageclass": 1, 
    "place_sex": 1, 
    "place_total": 1, 
    "result_url": "https://coderesearch.com/sts/services/10051/0000/m/1234", 
    "source": "br-timing", 
    "team": "Example Team", 
    "time": "02:11:47", 
    "time_net": "02:11:08"
}
```
