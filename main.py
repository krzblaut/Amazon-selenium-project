"""Program lets its user to obtain products data in a specified category at Amazon.de"""

import time
import json
from scrapping import AmazonStat
from google_sheets import GoogleSheetsData


# Ranges of sponsored ads for the first and other pages
page1Ad = [range(5, 14), range(17,32)]
page2Ad = [range(5, 17), range(20,32)]

# Loading available categories from categories.json file.
with open('categories.json', 'r') as file:
    myfile = file.read()
cat = json.loads(myfile)

# Creating category list.
cat_list = []
for key in cat:
    cat_list.append(key)

# Showing available categories.
print("Available categories:")
for i in cat_list:
    print(i)

choice = int(input("Choose category you want to scan: "))
cat_url = cat[cat_list[choice-1]]

target = int(input("Enter page range: "))
scrap = AmazonStat(cat_url, target)
sheets = GoogleSheetsData()

CurrentPage = scrap.what_page()
while CurrentPage < target+1:
    if CurrentPage == 1:
        for i in range(2, 34):
            if i in page1Ad[0] or i in page1Ad[1]:
                sheets.insert_data_row(scrap.prod_click(i))
            else:
                sheets.insert_data_row(scrap.spons_prod_click(i))
        scrap.next_page()
    else:
        for i in range(2, 34):
            if i in page2Ad[0] or i in page2Ad[1]:
                sheets.insert_data_row(scrap.prod_click(i))
            else:
                sheets.insert_data_row(scrap.spons_prod_click(i))
        scrap.next_page()
    time.sleep(1)
    CurrentPage = scrap.what_page()+1

scrap.quit()
print("Scanning finished.")


