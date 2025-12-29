from fastapi import APIRouter
from typing import Optional

import requests
import country
import navbar
import category
import database
import website
from sql import sql
from pprint import pprint

api = APIRouter(
    prefix="/ugandaui",
    tags=["ugandaui"],
    responses={404: {"message": "Request for a valid resource"}}
)


# compare strings ( languages )
def language_change(translation_language: str):
    return translation_language != 'en'  # return comparison


# define get request
async def make_get_request(url):
    response = requests.get(url)  # make api call
    return response.json()  # json decode response


# define get request
async def make_post_request(url, post_dictionary):
    response = requests.post(url, data=post_dictionary)  # make api call

    return response.json()  # json decode response


# compare strings ( languages )
def language_detect(language_abbreviation: str):
    return {
        'en': 'english',
        'fr': 'french'
    }.get(language_abbreviation, None)


# handle page requests
async def page(application_page: str, product_id: int = None, country_name: str = None, product_category_id: int = None,
               limit: int = None, offset: int = None, current_page_number: int = None, brand_id: int = None,
               brand_name: str = None, category_offset: int = 0, category_limit: int = 0):
    # test if mysql database connection is online / running
    database_connection = database.test_mysql_connection()

    if database_connection is False:
        return {'database_connection_offline': 'offline'}

    # load product module
    import product
    import brand

    # get results from new api

    # -- contact info
    new_contact_info = await country.country_profile('kenya')

    # -- navbar links
    # navbar_links = await navbar.menu('kenya')

    # -- website profile information
    website_profile = await website.async_profile('kenya')

    # -- universal sections for all pages

    # top bar
    support_number = new_contact_info[
        'phone'] if 'phone' in new_contact_info else '0789879074 - Airtel. 011442243 - Safaricom.'

    # top bar
    # navbar_links_results = navbar_links if navbar_links else False

    # footer
    footer = {
        'stores': {
            'title': 'Stores',
            'contents': [
                {
                    'text': 'Uganda',
                    'link': 'https://treatsnmore.ug',
                },
                {
                    'text': 'Kenya',
                    'link': 'https://treatsnmore.ke',
                },
                {
                    'text': 'Tanzania',
                    'link': 'https://treatsnmore.co.tz',
                },
                {
                    'text': 'Rwanda',
                    'link': 'https://treatsnmore.rw',
                },
                {
                    'text': 'Africa',
                    'link': 'https://treatsnmore.africa',
                },
            ]
        },
        'links': {
            'title': 'Links',
            'contents': [
                {
                    'text': 'About Us',
                    'link': '/about',
                },
                {
                    'text': 'Security Policies',
                    'link': '/security',
                },
                {
                    'text': 'FAQs',
                    'link': '/faqs',
                },
                {
                    'text': 'Terms and conditions',
                    'link': '/terms',
                }
            ]
        },
        'subscription': {
            'title': 'Stay Informed',
            'name': 'Your Name',
            'email': 'Your Email',
            'subscribe': 'Subscribe',
            'description': 'Subscribe to our newsletter to receive early discount offers, updates and new products info.',
        },
        'company': {
            'title': "Location",
            'content': 'TNP House, Plot 328, Block22, Kiwatule - Ntinda.',
        },
        'contact': {
            'title': website_profile['name'],
            'phone': website_profile['phone'],
            'email': website_profile['email'],
        },
        'guarantee': {
            'delivery': {
                'title': 'Fast and free delivery',
                'description': 'Free delivery for all orders over $200',
            },
            'money': {
                'title': 'Money back guarantee',
                'description': 'We return money within 30 days',
            },
            'support': {
                'title': '24/7 customer support',
                'description': 'Friendly 24/7 customer support',
            },
            'online': {
                'title': 'Secure online payment',
                'description': 'We possess SSL / Secure сertificate',
            },
        },
        'copyright': "All rights reserved. Treats 'N More"
    }

    """
    {
        'text': 'Terms & Conditions',
        'link': 'javascript:',
    },
    """
    """
    
                {
                    'text': 'Track Your Order',
                    'link': 'javascript:',
                },
                {
                    'text': 'Services',
                    'link': 'javascript:',
                },
                """

    # declare common variables

    # top bar
    track_order_text = 'Track your order'

    # support text
    support_text = 'Support'

    # home page
    if application_page == 'home':
        slideshow = {
            'products': [
                {
                    'image': 'https://api.treatsnmore.ug/img/banner/29.png',
                    'title': 'Buy your groceries - Free Delivery ',
                    'description': 'Zoobedooz Ribbons Fizzy Cherry',
                    'button_text': 'Get now @ rf 20',
                    'button_link': '/product/240',
                    'key': 0
                },
                {
                    'image': 'https://api.treatsnmore.ug/img/banner/31.png',
                    'title': 'Browse our spice collection',
                    'description': 'Garam Masala',
                    'button_text': 'Get now @ rf 35',
                    'button_link': '/product/431',
                    'key': 1
                },
                {
                    'image': 'https://api.treatsnmore.ug/img/banner/34.jpeg',
                    'title': 'Get yourself a tropical with a twist',
                    'description': 'Tropical With A Twist',
                    'button_text': 'Get now @ rf 20',
                    'button_link': '/product/223',
                    'key': 2
                },
            ],
            'banners': [
                {
                    'image': 'https://api.treatsnmore.ug/img/others/2.png',
                    'title': 'A world of chocolate with',
                    'description': 'Nougat',
                    'sub_text': 'Choose from a variety',
                    'button_text': 'Get now',
                    'button_link': '/brand/Amarula/8/0/1',
                    'key': 0
                },
                {
                    'image': 'https://api.treatsnmore.ug/img/others/3.jpg',
                    'title': 'Party at home with',
                    'description': 'Amarula',
                    'sub_text': 'Products',
                    'button_text': 'Get now',
                    'button_link': '/brand/Amarula/8/0/1',
                    'key': 0
                },
            ]
        }
        adcarousel = [
            {
                'image': 'https://api.treatsnmore.ug/img/banner/26.png',
                'title': 'Tea',
                'button_text': 'From rf 8.99',
                'button_link': '#',
                'key': 0
            },
            {
                'image': 'https://api.treatsnmore.ug/img/banner/27.jpg',
                'title': 'Chocolate Nibbles',
                'button_text': 'From rf 14.99',
                'button_link': '#',
                'key': 1
            },
            {
                'image': 'https://api.treatsnmore.ug/img/banner/28.jpg',
                'title': 'Amarula',
                'button_text': 'From rf 5.99',
                'button_link': 'http://localhost:3333/brand/Amarula/8/0/1',
                'key': 2
            },
            {
                'image': 'https://api.treatsnmore.ug/img/banner/30.png',
                'title': 'Gift Boxes',
                'button_text': 'From rf 7.99',
                'button_link': '#',
                'key': 4
            },
        ]
        home_products = await category.home_category_products('uganda', 8, category_offset, category_limit)
        # print(product)
        latest_products = await product.latest_products('uganda', 4)
        all_brands = await brand.all_brands()
        limited_ad = {
            'image': 'https://api.treatsnmore.ug/img/banner/34.png',
            'title': 'Chocolate Promo',
            'description': 'Amarula - Fudge Choc Coated 108G',
            'adtext': 'Limited time offer',
            'expirydate': '10/01/2022 07:00:00 PM',
            'buttontext': 'Get one now',
            'buttonlink': '/product/199',
            'days': '24',
            'hours': '8',
            'mins': '54',
        }

    # product page
    if application_page == 'product':

        # get country product_details
        country_details = await country.country_details_by_name(country_name)

        if country_details is None:
            product_details = None
            product_lines = None
            similar_products = None
            product_lines_total = 0
            product_lines_has_more = False
            product_lines_next_offset = None
            product_line_name = None
        else:
            # get product details

            # product images
            product_images = await category.all_product_images()

            # all category details
            all_categories_db = await category.all_categories()

            # all subscription packages for specific country
            sql_statement = sql()
            table = 'subscription_package_new'
            country_id_string = str(country_details['country_id'])
            subscription_packages_sql = sql_statement.select(table).where().json_id(table, 'country_id',
                                                                                    country_id_string).sql_string
            subscription_packages = await database.orm_async(table, subscription_packages_sql, 'list')

            # all subscription frequencies
            sql_statement = sql()
            table = 'subscription_frequency'
            subscription_frequency_sql = sql_statement.select(table).sql_string
            subscription_frequencies = await database.orm_async(table, subscription_frequency_sql, 'list')

            # format product / add necessary attributes
            # products_object to be used for adding necessary attributes to product
            product_object = {
                'country_details': country_details,
                'product_images': product_images,
                'category_details': all_categories_db,
                'subscription_packages': subscription_packages,
                'subscription_frequencies': subscription_frequencies,
            }

            product_details = await product.get_product(product_id, product_object)
            # Use paginated version for product_lines (initial load: 8 products)
            product_line_name = product_details['product_line']
            product_lines_dict = await product.get_product_line_products_with_pagination(
                product_line_name, product_object, limit=8, offset=0)
            product_lines = product_lines_dict['products']
            product_lines_total = product_lines_dict['total_count']
            product_lines_has_more = product_lines_dict['has_more']
            product_lines_next_offset = product_lines_dict['next_offset']
            similar_products = await product.get_similar_products(product_details['product_category_id'],
                                                                  product_object)

    # category page
    if application_page == 'category':

        # get country product_details
        country_details = await country.country_details_by_name(country_name)

        if country_details is None:
            category_products = None
            category_page_brands = None
            product_pagination = None
            category_total_count = 0
            category_has_more = False
            category_next_offset = None
        else:
            # get brands
            category_page_brands = await brand.all_brands()

            # get product details

            # product images
            product_images = await category.all_product_images()

            # all category details
            all_categories_db = await category.all_categories()

            # all subscription packages for specific country
            sql_statement = sql()
            table = 'subscription_package_new'
            country_id_string = str(country_details['country_id'])
            subscription_packages_sql = sql_statement.select(table).where().json_id(table, 'country_id',
                                                                                    country_id_string).sql_string
            subscription_packages = await database.orm_async(table, subscription_packages_sql, 'list')

            # all subscription frequencies
            sql_statement = sql()
            table = 'subscription_frequency'
            subscription_frequency_sql = sql_statement.select(table).sql_string
            subscription_frequencies = await database.orm_async(table, subscription_frequency_sql, 'list')

            # format product / add necessary attributes
            # products_object to be used for adding necessary attributes to product
            product_object = {
                'country_details': country_details,
                'product_images': product_images,
                'category_details': all_categories_db,
                'subscription_packages': subscription_packages,
                'subscription_frequencies': subscription_frequencies,
            }

            category_products_dict = await product.get_category_products_with_pagination(product_category_id,
                                                                                         product_object, limit, offset,
                                                                                         current_page_number)
            category_products = category_products_dict['products']
            product_pagination = category_products_dict['pagination']
            # Infinite scroll metadata
            category_total_count = category_products_dict['total_count']
            category_has_more = category_products_dict['has_more']
            category_next_offset = category_products_dict['next_offset']

    # category page
    if application_page == 'brand':

        # get country product_details
        country_details = await country.country_details_by_name(country_name)

        # get all brands
        all_brands = await brand.all_brands()

        if country_details is None:
            brand_products = None
            category_page_brands = None
            product_pagination = None
        else:
            # get brands
            category_page_brands = await brand.all_brands()

            # get product details

            # product images
            product_images = await category.all_product_images()

            # all category details
            all_categories_db = await category.all_categories()

            # all subscription packages for specific country
            sql_statement = sql()
            table = 'subscription_package_new'
            country_id_string = str(country_details['country_id'])
            subscription_packages_sql = sql_statement.select(table).where().json_id(table, 'country_id',
                                                                                    country_id_string).sql_string
            subscription_packages = await database.orm_async(table, subscription_packages_sql, 'list')

            # all subscription frequencies
            sql_statement = sql()
            table = 'subscription_frequency'
            subscription_frequency_sql = sql_statement.select(table).sql_string
            subscription_frequencies = await database.orm_async(table, subscription_frequency_sql, 'list')

            # format product / add necessary attributes
            # products_object to be used for adding necessary attributes to product
            product_object = {
                'country_details': country_details,
                'product_images': product_images,
                'category_details': all_categories_db,
                'subscription_packages': subscription_packages,
                'subscription_frequencies': subscription_frequencies,
            }

            brand_products_dict = await brand.get_brand_products_with_pagination(brand_name, product_object, limit,
                                                                                 offset, current_page_number,
                                                                                 country_name)
            brand_products = brand_products_dict['products']
            product_pagination = brand_products_dict['pagination']

    # 404 page
    if application_page == 'notfound':
        # error text
        error_text = 'Error code: 404'
        notfound_text = 'Page not found!'
        notfound_description = 'It seems we can’t find the page you are looking for.'
        home_text = 'Go to homepage'
        try_text = 'Or try'
        search_text = 'Search'

        # results needed for 404 page

        # navbar links
        # shop by brand
        # create our stores endpoint
        # create terms of use by country
        # useful links by country

    # return response to client
    page_object = {
        'topbar': {
            'support_text': support_text,
            'support_number': support_number,
            'track_order_text': track_order_text
        },
        'navbar': [],
        'footer': footer
    }

    if application_page == 'product':
        page_object['product_page'] = product_details
        page_object['product_lines'] = product_lines
        page_object['similar_products'] = similar_products
        # Infinite scroll metadata for product_lines
        page_object['product_lines_total'] = product_lines_total
        page_object['product_lines_has_more'] = product_lines_has_more
        page_object['product_lines_next_offset'] = product_lines_next_offset
        page_object['product_line_name'] = product_line_name

    if application_page == 'category':
        page_object['category_products'] = category_products
        page_object['category_page_brands'] = category_page_brands
        page_object['product_pagination'] = product_pagination
        # Infinite scroll metadata
        page_object['total_count'] = category_total_count
        page_object['has_more'] = category_has_more
        page_object['next_offset'] = category_next_offset

    if application_page == 'brand':
        page_object['brand_products'] = brand_products
        page_object['category_page_brands'] = category_page_brands
        page_object['product_pagination'] = product_pagination
        page_object['brands'] = all_brands

    if application_page == 'home':
        page_object['slideshow'] = slideshow
        #page_object['adcarousel'] = adcarousel
        page_object['home_products'] = home_products
        page_object['latest_products'] = latest_products
        page_object['limited_ad'] = limited_ad
        page_object['brands'] = all_brands

    if application_page == 'notfound':
        page_object['notfound'] = {
            'error_text': error_text,
            'notfound_text': notfound_text,
            'notfound_description': notfound_description,
            'home_text': home_text,
            'try_text': try_text,
            'search_text': search_text,
        }

    if application_page == 'about':
        page_object['about'] = True

    if application_page == 'security':
        page_object['security'] = True

    if application_page == 'faqs':
        faqs_url = "https://api.treatsnmore.ug/faq/get_all_faqs"

        # Making a get request
        response = requests.get(faqs_url)

        # format response
        response = response.json()

        # return response
        page_object['faqs'] = response

    if application_page == 'terms':
        faqs_url = "https://api.treatsnmore.ug/term_and_condition/get_all_term_and_conditions"

        # Making a get request
        response = requests.get(faqs_url)

        # format response
        response = response.json()

        # return response
        page_object['terms'] = response

    if application_page == 'shopping_cart':
        page_object['shopping_cart'] = True

    return page_object


# API endpoint for loading more brand/product_line products (infinite scroll)
# NOTE: This route MUST be defined BEFORE the catch-all /{application_page} route
@api.get("/product_line_products")
async def product_line_products_route(product_line: str, country_name: str, limit: int = 8, offset: int = 0):
    """Fetch paginated products from the same brand/product line for infinite scroll"""
    import product

    # get country details
    country_details = await country.country_details_by_name(country_name)

    if country_details is None:
        return {'error': 'Country not found', 'products': [], 'has_more': False}

    # product images
    product_images = await category.all_product_images()

    # all category details
    all_categories_db = await category.all_categories()

    # all subscription packages for specific country
    sql_statement = sql()
    table = 'subscription_package_new'
    country_id_string = str(country_details['country_id'])
    subscription_packages_sql = sql_statement.select(table).where().json_id(table, 'country_id',
                                                                            country_id_string).sql_string
    subscription_packages = await database.orm_async(table, subscription_packages_sql, 'list')

    # all subscription frequencies
    sql_statement = sql()
    table = 'subscription_frequency'
    subscription_frequency_sql = sql_statement.select(table).sql_string
    subscription_frequencies = await database.orm_async(table, subscription_frequency_sql, 'list')

    # product object for formatting
    product_object = {
        'country_details': country_details,
        'product_images': product_images,
        'category_details': all_categories_db,
        'subscription_packages': subscription_packages,
        'subscription_frequencies': subscription_frequencies,
    }

    # Get paginated products
    result = await product.get_product_line_products_with_pagination(product_line, product_object, limit, offset)

    return result


@api.get("/")
def welcome():
    return {
        "status": "info",
        "message": "You have reached the treatsnmore rwanda ui api api, specify the resources I can serve you",
        "data_status": False
    }


# page to display
@api.get("/{application_page}")
async def page_route(application_page: str, category_offset: int = 0, category_limit: int = 0):
    return await page(application_page, category_offset=category_offset, category_limit=category_limit)


# page to display
@api.get("/page/{application_page}")
async def page_route_new(application_page: str, product_id: Optional[int] = None, country_name: Optional[str] = None,
                         product_category_id: Optional[int] = None, brand_id: Optional[int] = None,
                         brand_name: Optional[str] = None, limit: Optional[int] = None, offset: Optional[int] = None,
                         current_page_number: Optional[int] = None):
    # update global product page attributes
    if application_page == 'product':
        return await page(application_page, product_id=product_id, country_name=country_name)
    # update global product page attributes
    if application_page == 'category':
        return await page(application_page, product_category_id=product_category_id, country_name=country_name,
                          limit=limit, offset=offset, current_page_number=current_page_number)
    if application_page == 'brand':
        return await page(application_page, brand_name=brand_name, country_name=country_name, limit=limit,
                          offset=offset, current_page_number=current_page_number)
    return {'detail': 'page not defined'}


async def update_with_translation(translation_key, translation_list):
    translate_index = 0
    match_found = False
    translation_text = 'Translation Not Matched'

    while translate_index < len(translation_list) and match_found is False:
        for translation_item in translation_list:
            for key, value in translation_item.items():
                if key == translation_key:
                    translation_text = value
                    match_found = True
            translate_index += 1
    return translation_text


# define api url
api_url = "https://api.treatsnmore.ug/"
local_api_url = "http://localhost:7012/"
