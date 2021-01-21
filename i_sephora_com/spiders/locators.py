class Locators:

    """Page 1"""
    
    # main locators
    CATEGORY = './text()'

    # additional locators
    PRODUCT_CATEGORIES = '//nav[@aria-label="Categories"]/div/div/a'
    PRODUCT_CATEGORY_PATH = './@href'

    """Page 2"""

    # main locators

    # additional locators
    PRODUCTS = '//div[@data-comp="ProductGrid "]//a'
    PRODUCT_PATH = './@href'
    PRODUCTS_AMOUNT = '//span[@data-at="number_of_products"]/text()'

    """Page 3"""

    # additional locators
    RAW_DATA = '//script[@id="linkStore"]/text()'
    # RAW_DATA_1 = '//div[@class="css-10bjc73 eanm77i0"]//text()'
    COMMENTS = '//div[@class="css-13o7eu2 eanm77i0"]'

