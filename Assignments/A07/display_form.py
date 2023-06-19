import PySimpleGUI as sg
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as BraveService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
#sg.set_options(font=("Arial Bold", 14))

def rendering(url):
    """Returns the page source HTML from a URL rendered by ChromeDriver.
          Args:
              url (str): The URL to get the page source HTML from.
          Returns:
              str: The page source HTML from the URL.
    """

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=BraveService(ChromeDriverManager(chrome_type=ChromeType.BRAVE).install()),
                              options=options) # run webdriver

    driver.get(url) # load the web page from the URL
    time.sleep(3) # wait  page to load data
    render = driver.page_source # get html content
    driver.quit()
    return render

def displayRecord( header, row):
    """
    Display data on tabular format
    :param header: header of table
    :param row: row datas
    :return: N/A
    """

    tbl1 = sg.Table(values=row, headings=header,
       auto_size_columns=True,
       display_row_numbers=False,
       justification='center', key='-TABLE-',
       selected_row_colors='red on yellow',
       enable_events=True,
       text_color='black',
       expand_x=True,
       expand_y=True,
       enable_click_events=True,
       )
    layout = [[tbl1]]
    window = sg.Window("Weather Observations ", layout, resizable=True)
    while True:
       event, values = window.read()
       if event == sg.WIN_CLOSED:
          break
       if '+CLICKED+' in event:
          sg.popup("You clicked row:{} Column: {}".format(event[2][0], event[2][1]))
    window.close()


def getHeaders(flag,soup):
    """
    Collect header for tables from html content
    :param flag: Ture for daily else false
    :param soup: html content
    :return: list of headers
    """
    thead = soup.find("thead")
    rows = thead.find_all("tr")
    # print(rows)
    headers = []
    for row in rows:
        cols = row.find_all("th") if flag else row.find_all("td")
        for col in cols:
            headers.append(col.text)

    # print(headers)
    return headers

def getRowDatas_Daily(soup):
    """
    This function for daily filter url
    Extract all required data from html content and display in GUI
    :param soup:  HTMl content
    :return: N/A
    """

    thead = soup.find("tbody") #get one tbody
    rows = thead.find_all("tr") #get all tr containing data
    # print(rows)
    rows_datas = [] #collect all row data

    for row in rows:
        cols = row.find_all("td") #get all td data for that row
        data = [] #collect all column data
        for col in cols:
            data.append(col.text)
        # print(data)
        rows_datas.append(data)
    """
    Call getHeaders function to get header for table 
    Call displayRecord to display data in table of GUI
    """
    displayRecord(getHeaders(True,soup), rows_datas)

def getRowDatas_Non_Daily(soup):
    """
    This functioned used for non daily that is monthly  or weekly url
    Extract the required data from html and display the datas in table of GUI
    :param soup:  html content
    :return: N/A
    """

    tbody = soup.find("tbody") # get one tbody
    rows = tbody.find("tr") # get tr of tbody
    # print(rows)
    tables = rows.find_all("table") # find all table containing data inside tr
    data_table = [] # collect all table datas
    for table in tables:
        rowss = table.find_all("tr")
        # print('+' * 20)
        # print(table)
        datas = []  #collect all rows data
        for r in rowss:
            # print(r)
            data = [] #collect all columns data
            colums = r.find_all("td")
            for col in colums:
                data.append(col.text)
            # print(data)

            datas.append(data)
        # print(datas)
        data_table.append(datas)
    # tbody - tr - td -table - tr- td
    # print(data_table)
    """
    Convert data_table list to required list to display the data in table
    - join multiple datas in one list  like  [ 'Max', 'Avg', 'Min'] to ['Max Avg Min' ]
    - Transpose rows to column as per our requirement to display data as per headers in html page
    """
    convert_table = []
    for row in data_table:
        converted_row = [' '.join(column) for column in row]
        convert_table.append(converted_row)

    # Pivot the convert_table to pivot_table using Zip
    pivot_table = [list(row) for row in zip(*convert_table)]
    #print(pivot_table)
    """
    Call getHeaders function to get header for table 
    Call displayRecord to display data in table of GUI
    """
    displayRecord(getHeaders(False,soup), pivot_table)


def displayForm(search_url,flag):
    """
    Using selenium obtained the async data sent back from selected wunderground url
    Used BS4 to parse the data and pull out the requested data.
    :param search_url: selected url
    :param flag: daily = true else false
    :return: N/A
    """
    #call function to get page data
    wunderground_page = rendering(search_url)
    #Parse data using BS4
    wunderground_soup = BeautifulSoup(wunderground_page, 'html.parser')
    #Filter data on the basis of need
    soup_container = wunderground_soup.find('lib-city-history-observation')
    """
    Call the function on the basis of flag : Daily or non daily  to extract the data and display in GUI
    """
    if flag:
        getRowDatas_Daily(soup_container)
    else:
        getRowDatas_Non_Daily(soup_container)