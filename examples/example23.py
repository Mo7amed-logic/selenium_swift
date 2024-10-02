from selenium_swift.browser import * 

class MyBrowser(ChromeBrowser):
    def __init__(self ) -> None:
        super().__init__(ChromeOption(), ChromeService() )
    async def tab_1(self):
        page = await self.get('https://books.toscrape.com/')
        products = await page.find_elements('css_selector','.thumbnail')
        print(products)
        for prd in products:
            # when click this element "prd" will open new page  
            prd.click()
            # you should interact with opened page like this:
            infoPage = page.focus_to_new_page()
            table_rows = await infoPage.find_elements('css_selector','table[class*="table-stripe"] tr') 
            print("********** table ****************")
            for row in table_rows:
                print(row.text)
             

if __name__ == "__main__":
    Browser.startBrowsers([MyBrowser()])