from selenium_swift.browser import *
import asyncio

class MyBrowser(ChromeBrowser):
    def __init__(self,download_path,extension,upload_file):
        self.extension = extension
        self.download_path = download_path 
        self.upload_file = upload_file
        super().__init__(ChromeOption('download.default_directory='+download_path),ChromeService())

    async def tab_download_files(self):
        page = await self.get('https://the-internet.herokuapp.com/download')
        a_tags = await page.find_elements('tag_name','a')
        for tag in a_tags:
            if tag.text.endswith(self.extension):tag.click()
        
        if self.extension == '.txt':
            await BrowserManager.startBrowsers([MyBrowser(self.download_path,'.pdf',False)])

        await page.wait_for_Download(self.download_path)

    async def tab_upload_files(self):
        if not self.upload_file:return
        page = await self.get('https://the-internet.herokuapp.com/upload')
        (await page.find_element('id','file-upload')).send_file(r'c:\Users\progr\Downloads\js_events_list.pdf')
        await page.sleep(2)

async def main():
    await BrowserManager.startBrowsers([MyBrowser(r'd:\text_download','.txt',True),
                                        MyBrowser(r'd:\images_download','.jpg',False),
                                        MyBrowser(r'd:\images_download','.png',False)],
                                        'parallel',3)

if __name__ == '__main__':
    asyncio.run(main())