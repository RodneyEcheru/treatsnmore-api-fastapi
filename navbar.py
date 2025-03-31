from fastapi import APIRouter

import country
import inventory
import database
import urllib.parse
from sql import sql
import category

api = APIRouter(
    prefix="/navbar",
    tags=["navbar"],
    responses={404: {"message": "Request for a valid resource"}}
)


@api.get("/")
def welcome():
    return {
        "message": "You have reached navbar endpoint, define resources to serve you with",
        "status": "info",
        "data_status": False
    }


@api.get("/menu/{country_name}")
async def menu(country_name: str):
    # - get country details from database
    # - get inventory by country id
    # - get product details
    # - get product categories
    # - get navbar
    # process navbar to desired format and return

    navbar = {}

    # country details
    country_details = await country.country_details_by_name(country_name)

    if country_details is not None:

        # inventory details inventory_product_details = await
        # inventory.inventory_category_product_details_by_country_id(country_details['country_id'])

        # navbar['inventory_product_details'] = inventory_product_details

        # navbar details
        navbar_details = await navbar_hirachy()

        # convert navbar details id's into int's
        if navbar_details:

            # convert category id's into int's

            for i in range(len(navbar_details)):

                # main_category
                main_nv = int(navbar_details[i]['main_category'])

                # exclude media hub
                if main_nv != 100:

                    navbar_details[i]['main_category'] = main_nv

                    # sub_categories
                    for isn in range(len(navbar_details[i]['sub_categories'])):
                        isc_nv = int(navbar_details[i]['sub_categories'][isn])
                        navbar_details[i]['sub_categories'][isn] = isc_nv

                    # main_sub_categories
                    main_snv = int(navbar_details[i]['main_sub_category'])
                    navbar_details[i]['main_sub_category'] = main_snv

        # all category details
        all_categories = await category.all_categories()

        # navbar['navbar_all_categories'] = all_categories

        final_navbar = []

        if navbar_details:
            merged_navbar = await merge_navbar(navbar_details)

            for i in range(len(merged_navbar)):

                main_navbar_object = {}

                # get main category details
                for ica in range(len(all_categories)):
                    if all_categories[ica]['product_category_id'] == merged_navbar[i]['main_category']:
                        main_navbar_object = await category_body(merged_navbar[i]['main_category'], all_categories)

                        main_navbar_object['sub_categories'] = merged_navbar[i]['sub_categories']
                        main_navbar_object['main_sub_category'] = merged_navbar[i]['main_sub_category']

                        final_navbar.append(main_navbar_object)

                # get sub category details
                if main_navbar_object:
                    for isc in range(len(main_navbar_object['sub_categories'])):

                        sub_categories_object = {}

                        for ica in range(len(all_categories)):

                            if all_categories[ica]['product_category_id'] == main_navbar_object['sub_categories'][isc]:
                                sub_categories_object = await category_body(main_navbar_object['sub_categories'][isc],
                                                                            all_categories)

                                main_navbar_object['sub_categories'][isc] = sub_categories_object

                    # get main sub category details
                    for imsc in range(len(main_navbar_object['main_sub_category'])):

                        sub_categories_object = {}

                        for ica in range(len(all_categories)):

                            if all_categories[ica]['product_category_id'] == main_navbar_object['main_sub_category'][imsc]:
                                sub_categories_object = await category_body(
                                    main_navbar_object['main_sub_category'][imsc],
                                    all_categories)

                                main_navbar_object['main_sub_category'][imsc] = sub_categories_object

                    # filter all sub categories into corresponding trees
                    for imscs in range(len(main_navbar_object['main_sub_category'])):

                        sub_categories_object = []

                        for ica in range(len(main_navbar_object['sub_categories'])):

                            if main_navbar_object['sub_categories'][ica]['product_category_id'] == main_navbar_object['main_sub_category'][imscs]['product_category_parent']:
                                sub_categories_object.append(main_navbar_object['sub_categories'][ica])

                        # main_navbar_object['sub_categories'] = sub_categories_object

        # navbar['navbar_details_dump'] = merged_navbar
        navbar['navbar_details'] = final_navbar

        navbar_list = []

        if final_navbar:
            for ifn in range(len(final_navbar)):

                # main category in navbar e.g glossaries
                navbar_object = {
                    'product_category_id': final_navbar[ifn]['product_category_id'],
                    'product_category': final_navbar[ifn]['product_category'],
                    'product_category_parent': final_navbar[ifn]['product_category_parent'],
                    'sub_categories': []
                }

                for ifnm in range(len(final_navbar[ifn]['main_sub_category'])):

                    # main sub categories e.g confectionary
                    main_subcategory = final_navbar[ifn]['main_sub_category'][ifnm]

                    # navbar_object['sub_categories'].append(final_navbar[ifn]['main_sub_category'][ifnm])

                    main_subcategory['sub_categories'] = []

                    for ifnms in range(len(final_navbar[ifn]['sub_categories'])):

                        # sub categories e.g sugar confectionary

                        # create a while loop to also loop through deeply nested sub categories

                        if main_subcategory['product_category_id'] == final_navbar[ifn]['sub_categories'][ifnms]['product_category_parent']:
                            main_subcategory['sub_categories'].append(final_navbar[ifn]['sub_categories'][ifnms])
                        else:
                            required_id = main_subcategory['product_category_id']

                            temp_product_category_parent_id = final_navbar[ifn]['sub_categories'][ifnms]['product_category_parent']

                            match = False
                            while not match:

                                new_parent_category = next((item for item in all_categories if item['product_category_id'] == temp_product_category_parent_id), False)

                                if required_id == new_parent_category['product_category_parent']:
                                    main_subcategory['sub_categories'].append(final_navbar[ifn]['sub_categories'][ifnms])
                                    match = True
                                else:
                                    if new_parent_category['product_category_parent']:
                                        temp_product_category_parent_id = new_parent_category['product_category_parent']
                                    else:
                                        match = True

                    navbar_object['sub_categories'].append(main_subcategory)

                navbar_list.append(navbar_object)

    else:
        return False

    # get country details from database
    # get inventory by country id
    # get product images
    # get product details
    # get product subscriptions
    # get product categories
    # get navbar

    # get all product categories
    # get all products
    # get navbar

    # process navbar to desired format and return

    return navbar_list


async def navbar_hirachy():
    sql_statement = sql()
    table = 'navbar'

    statement = sql_statement.select(table).sql_string

    results = database.orm(table, statement, 'list')

    return results


async def merge_navbar(navbar_list):
    # create two copies of list for comparison purposes

    # assign property of status do_not_loop

    new_list = []

    list_copy = navbar_list.copy()

    for i in range(len(navbar_list)):

        if 'do_not_loop' not in navbar_list[i]:

            current_main_sub_category = navbar_list[i]['main_sub_category']
            del navbar_list[i]['main_sub_category']
            main_sub_category = [current_main_sub_category]

            for ic in range(len(list_copy)):

                if 'do_not_loop' not in list_copy[ic]:

                    if navbar_list[i]['main_category'] == list_copy[ic]['main_category']:

                        if 'main_sub_category' in list_copy[ic] and list_copy[ic]['main_sub_category'] not in main_sub_category:
                            main_sub_category.append(list_copy[ic]['main_sub_category'])

                        navbar_list[i]['sub_categories'] = navbar_list[i]['sub_categories'] + list(
                            set(list_copy[ic]['sub_categories']) - set(navbar_list[i]['sub_categories']))

                        list_copy[ic]['do_not_loop'] = True
                        navbar_list[ic]['do_not_loop'] = True

            navbar_list[i]['main_sub_category'] = main_sub_category

            new_list.append(navbar_list[i])

            navbar_list[i]['do_not_loop'] = True

    return new_list


async def category_body(category_id, all_categories):
    main_navbar_object = {}
    for ica in range(len(all_categories)):
        if all_categories[ica]['product_category_id'] == category_id:
            main_navbar_object['product_category_id'] = all_categories[ica]['product_category_id']
            main_navbar_object['product_category'] = all_categories[ica]['product_category']
            main_navbar_object['product_category_parent'] = all_categories[ica]['product_category_parent']

            return main_navbar_object

    return False
