from selenium_swift.BrowserManager import *
from selenium_swift.web_option import ChromeOption
from selenium_swift.web_service import ChromeService


class PageInfo(NextPage):
    def __init__(self) -> None:
        super().__init__()
    async def showData(self):
        table_rows = await self.find_elements('css_selector','table[class*="table-stripe"] tr') 
        print("********** table 1 ****************")
        for row in table_rows:
            print(row.text)

class MyBrowserManager(ChromeBrowserManager):
    def __init__(self ) -> None:
        super().__init__(ChromeOption(), ChromeService() )
    async def tab_1(self):
        page = await self.get('https://books.toscrape.com/')
        products = await page.find_elements('css_selector','.thumbnail')
        print(products)
        for prd in products:
            # when click this element "prd" will open new page  
            prd.click()
            # you can interact with opened page easilly like this:
            await PageInfo().showData()

if __name__ == "__main__":
    BrowserManager.startBrowserManagers([MyBrowserManager()])
            
