from selenium_swift.browser import *
from selenium_swift.json_handler import save_json_data
import asyncio
from time import time
                     
class PageQuote(PageScrape):
    dataQuotes = []
    async def onResponse(self, **arg):
        self.set_implicite_timeout(2)
        quotes = await self.find_elements('css_selector','.quote')
        texts = (await quotes.find_element('css_selector','.text')).text
        authors = (await quotes.find_element('css_selector','small.author')).text
        tags = (await quotes.find_elements('css_selector','a.tag')).text
        data=[{'text':text,'author':author,'tags':tags} 
              for text,author,tags in zip(texts,authors,tags)]
        PageQuote.dataQuotes.append(data)

class PageTable(PageScrape):
    dataTables = []
    async def onResponse(self, **arg):
        rows_table = await self.find_elements('css_selector','table tr')
        PageTable.dataTables.append(rows_table.text)

class Browser(ChromeBrowser):
    def __init__(self):
        super().__init__(ChromeOption(),ChromeService())
    async def tab_1(self):
        for i in range(1,4):
            await PageQuote(f'https://quotes.toscrape.com/page/{i}/').crawl() 
    async def tab_2(self):
        for i in range(4,7):
            await PageQuote(f'https://quotes.toscrape.com/page/{i}/').crawl()  
    async def tab_3(self):
        for i in range(7,11):
            await PageQuote(f'https://quotes.toscrape.com/page/{i}/').crawl()
    async def tab_4(self):
        await PageTable(f'https://the-internet.herokuapp.com/challenging_dom').crawl()
    def onClose(self):
        print('browser closed ....')
        save_json_data(PageQuote.dataQuotes,'quotes.json')
        save_json_data(PageTable.dataTables,'table.json')
    
async def main():
    await BrowserManager.startBrowsers([Browser()])
    
if __name__ == '__main__':
    asyncio.run(main())