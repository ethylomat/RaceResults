# -*- coding: utf-8 -*-
import scrapy
import hashlib
import re
import arrow

from raceresults.items import RaceresultsItem

def cast_to_int(x):
    try:
        return int(x)
    except:
        return x

def strip(x):
    try:
        return x.strip()
    except:
        return x

class BrTimingSpider(scrapy.Spider):
    name = 'br_timing'
    allowed_domains = ['coderesearch.com']

    def start_requests(self):
        yield scrapy.Request(url="https://coderesearch.com/sts/services/10020", callback=self.get_years)

    def get_years(self, response):
        years = response.xpath('//select[@id="year"]').css("option::attr(value)").getall()

        for year in years:
            if year != "":# and year == "2018":
                url = "https://coderesearch.com/sts/services/10020/%s/0" % year
                yield scrapy.Request(url=url, callback=self.parse_year, meta={"year": int(year)})

    def parse_year(self, response):
        s = response.xpath('//div[@class="row competition"]')
        events = []
        for row in s:
            event_id = row.css("div[class*=description]").css("div[class*=omega]").css("a::attr(href)").get().split("/")[-1]
            event_date = strip(row.css("div[class*=description]").css("div[class*=alpha]").css("a::text").get())
            events.append((event_id, event_date))

        for event_id, event_date in events:
            #if event_id == "1170":
            url = "https://coderesearch.com/sts/services/10050/" + event_id
            yield scrapy.Request(url=url, callback=self.parse_event, meta={"event_url": url, "year": response.meta["year"], "event_date": event_date})

    def parse_event(self, response):
        contests = response.xpath('//select[@id="contest"]').css("option::attr(value)").getall()
        event_url = response.meta["event_url"]
        event_date = response.meta["event_date"]

        for contest in contests:
            contest_url = event_url + "/" + contest
            print(contest_url)
            yield scrapy.Request(url=contest_url, callback=self.parse_contest, meta={"list_url": contest_url, "year": response.meta["year"], "event_date": event_date})

    def parse_contest(self, response):
        event_name = response.xpath("//h1").css("h1::text").get().replace("Ergebnislisten - ", "").replace("\n", "").replace("\r", "").strip()
        competition = response.xpath("//h2").css("h2::text").get()

        distances_in_string = re.findall("(\d*[\.\,]*\d?)\s*km+", competition)
        if len(distances_in_string) == 1:
            distance = float(distances_in_string[0].replace(",", "."))
        elif len(distances_in_string) >= 2 and all(x == distances_in_string[0] for x in distances_in_string):
            distance = float(distances_in_string[0].replace(",", "."))
        else:
            distance = None

        event_year = response.meta["year"]
        event_date = response.meta["event_date"]


        for competitor in response.xpath('//table[@class="results"]/tbody/tr')[:]:
            if competitor.css("tr::attr(class)").get() in ["lead", "subsidiary"]:
                relay = True
            else:
                relay = False
            place_total = competitor.css('td[class=col-place-total]').css('a').css('div::text').get()
            place_sex = competitor.css('td[class=col-place-sex]').css('a').css('div::text').get()
            place_ageclass = competitor.css('td[class=col-place-ageclass]').css('a').css('div::text').get()
            bib_number = competitor.css('td[class=col-number]').css('a').css('div::text').get()
            name = competitor.css('td[class=col-competitor]').css('a').css('div::text').get()
            team = competitor.css('td[class=col-team]').css('a').css('div::text').get()
            birth = competitor.css('td[class=col-birth]').css('a').css('div::text').get()
            nationality = competitor.css('td[class=col-nationality]').css('a::text').get()
            ageclass = competitor.css('td[class=col-ageclass]').css('a').css('div::text').get()
            time = competitor.css('td[class*=col-time]').css('a::text').get()
            time_net = competitor.css('td[class*=col-net-time]').css('a::text').get()
            laps = competitor.css('td[class*=col-lap-count-interims]').css('a::text').get()

            result_url = competitor.css('td[class=col-competitor]').css('a::attr(href)').get()
            list_url = response.meta["list_url"]

            if "," in name:
                firstname = name.split(",")[1].strip()
                lastname = name.split(",")[0].strip()
            else:
                if len(name.split()) > 1:
                    firstname = " ".join(name.split()[0:-1])
                    lastname = name.split()[-1]
                else:
                    firstname, lastname = None, None


            rr = RaceresultsItem()

            rr["event_name"] = strip(event_name)
            rr["competition"] = strip(competition)
            rr["event_year"] = event_year
            rr["event_date"] = arrow.get(strip(event_date), 'DD.MM.YYYY').datetime
            rr["event_date_str"] = strip(event_date)

            rr["name"] = strip(name)
            rr["lastname"] = strip(lastname)
            rr["firstname"] = strip(firstname)
            rr["team"] = team
            rr["birth"] = cast_to_int(birth)
            rr["nationality"] = strip(nationality)
            rr["time"] = strip(time)
            rr["laps"] = cast_to_int(laps)
            rr["distance"] = distance
            rr["time_net"] = strip(time_net)

            rr["place_total"] = cast_to_int(place_total)
            rr["place_sex"] = cast_to_int(place_sex)
            rr["place_ageclass"] = cast_to_int(place_ageclass)

            rr["bib_number"] = bib_number
            rr["ageclass"] = ageclass

            rr["result_url"] = result_url
            rr["list_url"] = list_url

            tohash = str(event_name) + str(competition) + str(name) + str(team) + str(event_date)
            hobject = hashlib.sha256(tohash.encode())

            hash_str = str(hobject.hexdigest())

            rr["identityhash"] = hash_str
            rr["_id"] = hash_str
            rr["collection"] = "race_results"
            rr["source"] = "br-timing"

            if relay == False:
                yield rr
            else:
                pass

