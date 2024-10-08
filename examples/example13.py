from selenium_swift.BrowserManager import *

class MyBrowserManager(ChromeBrowserManager):
    def __init__(self) -> None:
        self.path_download = r"c:\Users\progr\OneDrive\Bureau\test_download"
        option = ChromeOption('download.default_directory='+self.path_download)
        super().__init__(option, ChromeService())
    async def tab_1(self):
        #JQueryUI - Menu
        page = await self.get('https://the-internet.herokuapp.com/jqueryui/menu#')
        ################################
        enabled_element = await page.find_element('id',"ui-id-3")
        mouse = page.mouse
        mouse.move_to_element(enabled_element)
        await page.sleep(1)
        ##################################
        download_element = await page.find_element('id',"ui-id-4")
        mouse.move_to_element(download_element)
        await page.sleep(1)
        #######################################
        e = await page.find_element('id','ui-id-5')
        mouse.move_to_element(e)
        e.click()
        await page.wait_for_Download(self.path_download)

if __name__ == "__main__":
    BrowserManager.startBrowserManagers([MyBrowserManager()])