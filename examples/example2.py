from selenium_swift.BrowserManager import *


class MyBrowserManager(ChromeBrowserManager):
    def __init__(self) -> None:
        super().__init__(ChromeOption(), ChromeService())
    async def tab_1(self):
        page = await PageEvent('https://the-internet.herokuapp.com/checkboxes').open()
        checkbox1 = await page.find_element('css_selector','input[type="checkbox"]:nth-of-type(1)')
        checkbox2 = await page.find_element('css_selector','input[type="checkbox"]:nth-of-type(2)')
        await page.sleep(1)
        checkbox1.click()
        await page.sleep(1)
        checkbox2.click()
    async def tab2(self):
        page = await self.get('https://the-internet.herokuapp.com/disappearing_elements')
        home_link = await page.find_element('css_selector',"li:nth-child(1) a")
        about_link = await page.find_element('css_selector',"li:nth-child(2) a")
        contact_us_link = await page.find_element('css_selector',"li:nth-child(3) a")
        portfolio_link = await page.find_element('css_selector',"li:nth-child(4) a")
        #galerie_link = await page.find_element('css_selector',"li:nth-child(5) a")
        await page.sleep(1)
        # when click "home_link" it will open new page
        home_link.click()
        home_page = page.focus_to_new_page()
        print(home_page.driver.page_source)
        # when click "about_link" it will open new page
        await page.sleep(1)
        about_link.click()
        about_page = page.focus_to_new_page()
        print(about_page.driver.page_source)
        # when click "contact_us_link" it will open new page
        await page.sleep(1)
        contact_us_link.click()
        contact_page = page.focus_to_new_page()
        print(contact_page.driver.page_source)
        # when click "contact_us_link" it will open new page
        await page.sleep(1)
        portfolio_link.click()
        portfolio_page = page.focus_to_new_page()
        print(portfolio_page.driver.page_source)
        #and so on ..........
        await page.sleep(1)
        contact_us_link.click()
        contact_page = page.focus_to_new_page()
        print(contact_page.driver.page_source)

if __name__ == "__main__":
    BrowserManager.startBrowserManagers([MyBrowserManager()])


