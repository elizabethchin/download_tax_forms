import os
from bs4 import BeautifulSoup as bs
import requests


def download_pdfs(tax_form_name_input, range_of_years_input):

    """Downloads tax form pdfs from specified range of years."""

    if not tax_form_name_input or not range_of_years_input:
        print("One or more input is missing, please try again.")
        return None


    # convert range_of_years input to a list of all the years
    range_of_years = range_of_years_input
    range_of_years = range_of_years.split("-")
    range_of_years = (list(range(int(range_of_years[0]), int(range_of_years[1]) + 1)))

    index_of_first_row = 0

    tax_form_name_requested = tax_form_name_input

    # remove all whitespaces in input
    url_tax_form_name_requested = tax_form_name_requested.replace(" ", "")

    url = f"https://apps.irs.gov/app/picklist/list/priorFormPublication.html?indexOfFirstRow={index_of_first_row}&sortColumn=sortOrder&value={url_tax_form_name_requested}&criteria=formNumber&resultsPerPage=200&isDescending=false"


    #get a response object from the url
    response = requests.get(url)

    #text obtained from response
    html = response.content
    soup = bs(html, "lxml")

    #get maximum index to prevent out of range error during pagination
    max_index = soup.find_all(class_=["ShowByColumn"])[0].get_text(strip=True)
    max_index = max_index.split()[-2].strip(",")
    max_index = int(max_index.replace(',', ''))

    # dictionary of pdfs by year
    results = {}

    #iterate through the pages of results
    while index_of_first_row < max_index:

        # get list of product numbers and years
        product_numbers = soup.find_all("td", class_="LeftCellSpacer")
        years = soup.find_all("td", class_="EndCellSpacer")

        #iterate through list of product numbers 
        for i, product_number in enumerate(product_numbers):
            product_number_text = product_number.get_text(strip=True)
            product_number_links = product_number.find_all("a", href=True)

            # use casefold to eliminate problems with capitalization
            if product_number_text.casefold() == tax_form_name_requested.casefold():
                
                #iterate through list of links and append link and year to dictionary
                for link in product_number_links:
                    years[i] = years[i].get_text(strip=True)
                    results[years[i]] = link["href"]

        index_of_first_row += 25


    #create subdirectory 
    if not os.path.exists(tax_form_name_requested):
        os.makedirs(tax_form_name_requested)

    #iterate through input range of years and retrieve pdf link from dictionary
    for year in range_of_years:

        #get pdf link
        pdf_url = results[str(year)]

        #get response object
        response = requests.get(pdf_url)
        year = str(year)

        #create pdf file
        pdf = open(tax_form_name_requested + "/" + tax_form_name_requested + " - " + str(year) + ".pdf", "wb")
        pdf.write(response.content)
        pdf.close()
    print(tax_form_name_requested + " " + range_of_years_input + " PDFs downloaded")

    return os.path.exists(tax_form_name_requested)


# print(download_pdfs("Form W-2", "2018-2020"))
# print(download_pdfs("", ""))