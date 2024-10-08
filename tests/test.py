from selenium_swift.browser import *
from selenium_swift.web_option import ChromeOption
from selenium_swift.web_service import ChromeService 

path_downloas1 = r"D:\my_packages_python\selenium_swift\down1"
path_downloas2 = r"D:\my_packages_python\selenium_swift\down2"
class MyBrowser(ChromeBrowser):
    def __init__(self,path_download,extension) -> None:
        self.exten = extension
        self.path_down = path_download
        user_data_dir = r"C:\Users\progr\AppData\Local\Google\Chrome\User Data\medhasnaoui833"
        super().__init__(ChromeOption('--user-data-dir='+user_data_dir,
                                      '--remote-debugging-port=9222',
                                      '--no-sandbox',
                                      'download.default_directory='+path_download,
                                      '--undetect_chrome_enable',
                                      '--window-size=1920x1080',
                                      '--headless'
                                       ), ChromeService(),remote_server_url="http://127.0.0.1:4444/wd/hub")
    async def tab_1(self):
        page = await self.get('https://the-internet.herokuapp.com/download')
        links = await page.find_elements('css_selector',"a")
        k = 0
        for link in links:
            if link.text.endswith(self.exten):
                link.click()
                print(link.text)
                k+=1
            if k == 5:break

        await page.wait_for_Download(self.path_down)
 

if __name__ == "__main__":
    BrowserManager.startBrowsers([MyBrowser(path_downloas2,'.txt'),MyBrowser(path_downloas2,'.pdf')])
    
    
 