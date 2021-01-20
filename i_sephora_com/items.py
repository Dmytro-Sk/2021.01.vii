# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SephoraComItem(scrapy.Item):
    category = scrapy.Field()
    oil_free = scrapy.Field()
    paraben_free = scrapy.Field()
    sulfate_free = scrapy.Field()
    gluten_free = scrapy.Field()
    silicone_free = scrapy.Field()
    vegan = scrapy.Field()
    price = scrapy.Field()
    skin_type = scrapy.Field()
    skincare_concerns = scrapy.Field()
    what_it_is = scrapy.Field()
    number_of_stars = scrapy.Field()
    review_title = scrapy.Field()
    review_description = scrapy.Field()
    reviewer_skin_type = scrapy.Field()
    reviewer_skin_tone = scrapy.Field()
