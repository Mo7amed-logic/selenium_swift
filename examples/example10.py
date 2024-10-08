from selenium_swift.BrowserManager import *

class MyBrowserManager(ChromeBrowserManager):
    def __init__(self) -> None:
        self.path_download = r"c:\Users\progr\OneDrive\Bureau\test_download"
        option = ChromeOption('download.default_directory='+self.path_download)
        super().__init__(option, ChromeService())
    async def tab_1(self):
        #Horizontal Slider
        page = await self.get('https://the-internet.herokuapp.com/horizontal_slider')
        e = await page.find_element('css_selector',"input[type='range']")
        e.drag_and_drop_by_offset(50,0)
        await page.sleep(2)
if __name__ == "__main__":
    BrowserManager.startBrowserManagers([MyBrowserManager()])