from selenium_swift.BrowserManager import *

class MyBrowserManager(ChromeBrowserManager):
    def __init__(self) -> None:
        super().__init__(ChromeOption(), ChromeService())
    async def tab_1(self):
        #Nested Frames
        page = await self.get('https://the-internet.herokuapp.com/nested_frames')
        frame = await page.find_element('css_selector','frame[src="/frame_top"]')
        frame_childs = await frame.find_elements('tag_name','frame')
   
        for f_child in frame_childs:
            try:
                body = await f_child.find_element('tag_name','body')
                print(body.text)
            except:
                print('ddd',f_child)

        frame_bottom = await page.find_element('css_selector','frame[src="/frame_bottom"]')
        html = await frame_bottom.find_element('tag_name','html')
        print('html_content:',html.text)
        await page.sleep(2)

if __name__ == "__main__":
    BrowserManager.startBrowserManagers([MyBrowserManager()])