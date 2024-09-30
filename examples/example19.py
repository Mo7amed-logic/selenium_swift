from selenium_swift.browser import *
class MyBrowser(ChromeBrowser):
    def __init__(self) -> None:
        super().__init__(ChromeOption(), ChromeService())
    async def tab_1(self):
        #Data Table
        page = await self.get('https://the-internet.herokuapp.com/tables')
        rows_table1 = await page.find_elements('css_selector','#table1 tr')
        rows_table2 = await page.find_elements('css_selector','#table2 tr')
        print('********* TABLE 1 ******************')
        for row in rows_table1:
            th_or_td = await row.find_elements('css_selector','th,td')
            for t_h_d in th_or_td:
                print(t_h_d.text+"|",end="")
            print()
            
        print('********* TABLE 2 ******************')
        for row in rows_table2:print(row.text)
         

if __name__ == "__main__":
    Browser.startBrowsers([MyBrowser()])