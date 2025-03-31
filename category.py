from fastapi import APIRouter

import database
import country
import product as product_class
from sql import sql

api = APIRouter(
    prefix="/category",
    tags=["category"],
    responses={404: {"message": "Request for a valid resource"}}
)


async def all_categories():
    sql_statement = sql()
    table = 'product_category'

    statement = sql_statement.select(table).sql_string

    results = database.orm(table, statement, 'list')

    if results:
        """
        remove media hub category
        new_categories = []
        for i in range(len(results)):
            if int(results[i]['product_category_id']) != 100:
                new_categories.append(results[i])

        results = new_categories
        """

        # convert some properties to integers
        for category in results:
            category['product_category_id'] = int(category['product_category_id'])
            category['business_id'] = int(category['business_id'])
            if category['product_category_parent']:
                category['product_category_parent'] = int(category['product_category_parent'])

        # filter out media hub categories
        """
        media_categories = []
        temporary_categories = results
        temporary_parents = [100]

        while len(temporary_parents) > 0:
            pass
        """

        # get media categories

    return results


async def all_product_images():
    sql_statement = sql()
    table = 'product_gallery'

    statement = sql_statement.select(table).sql_string

    results = database.orm(table, statement, 'list')

    if results:
        for i in range(len(results)):
            product_id = int(results[i]['product_id'])
            results[i]['product_id'] = product_id

    return results


def convert_product_attributes_to_int(product):
    return product_class.convert_product_attributes_to_int(product)


def attach_image_gallery_to_product(product, product_images):
    product['image_gallery'] = []
    for image in product_images:
        if int(image['product_id']) == product['product_id']:
            product['image_gallery'].append(image)
    return product


def attach_secondary_category_to_product(product, categories):
    if product['secondary_product_category_id']:
        product['secondary_product_category'] = next((item for item in categories if item['product_category_id'] == product['secondary_product_category_id']), False)
    return product


def attach_subscription_to_product(product, subscription_packages, subscription_frequencies):
    subscription_package = next((item for item in subscription_packages if item['product_line'] == product['product_line']), None)
    if subscription_package is not None:
        subscription_frequency = next((frequency for frequency in subscription_frequencies if frequency['subscription_frequency_id'] == int(subscription_package['subscription_frequency_id'])), None)

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
            product = convert_product_attributes_to_int(product)

            # attach image gallery to product
            product = attach_image_gallery_to_product(product, products_object['product_images'])

            # attach secondary category to product
            product = attach_secondary_category_to_product(product, products_object['category_details'])

            # attach subscription details to product
            product = attach_subscription_to_product(product, products_object['subscription_packages'], products_object['subscription_frequencies'])

    return products_object['products']


def create_home_product_hierarchy(products_dictionary):
    # create category hierarchy
    category_hierarchy = []

    # get all categories from database
    all_categories_db = products_dictionary['all_categories_db']
    products = products_dictionary['products']
    total_product_count = products_dictionary['total_product_count']

    # format categories if not empty
    if all_categories_db is not None:

        # get main categories
        category_hierarchy = [product_category for product_category in all_categories_db if
                              product_category['product_category_parent'] is None]

        # other categories with parent categories
        other_categories = [product_category for product_category in all_categories_db if
                            product_category['product_category_parent'] is not None]

        if category_hierarchy is not None:

            # create subcategories array for each main category
            for category_parent in category_hierarchy:
                category_parent['sub_categories'] = []

            # add each category to a main category
            for category in other_categories:

                # match_found = None
                parent_found = None
                temporary_category = category

                while parent_found is None:

                    # loop through main categories to find parent
                    for main_category in category_hierarchy:
                        if temporary_category['product_category_parent'] == main_category['product_category_id']:
                            main_category['sub_categories'].append(category.copy())
                            parent_found = True

                    # if parent not found
                    if parent_found is None:
                        for item in all_categories_db:
                            if temporary_category['product_category_parent'] == item['product_category_id']:
                                temporary_category = item
                                break

    # attach product details to category hierarchy
    category_hierarchy_object = {
        'products': products,
        'category_hierarchy': category_hierarchy,
        'total_product_count': total_product_count,
    }
    category_hierarchy = attach_products_to_category_hierarchy(category_hierarchy_object)

    # remove magazines from home page products
    for i in range(len(category_hierarchy)):
        if category_hierarchy[i]['product_category_id'] == 100:
            del category_hierarchy[i]
            break

    return category_hierarchy


def attach_products_to_category_hierarchy(category_hierarchy_object):

    products = category_hierarchy_object['products']  # get all products
    category_hierarchy = category_hierarchy_object['category_hierarchy']  # get categories

    # add products to main categories
    for category in category_hierarchy:
        category['products'] = []

        # limit products by unique category and total_product_count
        unique_category_ids = []
        product_limit = category_hierarchy_object['total_product_count']

        product_count = 0
        generic_product_count = 0
        while product_count < product_limit and generic_product_count < len(products):
            # get products from main categories
            for product in products:
                if product['product_category_id'] not in unique_category_ids and product['product_category_parent'] == category['product_category_id']:
                    if product_count != product_limit:
                        category['products'].append(product)
                        unique_category_ids.append(product['product_category_id'])
                        product_count += 1
                    else:
                        break
                generic_product_count += 1

            # get products from sub categories
            if category['sub_categories'] is not None:
                for sub_category in category['sub_categories']:
                    for product in products:
                        if product['product_category_id'] not in unique_category_ids and product['product_category_parent'] == sub_category['product_category_id']:
                            if product_count != product_limit:
                                category['products'].append(product)
                                unique_category_ids.append(product['product_category_id'])
                                product_count += 1
                            else:
                                break
                        generic_product_count += 1

    # return only categories with products
    new_category_hierarchy = []

    # filter categories with products
    for category in category_hierarchy:
        if len(category['products']) > 0:
            new_category_hierarchy.append(category)

    return new_category_hierarchy


@api.get("/")
def welcome():
    return {
        "message": "You have reached category endpoint, define resources to serve you with",
        "status": "info",
        "data_status": False
    }


@api.get("/category/{category_identifier}")
async def category_type(category_id):

    if category_id == 'all':
        return await all_categories()

    return {
        'category_type': id,
    }


@api.get("/{country_name}/{total_product_count}")
async def home_category_products(country_name: str, total_product_count: int):
    # global all_categories  # <-- access global function

    # country details
    country_details = await country.country_details_by_name(country_name)

    if country_details is not None:
        country_id = country_details['country_id']

        # all category details
        all_categories_db = await all_categories()

        # product images
        product_images = await all_product_images()

        # all subscription packages for specific country
        sql_statement = sql()
        table = 'subscription_package_new'
        country_id_string = str(country_id)
        subscription_packages_sql = sql_statement.select(table).where().json_id(table, 'country_id', country_id_string).sql_string
        subscription_packages = await database.orm_async(table, subscription_packages_sql, 'list')

        # all subscription frequencies
        sql_statement = sql()
        table = 'subscription_frequency'
        subscription_frequency_sql = sql_statement.select(table).sql_string
        subscription_frequencies = await database.orm_async(table, subscription_frequency_sql, 'list')

        # all products
        sql_statement = sql()
        table = 'inventory'
        statement = sql_statement.select(table).join('inner', table, 'product_id', 'product', 'product_id').join('inner',
                                                                                                                'product',
                                                                                                                'product_category_id',
                                                                                                                'product_category',
                                                                                                                'product_category_id').where().id(
            'country_id', country_id).order_by('product.timestamp', 'DESC').sql_string

        # get all products
        products = await database.orm_async(table, statement, 'list')

        # format all products / add necessary attributes

        # products_object to be used for adding necessary attributes to products
        products_object = {
            'products': products,
            'product_images': product_images,
            'category_details': all_categories_db,
            'subscription_packages': subscription_packages,
            'subscription_frequencies': subscription_frequencies,
        }
        products = format_products(products_object)

        # results = convert_product_attributes_to_int(results)

        # create dictionary of attributes
        products_dictionary = {
            'all_categories_db': all_categories_db,
            'products': products,
            'product_images': product_images,
            'subscription_packages': subscription_packages,
            'subscription_frequencies': subscription_frequencies,
            'total_product_count': total_product_count,
        }

        category_hierarchy = create_home_product_hierarchy(products_dictionary)

        # add products to categories

        return category_hierarchy

    return {
        'State': 'Country details not found'
    }

