import requests
import pprint
from bs4 import BeautifulSoup
import json

page = requests.get("https://docs.google.com/spreadsheets/d/1npvD9XLzRR-PT6VDDTk2GlfBIoTSG8MzEdw5t0ynQ8A/pubhtml")

# https://docs.google.com/spreadsheets/d/e/2PACX-1vSJG6X_KHn0d_rlvbhJv-tfkyCPka2pOKKUDtT6qWmOVw-B8gPSeIMeRwXYNgsGg9vpfw9102mcbZax/pubhtml
# header = {
#     'header': 5,
#     'route': 2,
#     'dir': 3,
#     'days': 4,
#     'timer': 5,
#     'columns': 2,
# }

# https://docs.google.com/spreadsheets/d/1hViM_8Li6BQcAq5nT0E4aB982mdYP7hXIaCIYCpRdDU/pubhtml
    # None

# https://docs.google.com/spreadsheets/d/1npvD9XLzRR-PT6VDDTk2GlfBIoTSG8MzEdw5t0ynQ8A/pubhtml
meta = {
    'header': 5,
    'footer': 2,
    'route': 2,
    'dir': 3,
    'days': 4,
    'timer': 5,
    'columns': 1,
}

# https://docs.google.com/spreadsheets/d/1am7nqfA2HA4L_-YfZJUmKkdcv3wrrsg8Zc3iRxIjYgY/pubhtml
# meta = {
#     'header': 5,
#     'footer': 1,
#     'route': 2,
#     'dir': 3,
#     'days': 4,
#     'timer': 5,
#     'columns': 2,
# }

# ========================================================================

schedule = {}
if page.status_code == 200:
    print ("-- http request succeded --")

    # parse and find data
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find('tbody')
    rows = table.find_all('tr')

    # divde rows in to cells
    rows = [row.find_all('td') for row in rows]

    # filter out html
    rows = [[cell.string for cell in row] for row in rows]

    # get information
    schedule["route"]=rows[meta['route']-1][0]
    schedule["dir1"]=rows[meta['dir']-1][0]
    schedule["dir2"]=rows[meta['dir']-1][1]
    schedule["days"] = []
    for column in range(meta['columns']):
       schedule["days"].append(rows[meta['days']-1][column+1])

    # select only departures
    body = rows[meta['header']:-meta['footer']]
    schedule['courses'] = []

    # divide departures from diferent directions
    for row in body:
        for column in range(meta['columns']):
            schedule['courses'].append({
                'hour':row[0],
                'minute':row[1+column],
                'dir': schedule["dir1"],
                'route': schedule["route"],
                'days': schedule["days"][0+column],
            })
            schedule['courses'].append({
                'hour':row[1 + meta['columns']],
                'minute':row[2+column + meta['columns']],
                'dir': schedule["dir2"],
                'route': schedule["route"],
                'days': schedule["days"][0+column],
            })

    # correct departures with double minutes, empty and with strings
    for i, course in enumerate(schedule['courses']):
        # double minutes?
        if len(course['minute'].split(' '))>1:
            del schedule['courses'][i]
            for i,x in enumerate(course['minute'].split(' ')):
                # TODO: strings | before creating check if next is string
                # try:
                #     int(x)
                # except ValueError:
                #     print (x)

                schedule['courses'].append({
                    'hour':course['hour'],
                    'minute':x,
                    'dir': course['dir'],
                    'route': course['route'],
                    'days': course['days'],
                })
        # empty?
        if course['minute']=='-':
            del schedule['courses'][i]

    pprint.pprint(schedule)

    with open('data.json', 'w') as outfile:
        json.dump(schedule, outfile)

else:
    print ("-- couldn't resolve http request --")

print ("=== PROGMRAM END ===")