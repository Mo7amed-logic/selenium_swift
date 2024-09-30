from selenium_swift.browser import *

class MyBrowser(ChromeBrowser):
    def __init__(self) -> None:
        super().__init__(ChromeOption(), ChromeService())
    async def tab_1(self):
        #JavaScript Alerts
        page = await self.get('https://the-internet.herokuapp.com/javascript_alerts')
        button_1 = await page.find_element('css_selector','li:nth-child(1) button')
        button_2 = await page.find_element('css_selector','li:nth-child(2) button')
        button_3 = await page.find_element('css_selector','li:nth-child(3) button')

        button_1.click()
        await page.sleep(1)
        page.alert().accept()

        button_2.click()
        await page.sleep(1)
        page.alert().cancel()

        button_3.click()
        await page.sleep(1)
        page.alert().send_keys("hello JS prompt!")

        await page.sleep(3)

if __name__ == "__main__":
    Browser.startBrowsers([MyBrowser()])