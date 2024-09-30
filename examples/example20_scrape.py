from selenium_swift.browser import * 

class Scrap(PageScrape):
    async def onResponse(self, **arg):
        quote_elements = await self.find_elements('css_selector','.text')
        for quote in quote_elements:
            print(quote.text)

class MyBrowser(ChromeBrowser):
    def __init__(self) -> None:
        super().__init__(ChromeOption(), ChromeService())
    async def tab_1(self):
        for i in range(1,3):
            await Scrap(f'https://quotes.toscrape.com/page/{i}/').crawl(my_index=i)
    async def tab_2(self):
        for i in range(3,6):
            await Scrap(f'https://quotes.toscrape.com/page/{i}/').crawl(my_index=i)
    async def tab_3(self):
        for i in range(6,9):
            await Scrap(f'https://quotes.toscrape.com/page/{i}/').crawl(my_index=i)
    async def tab_4(self):
        for i in range(9,11):
            await Scrap(f'https://quotes.toscrape.com/page/{i}/').crawl(my_index=i)

if __name__ == "__main__":
    Browser.startBrowsers([MyBrowser()])