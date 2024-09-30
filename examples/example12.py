from selenium_swift.browser import *

class MyBrowser(ChromeBrowser):
    def __init__(self) -> None:
        self.path_download = r"c:\Users\progr\OneDrive\Bureau\test_download"
        option = ChromeOption('download.default_directory='+self.path_download)
        super().__init__(option, ChromeService())
    async def tab_1(self):
        #Infinit Scroll
        page = await self.get('https://the-internet.herokuapp.com/infinite_scroll')
        while True:
            page.scrollToBottom()
            print(page.is_at_bottom())
            await page.sleep(0.5)
if __name__ == "__main__":
    Browser.startBrowsers([MyBrowser()])