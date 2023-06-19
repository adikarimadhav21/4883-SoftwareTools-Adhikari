import PySimpleGUI as sg
import pandas as pd
import datetime
from display_form  import displayForm

def buildWeatherurl(filter,airport,year,month,day):
    """
    Combine all params with base url and return full url
    :param filter: selected option of daily,weekly, monthly
    :param airport: selected airport code
    :param year: selected year
    :param month: selected month
    :param day:  selected day
    :return: url
    """
    base_url = "https://wunderground.com/history"

    # build the url to scrape weather from
    url = f"{base_url}/{filter}/{airport}/date/{year}-{month}-{day}"
    return url;


def inputForm():
    """
       Create a input form using PySimpleGUI.
          Args:
              N/A.
          Returns:
              N/A
    """
    #read airports code file using pandas
    df=pd.read_json("Assignments/A07/airports.json")
    df = df.sort_values(by=["country", "icao"])

    # Define the range of values for the date dropdowns and filters
    months = list(range(1, 12))
    days = list(range(1, 32))
    years = list(range(2000, 2023))
    filters = ["daily", "weekly", "monthly"]

    # Get the current date for default placeholder in form fields
    current_date = datetime.datetime.now()
    current_month = current_date.month
    current_day = current_date.day
    current_year = current_date.year

    # Define the width of the dropdowns
    dropdown_width = 40
    text_width = 12

    # Set the theme and color scheme
    #sg.theme("DarkAmber")
    sg.theme("LightBrown3")
    

    text_color = "black"
    button_color = ("white", "dark green")
    cancel_color = ("white", "red")

    # Create the PySimpleGUI layout
    layout = [
        [sg.Text("Select a Airport:",size=(text_width, 1), text_color=text_color), sg.Combo([f"{row['icao']}, {row['city']}, {row['country']}" for _, row in df.iterrows()],
                                             default_value="KDFW, Dallas-Fort Worth, United States",
                                             key="-CODE-", size=(dropdown_width, 1), text_color=text_color)],
        [sg.Text("Select a month:",size=(text_width, 1), text_color=text_color), sg.Combo(months, default_value=current_month, key="-MONTH-", size=(dropdown_width, 1), text_color=text_color)],
        [sg.Text("Select a day:",size=(text_width, 1), text_color=text_color), sg.Combo(days, default_value=current_day, key="-DAY-", size=(dropdown_width, 1), text_color=text_color)],
        [sg.Text("Select a year:",size=(text_width, 1), text_color=text_color), sg.Combo(years, default_value=current_year, key="-YEAR-", size=(dropdown_width, 1), text_color=text_color)],
        [sg.Text("Select a filter:",size=(text_width, 1), text_color=text_color), sg.Combo(filters, default_value="daily", key="-FILTER-", size=(dropdown_width, 1), text_color=text_color)],
        [sg.Button("Submit", button_color=button_color),sg.Button("Cancel", button_color=cancel_color)]

    ]

    # Create the PySimpleGUI window
    window = sg.Window("URL Selection", layout)

    # Event loop
    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == "Cancel":
            break

        if event == "Submit":
            selected_code = values["-CODE-"]
            selected_month = values["-MONTH-"]
            selected_day = values["-DAY-"]
            selected_year = values["-YEAR-"]
            selected_filter = values["-FILTER-"]

            # Split the selected city into its components
            selected_airport_code,selected_city, selected_country = selected_code.split(", ")

            # Print the selected options
            print(f"Airport: {selected_city.strip()}")
            print(f"Country: {selected_country.strip()}")
            print(f"Airport Code: {selected_airport_code.strip()}")
            print(f"Date: {selected_month}/{selected_day}/{selected_year}")
            print(f"Filter: {selected_filter}")
            #Call buildWeatherurl function to build the url to scrape weather from
            selected_url= buildWeatherurl(selected_filter, selected_airport_code, selected_year, selected_month, selected_day)
            print(selected_url)
            # The data display is different format for daily and weekly or monthly so create a flag which is used later
            flag= True if selected_filter=="daily" else False
            """
            Call displayForm function to get all data and display in output GUI
            """
            displayForm(selected_url,flag)

    # Close the window
    window.close()
