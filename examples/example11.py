from selenium_swift.browser import *
from selenium_swift.web_option import ChromeOption
from selenium_swift.web_service import ChromeService 
from selenium_swift.mouse_controller import MouseController

class MyBrowser(ChromeBrowser):
    def __init__(self) -> None:
        self.path_download = r"c:\Users\progr\OneDrive\Bureau\test_download"
        option = ChromeOption('download.default_directory='+self.path_download)
        super().__init__(option, ChromeService())
    async def tab_1(self):
        #Hovers
        page = await self.get('https://the-internet.herokuapp.com/hovers')
        elements = await page.find_elements('css_selector','div.figure')
        e = elements[2]
        x,y = e.location
        mouse_control = MouseController(page)
        #mouse_control.move_to_element(e)
        mouse_control.move_to(x,y)
        await page.sleep(3)
if __name__ == "__main__":
    Browser.startBrowsers([MyBrowser()])