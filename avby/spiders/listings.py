# -*- coding: utf-8 -*-
import scrapy
import json
from tqdm import tqdm
from avby.spiders.avlist import brands_code_list


class ListingsSpider(scrapy.Spider):
    name = 'listings'
    allowed_domains = ['av.by']
    finalcars = []

    def start_requests(self):
        query = {
            "page": 1,
            "properties": [
                {
                    "name": "brands",
                    "property": 5,
                    "value": [
                        [
                            {
                                "name": "brand",
                                "value": 6
                            }
                        ]
                    ]
                },
                {
                    "name": "price_currency",
                    "value": 2
                }
            ],
            "sorting": 1
        }

        yield scrapy.Request(
            url="https://api.av.by/offer-types/cars/filters/main/apply",
            method="POST",
            body=json.dumps(query),
            headers={
                "Content-Type": "application/json"
            },
            callback=self.parse
        )

    def parse(self, response):
        resp_dict = json.loads(response.body)
        count = resp_dict.get('count')
        pages = resp_dict.get('pageCount')
        page = resp_dict.get('page')
        html = resp_dict.get('adverts')

        # yield {
        #     'page': page,
        #     'html': html
        # }

        

        cars = {
            'page': page,
            'html': html
        }

        self.finalcars.append(cars)

        file_name = 'cars.json'
 
        with open(file_name, 'w', encoding='utf-8') as json_file:
            json.dump(self.finalcars, json_file, ensure_ascii = False, indent =4)


        if page <= pages:
            for x in range(2, pages):

                query = {
                    "page": x,
                    "properties": [
                        {
                            "name": "brands",
                            "property": 5,
                            "value": [
                                [
                                    {
                                        "name": "brand",
                                        "value": 6
                                    }
                                ]
                            ]
                        },
                        {
                            "name": "price_currency",
                            "value": 2
                        }
                    ],
                    "sorting": 1
                }

                yield scrapy.Request(
                    url="https://api.av.by/offer-types/cars/filters/main/apply",
                    method="POST",
                    body=json.dumps(query),
                    headers={
                        "Content-Type": "application/json"
                    },
                    callback=self.parse
                )
