
from fastapi import APIRouter

import database
from sql import sql

api = APIRouter(
    prefix="/brand",
    tags=["brand"],
    responses={404: {"message": "Request for a valid resource"}}
)


async def create_brand_pagination(total_item_count: int, items_per_page: int, current_page_number: int, brand_name: str, limit: int, offset: int):

    # convert limit to int
    limit = int(limit)

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
            'link': f'/brand/{brand_name}/{limit}/{offset - limit}/{current_page_number - 1}',
            'type': 'previous',
            'text': 'prev'
        })

        if minimum_number > 1:
            pagination_list.append({
                'active_state': False,
                'link': f'/brand/{brand_name}/{limit}/0/1',
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
                'link': f'/brand/{brand_name}/{limit}/{page_number * limit - limit}/{page_number}',
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
                'link': f'/brand/{brand_name}/{limit}/{total_number_of_pages * limit - limit}/{total_number_of_pages}',
                'type': 'number',
                'text': total_number_of_pages,
            })

        pagination_list.append({
            'active_state': False,
            'link': f'/brand/{brand_name}/{limit}/{offset + limit}/{current_page_number + 1}',
            'type': 'next',
            'text': 'next'
        })
    return pagination_list


async def get_brand_products_with_pagination(brand_name: str, product_object: dict, limit: int, offset: int, current_page_number: int, country_name: str):

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
        'country_id', country_id).and_().id('product_line', brand_name).order_by('product.product_id', 'DESC').paginate(offset, limit).sql_string

    sql_statement = sql()
    product_count_statement = sql_statement.custom_select(f'count(*) AS product_count', table).join(
        'inner', table, 'product_id', 'product', 'product_id').join(
        'inner',
        'product',
        'product_category_id',
        'product_category',
        'product_category_id').where().id(
        'country_id', country_id).and_().id('product_line', brand_name).sql_string

    # get product count details from database
    products = await database.orm_async(table, statement, 'list')
    product_count = await database.orm_async(table, product_count_statement, 'dictionary')

    product_pagination = await create_brand_pagination(product_count['product_count'], limit, current_page_number, brand_name, limit, offset)

    product_object['products'] = products

    import product

    products = product.format_products(product_object)

    return {'products': products, 'pagination': product_pagination}


@api.get("/")
def welcome():
    return {
        "message": "You have reached brands endpoint, define resources to serve you with",
        "status": "info",
        "data_status": False
    }


@api.get("/all")
async def all_brands():

    # all brands
    sql_statement = sql()
    table = 'brand'
    statement = sql_statement.select(table).order_by('brand_id', 'DESC').sql_string

    # get all brands
    brands = await database.orm_async(table, statement, 'list')

    return brands

