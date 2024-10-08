from selenium_swift.browser import *
from selenium_swift.web_option import ChromeOption
from selenium_swift.web_service import ChromeService 
from selenium_swift.captcha_to_solve.ai_captcha import solve_image_captcha
import asyncio
path_download1 = r"D:\my_packages_python\selenium_swift\down1"
path_download2 = r"D:\my_packages_python\selenium_swift\down2"
profile = None
class Browser(ChromeBrowser):
    def __init__(self,profile,path_download,extension) -> None:
        self.exten = extension
        self.path_down = path_download
        user_data_dir = r"C:\Users\progr\AppData\Local\Google\Chrome\User Data\\"+profile
        super().__init__(ChromeOption(
                                      '--user-data-dir='+user_data_dir,
                                      '--download.default_directory='+path_download,
                                      '--undetect_chrome_enable',
                                      '--no-sandbox',
                                      "--disable-dev-shm-usage",
                                      '--blink-settings=imagesEnabled=false',
                                      '--window-size=300x300'
                                       ), ChromeService())
    async def tab_2(self):
        page = await self.get('https://the-internet.herokuapp.com/download')
        links = await page.find_elements('css_selector',"a")
        if page:
            page2 = await self.get('https://www.google.com') 
        text=await solve_image_captcha(r'c:\Users\progr\Downloads\captcha2.png')
        print(text,30*'=')
        k = 0
        for link in links:
            if link.text.endswith('.txt'):
                link.click()
                print(link.text)
                k += 1
            if k == 3:break
        await page.wait_for_Download(self.path_down)
        await page.sleep(5)
         
            
async def main():
    await BrowserManager.startBrowsers([Browser('medhasnaoui500',path_download1,'.png') 
                                   ] )
    #await BrowserManager.startBrowsers([Browser('medhasnaoui833',path_download1,'.pdf'),
    #                                    Browser('medhasnaoui500',path_download2,'.jpg')],'parallel')
if __name__ == "__main__":
     asyncio.run(main())
    
    



