from dataclasses import dataclass
from tabulate import tabulate
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from pyfiglet import Figlet


"""Constants"""
tapology_source = 'https://www.tapology.com/fightcenter?group=major&page='
session = HTMLSession()

"""DataClasses"""
@dataclass
class Fighter:
    bout_no: str
    name: str
    ranking: str
    record: str
    betting_odds: str
    fight_predictions: str
    age: str
    latest_weight: str
    height: str
    reach: str
    nationality: str

@dataclass
class Event:
    event_name: str
    headline: str
    weightclass: str
    location: str
    time: str
    event_url: str

"""Scrape and parse a list of all the events"""
def scrape_event_tuple(page_number=0, user_promotions=[]) -> tuple[list, int]:
    page_html = session.get(f"{tapology_source}{page_number}").text

    #Parse list of events
    total_events = []
    total_events_amount = 0
    soup = BeautifulSoup(page_html, 'html.parser')
    all_events = soup.find_all(class_="fcListing")

    #For each event, create an Event() instance
    for event in all_events:
        event_name = ' '.join((event.find('span', class_='name').get_text(strip=True)).split())

        if any(promo in event_name.lower() for promo in user_promotions):
            event_listing = Event(event_name="", headline="", weightclass="", location="", time="", event_url="")
            try:
                event_listing.event_name = ' '.join((event.find('span', class_='name').get_text(strip=True)).split())
            except AttributeError as e:
                event_listing.event_name = "<No event name>"
            try:
                event_listing.headline = ' '.join((event.find('span', class_="billing").get_text(strip=True)).split())
            except AttributeError as e:
                event_listing.headline = "<Headline undecided>"
            try:
                event_listing.weightclass = ' '.join((event.find('span', class_="bout").get_text(strip=True)).split())
            except AttributeError as e:
                event_listing.weightclass = "<Weightclass undecided>"
            try:
                event_listing.location = ' '.join((event.find('span', class_="venue-location").get_text(strip=True)).split())
            except AttributeError as e:
                event_listing.location = "<Location undecided>"
            try:
                event_listing.time = ' '.join((event.find('span', class_="datetime").get_text(strip=True)).split())
            except AttributeError as e:
                event_listing.time = "<Date undecided>"
            try:
                event_listing.event_url = f"https://www.tapology.com{event.find('span', class_='name').find('a')['href']}"
            except AttributeError as e:
                event_listing.event_url = "<No URL>"
            total_events_amount += 1
            total_events.append(event_listing)

    return total_events, total_events_amount

"""Scrape and parse a list of each individual bout url"""
def scrape_bout_list(user_event) -> list:
    event_html = session.get(user_event).text

    #Parse bout list
    total_bout_urls = []
    soup = BeautifulSoup(event_html, 'html.parser')
    bout_urls = soup.find_all(class_="fightCardMatchup")

    for bout in bout_urls:
        url = f"https://www.tapology.com{bout.find('a').get('href')}"
        total_bout_urls.append(url)

    return(total_bout_urls)

"""Scrape and parse each individual bout details"""
def scrape_bout_details_list(bout_url) -> list:
    bout_title_list = []

    for each_url in bout_url:
        bout_html = session.get(each_url).text
        soup = BeautifulSoup(bout_html, 'html.parser')

        #Parse fighter1 details
        fighter1 = Fighter(bout_no="", name="", ranking="", record="", betting_odds="", fight_predictions="", age="", latest_weight="", height="", reach="", nationality="")
        try:
            fighter1.name = ' '.join((soup.find('span', class_='fName left').get_text(strip=True)).split())
        except AttributeError as e:
            fighter1.name = "<Fighter name N/A>"
        try:
            f1_ranking = ' '.join(soup.find('table', class_='fighterStats spaced').find('td', string='Ranking').find_parent('tr').find_all('td')[0].find('div').get_text(strip=True).split())
            f1_ranking_category = ''.join(soup.find('table', class_='fighterStats spaced').find('td', string='Ranking').find_parent('tr').find_all('td')[0].find('a').get_text(strip=True).split())
            fighter1.ranking = f'{f1_ranking} {f1_ranking_category}'
        except AttributeError as e:
            fighter1.ranking = "<Ranking N/A>"
        try:
            fighter1.record = ''.join(soup.find('table', class_='fighterStats spaced').find('td', string='Pro Record At Fight').find_parent('tr').find_all('td')[0].get_text(strip=True).split())
        except AttributeError as e:
            fighter1.record = "<Record N/A>"
        try:
            fighter1.betting_odds = ' '.join(soup.find('table', class_='fighterStats spaced').find('td', string='Betting Odds').find_parent('tr').find_all('td')[0].get_text(strip=True).split())
        except AttributeError as e:
            fighter1.betting_odds = "<Betting odds N/A>"
        try:
            fighter1.age = ' '.join(soup.find('table', class_='fighterStats spaced').find('td', string='Age at Fight').find_parent('tr').find_all('td')[0].get_text(strip=True).split())
        except AttributeError as e:
            fighter1.age = "<Age N/A>"
        try:
            fighter1.latest_weight = ' '.join(soup.find('table', class_='fighterStats spaced').find('td', string='Latest Weight').find_parent('tr').find_all('td')[0].get_text(strip=True).split())
        except AttributeError as e:
            fighter1.latest_weight = "<Last weight N/A>"
        try:
            fighter1.height = ' '.join(soup.find('table', class_='fighterStats spaced').find('td', string='Height').find_parent('tr').find_all('td')[0].get_text(strip=True).split())
        except AttributeError as e:
            fighter1.height = "<Height N/A>"
        try:
            fighter1.reach = ' '.join(soup.find('table', class_='fighterStats spaced').find('td', string='Reach').find_parent('tr').find_all('td')[0].get_text(strip=True).split())
        except AttributeError as e:
            fighter1.reach = "<Reach N/A>"
        try:
            fighter1.nationality = ' '.join(soup.find('table', class_='fighterStats spaced').find('td', string='Nationality').find_parent('tr').find_all('td')[0].get_text(strip=True).split())
        except AttributeError as e:
            fighter1.nationality = "<Nationality N/A>"
        try:
            fighter1.bout_no = ' '.join(soup.find('div', class_='details details_with_poster clearfix').find('strong', string='Bout Billing:').find_next_sibling('span').find_next_sibling('span').get_text(strip=True).split())
        except AttributeError as e:
            fighter1.bout_no = "<Bout billing N/A>"
        try:
            surname = " ".join(fighter1.name.split()[1:])
            fighter1.fight_predictions = ' '.join((soup.find('div', class_='stat_label', string=surname).find_parent('div').find('div', class_='number').get_text(strip=True)).split())
        except AttributeError as e:
            fighter1.fight_predictions = "<Fight predictions N/A>"

        #Parse fighter2 details
        fighter2 = Fighter(bout_no="", name="", ranking="", record="", betting_odds="", fight_predictions="", age="", latest_weight="", height="", reach="", nationality="")
        try:
            fighter2.name = ' '.join((soup.find('span', class_='fName right').get_text(strip=True)).split())
        except AttributeError as e:
            fighter2.name = "<Fighter name N/A>"
        try:
            f2_ranking = ' '.join(soup.find('table', class_='fighterStats spaced').find('td', string='Ranking').find_parent('tr').find_all('td')[4].find('div').get_text(strip=True).split())
            f2_ranking_category = ''.join(soup.find('table', class_='fighterStats spaced').find('td', string='Ranking').find_parent('tr').find_all('td')[4].find('a').get_text(strip=True).split())
            fighter2.ranking = f'{f2_ranking} {f2_ranking_category}'
        except AttributeError as e:
            fighter2.ranking = "<Ranking N/A>"
        try:
            fighter2.record = ''.join(soup.find('table', class_='fighterStats spaced').find('td', string='Pro Record At Fight').find_parent('tr').find_all('td')[4].get_text(strip=True).split())
        except AttributeError as e:
            fighter2.record = "<Record N/A>"
        try:
            fighter2.betting_odds = ' '.join(soup.find('table', class_='fighterStats spaced').find('td', string='Betting Odds').find_parent('tr').find_all('td')[4].get_text(strip=True).split())
        except AttributeError as e:
            fighter2.betting_odds = "<Betting odds N/A>"
        try:
            fighter2.age = ' '.join(soup.find('table', class_='fighterStats spaced').find('td', string='Age at Fight').find_parent('tr').find_all('td')[4].get_text(strip=True).split())
        except AttributeError as e:
            fighter2.age = "<Age N/A>"
        try:
            fighter2.latest_weight = ' '.join(soup.find('table', class_='fighterStats spaced').find('td', string='Latest Weight').find_parent('tr').find_all('td')[4].get_text(strip=True).split())
        except AttributeError as e:
            fighter2.latest_weight = "<Last weight N/A>"
        try:
            fighter2.height = ' '.join(soup.find('table', class_='fighterStats spaced').find('td', string='Height').find_parent('tr').find_all('td')[4].get_text(strip=True).split())
        except AttributeError as e:
            fighter2.height = "<Height N/A>"
        try:
            fighter2.reach = ' '.join(soup.find('table', class_='fighterStats spaced').find('td', string='Reach').find_parent('tr').find_all('td')[4].get_text(strip=True).split())
        except AttributeError as e:
            fighter2.reach = "<Reach N/A>"
        try:
            fighter2.nationality = ' '.join(soup.find('table', class_='fighterStats spaced').find('td', string='Nationality').find_parent('tr').find_all('td')[4].get_text(strip=True).split())
        except AttributeError as e:
            fighter2.nationality = "<Nationality N/A>"
        try:
            fighter2.bout_no = ' '.join(soup.find('div', class_='details details_with_poster clearfix').find('strong', string='Bout Billing:').find_next_sibling('span').find_next_sibling('span').get_text(strip=True).split())
        except AttributeError as e:
            fighter2.bout_no = "<Bout billing N/A>"
        try:
            surname = " ".join(fighter2.name.split()[1:])
            fighter2.fight_predictions = ' '.join((soup.find('div', class_='stat_label', string=surname).find_parent('div').find('div', class_='number').get_text(strip=True)).split())
        except AttributeError as e:
            fighter2.fight_predictions = "<Fight predictions N/A>"

        bout_title_list.append(fighter1)
        bout_title_list.append(fighter2)

    return bout_title_list

def main():
    user_promotions = input('What promotions do you want to search? ').lower().split(", ")
    total_events = []
    total_events_amount = 0
    tabulate_event_list = ['EVENT #','EVENT NAME','HEADLINING','WEIGHT-CLASS','LOCATION','DATE', 'URL']

    #Iterate through multiple pages to get total events
    for x in range(1, 3):
        events, events_amount = scrape_event_tuple(x, user_promotions)
        total_events.extend(events)
        total_events_amount += events_amount

    #Create an additional row number column, add all values to a new list
    total_numbered_events = []
    for i, event in enumerate(total_events):
        numbered_event = [i + 1, event.event_name, event.headline, event.weightclass,
                            event.location, event.time, event.event_url]
        total_numbered_events.append(numbered_event)

    #Print event list tabulate
    print(f'\n {tabulate(total_numbered_events, headers=tabulate_event_list, tablefmt="grid")}')
    print(f'TOTAL EVENTS: {total_events_amount}\n')

    #Get user input and return urls to each bout of the event
    user_event_selection = int(input('Which Event # do you want to look at? '))
    user_event = total_numbered_events[user_event_selection-1]
    bout_url_list = scrape_bout_list(user_event[6])

    #Scrape detail from each bout
    tabulate_bout_list = ['BOUT #','FIGHTER','RANKING','RECORD','BETTING ODDS','PREDICTION','AGE AT FIGHT', 'LAST WEIGH-IN', 'HEIGHT', 'REACH', 'NATIONALITY']
    bout_details_list = scrape_bout_details_list(bout_url_list)
    print(f'bout_details_list type: {type(bout_details_list)}')
    fig_event = Figlet(font='small')
    fig_headliner = Figlet(font='slant')
    print(f'{fig_event.renderText(user_event[1])} - {fig_headliner.renderText(user_event[2])}')
    print(f'{user_event[1]} - {user_event[2]} - {user_event[3]} - {user_event[4]} - {user_event[5]} - {user_event[6]}')
    print(f'{tabulate(bout_details_list, headers=tabulate_bout_list, tablefmt="grid")}\n')

if __name__ == "__main__":
    main()

"""
OUTSTANDING
- contains "weigh"
- look into grouping each bout for visual simplicity
- do something with the numerical values we've received
- use rich to highlight differences
- refine user input
"""
