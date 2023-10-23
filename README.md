# MMA Fight Predictor

## VIDEO DEMO 

[youtu.be/dEMaXo87cwU](https://youtu.be/dEMaXo87cwU)

## DESCRIPTION 

The MMA Fight Predictor is a python CLI application that allows the user to visually check on one line what the fans predict will happen in a fight, versus the odds the bookmakers are giving. 

The aim for this is to gauge when a divergence between the two sources is present to give us an intuitive low risk high reward bet.

The project also returns various details on events such as date and location, and details on the fighters such as ranking, age, weight, record, etc

The data sources are scraped from the [Tapology.com](http://Tapology.com) website using [requests-html](https://requests.readthedocs.io/projects/requests-html/en/latest/) to make the HTTP request, and the relevant details are parsed using [Beautifulsoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/). The data is presented visually using [Tabulate](https://pypi.org/project/tabulate/). For added presentation, the event title is shown as ASCII art via [pyfiglet](https://pypi.org/project/pyfiglet/).

## FILES AND FUNCTIONS

<details>

<summary> project.py </summary>

**IMPORTS**

- `from dataclasses import dataclass`
    - imports `dataclass` to store the scraped values for individual events and fighters.
- `from tabulate import tabulate`
    - imports `tabulate` to visually represent the list for dataclasses
- `from bs4 import BeautifulSoup`
    - imports `BeautifulSoup` to parse through the html
- `from requests_html import HTMLSession`
    - imports `HTMLSession` to get the html for each page
- `from pyfiglet import Figlet`
    - imports `figlet` to generate simple ASCII art of each event header

**FUNCTIONS**

- `@dataclass class Fighter`
    
    A data class that holds each fighter’s statistics/details for a bout: *********************************bout_no, name, ranking, record, betting_odds, fight_predictions, age, latest_weight, height, reach, nationality*********************************
    
- `@dataclass class Event`
    
    A data class that holds the event details: ***********event_name, headline, weightclass, location, time, event_url***********
    
- `def scrape_event_tuple(page_number=0, user_promotions=[]) -> tuple[list, int]:`
    
    A function to fetch the html of a url, and parse the relevant details into a list of Event dataclasses
    
    This function receives an int of 1 or 2 (specified in a for loop in main()). We use an HTMLSession() from the requests_html library to get the text (ie html) from a tapology url page, 1 or 2 depending on the int.
    
    The user_promotions list contains the promotions to search within these urls, specified by user input in main() (eg: ************************ufc, bellator, pfl, etc************************)
    
    Once we’ve gotten the html text and saved it to a variable (page_html in this context), we can use BeautifulSoup to parse through the content easily by filtering the html further to only include content within the “fcListing” div class.
    
    A for loop is used to check that the content of a span within the html with a class “name” matches the items in the user promotion list. If it does, the relevant event details are gotten and appended to a total_events list which is then returned by the function. 
    
- `def scrape_bout_list(user_event) -> list:`
    
    Function that fetches the html from a user selected event url, and returns a list of urls (`total_bout_urls`) to each bout in that event
    
    Each bout url is further scraped in the next function to return more relevant details
    
- `def scrape_bout_details_list(bout_url) -> list:`
    
    This function iterates through the list of bout urls. Each bout page contains the necessary values to build out a list of `Fighter` dataclasses. 
    
    The function returns a list of `Fighter`'s, and an int of the total fights in an event
    
- `def main():`
    
    The programme is ran within the main function. Here we ask the user to specify which promotions they’d like to search for. We then iterate through 2 pages of the tapology website as events too far in the future may not exist or have relevant information.
    
    We also use tabulate here to illustrate the list of dataclasses in a clear table for user inspection.
    

</details>

<details>

<summary> test_project.py </summary>

- Contains the functions to use with `pytest`.

</details>

## DESIGN CHOICES

The programme does what it is expected of it, however there are a few outstanding implementations that would ultimately add to the user experience:

- Additional values: In the `Fighter` dataclass, add ***********gender, finish prediction***********
- A better visual representation: Determine how best to illustrate a single fight, and divergences. Is it worth creating a webApp in order to allow users to sort, filter, etc?
- Highlight differences  between fighters: height, reach, weight, age, etc
- Refine user input: create some better error handling
- Additional functionality: offer to export table as a csv, search for other combat sports (boxing, muay thai, etc)
