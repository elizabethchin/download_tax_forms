
import json
from bs4 import BeautifulSoup as bs
import requests


def create_json(form_name_requested):
    """Creates a JSON object of a specified form name. The object will return product number, title, and the max and min years the form is available for download"""

    if not form_name_requested:
        print("There is no input, please enter the form name.")
        return None

    index_of_first_row = 0

    # this will remove all whitespaces from input to prevent errors while searching url
    tax_form_name_requested = form_name_requested.replace(" ", "")

    # irs website with all the forms
    url = f"https://apps.irs.gov/app/picklist/list/priorFormPublication.html?indexOfFirstRow={index_of_first_row}&sortColumn=sortOrder&value={tax_form_name_requested}&criteria=formNumber&resultsPerPage=200&isDescending=false"

    # get a response object from the url
    response = requests.get(url)

    # text obtained from response
    html = response.content
    soup = bs(html, "lxml")

    # get maximum index to prevent out of range error during pagination
    max_index = soup.find_all(class_=["ShowByColumn"])[0].get_text(strip=True)
    max_index = max_index.split()[-2].strip(",")
    max_index = int(max_index.replace(',', ''))

    # result dictionary for form requested
    results = {"form_number": None,
               "form_title": None,
               "min_year": float("inf"),
               "max_year": float("-inf")}

    # keep track of all the years the form was available for
    years_list = []

    # iterate through the pages of results
    while index_of_first_row < max_index:

        # get list of product numbers, titles, and years
        product_numbers = soup.find_all("td", class_="LeftCellSpacer")
        titles = soup.find_all("td", class_="MiddleCellSpacer")
        years = soup.find_all("td", class_="EndCellSpacer")

        # iterate through list of product numbers
        for i, product_number in enumerate(product_numbers):

            # this is to make sure product_number has no whitespaces so you're able to compare to user input
            product_number = product_number.get_text(strip=True)
            strip_product_number = product_number.replace(" ", "")

            # check if form is the same as what the user requested, use casefold to eliminate problems with capitalization
            if strip_product_number.casefold() == tax_form_name_requested.casefold():
                results["form_number"] = product_number
                results["form_title"] = titles[i].get_text(strip=True)
                year = years[i].get_text(strip=True)
                years_list.append(float(year))
                results["min_year"] = min(years_list)
                results["max_year"] = max(years_list)

        index_of_first_row += 25

    # create JSON object
    json_dump = json.dumps(results)
    json_object = json.loads(json_dump)
    return(json_object)

# print(create_json("FormW-2"))


def list_of_tax_form_objects(list_of_tax_forms):
    """Creates a list of JSON objects of tax forms."""

    if not list_of_tax_forms:
        print("There is no input.")
        return None

    elif type(list_of_tax_forms) != list:
        print("Input is not a list please try again.")
        return None

    results = []

    for form in list_of_tax_forms:
        result = create_json(form)
        results.append(result)

    return results

# print(list_of_tax_form_objects(["Form W-2", "Form 11-C", "Form 1095-C"]))
# print(list_of_tax_form_objects(""))
# print(list_of_tax_form_objects("form W-2"))
# print(list_of_tax_form_objects([" form  W-2"]))
