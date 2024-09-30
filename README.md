# selenium_swift

**`selenium_swift`** is a powerful Python package designed to accelerate and simplify web scraping tasks using Selenium. With a focus on speed, accuracy, and ease of use, `selenium_swift` offers advanced features that cater to both beginners and experienced developers.

## Key Features

- **Advanced Element Handling:** Interact with web elements effortlessly using a high-level API. The `Element` class supports synchronous and asynchronous operations, making actions like clicking, sending keys, and capturing screenshots straightforward.

- **Frame Management:** The `Frame` class makes working with iframes easier by providing methods to switch and focus on specific frames, ensuring precise element interactions within complex page structures.

- **Chrome Extension Integration:** Use the `ChromeExtension` class to manage and interact with Chrome extensions directly within your scraping tasks.

- **Flexible WebDriver Options:** Configure WebDriver settings with the `WebOption` class, including headless mode, proxy settings, and custom profiles. Tailor your WebDriver to suit specific scraping needs.

- **Automatic Driver Management:** The `WebService` class handles WebDriver installations for Chrome, Firefox, and Edge browsers, leveraging `webdriver-manager` for seamless driver management.

- **Asynchronous and Synchronous Support:** Choose between async programming with `asyncio` or traditional synchronous methods to optimize performance and flexibility.

- **User-Friendly API:** Designed for simplicity and efficiency, `selenium_swift` abstracts complex Selenium operations, making web scraping accessible to beginners while offering powerful tools for advanced users.

## Installation

Install `selenium_swift` from PyPI using pip:

```bash
pip install selenium_swift
```
## Usage Example

### Example 1:
This example shows how to use `selenium_swift` to scrape a web page. Follow these steps:

1. Create your own `Scrap` class that extends from the `PageScrape` 
class and contains the `async def onResponse` method that includes your **arg**.
2. Create a `MyBrowser` class that extends from `ChromeBrowser`, `FirefoxBrowser`, or `EdgeBrowser`.
Here, I use `ChromeBrowser`. You should create async methods that begin with "tab", e.g.,
`tab_1`, `tab_2`, etc. Each tab method will open a tab in your browser.

```python
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
        for i in range(1, 3):
            await Scrap(f'https://quotes.toscrape.com/page/{i}/').crawl(my_index=i)

    async def tab_2(self):
        for i in range(3, 6):
            await Scrap(f'https://quotes.toscrape.com/page/{i}/').crawl(my_index=i)

    async def tab_3(self):
        for i in range(6, 9):
            await Scrap(f'https://quotes.toscrape.com/page/{i}/').crawl(my_index=i)

    async def tab_4(self):
        for i in range(9, 11):
            await Scrap(f'https://quotes.toscrape.com/page/{i}/').crawl(my_index=i)

if __name__ == "__main__":
    Browser.startBrowsers([MyBrowser()])
```

### Example 2: Concurrent File Upload and Download
This example demonstrates how to concurrently upload and download files using the `selenium_swift` package with a custom browser class. 

#### Step 1: Create the MyBrowser Class
In this step, we will create a class named `MyBrowser` for example , which extends from the `ChromeBrowser` class. This class will contain two asynchronous methods: `tab_download` and `tab_upload`. Each method will handle a specific functionality—downloading files and uploading files—by opening separate tabs in the browser.

```python
from selenium_swift.browser import *

class MyBrowser(ChromeBrowser):
    def __init__(self) -> None:
        # Set the download directory
        self.path_download = r"c:\Users\progr\OneDrive\Bureau\test_download"
        option = ChromeOption('download.default_directory=' + self.path_download)
        super().__init__(option, ChromeService())

```
- **Initialization:** The `__init__` method sets the download directory for downloaded files using the `ChromeOption` class. This ensures that all downloaded files will be saved to the specified path.

#### Step 2: Implement the `tab_download` Method
The `tab_download` method will navigate to a page that contains downloadable files. It will identify links to PDF files and initiate the download process.

```python
    async def tab_download(self):
        # Navigate to the download page
        page = await self.get('https://the-internet.herokuapp.com/download')
        link_list = await page.find_elements('css_selector', 'a')
        
        # Iterate through the links and click on those that end with '.pdf'
        for link in link_list:
            if link.text.endswith('.pdf'):
                link.click()
        
        # Wait for the download to complete (put this statment in the end of the tab)
        await page.wait_for_Download(self.path_download)
```
- **File Download Logic:** The method retrieves all links on the page and checks if they end with the `.pdf` extension. If so, it clicks the link to start the download.

- **Waiting for Downloads:** The await `page.wait_for_Download(self.path_download)` statement ensures that the method waits until the download is completed before browser close all the tabs. 

#### Step 3: Implement the `tab_upload` Method
The `tab_upload` method will navigate to a file upload page, locate the file input element, and upload a specified file.

```python
    async def tab_upload(self):
        # Navigate to the upload page
        page = await self.get('https://the-internet.herokuapp.com/upload')
        
        # Locate the file input element and upload a file
        input_file = await page.find_element('id', "file-upload")
        input_file.send_file(r'c:\Users\progr\Downloads\DATA_Data_Analysis_2_AR.pdf')
        
        # Optional: wait for a brief period to ensure the file is uploaded
        await page.sleep(3)

```

- **File Upload Logic:** The method retrieves the file input element by its ID and uses the `send_file` method to upload a specified file from the local system.
- **Sleep Function:** The `await page.sleep(3)` statement pauses the execution for 3 seconds, allowing time for the file upload to complete. It’s important to use `page.sleep()` instead of time.sleep() in asynchronous code. Using `time.sleep()` will block the entire event loop, preventing other asynchronous tasks from running, which can lead to unresponsive behavior in your application. By using `await page.sleep()`, the event loop remains active, allowing other tasks to be executed concurrently while waiting.

#### Step 4: Running the Browser
Finally, we will execute the `MyBrowser` class to start the browser and perform the file upload and download tasks concurrently.

```python
if __name__ == "__main__":
    Browser.startBrowsers([MyBrowser()])

```
### Summary 
This example showcases how to create a custom browser class using `selenium_swift` for handling file uploads and downloads. By organizing the functionality into methods, you can easily maintain and extend the capabilities of your web scraping tasks.
```python
from selenium_swift.browser import *

class MyBrowser(ChromeBrowser):
    def __init__(self) -> None:
        # Set the download directory
        self.path_download = r"c:\Users\progr\OneDrive\Bureau\test_download"
        option = ChromeOption('download.default_directory=' + self.path_download)
        super().__init__(option, ChromeService())
    async def tab_download(self):
        # Navigate to the download page
        page = await self.get('https://the-internet.herokuapp.com/download')
        link_list = await page.find_elements('css_selector', 'a')
        
        # Iterate through the links and click on those that end with '.pdf'
        for link in link_list:
            if link.text.endswith('.pdf'):
                link.click()
        
        # Wait for the download to complete (put this statment in the end of the tab)
        await page.wait_for_Download(self.path_download)
    async def tab_upload(self):
        # Navigate to the upload page
        page = await self.get('https://the-internet.herokuapp.com/upload')
        
        # Locate the file input element and upload a file
        input_file = await page.find_element('id', "file-upload")
        input_file.send_file(r'c:\Users\progr\Downloads\DATA_Data_Analysis_2_AR.pdf')
        
        # Optional: wait for a brief period to ensure the file is uploaded
        await page.sleep(3)
```
### Example 3: Custom Page Handling in selenium_swift

This example demonstrates how to create custom page classes that extend the `PageEvent` class within the `selenium_swift` framework. This approach allows for modular and organized handling of web interactions, such as downloading and uploading files.

#### Overview
In this implementation, two separate pages are created:
1. **PageDownload:** This class is designed for downloading files from a specific webpage.
2. **PageUpload:** This class facilitates uploading files to a designated webpage.

You can create custom page classes to manage complex interactions, such as clicks, file uploads, mouse events, and other interactions.

#### Implementation
```python
from selenium_swift.browser import *

# Define the PageDownload class to handle file downloads
class PageDownload(PageEvent):
    def __init__(self) -> None:
        super().__init__('https://the-internet.herokuapp.com/download')
    async def download_images(self):
        link_list = await self.find_elements('css_selector', 'a')
        for link in link_list:
            if link.text.endswith(('.png', '.jpg')):
                link.click()

    async def download_pdf(self):
        link_list = await self.find_elements('css_selector', 'a')
        for link in link_list:
            if link.text.endswith('.pdf'):
                link.click()

    async def download_text_files(self):
        link_list = await self.find_elements('css_selector', 'a')
        for link in link_list:
            if link.text.endswith('.txt'):
                link.click()

# Define the PageUpload class to handle file uploads
class PageUpload(PageEvent):
    def __init__(self) -> None:
        super().__init__('https://the-internet.herokuapp.com/upload')

    async def upload_image(self, image_path):
        input_file = await self.find_element('id', "file-upload")
        input_file.send_file(image_path)

    async def upload_pdf(self, pdf_path):
        input_file = await self.find_element('id', "file-upload")
        input_file.send_file(pdf_path)

    async def upload_text_file(self, text_file_path):
        input_file = await self.find_element('id', "file-upload")
        input_file.send_file(text_file_path)

# Define the MyBrowser1 class to manage download and upload actions
class MyBrowser1(ChromeBrowser):
    def __init__(self) -> None:
        self.path_download = r"c:\Users\progr\OneDrive\Bureau\test_download"
        option = ChromeOption('download.default_directory=' + self.path_download)
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

# Start the browser and run the download and upload tasks
if __name__ == "__main__":
    Browser.startBrowsers([MyBrowser1()])
```

#### Explanation
1. **Custom Page Classes:** 
    - **PageDownload:** This class encapsulates methods to download different file types. Each method fetches all links on the page and clicks on the ones that match the specified file extensions.
        - `download_images()`: Downloads image files with `.png` or `.jpg` extensions.
        - `download_pdf()`: Downloads files with a `.pdf` extension.
        - `download_text_files()`: Downloads files with a `.txt` extension.
    - **PageUpload:** This class provides methods to upload files. Each method allows for the upload of a specific file type.  
        - `upload_image(image_path)`: Uploads an image file.
        - `upload_pdf(pdf_path)`: Uploads a PDF file.
        - `upload_text_file(text_file_path)`: Uploads a text file.
2. **MyBrowser1 Class:**
    - This class extends `ChromeBrowser` and manages two separate tabs for downloading and uploading files. The methods prefixed with `tab_` signal to the browser that they will open a new tab.
    - `tab_download()`: Opens the download page and executes methods to download various file types, followed by waiting for the download to complete.
    - `tab_upload()`: Opens the upload page and executes methods to upload specified files. The sleep method is called to pause execution for a brief period, allowing the upload to complete.

#### Conclusion
By extending the `PageEvent` class, you can create specialized page handling classes that streamline file download and upload processes, making your web scraping tasks more efficient and organized. This structure also enhances readability and maintainability of your code.


