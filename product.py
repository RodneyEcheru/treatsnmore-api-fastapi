from fastapi import APIRouter

import database
import country
import category

from sql import sql

api = APIRouter(
    prefix="/product",
    tags=["product"],
    responses={404: {"message": "Request for a valid resource"}}
)


def convert_product_attributes_to_int(product):
    if product['business_id'] is not None:
        product['business_id'] = int(product['business_id'])
    product['country_id'] = int(product['country_id'])

    if product['inventory'] is not None and product['inventory']:
        product['inventory'] = int(product['inventory'])
        product['availability'] = "available" if product['inventory'] > 0 else "out_of_stock"
    else:
        product['availability'] = "out_of_stock"

    if product['inventory_price'] is not None and product['inventory_price']:
        product['inventory_price'] = int(product['inventory_price'])

    if product['discount_price'] is not None and product['discount_price']:
        product['discount_price'] = int(product['discount_price'])
    if product['secondary_product_category_id'] is not None and product['secondary_product_category_id']:
        product['secondary_product_category_id'] = int(product['secondary_product_category_id'])
    if product['product_category_parent'] is not None:
        product['product_category_parent'] = int(product['product_category_parent'])

    # set selling price depending on discount status
    product['selling_price'] = product['discount_price'] if product['discount_price'] != 0 else product['inventory_price']
    return product


def attach_image_gallery_to_product(product, product_images):
    product['image_gallery'] = []
    for image in product_images:
        if int(image['product_id']) == int(product['product_id']):
            product['image_gallery'].append(image)
    return product


def attach_secondary_category_to_product(product, categories):
    if product['secondary_product_category_id']:
        product['secondary_product_category'] = next((item for item in categories if int(item['product_category_id']) == int(product['secondary_product_category_id'])), False)
    return product


def attach_parent_category_to_product(product, categories):
    if product['product_category_parent'] is not None:
        product['product_category_parent'] = next((item for item in categories if int (item['product_category_id']) == int(product['product_category_parent'])), False)
    return product


def attach_subscription_to_product(product, subscription_packages, subscription_frequencies):
    subscription_package = next((item for item in subscription_packages if item['product_line'] == product['product_line']), None)
    if subscription_package is not None:
        subscription_frequency = next((frequency for frequency in subscription_frequencies if int(frequency['subscription_frequency_id']) == int(subscription_package['subscription_frequency_id'])), None)

        if subscription_frequency is not None:
            product['subscription'] = True
            product['subscription_frequency'] = subscription_frequency['subscription_frequency']
            product['subscription_minimum'] = subscription_package['minimum_quantity']
            product['product_subscription_line'] = subscription_package['product_line']
            product['subscription_maximum'] = subscription_package['maximum_quantity']
            product['maximum_subscription_period'] = subscription_package['maximum_subscription_period']
        else:
            product['subscription'] = False
    else:
        product['subscription'] = False
    return product


def format_products(products_object):
    if len(products_object['products']) > 0:
        for product in products_object['products']:

            # format integer properties of products
            product = format_product(product, products_object)

    return products_object['products']


def format_product(product, product_object):

    # format integer properties of products
    product = convert_product_attributes_to_int(product)

    # attach image gallery to product
    product = attach_image_gallery_to_product(product, product_object['product_images'])

    # attach secondary category to product
    product = attach_secondary_category_to_product(product, product_object['category_details'])

    # attach parent category to product
    product = attach_parent_category_to_product(product, product_object['category_details'])

    # attach subscription details to product
    product = attach_subscription_to_product(product, product_object['subscription_packages'], product_object['subscription_frequencies'])

    return product


def format_plain_products(products_object):
    if len(products_object['products']) > 0:
        for product in products_object['products']:
            # format integer properties of products
            product = convert_product_attributes_to_int(product)

    return products_object['products']


async def latest_products(country_name: str, total_product_count: int):
    # country details
    country_details = await country.country_details_by_name(country_name)

    if country_details is not None:
        country_id = country_details['country_id']

        # all products
        sql_statement = sql()
        table = 'inventory'
        statement = sql_statement.select(table).join('inner', table, 'product_id', 'product', 'product_id').join(
            'inner',
            'product',
            'product_category_id',
            'product_category',
            'product_category_id').where().id(
            'country_id', country_id).order_by('product.timestamp', 'DESC').limit(total_product_count).sql_string

        # get all products
        products = await database.orm_async(table, statement, 'list')

        # format all products / add necessary attributes

        # products_object to be used for adding necessary attributes to products
        products_object = {
            'products': products
        }
        products = format_plain_products(products_object)

        return products

    return {
        'State': 'Country details not found'
    }


async def get_product(product_id: int, product_object: dict):

    # country details
    country_id = product_object['country_details']['country_id']

    # get product
    sql_statement = sql()
    table = 'inventory'
    statement = sql_statement.select(table).join(
        'inner', table, 'product_id', 'product', 'product_id').join(
        'inner',
        'product',
        'product_category_id',
        'product_category',
        'product_category_id').where().id(
        'country_id', country_id).and_().id(
        'product.product_id', product_id
    ).sql_string

    # get product details from database
    product = await database.orm_async(table, statement, 'dictionary')

    # format product / add necessary attributes
    # products_object to be used for adding necessary attributes to product
    product_object['products'] = product

    # format single product
    product = format_product(product, product_object)

    return product


async def get_plain_product(product_id: int, country_name: str):

    # get country product_details
    country_details = await country.country_details_by_name(country_name)

    # check if country registered
    if country_details is None:
        return False
    else:

        # country details
        country_id = country_details['country_id']

        product_images = await category.all_product_images()

        # get product
        sql_statement = sql()
        table = 'inventory'
        statement = sql_statement.select(table).join(
            'inner', table, 'product_id', 'product', 'product_id').join(
            'inner',
            'product',
            'product_category_id',
            'product_category',
            'product_category_id').where().id(
            'country_id', country_id).and_().id(
            'product.product_id', product_id
        ).sql_string

        # get product details from database
        product = await database.orm_async(table, statement, 'dictionary')

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
        product_object = {'country_details': country_details, 'product_images': product_images,
                          'category_details': all_categories_db, 'subscription_packages': subscription_packages,
                          'subscription_frequencies': subscription_frequencies, 'products': product}

        # format single product
        product = format_product(product, product_object)

        return product


async def get_product_line_products(product_line: str, product_object: dict):

    # country details
    country_id = product_object['country_details']['country_id']

    # get product
    sql_statement = sql()
    table = 'inventory'
    statement = sql_statement.select(table).join(
        'inner', table, 'product_id', 'product', 'product_id').join(
        'inner',
        'product',
        'product_category_id',
        'product_category',
        'product_category_id').where().id(
        'country_id', country_id).and_().id(
        'product.product_line', product_line
    ).sql_string

    # get product details from database
    products = await database.orm_async(table, statement, 'list')

    product_object['products'] = products

    # format product / add necessary attributes
    products = format_products(product_object)

    return products


async def get_similar_products(product_category_id: int, product_object: dict):

    # country details
    country_id = product_object['country_details']['country_id']

    # get products
    sql_statement = sql()
    table = 'inventory'
    statement = sql_statement.select(table).join(
        'inner', table, 'product_id', 'product', 'product_id').join(
        'inner',
        'product',
        'product_category_id',
        'product_category',
        'product_category_id').where().id(
        'country_id', country_id).and_().id(
        'product.product_category_id', product_category_id
    ).sql_string

    # get product details from database
    products = await database.orm_async(table, statement, 'list')

    product_object['products'] = products

    products = format_products(product_object)

    return products


async def create_pagination(total_item_count: int, items_per_page: int, current_page_number: int, product_category_id: int, limit: int, offset: int):

    # get total number of pages
    total_number_of_pages = -(-total_item_count // items_per_page)

    # if current page is greater than total pages
    if current_page_number > total_number_of_pages:
        current_page_number = total_number_of_pages

    # if if current page is less than first page
    if current_page_number < 1:
        current_page_number = 1

    # the offset of the list, based on current page
    # list_offset = (current_page_number - 1) * items_per_page

    # find minimum pagination number
    middle_number = current_page_number
    upper_limit = total_number_of_pages
    lower_limit = 0

    # numbers on each side of current page in pagination (centered current page in pagination)
    numbers_on_each_side = 2

    # find minimum number
    minimum_generated = 0
    minimum_number = middle_number
    while minimum_generated < numbers_on_each_side:
        if minimum_number > (lower_limit + 1):
            minimum_number -= 1
            minimum_generated += 1
        else:
            break

    # numbers to carry forward
    forward = 0
    if minimum_generated != numbers_on_each_side:
        forward = numbers_on_each_side - minimum_generated

    # find max
    maximum_generated = 0
    maximum_number = middle_number
    while maximum_generated < numbers_on_each_side:
        if maximum_number <= (upper_limit - 1):
            maximum_number += 1
            maximum_generated += 1
        else:
            break

    # numbers to carry backward
    backward = 0
    if maximum_generated != numbers_on_each_side:
        backward = numbers_on_each_side - maximum_generated

    # carry backward
    carried_over = 0
    while carried_over < backward:
        if minimum_number > (lower_limit + 1):
            minimum_number -= 1
            carried_over += 1
        else:
            break

    # carry forward
    carried_over = 0
    while carried_over < forward:
        if maximum_number < (upper_limit - 1):
            maximum_number += 1
            carried_over += 1
        else:
            break

    # generate page array
    page_array = []

    if total_item_count > 0:
        while minimum_number <= maximum_number:
            page_array.append(minimum_number)
            minimum_number += 1

    pagination_list = []

    if current_page_number > 1:
        pagination_list.append({
            'active_state': False,
            'link': f'/category/{product_category_id}/{limit}/{offset - limit}/{current_page_number - 1}',
            'type': 'previous',
            'text': 'prev'
        })

        if minimum_number > 1:
            pagination_list.append({
                'active_state': False,
                'link': f'/category/{product_category_id}/{limit}/0/1',
                'type': 'number',
                'text': '1',
            })
            pagination_list.append({
                'active_state': False,
                'link': '#',
                'type': 'dots',
                'text': '...',
            })

    pagination_list.append({
        'active_state': False,
        'link': '#',
        'type': 'plain',
        'text': f'{current_page_number} / {total_number_of_pages}',
    })

    for page_number in page_array:
        if page_number == current_page_number:

            # active state for current page
            pagination_list.append({
                'active_state': True,
                'link': '#',
                'type': 'number',
                'text': current_page_number
            })
        else:
            # links to other pages
            pagination_list.append({
                'active_state': False,
                'link': f'/category/{product_category_id}/{limit}/{page_number * limit - limit}/{page_number}',
                'type': 'number',
                'text': page_number
            })

    if current_page_number != total_number_of_pages:

        if maximum_number < total_number_of_pages:
            pagination_list.append({
                'active_state': False,
                'link': '#',
                'type': 'dots',
                'text': '...',
            })
            pagination_list.append({
                'active_state': False,
                'link': f'/category/{product_category_id}/{limit}/{total_number_of_pages * limit - limit}/{total_number_of_pages}',
                'type': 'number',
                'text': total_number_of_pages,
            })

        pagination_list.append({
            'active_state': False,
            'link': f'/category/{product_category_id}/{limit}/{offset + limit}/{current_page_number + 1}',
            'type': 'next',
            'text': 'next'
        })
    return pagination_list


async def get_category_products_with_pagination(product_category_id: int, product_object: dict, limit: int, offset: int, current_page_number: int):

    # country details
    country_id = product_object['country_details']['country_id']

    # get products
    sql_statement = sql()
    table = 'inventory'
    statement = sql_statement.select(table).join(
        'inner', table, 'product_id', 'product', 'product_id').join(
        'inner',
        'product',
        'product_category_id',
        'product_category',
        'product_category_id').where().id(
        'country_id', country_id).and_().id(
        'product.product_category_id', product_category_id
    ).order_by('product.product_id', 'DESC').paginate(offset, limit).sql_string

    sql_statement = sql()
    product_count_statement = sql_statement.custom_select(f'count(*) AS product_count', table).join(
        'inner', table, 'product_id', 'product', 'product_id').join(
        'inner',
        'product',
        'product_category_id',
        'product_category',
        'product_category_id').where().id(
        'country_id', country_id).and_().id(
        'product.product_category_id', product_category_id
    ).sql_string

    # get product count details from database
    products = await database.orm_async(table, statement, 'list')
    product_count = await database.orm_async(table, product_count_statement, 'dictionary')

    product_pagination = await create_pagination(product_count['product_count'], limit, current_page_number, product_category_id, limit, offset)

    product_object['products'] = products

    products = format_products(product_object)

    return {'products': products, 'pagination': product_pagination}


@api.get("/")
def welcome():
    return {
        "message": "You have reached products endpoint, define resources to serve you with",
        "status": "info",
        "data_status": False
    }


# latest products by country
@api.get("/{country_name}/{total_product_count}")
async def latest_products_route(country_name: str, total_product_count: int):

    return await latest_products(country_name, total_product_count)


# latest products by country
@api.get("/get/{product_id}/{country_name}")
async def single_product(product_id: int, country_name: str):

    return await get_plain_product(product_id, country_name)
