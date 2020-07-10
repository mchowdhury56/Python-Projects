from selenium import webdriver
from time import sleep

class stats:
    def __init__(self):
        self.driver = webdriver.Chrome()

    def get_data(self,country = 'World'):
        self.driver.get('https://www.worldometers.info/coronavirus/')
        sleep(5)
        table = self.driver.find_element_by_xpath('//*[@id="main_table_countries_today"]/tbody[1]')
        country_element = table.find_element_by_xpath(f"//td[contains(., '{country}')]")
        row = country_element.find_element_by_xpath("./..")
        data = []
        for i in range(2,10):
            cell = row.find_element_by_xpath(f'./td[{i}]').text
            data.append('N/A') if len(cell) <= 0 else data.append(cell)
        total_cases = data[1]
        new_cases = data[2]
        total_deaths = data[3]
        new_deaths = data[4]
        active_cases = data[5]
        total_recovered = data[6]
        serious_critical = data[7]

        print(country + " Statistics: ") if country != 'World' else print("Worldwide Statistics: ")
        print("Total cases: " + total_cases)
        print("New cases: " + new_cases)
        print("Total deaths: " + total_deaths)
        print("New deaths: " + new_deaths)
        print("Active cases: " + active_cases)
        print("Total recovered: " + total_recovered)
        print("Serious, critical cases: " + serious_critical)

        self.driver.close()
        self.driver.quit()


if __name__ == "__main__":
    print("Information proivded from 'https://www.worldometers.info/coronavirus/'. Please check the site for the proper country name in order to avoid errors.")
    print("Enter the full name of the country whose statistics you want.\n" + 
        "Note: type USA for United States, UK for United Kingdom, UAE for United Arab Emirates, and DRC for the Congo." )
    country = input("If no country is given, Worldwide statistics will be provided by default.\n")
    print("Note: statistics that have N/A mean that particular statistic for the day has not been recorded.")
    bot = stats()
    bot.get_data(country)
