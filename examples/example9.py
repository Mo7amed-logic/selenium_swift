from selenium_swift.BrowserManager import *


class MyBrowserManager(ChromeBrowserManager):
    def __init__(self) -> None:
        self.path_download = r"c:\Users\progr\OneDrive\Bureau\test_download"
        option = ChromeOption('download.default_directory='+self.path_download)
        super().__init__(option, ChromeService())
    async def tab_1(self):
        #find my public ip 
        page = await self.get('https://www.google.com/search?q=what+is+my+ip+google&oq=what+is+my+ip+google&gs_lcrp=EgZjaHJvbWUyBggAEEUYOdIBCjE3MDY0ajBqMTWoAgiwAgE&sourceid=chrome&ie=UTF-8')
        my_ip = (await page.find_element('css_selector','form[class="yf"],form[jsname="I9GLp"],form[jsaction *="submit"]')).text 
        print(my_ip)
        await page.sleep(2)

if __name__ == "__main__":
    BrowserManager.startBrowserManagers([MyBrowserManager()])