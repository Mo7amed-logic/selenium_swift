from selenium_swift.browser import *
from selenium_swift.web_option import ChromeOption
from selenium_swift.web_service import ChromeService 


class MyBrowser(ChromeBrowser):
    def __init__(self) -> None:
        self.path_download = r"c:\Users\progr\OneDrive\Bureau\test_download"
        option = ChromeOption('download.default_directory='+self.path_download)
        super().__init__(option, ChromeService())
    async def tab_1(self):
        #login_page
        page = await self.get('https://the-internet.herokuapp.com/login')
        user_name_input = await page.find_element('id','username')
        password_input = await page.find_element('id','password')

        user_name_input.send_keys('mohamed hasnaoui')
        password_input.send_keys('123456789').submit()

        await page.sleep(2)

if __name__ == "__main__":
    Browser.startBrowsers([MyBrowser()])