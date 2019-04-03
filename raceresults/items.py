# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RaceresultsItem(scrapy.Item):
    event_name = scrapy.Field()
    competition = scrapy.Field()
    event_year = scrapy.Field()
    event_date = scrapy.Field()
    event_date_str = scrapy.Field()

    name = scrapy.Field()
    firstname = scrapy.Field()
    lastname = scrapy.Field()
    name = scrapy.Field()
    team = scrapy.Field()
    birth = scrapy.Field()
    nationality = scrapy.Field()

    time = scrapy.Field()
    time_net = scrapy.Field()

    distance = scrapy.Field()
    laps = scrapy.Field()

    place_total = scrapy.Field()
    place_sex = scrapy.Field()
    place_ageclass = scrapy.Field()
    bib_number= scrapy.Field()
    ageclass = scrapy.Field()

    result_url = scrapy.Field()
    list_url = scrapy.Field()

    identityhash = scrapy.Field()
    _id = scrapy.Field()
    collection = scrapy.Field()
    source = scrapy.Field()
    pass


