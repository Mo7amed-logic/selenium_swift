from selenium_swift.BrowserManager import *

class MyBrowserManager(ChromeBrowserManager):
    def __init__(self) -> None:
        self.path_download = r"c:\Users\progr\OneDrive\Bureau\test_download"
        option = ChromeOption('download.default_directory='+self.path_download)
        super().__init__(option, ChromeService())
    async def tab_download(self):
        #file_download 
        page = await self.get('https://the-internet.herokuapp.com/download')
        link_list = await page.find_elements('css_selector','a')
        for link in link_list:
            if link.text.endswith('.pdf'):
                link.click()
        
        # .....
        # ......

        #make sure to call "page.wait_for_Download" in the end of this tab 
        await page.wait_for_Download(self.path_download)
    async def tab_upload(self):
        #file_upload 
        page = await self.get('https://the-internet.herokuapp.com/upload')
        input_file = await page.find_element('id',"file-upload")
        print(input_file)
        input_file.send_file(r'c:\Users\progr\Downloads\DATA_Data_Analysis_2_AR.pdf')
        
        await page.sleep(3)
if __name__ == "__main__":
    BrowserManager.startBrowserManagers([MyBrowserManager()])