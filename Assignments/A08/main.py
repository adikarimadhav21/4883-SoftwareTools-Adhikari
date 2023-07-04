from fastapi import FastAPI, HTTPException,Query
from fastapi.responses import JSONResponse
import uvicorn
import pandas as pd
from fastapi.responses import RedirectResponse


app = FastAPI()

# Load data from the CSV file
data = pd.read_csv('data.csv')

@app.get("/")
def get_documentation():
    """
    Retrieves the documentation provided by Swagger.

    """
    return RedirectResponse(url="/docs")
@app.get("/countries")
def get_countries():
    """
    This method will retrieves a list of unique countries'

    - **Params:**
      - None
    
    - **Returns:**
      - (object) : list of countries 

    #### Request Url Example:

    [http://127.0.0.1:8000/countries](http://127.0.0.1:8000/countries)

    #### Response boady Example:

        {
            "countries": [
                "Afghanistan",
                "Albania",
                "Algeria",
                "American Samoa"
                ],
            "success": True
        }
    
    """
    try:
        countries = data['Country'].unique().tolist()
        return {"countries": countries,"success": True}
    except Exception as e:
        return {"error": str(e),"success": False}

@app.get("/regions")
def get_regions():
    """
    This method will retrieves a list of available WHO regions
    - **Params:**
      - None
    
    - **Returns:**
      - (object) : list of regions 

    #### Request Url Example:

    [http://127.0.0.1:8000/regions](http://127.0.0.1:8000/regions)

    #### Response boady Example:

        {
        "regions": [
            "EMRO",
            "EURO",
            "AFRO",
            "WPRO",
            "AMRO",
            "SEARO",
            "Other"
        ],
        "success": true
        }
        
    """
    try:
        regions = data['WHO_region'].unique().tolist()
        return {"regions": regions,"success": True}
    except Exception as e:
        return {"error": str(e),"success": False}

@app.get("/deaths")
def get_total_deaths(country: str = Query(None), region: str = Query(None), year: int = Query(None)):
    """
    This method will return a total death count or can be filtered by country or region or year.
    - **Params:**
      - country (str) : A country name
      - region (str) : A region name
      - year (int) : A 4 digit year
    - **Returns:**
      - (int) : The total sum based on filters (if any)

    #### Request URL Example 1:

    [http://127.0.0.1:8000/deaths](http://127.0.0.1:8000/deaths)

    #### Response boady example 1:
        {
        "total_deaths": 6945714,
        "params": {
            "country": null,
            "region": null,
            "year": null
        },
        "success": true
        }
    #### Request URL Example 2:

    [http://127.0.0.1:8000/deaths?country=Nepal&year=2023](http://127.0.0.1:8000/deaths?country=Nepal&year=2023)

    #### Response boady example 2:

        {
        "total_deaths": 12,
        "params": {
            "country": "Nepal",
            "region": null,
            "year": 2023
        },
        "success": true
        }

    """
    try:
        remaining_data = data

        if country:
            remaining_data = remaining_data.loc[remaining_data['Country'] == country]
        
        if region:
            remaining_data = remaining_data.loc[remaining_data['WHO_region'] == region]
        
        if year:
            remaining_data = remaining_data.loc[remaining_data['Date_reported'].str.startswith(str(year))]

        #find total death
        total_deaths = remaining_data['New_deaths'].sum()
        death={
            "total_deaths":  int(total_deaths),
            "params": {
                    "country": country,
                    "region": region,
                    "year": year
                },
                "success": True,
            }

        return death
    except Exception as e:
        return {"error": str(e),"success": False,"params": {
                    "country": country,
                    "region": region,
                    "year": year
                }}


@app.get("/cases")
def get_total_cases(country: str = Query(None), region: str = Query(None), year: int = Query(None)):
    """
    This method will return a total new cases count or can be filtered by country or region or year.

    - **Params:**
      - country (str) : A country name
      - region (str) : A region name
      - year (int) : A 4 digit year
    - **Returns:**
      - (int) : The total sum based on filters (if any)

    #### Request URL Example 1:

    [http://127.0.0.1:8000/cases](http://127.0.0.1:8000/cases)

    #### Response boady example 1:
        {
        "total_cases": 768187096,
        "params": {
            "country": null,
            "region": null,
            "year": null
        },
        "success": true
        }
    #### Request URL Example 2:

    [http://127.0.0.1:8000/cases?country=Nepal&year=2023](http://127.0.0.1:8000/cases?country=Nepal&year=2023)

    #### Response boady example 2:

        {
        "total_cases": 2361,
        "params": {
            "country": "Nepal",
            "region": null,
            "year": 2023
        },
        "success": true
        }

    """
    try:
        remaining_data = data

        if country:
            remaining_data = remaining_data.loc[remaining_data['Country'] == country]
        
        if region:
            remaining_data = remaining_data.loc[remaining_data['WHO_region'] == region]
        
        if year:
            remaining_data = remaining_data.loc[remaining_data['Date_reported'].str.startswith(str(year))]

    # print(remaining_data)
    #sum new_casess to find total cases
        total_cases = remaining_data['New_cases'].sum()
        new_cases={
            "total_cases":  int(total_cases),
            "params": {
                    "country": country,
                    "region": region,
                    "year": year
                },
                "success": True,
            }

        return new_cases
    except Exception as e:
        return {"error": str(e),"success": False,"params": {
                    "country": country,
                    "region": region,
                    "year": year
                }}



@app.get("/max_deaths")
def get_country_with_max_deaths(min_date: str = None, max_date: str = None):
        """
    This method will find the country with the most deaths or find the country with the most deaths between a range of dates.

    - **Params:**
      - min_date (str) : start date
      - max_date (str) : end date
    - **Returns:**
      - (int) : max death with country

    #### Request URL Example 1:

    [http://127.0.0.1:8000/max_deaths](http://127.0.0.1:8000/max_deaths)

    #### Response boady example 1:
        {
        "max_deaths_country": "United States of America",
        "cumulative_deaths": 1127152,
        "params": {
            "min_date": null,
            "max_date": null
        },
        "success": true
        }
    
    #### Request URL Example 2:

    [http://127.0.0.1:8000/max_deaths?min_date=2021-06-01&max_date=2021-12-31](http://127.0.0.1:8000/max_deaths?min_date=2021-06-01&max_date=2021-12-31)

    #### Response boady example 2:

        {
        "max_deaths_country": "United States of America",
        "cumulative_deaths": 819055,
        "params": {
            "min_date": "2021-06-01",
            "max_date": "2021-12-31"
        },
        "success": true
        }
    """
        try:
            if min_date and max_date:
                remaining_data = data[(data["Date_reported"] >= min_date) & (data["Date_reported"] <= max_date)]
            else:
                remaining_data = data

            max_deaths_per_country = remaining_data.groupby("Country")["Cumulative_deaths"].max().reset_index()
            max_deaths_row = max_deaths_per_country.loc[max_deaths_per_country["Cumulative_deaths"].idxmax()]
        
            max_deaths_country = {
                "max_deaths_country": max_deaths_row["Country"],
                "cumulative_deaths": int(max_deaths_row["Cumulative_deaths"]),
                "params": {
                    "min_date": min_date,
                    "max_date": max_date
                },
                "success": True,
            }

            return max_deaths_country
        except Exception as e:
             return {"error": str(e),"success": False,"params": {
                 "min_date": min_date,
                    "max_date": max_date
                }}


@app.get("/min_deaths")
def get_country_with_min_deaths(min_date: str = None, max_date: str = None):
        """
    This method will find the country with the least deaths or find the country with the least deaths between a range of dates.

    - **Params:**
      - min_date (str) : start date
      - max_date (str) : end date
    - **Returns:**
      - (int) : least death with country

    #### Request URL Example 1:

    [http://127.0.0.1:8000/min_deaths](http://127.0.0.1:8000/min_deaths)

    #### Response boady example 1:
        {
        "min_deaths_country": "Democratic People's Republic of Korea",
        "cumulative_deaths": 0,
        "params": {
            "min_date": null,
            "max_date": null
        },
        "success": true
        }
    
    #### Request URL Example 2:

    [http://127.0.0.1:8000/min_deaths?min_date=2021-06-01&max_date=2021-12-31](http://127.0.0.1:8000/min_deaths?min_date=2021-06-01&max_date=2021-12-31)

    #### Response boady example 2:

        {
        "min_deaths_country": "American Samoa",
        "cumulative_deaths": 0,
        "params": {
            "min_date": "2021-06-01",
            "max_date": "2021-12-31"
        },
        "success": true
        }
    """
        try:
            if min_date and max_date:
                remaining_data = data[(data["Date_reported"] >= min_date) & (data["Date_reported"] <= max_date)]
            else:
                remaining_data = data
            #find  total death with respective country 
            max_deaths_per_country = remaining_data.groupby("Country")["Cumulative_deaths"].max().reset_index()
            #find minmum death among the country
            min_deaths_row = max_deaths_per_country.loc[max_deaths_per_country["Cumulative_deaths"].idxmin()]
            min_deaths_country = {
                "min_deaths_country": min_deaths_row["Country"],
                "cumulative_deaths": int(min_deaths_row["Cumulative_deaths"]),
                "params": {
                    "min_date": min_date,
                    "max_date": max_date
                },
                "success": True,
            }

            return min_deaths_country
        except Exception as e:
             return {"error": str(e),"success": False,"params": {
                 "min_date": min_date,
                    "max_date": max_date
                }}


@app.get("/avg_deaths")
def get_average_deaths():
    """
    This method will retrieves the average number of deaths between all countries
    - **Params:**
      - None
    
    - **Returns:**
      - (float) : the average number of deaths between all countries

    #### Request Url Example:

    [http://127.0.0.1:8000/avg_deaths](http://127.0.0.1:8000/avg_deaths)

    #### Response boady Example:
    
        {
            "overall_death_average":{
                "overall_cumulative_deaths":1127152,
                "countries_count":237,
                "average_deaths":"4755.9156118143455"
            },
            "average_deaths_per_country":{
                "Afghanistan":{
                    "cumulative_cases":222954,
                    "cumulative_deaths":7922,
                    "average_deaths":"0.03553199314656835"
                },
                "Albania":{
                    "cumulative_cases":334090,
                    "cumulative_deaths":3604,
                    "average_deaths":"0.010787512346972374"
                }
            },
            "success":true
        }
        
    """
    try:
        unique_countries = data["Country"].nunique()
        max_cumulative_deaths = data["Cumulative_deaths"].max()
        average_deaths = max_cumulative_deaths / unique_countries

        overal_death= {
            "overall_cumulative_deaths": int(max_cumulative_deaths),
            "countries_count":unique_countries,
            "average_deaths": str(average_deaths)
        }
        ## find maxium cases and death per country 
        max_cumulative_cases_per_country = data.groupby("Country")["Cumulative_cases"].max().reset_index()
        max_cumulative_deaths_per_country = data.groupby("Country")["Cumulative_deaths"].max().reset_index()

        max_cumulative_data = pd.merge(max_cumulative_cases_per_country, max_cumulative_deaths_per_country, on="Country")
        max_cumulative_data.fillna("0")
        # find average death per country 
        max_cumulative_data["Average_Deaths"] = max_cumulative_data["Cumulative_deaths"] / max_cumulative_data["Cumulative_cases"]
        max_cumulative_data.fillna("0")



        average_deaths_per_country = {}
        for _, row in max_cumulative_data.iterrows():
            country = row["Country"]
            cumulative_cases = row["Cumulative_cases"]
            cumulative_deaths = row["Cumulative_deaths"]
            average_deaths = row["Average_Deaths"]

            average_deaths_per_country[country] = {
                "cumulative_cases": cumulative_cases,
                "cumulative_deaths": cumulative_deaths,
                "average_deaths": str(average_deaths)
            }

        return {"overall_death_average": overal_death ,"average_deaths_per_country":average_deaths_per_country,"success": True}
       # return average_death
    except Exception as e:
             return {"error": str(e),"success": False}

if __name__ == "__main__":
        uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="debug", reload=True) #host="127.0.0.1"