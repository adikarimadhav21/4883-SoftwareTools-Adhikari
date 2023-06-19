
from input_form import inputForm

"""
Web Scraping:

Used PySimpleGui to create a data entry form that includes day, month, year, airport, and filter (daily,weekly,monthly)
Submit input form which will create the appropriate URL to query wunderground for the specified weather data.
Use selenium to obtain the async data sent back from wunderground.
Use BS4 to parse the data and pull out the requested data.
Finally, use PySimpleGui tabular view to display the data received from the initial request
"""

if __name__ == '__main__':
    """
    Call input GUI where we can entry data
    """
    inputForm()
