from fastapi import APIRouter

import requests
import country
import navbar
import translate
import category
import brand
import database
import website
import urllib.parse
from sql import sql

api = APIRouter(
    prefix="/rwandaui",
    tags=["rwandaui"],
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


async def page(preferred_language: str, application_page: str):

    # load product module
    import product

    # check if requesting for language translation
    changelanguage = language_change(preferred_language)

    # get results from new api

    # -- contact info
    new_contact_info = await country.country_profile('kenya')

    # -- navbar links
    navbar_links = await navbar.menu('kenya')

    # -- website profile information
    website_profile = await website.async_profile('kenya')

    # -- universal sections for all pages

    # top bar
    support_number = new_contact_info['phone'] if 'phone' in new_contact_info else ''

    # top bar
    navbar_links_results = navbar_links if navbar_links else False

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
                    'text': 'Track Your Order',
                    'link': '#',
                },
                {
                    'text': 'Services',
                    'link': '#',
                },
                {
                    'text': 'Terms & Conditions',
                    'link': '#',
                },
                {
                    'text': 'Security Policies',
                    'link': '#',
                },
                {
                    'text': 'About Us',
                    'link': '#',
                },
                {
                    'text': 'FAQs',
                    'link': '#',
                },
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
            'content': 'Nairobi Office Kogo Plaza, Ground Floor, Suite 1 Nairobi, Kenya.',
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
        'copyright': 'All rights reserved. Made byCreatex Studio'
    }

    # determine if translation required
    # translate if need be translated
    # return result to client

    # get current language
    # check if requesting for language translation

    # declare common variables

    # top bar
    track_order_text = 'Track your order'

    # support text
    support_text = 'Support'

    # home page
    if application_page == 'home':
        slideshow = [
            {
                'image': '/img/demo/shop-homepage/hero/01.png',
                'title': 'Outdoor HD Cloud Security Camera',
                'description': 'Stay connected 24/7. Free trial for 30 days',
                'button_text': 'Get now - rw 20',
                'button_link': '#',
                'key': 0
            },
            {
                'image': '/img/demo/shop-homepage/hero/02.png',
                'title': 'Running Sneakers Sports Collection',
                'description': 'Run like never before. Money back guarantee',
                'button_text': 'Get now - rw 35',
                'button_link': '#',
                'key': 1
            },
            {
                'image': '/img/demo/shop-homepage/hero/03.png',
                'title': 'Wireless Virtual Reality Headset',
                'description': 'Experience gaming like never before. Money back guarantee',
                'button_text': 'Get now - rw 20',
                'button_link': '#',
                'key': 2
            },
        ]
        adcarousel = [
            {
                'image': '/img/shop/categories/01.jpg',
                'title': 'Clothing',
                'button_text': 'From rw 8.99',
                'button_link': '#',
                'key': 0
            },
            {
                'image': '/img/shop/categories/02.jpg',
                'title': 'Electronics',
                'button_text': 'From rw 14.99',
                'button_link': '#',
                'key': 1
            },
            {
                'image': '/img/shop/categories/03.jpg',
                'title': 'Accessories',
                'button_text': 'From rw 5.99',
                'button_link': '#',
                'key': 2
            },
            {
                'image': '/img/shop/categories/04.jpg',
                'title': 'Kids',
                'button_text': 'From rw 7.99',
                'button_link': '#',
                'key': 4
            },
        ]
        home_products = await category.home_category_products('Kenya', 4)
        # print(product)
        latest_products = await product.latest_products('Kenya', 4)
        all_brands = await brand.all_brands()
        limited_ad = {
            'image': '/img/demo/shop-homepage/banner.png',
            'title': 'Virtual Reality',
            'description': 'Gadgets from top brands at discounted price',
            'adtext': 'Limited time offer',
            'expirydate': '10/01/2021 07:00:00 PM',
            'buttontext': 'Get one now',
            'buttonlink': '#',
        }
        # results needed for home page

        # navbar links
        # rwanda slideshow banner
        # rwanda home category links
        # groceries
        # promotional banner
        # magazines
        # shop by brand
        # create our stores endpoint
        # create terms of use by country
        # useful links by country

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

    # translate if need be

    if preferred_language == 'fr':
        translation_list = [{'track_order_text': track_order_text}, {'support_text': support_text}]

        # translate footer
        translation_list.append({footer['stores']['title']: footer['stores']['title']})
        for content in footer['stores']['contents']:
            translation_list.append({content['text']: content['text']})
        translation_list.append({footer['links']['title']: footer['links']['title']})
        for content in footer['links']['contents']:
            translation_list.append({content['text']: content['text']})
        translation_list.append({footer['subscription']['title']: footer['subscription']['title']})
        translation_list.append({footer['subscription']['name']: footer['subscription']['name']})
        translation_list.append({footer['subscription']['email']: footer['subscription']['email']})
        translation_list.append({footer['subscription']['subscribe']: footer['subscription']['subscribe']})
        translation_list.append({footer['subscription']['description']: footer['subscription']['description']})
        translation_list.append({footer['company']['title']: footer['company']['title']})
        translation_list.append({footer['company']['content']: footer['company']['content']})
        translation_list.append({footer['contact']['title']: footer['contact']['title']})
        translation_list.append({footer['contact']['phone']: footer['contact']['phone']})
        translation_list.append({footer['contact']['email']: footer['contact']['email']})
        translation_list.append({footer['guarantee']['delivery']['title']: footer['guarantee']['delivery']['title']})
        translation_list.append(
            {footer['guarantee']['delivery']['description']: footer['guarantee']['delivery']['description']})
        translation_list.append({footer['guarantee']['money']['title']: footer['guarantee']['money']['title']})
        translation_list.append(
            {footer['guarantee']['money']['description']: footer['guarantee']['money']['description']})
        translation_list.append({footer['guarantee']['support']['title']: footer['guarantee']['support']['title']})
        translation_list.append(
            {footer['guarantee']['support']['description']: footer['guarantee']['support']['description']})
        translation_list.append({footer['guarantee']['online']['title']: footer['guarantee']['online']['title']})
        translation_list.append(
            {footer['guarantee']['online']['description']: footer['guarantee']['online']['description']})
        translation_list.append({footer['copyright']: footer['copyright']})

        # translate home page

        if application_page == 'home':
            # home page

            # translate slideshow
            if slideshow is not None:

                index = 0

                while index < len(slideshow):
                    for item in slideshow:
                        translation_list.append({item['title']: item['title']})
                        translation_list.append({item['description']: item['description']})
                        translation_list.append({item['button_text']: item['button_text']})

                        index += 1

            # translate adcarousel
            if adcarousel is not None:

                index = 0

                while index < len(adcarousel):
                    for item in adcarousel:
                        translation_list.append({item['title']: item['title']})
                        translation_list.append({item['button_text']: item['button_text']})

                        index += 1

            # translate home_products
            if home_products is not None:
                for main_category in home_products:
                    translation_list.append({main_category['product_category']: main_category['product_category']})
                    if main_category['sub_categories'] is not None:
                        for sub_category in main_category['sub_categories']:
                            translation_list.append(
                                {sub_category['product_category']: sub_category['product_category']})
                    if main_category['products'] is not None:
                        for product in main_category['products']:
                            translation_list.append({product['product_line']: product['product_line']})
                            translation_list.append({product['product']: product['product']})
                            translation_list.append({product['product_description']: product['product_description']})
                            translation_list.append({product['product_category']: product['product_category']})

            # translate home_products
            if latest_products is not None:
                for product in latest_products:
                    translation_list.append({product['product_line']: product['product_line']})
                    translation_list.append({product['product']: product['product']})
                    translation_list.append({product['product_description']: product['product_description']})
                    translation_list.append({product['product_category']: product['product_category']})

            # translate ad
            if limited_ad is not None:
                translation_list.append({limited_ad['title']: limited_ad['title']})
                translation_list.append({limited_ad['description']: limited_ad['description']})
                translation_list.append({limited_ad['adtext']: limited_ad['adtext']})
                translation_list.append({limited_ad['buttontext']: limited_ad['buttontext']})

        if application_page == 'notfound':
            # error text 404 page
            translation_list.append({'error_text': error_text})
            translation_list.append({'notfound_text': notfound_text})
            translation_list.append({'notfound_description': notfound_description})
            translation_list.append({'home_text': home_text})
            translation_list.append({'try_text': try_text})
            translation_list.append({'search_text': search_text})

        if navbar_links_results is not None:

            # translate main navbar such as Media Hub
            for i in range(len(navbar_links_results)):

                translation_list.append(
                    {navbar_links_results[i]['product_category']: navbar_links_results[i]['product_category']})

                # translate main sub category such as News stand
                if navbar_links_results[i]['sub_categories'] is not None:
                    for ims in range(len(navbar_links_results[i]['sub_categories'])):

                        translation_list.append({navbar_links_results[i]['sub_categories'][ims]['product_category']:
                                                     navbar_links_results[i]['sub_categories'][ims][
                                                         'product_category']})

                        # translate sub category such as Current Affairs & Business
                        if navbar_links_results[i]['sub_categories'][ims]['sub_categories'] is not None:
                            for imss in range(len(navbar_links_results[i]['sub_categories'][ims]['sub_categories'])):
                                translation_list.append({navbar_links_results[i]['sub_categories'][ims][
                                                             'sub_categories'][imss]['product_category']:
                                                             navbar_links_results[i]['sub_categories'][ims][
                                                                 'sub_categories'][imss]['product_category']})

        # translate array of lists
        translation_list = await translate.translate_array('fr', translation_list)

        # update text translations

        # update track_order_text
        track_order_text = await update_with_translation('track_order_text', translation_list)

        # update support_text
        support_text = await update_with_translation('support_text', translation_list)

        # translate footer
        footer['stores']['title'] = await update_with_translation(footer['stores']['title'], translation_list)
        for content in footer['stores']['contents']:
            content['text'] = await update_with_translation(content['text'], translation_list)
        footer['links']['title'] = await update_with_translation(footer['links']['title'], translation_list)
        for content in footer['links']['contents']:
            content['text'] = await update_with_translation(content['text'], translation_list)
        footer['subscription']['title'] = await update_with_translation(footer['subscription']['title'],
                                                                        translation_list)
        footer['subscription']['name'] = await update_with_translation(footer['subscription']['name'], translation_list)
        footer['subscription']['email'] = await update_with_translation(footer['subscription']['email'],
                                                                        translation_list)
        footer['subscription']['subscribe'] = await update_with_translation(footer['subscription']['subscribe'],
                                                                            translation_list)
        footer['subscription']['description'] = await update_with_translation(footer['subscription']['description'],
                                                                              translation_list)
        footer['company']['title'] = await update_with_translation(footer['company']['title'], translation_list)
        footer['company']['content'] = await update_with_translation(footer['company']['content'], translation_list)
        footer['contact']['title'] = await update_with_translation(footer['contact']['title'], translation_list)
        footer['contact']['phone'] = await update_with_translation(footer['contact']['phone'], translation_list)
        footer['contact']['email'] = await update_with_translation(footer['contact']['email'], translation_list)
        footer['guarantee']['delivery']['title'] = await update_with_translation(
            footer['guarantee']['delivery']['title'], translation_list)
        footer['guarantee']['delivery']['description'] = await update_with_translation(
            footer['guarantee']['delivery']['description'], translation_list)
        footer['guarantee']['money']['title'] = await update_with_translation(footer['guarantee']['money']['title'],
                                                                              translation_list)
        footer['guarantee']['money']['description'] = await update_with_translation(
            footer['guarantee']['money']['description'], translation_list)
        footer['guarantee']['support']['title'] = await update_with_translation(footer['guarantee']['support']['title'],
                                                                                translation_list)
        footer['guarantee']['support']['description'] = await update_with_translation(
            footer['guarantee']['support']['description'], translation_list)
        footer['guarantee']['online']['title'] = await update_with_translation(footer['guarantee']['online']['title'],
                                                                               translation_list)
        footer['guarantee']['online']['description'] = await update_with_translation(
            footer['guarantee']['online']['description'], translation_list)
        footer['copyright'] = await update_with_translation(footer['copyright'], translation_list)

        # update home page translations
        if application_page == 'home':
            # home page

            # translate slideshow
            if slideshow is not None:

                index = 0

                while index < len(slideshow):
                    for item in slideshow:
                        slideshow[index]['title'] = await update_with_translation(slideshow[index]['title'],
                                                                                  translation_list)
                        slideshow[index]['description'] = await update_with_translation(slideshow[index]['description'],
                                                                                        translation_list)
                        slideshow[index]['button_text'] = await update_with_translation(slideshow[index]['button_text'],
                                                                                        translation_list)

                        index += 1

            # translate adcarousel
            if adcarousel is not None:

                index = 0

                while index < len(adcarousel):
                    for item in adcarousel:
                        adcarousel[index]['title'] = await update_with_translation(adcarousel[index]['title'],
                                                                                   translation_list)
                        adcarousel[index]['button_text'] = await update_with_translation(
                            adcarousel[index]['button_text'], translation_list)

                        index += 1

            # translate home_products
            if home_products is not None:
                for main_category in home_products:
                    main_category['product_category'] = await update_with_translation(main_category['product_category'],
                                                                                      translation_list)
                    if main_category['sub_categories'] is not None:
                        for sub_category in main_category['sub_categories']:
                            sub_category['product_category'] = await update_with_translation(
                                sub_category['product_category'], translation_list)
                    if main_category['products'] is not None:
                        for product in main_category['products']:
                            product['product_line'] = await update_with_translation(product['product_line'],
                                                                                    translation_list)
                            product['product'] = await update_with_translation(product['product'], translation_list)
                            product['product_description'] = await update_with_translation(
                                product['product_description'], translation_list)
                            product['product_category'] = await update_with_translation(product['product_category'],
                                                                                        translation_list)

            # translate home_products
            if latest_products is not None:
                for product in latest_products:
                    product['product_line'] = await update_with_translation(product['product_line'], translation_list)
                    product['product'] = await update_with_translation(product['product'], translation_list)
                    product['product_description'] = await update_with_translation(product['product_description'],
                                                                                   translation_list)
                    product['product_category'] = await update_with_translation(product['product_category'],
                                                                                translation_list)

            # translate ad
            if limited_ad is not None:
                limited_ad['title'] = await update_with_translation(limited_ad['title'], translation_list)
                limited_ad['description'] = await update_with_translation(limited_ad['description'], translation_list)
                limited_ad['adtext'] = await update_with_translation(limited_ad['adtext'], translation_list)
                limited_ad['buttontext'] = await update_with_translation(limited_ad['buttontext'], translation_list)

        # update error page translations
        if application_page == 'notfound':
            # update error text 404 page
            error_text = await update_with_translation('error_text', translation_list)
            notfound_text = await update_with_translation('notfound_text', translation_list)
            notfound_description = await update_with_translation('notfound_description', translation_list)
            home_text = await update_with_translation('home_text', translation_list)
            try_text = await update_with_translation('try_text', translation_list)
            search_text = await update_with_translation('search_text', translation_list)

        # update navbar_links_results
        if navbar_links_results is not None:

            # translate main navbar such as Media Hub
            for i in range(len(navbar_links_results)):
                navbar_links_results[i]['product_category'] = await update_with_translation(
                    navbar_links_results[i]['product_category'], translation_list)

                # translate main sub category such as News stand
                if navbar_links_results[i]['sub_categories'] is not None:
                    for ims in range(len(navbar_links_results[i]['sub_categories'])):
                        navbar_links_results[i]['sub_categories'][ims][
                            'product_category'] = await update_with_translation(
                            navbar_links_results[i]['sub_categories'][ims]['product_category'], translation_list)

                        # translate sub category such as Current Affairs & Business
                        if navbar_links_results[i]['sub_categories'][ims]['sub_categories'] is not None:
                            for imss in range(len(navbar_links_results[i]['sub_categories'][ims]['sub_categories'])):
                                navbar_links_results[i]['sub_categories'][ims]['sub_categories'][imss][
                                    'product_category'] = await update_with_translation(
                                    navbar_links_results[i]['sub_categories'][ims]['sub_categories'][imss][
                                        'product_category'], translation_list)

    # return response to client
    page_object = {
        'changelanguage': changelanguage,
        'preferred_language': preferred_language,
        'topbar': {
            'support_text': support_text,
            'support_number': support_number,
            'track_order_text': track_order_text
        },
        'navbar': navbar_links_results,
        'footer': footer
    }

    if application_page == 'home':
        page_object['slideshow'] = slideshow
        page_object['adcarousel'] = adcarousel
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

    return page_object


@api.get("/")
def welcome():
    return {
        "status": "info",
        "message": "You have reached the treatsnmore rwanda ui api api, specify the resources I can serve you",
        "data_status": False
    }


# page to display
@api.get("/{preferred_language}/{application_page}")
async def page_route(preferred_language: str, application_page: str):
    return await page(preferred_language, application_page)


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
