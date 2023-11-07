import time
from datetime import datetime

import scrapy
from scrapy.http import Response, HtmlResponse
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from tqdm import tqdm


class FootballSpider(scrapy.Spider):
    name = "football"
    allowed_domains = ["sportsbook.caesars.com"]
    start_urls = ["https://sportsbook.caesars.com/us/az/bet/football/events/all"]

    def __init__(self, *args, **kwargs):
        super(FootballSpider, self).__init__(*args, **kwargs)
        chrome_options = Options()
        # chrome_options.add_argument("--headless")  # not load all page data in headless mode
        self.driver = webdriver.Chrome(options=chrome_options)

    def close(self, reason):
        self.driver.close()

    def parse(self, response: Response, **kwargs):
        self.logger.info("Open football matches start page")
        self.driver.get(response.url)
        time.sleep(5)

        response = self.create_html_response()
        states = response.css(".states a")

        for state in states:
            for match_data in self.parse_matches_for_state(state=state):
                yield match_data

    def parse_matches_for_state(self, state):
        state_name = state.css(".stateFullName::text").get()
        state_code = state.css("a::attr(data-qa)").get()[-2:]
        country = "us"

        if state_code == "on":
            country = "ca"

        state_matches_url = f"https://sportsbook.caesars.com/{country}/{state_code}/bet/football/events/all"

        self.logger.info(f"Open football matches page for state: {state_name}")
        self.driver.get(state_matches_url)
        time.sleep(5)

        self.click_view_all_buttons()
        self.scroll_page_down()
        response = self.create_html_response()

        for match_data in self.parse_football_matches(
            response=response, state_name=state_name
        ):
            yield match_data

    def parse_football_matches(self, response, state_name):
        self.logger.info(f"Start receiving football matches data for {state_name}")
        for event_list in response.css(".competitionExpander"):
            title = event_list.css("span.title::text").get()

            for event in event_list.css(".groupedMarketTemplateGrid"):
                date_string = event.css("span.date::text").get()
                match_date = (
                    datetime.strptime(date_string, "%b %d | %I:%M%p").replace(year=2023)
                    if date_string
                    else datetime.now()
                )
                team1_name = event.css("a.firstCompetitor .truncate2Rows::text").get()
                team2_name = event.css("a.lastCompetitor .truncate2Rows::text").get()
                team1_cof, draw, team2_cof = event.css(
                    ".cui-text-fg-primary::text"
                ).getall() or (None, None, None)

                yield {
                    "state": state_name,
                    "competition": title,
                    "match_date": match_date,
                    "team1_name": team1_name,
                    "team2_name": team2_name,
                    "team1_cof": team1_cof,
                    "team2_cof": team2_cof,
                    "draw": draw,
                }
        self.logger.info(
            f"Football matches data for {state_name} received successfully"
        )

    def create_html_response(self):
        page_source = self.driver.page_source
        response = HtmlResponse(
            url=self.driver.current_url, body=page_source, encoding="utf-8"
        )
        return response

    def click_view_all_buttons(self):
        view_all_buttons = self.driver.find_elements(
            By.CSS_SELECTOR, ".SportDailyListContainer .expanderHeaderRight"
        )
        for button in tqdm(view_all_buttons[1:], desc="Clicking ViewAll buttons"):
            self.driver.execute_script("arguments[0].click();", button)

    def scroll_page_down(self):
        element = self.driver.find_element(By.CSS_SELECTOR, "body")
        last_position = self.driver.execute_script("return window.pageYOffset;")

        with tqdm(desc="Scroll page down") as pbar:
            while True:
                element.send_keys(Keys.PAGE_DOWN)
                time.sleep(1)
                new_position = self.driver.execute_script("return window.pageYOffset;")

                if new_position == last_position:
                    break

                last_position = new_position
                pbar.update(1)
