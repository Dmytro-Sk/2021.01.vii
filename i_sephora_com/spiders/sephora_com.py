import scrapy
from scrapy.crawler import CrawlerProcess
import re

from vii_sephora_com.i_sephora_com.spiders.locators import Locators
from vii_sephora_com.i_sephora_com.items import SephoraComItem


class SephoraComSpider(scrapy.Spider):
    name = 'sephora_com'
    start_urls = ['https://www.sephora.com/shop/skincare']

    custom_settings = {
        # 'FEED_EXPORT_BATCH_ITEM_COUNT': 100,
        'FEED_FORMAT': 'csv',
        'FEED_URI': f"../../iii_results/%(batch_id)02d-{'_'.join(re.findall(r'[A-Z][^A-Z]*', __qualname__)[:-1]).lower()}.csv",
        'FEED_EXPORT_FIELDS': [
            'category',
            'oil_free',
            'paraben_free',
            'sulfate_free',
            'gluten_free',
            'silicone_free',
            'vegan',
            'price',
            'skin_type',
            'skincare_concerns',
            'what_it_is',
            'number_of_stars',
            'review_title',
            'review_description',
            'reviewer_skin_type',
            'reviewer_skin_tone',
        ]
    }

    def parse(self, response, **kwargs):
        items = SephoraComItem()

        category = response.xpath(Locators.CATEGORY).get()
        oil_free = response.xpath(Locators.OIL_FREE).get()
        paraben_free = response.xpath(Locators.PARABEN_FREE).get()
        sulfate_free = response.xpath(Locators.SULFATE_FREE).get()
        gluten_free = response.xpath(Locators.GLUTEN_FREE).get()
        silicone_free = response.xpath(Locators.SILICONE_FREE).get()
        vegan = response.xpath(Locators.VEGAN).get()
        price = response.xpath(Locators.PRICE).get()
        skin_type = response.xpath(Locators.SKIN_TYPE).get()
        skincare_concerns = response.xpath(Locators.SKINCARE_CONCERNS).get()
        what_it_is = response.xpath(Locators.WHAT_IT_IS).get()
        number_of_stars = response.xpath(Locators.NUMBER_OF_STARS).get()
        review_title = response.xpath(Locators.REVIEW_TITLE).get()
        review_description = response.xpath(Locators.REVIEW_DESCRIPTION).get()
        reviewer_skin_type = response.xpath(Locators.REVIEWER_SKIN_TYPE).get()
        reviewer_skin_tone = response.xpath(Locators.REVIEWER_SKIN_TONE).get()

        items['category'] = category
        items['oil_free'] = oil_free
        items['paraben_free'] = paraben_free
        items['sulfate_free'] = sulfate_free
        items['gluten_free'] = gluten_free
        items['silicone_free'] = silicone_free
        items['vegan'] = vegan
        items['price'] = price
        items['skin_type'] = skin_type
        items['skincare_concerns'] = skincare_concerns
        items['what_it_is'] = what_it_is
        items['number_of_stars'] = number_of_stars
        items['review_title'] = review_title
        items['review_description'] = review_description
        items['reviewer_skin_type'] = reviewer_skin_type
        items['reviewer_skin_tone'] = reviewer_skin_tone

        yield items


if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(SephoraComSpider)
    process.start()
