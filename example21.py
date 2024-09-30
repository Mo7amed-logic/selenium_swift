from selenium_swift.browser import * 

# this example show you how to create custom page that should extend from PageEvent class 
# here i have a web page that i want to download some files from it so i creat this page separetly and i name it PageDownload
# and other web page i want to uplaod some files to it so i create it separetly and i name it PageUpload
# you can create your custom page that handle complex interaction lick click, sendfile , mouse event, and others ineraction

class PageDownload(PageEvent):
    def __init__(self) -> None:
        super().__init__('https://the-internet.herokuapp.com/download')
    async def download_images(self):
        link_list = await self.find_elements('css_selector','a')
        for link in link_list:
            if link.text.endswith(('.png','.jpg')):
                link.click() 
    async def download_pdf(self):
        link_list = await self.find_elements('css_selector','a')
        for link in link_list:
            if link.text.endswith('.pdf'):
                link.click()  
    async def download_text_files(self):
        link_list = await self.find_elements('css_selector','a')
        for link in link_list:
            if link.text.endswith('.txt'):
                link.click()   

class PageUpload(PageEvent):
    def __init__(self) -> None:
        super().__init__("https://the-internet.herokuapp.com/upload")
    async def upload_image(self,image_path):
        input_file = await self.find_element('id',"file-upload")
        input_file.send_file(image_path)
    async def upload_pdf(self,pdf_path):
        input_file = await self.find_element('id',"file-upload")
        input_file.send_file(pdf_path)
    async def upload_text_file(self,text_file_path):
        input_file = await self.find_element('id',"file-upload")
        input_file.send_file(text_file_path)


# this my browser i name it "MyBrowser1" extend fro ChromeBrowser and this browser contains 2
# one handle for download i name it "tab_download" and other i name it "tab_upload" for upload
# and as you can see the name of async method that handles page should be begin with "tab" so browser know that 
# this will open a tab 
class MyBrowser1(ChromeBrowser):
    def __init__(self) -> None:
        self.path_download = r"c:\Users\progr\OneDrive\Bureau\test_download"
        option = ChromeOption('download.default_directory='+self.path_download)
        super().__init__(option, ChromeService())
    async def tab_download(self):
        page_download = await PageDownload().open()
        await page_download.download_pdf() 
        await page_download.download_images() 
        await page_download.download_text_files() 
        await page_download.wait_for_Download(self.path_download)
    async def tab_upload(self):
        page_upload = await PageUpload().open()
        await page_upload.upload_image(r"c:\Users\progr\Downloads\nature2.jpg")
        await page_upload.upload_pdf(r"c:\Users\progr\Downloads\DATA_Data_Analysis_2_AR.pdf")
        await page_upload.upload_text_file(r'd:\ascii.txt')
        await page_upload.sleep(3)

if __name__ == "__main__":
    Browser.startBrowsers([MyBrowser1()])
