import scrapy
from scrapy.crawler import CrawlerProcess
import json
import re

from vii_sephora_com.i_sephora_com.spiders.locators import Locators
from vii_sephora_com.i_sephora_com.items import SephoraComItem


class SephoraComSpider(scrapy.Spider):
    name = 'sephora_com'
    start_urls = ['https://www.sephora.com/shop/skincare']

    custom_settings = {
        # 'ITEM_PIPELINES': {
        #     'vii_sephora_com.i_sephora_com.pipelines.SephoraComPipeline': 300
        # },
        'FEED_EXPORT_BATCH_ITEM_COUNT': 10_000,
        'FEED_FORMAT': 'csv',
        'FEED_URI': f"../../iii_results/%(batch_id)02d-{'_'.join(re.findall(r'[A-Z][^A-Z]*', __qualname__)[:-1]).lower()}.csv",
        'FEED_EXPORT_FIELDS': [
            'product_name',
            'product_url',
            'product_id',
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

    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip,deflate,br",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Host": "api.bazaarvoice.com",
        "Origin": "https",
        "Pragma": "no-cache",
        "Referer": "https",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "User-Agent": "Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/87.0.4280.141Safari/537.36"
    }

    def parse(self, response, **kwargs):
        do_not_needed_categories = ['BB & CC Creams', 'Beauty Supplements', 'Facial Rollers', 'For Face', 'For Body',
                                    'Facial Cleansing Brushes', 'Hair Removal', 'Anti-Aging', 'Teeth Whitening']

        product_categories = response.xpath(Locators.PRODUCT_CATEGORIES)
        # for product_category in product_categories[0:1]:
        for product_category in product_categories:
            product_category_path = product_category.xpath(Locators.PRODUCT_CATEGORY_PATH).get()
            category = product_category.xpath(Locators.CATEGORY).get()
            if category not in do_not_needed_categories:
                category_url = f'https://www.sephora.com{product_category_path}?currentPage=1'
                yield scrapy.Request(url=category_url,
                                     callback=self.second_requests,
                                     cb_kwargs={'category': category})

    def second_requests(self, response, **kwargs):
        products = response.xpath(Locators.PRODUCTS)
        # for product in products[1:2]:
        for product in products:
            product_path = product.xpath(Locators.PRODUCT_PATH).get()
            product_url = f'https://www.sephora.com{product_path}'

            yield scrapy.Request(url=product_url, callback=self.parse_item,
                                 cb_kwargs={'category': kwargs['category']})

        products_amount = int(re.search(r'(\d+)', response.xpath(Locators.PRODUCTS_AMOUNT).get()).group(1))
        pages = products_amount // 60 + 1 if products_amount / 60 > products_amount // 60 else products_amount // 60
        current_page = int(re.search(r'(\d+)', response.url).group(1))
        if pages > current_page:
            next_products_url = f'{response.url[:-1]}{current_page + 1}'

            yield scrapy.Request(url=next_products_url, callback=self.second_requests,
                                 cb_kwargs={'category': kwargs['category']})

    def parse_item(self, response, **kwargs):
        raw_data = response.xpath(Locators.RAW_DATA).get()
        data = json.loads(raw_data)

        product_name = data['page']['product']['productDetails']['brand']['displayName']
        product_id = data['page']['product']['currentSku']['skuId']
        product_url = response.url
        item_id = data['page']['product']['productDetails']['productId']
        reviews_amount = int(data['page']['product']['productDetails']['reviews'])
        price = data['page']['product']['currentSku']['listPrice'].split('$')[1]

        try:
            description = data['page']['product']['productDetails']['longDescription']

            description = re.sub(r'</?b>', '', description)
            description = re.sub(r'</?strong>', '', description)
            description = re.sub(r'<br ?/?>', '\n', description)

            skin_type = ''.join(
                re.findall(r'(?<=Skin Type:)\s?\s?(.*)\.?', description)) if 'Skin Type:' in description else None
            skincare_concerns = ''.join(re.findall(r'(?<=Skincare Concerns:)\s?\s?(.*)\.?',
                                                   description)) if 'Skincare Concerns:' in description else None
            what_it_is = ''.join(
                re.findall(r'(?<=What it is:)\s?\s?(.*)\.?', description)) if 'What it is:' in description else None

            oils_free = re.findall(r'[Oo]il[-\ns.,! ]', description)
            if not oils_free:
                oil_free = None
            else:
                for oil in oils_free:
                    if oil in description:
                        oil_free = 'yes'
                        break
                    else:
                        oil_free = None

            parabens_free = re.findall(r'[Pp]araben[-\ns.,! ]', description)
            if not parabens_free:
                paraben_free = None
            else:
                for paraben in parabens_free:
                    if paraben in description:
                        paraben_free = 'yes'
                        break
                    else:
                        paraben_free = None

            sulfates_free = re.findall(r'[Ss]ulfate[-\ns.,! ]', description)
            if not sulfates_free:
                sulfate_free = None
            else:
                for sulfate in sulfates_free:
                    if sulfate in description:
                        sulfate_free = 'yes'
                        break
                    else:
                        sulfate_free = None

            glutens_free = re.findall(r'[Gg]luten[-\ns.,! ]', description)
            if not glutens_free:
                gluten_free = None
            else:
                for gluten in glutens_free:
                    if gluten in description:
                        gluten_free = 'yes'
                        break
                    else:
                        gluten_free = None

            silicones_free = re.findall(r'[Ss]ilicone[-\ns.,! ]', description)
            if not silicones_free:
                silicone_free = None
            else:
                for silicone in silicones_free:
                    if silicone in description:
                        silicone_free = 'yes'
                        break
                    else:
                        silicone_free = None

            vegans = re.findall(r'[Vv]egan[-\ns.,! ]', description)
            if not vegans:
                vegan = None
            else:
                for vegan in vegans:
                    if vegan in description:
                        vegan = 'yes'
                        break
                    else:
                        vegan = None

        except:
            skin_type = None
            skincare_concerns = None
            what_it_is = None
            oil_free = None
            paraben_free = None
            sulfate_free = None
            gluten_free = None
            silicone_free = None
            vegan = None

        iterations = reviews_amount // 100 + 1 if reviews_amount / 100 > reviews_amount // 100 else reviews_amount // 100
        # for i in range(0, 100, 100):
        for i in range(0, iterations * 100, 100):
            url = f'https://api.bazaarvoice.com/data/reviews.json?Filter=contentlocale%3Aen*&Filter=ProductId%3A{item_id}&Sort=SubmissionTime%3Adesc&Limit={100}&Offset={i}&Include=Products%2CComments&Stats=Reviews&passkey=caQ0pQXZTqFVYA1yYnnJ9emgUiW59DXA85Kxry8Ma02HE&apiversion=5.4&Locale=en_US'
            yield scrapy.Request(url=url, headers=self.headers, callback=self.parse_review,
                                 cb_kwargs={
                                     'product_name': product_name,
                                     'product_url': product_url,
                                     'product_id': product_id,
                                     'category': kwargs['category'],
                                     'oil_free': oil_free,
                                     'paraben_free': paraben_free,
                                     'sulfate_free': sulfate_free,
                                     'gluten_free': gluten_free,
                                     'silicone_free': silicone_free,
                                     'vegan': vegan,
                                     'price': price,
                                     'skin_type': skin_type,
                                     'skincare_concerns': skincare_concerns,
                                     'what_it_is': what_it_is,
                                 })

    @staticmethod
    def parse_review(response, **kwargs):
        items = SephoraComItem()

        data = json.loads(response.body)

        items_amount = len(data['Results'])
        # for review in range(0, 6):
        for review in range(items_amount):
            try:
                review_title = data['Results'][review]['Title']
            except:
                review_title = None
            try:
                number_of_stars = data['Results'][review]['Rating']
            except:
                number_of_stars = None
            try:
                review_description = data['Results'][review]['ReviewText']
            except:
                review_description = None
            try:
                reviewer_skin_type = data['Results'][review]['ContextDataValues']['skinType']['Value']
            except:
                reviewer_skin_type = None
            try:
                reviewer_skin_tone = data['Results'][review]['ContextDataValues']['skinTone']['Value']
            except:
                reviewer_skin_tone = None

            items['product_name'] = kwargs['product_name']
            items['product_url'] = kwargs['product_url']
            items['product_id'] = kwargs['product_id']
            items['category'] = kwargs['category']
            items['oil_free'] = kwargs['oil_free']
            items['paraben_free'] = kwargs['paraben_free']
            items['sulfate_free'] = kwargs['sulfate_free']
            items['gluten_free'] = kwargs['gluten_free']
            items['silicone_free'] = kwargs['silicone_free']
            items['vegan'] = kwargs['vegan']
            items['price'] = kwargs['price']
            items['skin_type'] = kwargs['skin_type']
            items['skincare_concerns'] = kwargs['skincare_concerns']
            items['what_it_is'] = kwargs['what_it_is']
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
