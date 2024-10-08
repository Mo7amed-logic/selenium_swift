# selenium_swift
<img src="https://raw.githubusercontent.com/Mo7amed-logic/selenium_swift/refs/heads/master/selen_img1.webp" alt="selenium_swift" width="300"/>

**`selenium_swift`** is a powerful Python package designed to accelerate and simplify web scraping tasks using Selenium. With a focus on speed, accuracy, and ease of use, `selenium_swift` offers advanced features that cater to both beginners and experienced developers.

## Key Features

- **Advanced Element Handling:** Interact with web elements effortlessly using a high-level API. The `Element` class supports synchronous and asynchronous operations, making actions like clicking, sending keys, and capturing screenshots straightforward.

- **Frame Management:** The `Frame` class makes working with iframes easier by providing methods to switch and focus on specific frames, ensuring precise element interactions within complex page structures.

- **Chrome Extension Integration:** Use the `ChromeExtension` class to manage and interact with Chrome extensions directly within your scraping tasks.

- **Flexible WebDriver Options:** Configure WebDriver settings with the `WebOption` class, including headless mode, proxy settings, and custom profiles. Tailor your WebDriver to suit specific scraping needs.

- **Automatic Driver Management:** The `WebService` class handles WebDriver installations for Chrome, Firefox, and Edge BrowserManagers, leveraging `webdriver-manager` for seamless driver management.

- **Asynchronous and Synchronous Support:** Choose between async programming with `asyncio` or traditional synchronous methods to optimize performance and flexibility.

- **User-Friendly API:** Designed for simplicity and efficiency, `selenium_swift` abstracts complex Selenium operations, making web scraping accessible to beginners while offering powerful tools for advanced users.

## Installation

Install `selenium_swift` from PyPI using pip:

```bash
pip install selenium-swift
```
## Usage Example

### Example 1:
#### Explanation
This example demonstrates how to handle interactions with pages that open as a result of an event (such as a click or key press) using a custom BrowserManager class built on top of `ChromeBrowserManager`. The code showcases how to find elements on a page, trigger events to open new pages, and interact with the newly opened pages asynchronously.

##### Key Concepts:

1. **BrowserManager Class:** We define a class `MyBrowserManager` that extends from `ChromeBrowserManager` to customize BrowserManager behavior.

2. **Async Tab Method:** Methods that interact with BrowserManager tabs should be named with a `tab` prefix, which the framework recognizes as a tab interaction.

3. **Page Navigation:** The example shows how to load a page, find specific elements (in this case, product thumbnails), and handle page transitions when an event (like a click) triggers the opening of a new page.

4. **Handling New Pages:** After triggering an event that opens a new page, the script switches focus to the new page and interacts with its contents.

#### Example Code 

```python
from selenium_swift.BrowserManager import * 

class MyBrowserManager(ChromeBrowserManager):
    """
    MyBrowserManager extends ChromeBrowserManager to define custom interactions with web pages.
    This class demonstrates how to interact with elements on a page and handle events
    that open new BrowserManager tabs or windows.
    """
    
    def __init__(self) -> None:
        # Initialize the BrowserManager with Chrome-specific options and service
        super().__init__(ChromeOption(), ChromeService())
    
    async def tab_1(self):
        """
        This method opens a webpage and interacts with its elements. Specifically, it clicks on
        product thumbnails, which open new pages, and interacts with the newly opened page.
        """
        # Open the page at the specified URL
        page = await self.get('https://books.toscrape.com/')
        
        # Find all product elements in page
        products = await page.find_elements('css_selector', '.thumbnail')
        print(f"Found {len(products)} products.")
        
        # Loop through each product, click it to open a new page, and interact with the new page
        for prd in products:
            # Click the product, which opens a new page
            prd.click()
            
            # Switch focus to the newly opened page
            infoPage = page.focus_to_new_page()
            
            # Find the rows in the table on the new page using a CSS selector
            table_rows = await infoPage.find_elements('css_selector', 'table[class*="table-stripe"] tr')
            print("********** Table Content **********")
            
            # Loop through the table rows and print their text content
            for row in table_rows:
                print(row.text)
    
if __name__ == "__main__":
    # Start the BrowserManager with an instance of MyBrowserManager
    BrowserManager.startBrowserManagers([MyBrowserManager()])
```

#### Breakdown of the Code
1. `MyBrowserManager` Class: This class inherits from `ChromeBrowserManager`. Inside, we define the `tab_1` method to represent interactions on the first tab on window opened by the BrowserManager.
    - The `super().__init__(ChromeOption(), ChromeService()) `ensures that the BrowserManager is initialized with default Chrome options and services.

2. `tab_1` Method:
    - This method loads the page `https://books.toscrape.com/.`
    - It finds all product elements on the page using the CSS selector .`thumbnail.`
    - For each product, the script clicks it, causing a new page to open.
    - Once the new page is opened, the script switches focus to that page using `focus_to_new_page().`
    - It then locates a table of data on the new page using a CSS selector, iterates through the rows, and prints the content of each row.

3. BrowserManager Startup: The `if __name__ == "__main__":` block ensures that the script runs the BrowserManager when executed. It calls `BrowserManager.startBrowserManagers([MyBrowserManager()])` to start the BrowserManager and execute the interactions defined in `tab_1`.

#### Key Considerations
- **Async Interactions:** The example utilizes async programming to handle potentially slow operations (like loading a page or finding elements) without blocking the main thread.
- **Scalability:** You can extend this by adding more tab methods (e.g., `tab_2`, `tab_3`, etc.) to handle different interactions or pages.
- **Error Handling:** In production environments, adding error handling (e.g., for timeouts or missing elements) is important for robustness.

This example is designed to demonstrate how to automate interaction with pages that open through events and how to interact with the newly opened page.


### Example 2:
#### Explanation
This example demonstrates how to interact with new pages opened by an event (e.g., a click) using an object-oriented approach. Instead of directly focusing on a new page using `focus_to_new_page()`, we create a `PageInfo` class that extends `NextPage`, a base class designed for handling pages that are opened from other pages.

##### Key Concepts: 
1. **Page Class (`PageInfo`):** This class inherits from `NextPage` and is used to represent and interact with pages that are opened by user interactions (like clicking on an element).

2. **Separation of Concerns:** Each page interaction is encapsulated within its own class, making the code modular and easier to maintain.

3. **Async Page Interactions:** The `showData` method in `PageInfo` asynchronously finds elements and displays their data, demonstrating how to interact with a newly opened page.

### Example Code 
```python 
from selenium_swift.BrowserManager import *  # Import base BrowserManager classes
from selenium_swift.web_option import ChromeOption  # Import Chrome options
from selenium_swift.web_service import ChromeService  # Import Chrome services

class PageInfo(NextPage):
    """
    PageInfo is a class that extends NextPage. It is used to handle the
    new page that opens after interacting with an element on the current page.
    This class encapsulates interactions with the new page.
    """
    def __init__(self) -> None:
        super().__init__()  # Initialize the NextPage base class

    async def showData(self):
        """
        This method finds table rows on the newly opened page and prints the content
        of each row. The data is located using a CSS selector.
        """
        # Locate the table rows using the CSS selector
        table_rows = await self.find_elements('css_selector', 'table[class*="table-stripe"] tr')
        
        # Print the content of each table row
        print("********** Table Content **********")
        for row in table_rows:
            print(row.text)

class MyBrowserManager(ChromeBrowserManager):
    """
    MyBrowserManager is a custom BrowserManager class that extends ChromeBrowserManager.
    It contains methods to interact with the main page and handle navigation
    to new pages.
    """
    def __init__(self) -> None:
        # Initialize ChromeBrowserManager with default Chrome options and services
        super().__init__(ChromeOption(), ChromeService())

    async def tab_1(self):
        """
        This method interacts with the first tab. It opens a webpage, locates product elements,
        and handles navigation to the new page when a product is clicked.
        """
        # Load the main page
        page = await self.get('https://books.toscrape.com/')
        
        # Find all product elements on the page
        products = await page.find_elements('css_selector', '.thumbnail')
        print(f"Found {len(products)} products.")
        
        # Loop through the products and handle interactions with the new page
        for prd in products:
            # Click the product, which opens a new page
            prd.click()

            # Create an instance of PageInfo to represent the new page
            # and interact with it using the showData method
            await PageInfo().showData()

if __name__ == "__main__":
    # Start the BrowserManager with an instance of MyBrowserManager and open the first tab
    BrowserManager.startBrowserManagers([MyBrowserManager()])

```
### Breakdown of the Code
1. **`PageInfo` Class:**
    - This class extends `NextPage`, which is designed to represent a page that opens as a result of an interaction (like clicking on an element).
    - The method `showData` asynchronously finds table rows using a CSS selector and prints the content of each row.

2. **`MyBrowserManager` Class:**
    - This class extends `ChromeBrowserManager` and defines the `tab_1` method for interactions on the main page.
    - It opens the main page (`https://books.toscrape.com/`) and locates all product elements using the `.thumbnail` CSS selector.
    - When a product is clicked, a new page opens. Instead of focusing directly on the new page, an instance of `PageInfo` is created, and the `showData` method is called to interact with the new page.

3. **BrowserManager Flow:**
    - The BrowserManager starts by opening the main page, where it finds and clicks on product elements.
    - Each click opens a new page, which is handled by `PageInfo.` This class abstracts the interaction with the newly opened page, making the code cleaner and more modular.

4. **Object-Oriented Design:**
    - By using a class (`PageInfo`) to represent the new page, you ensure that all interactions with that page are encapsulated in one place. This separation of concerns makes the code easier to maintain and extend.
    - The base class `NextPage` can be extended further if more features need to be added, and `PageInfo` can be customized for specific interactions with different pages.
This example shows how to manage page interactions using class inheritance, following best practices for code organization and readability.


### Example 3:
This example shows how to use `selenium_swift` to scrape a web page. Follow these steps:

1. Create your own `Scrap` class that extends from the `PageScrape` 
class and contains the `async def onResponse` method that includes your **arg**.
2. Create a `MyBrowserManager` class that extends from `ChromeBrowserManager`, `FirefoxBrowserManager`, or `EdgeBrowserManager`.
Here, I use `ChromeBrowserManager`. You should create async methods that begin with "tab", e.g.,
`tab_1`, `tab_2`, etc. Each tab method will open a tab in your BrowserManager.

```python
from selenium_swift.BrowserManager import * 

class Scrap(PageScrape):
    async def onResponse(self, **arg):
        quote_elements = await self.find_elements('css_selector','.text')
        for quote in quote_elements:
            print(quote.text)

class MyBrowserManager(ChromeBrowserManager):
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
    BrowserManager.startBrowserManagers([MyBrowserManager()])
```

### Example 4: Concurrent File Upload and Download
This example demonstrates how to concurrently upload and download files using the `selenium_swift` package with a custom BrowserManager class. 

#### Step 1: Create the MyBrowserManager Class
In this step, we will create a class named `MyBrowserManager` for example , which extends from the `ChromeBrowserManager` class. This class will contain two asynchronous methods: `tab_download` and `tab_upload`. Each method will handle a specific functionality—downloading files and uploading files—by opening separate tabs in the BrowserManager.

```python
from selenium_swift.BrowserManager import *

class MyBrowserManager(ChromeBrowserManager):
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

- **Waiting for Downloads:** The await `page.wait_for_Download(self.path_download)` statement ensures that the method waits until the download is completed before BrowserManager close all the tabs. 

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

#### Step 4: Running the BrowserManager
Finally, we will execute the `MyBrowserManager` class to start the BrowserManager and perform the file upload and download tasks concurrently.

```python
if __name__ == "__main__":
    BrowserManager.startBrowserManagers([MyBrowserManager()])

```
### Summary 
This example showcases how to create a custom BrowserManager class using `selenium_swift` for handling file uploads and downloads. By organizing the functionality into methods, you can easily maintain and extend the capabilities of your web scraping tasks.
```python
from selenium_swift.BrowserManager import *

class MyBrowserManager(ChromeBrowserManager):
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
### Example 5: Custom Page Handling in selenium_swift

This example demonstrates how to create custom page classes that extend the `PageEvent` class within the `selenium_swift` framework. This approach allows for modular and organized handling of web interactions, such as downloading and uploading files.

#### Overview
In this implementation, two separate pages are created:
1. **PageDownload:** This class is designed for downloading files from a specific webpage.
2. **PageUpload:** This class facilitates uploading files to a designated webpage.

You can create custom page classes to manage complex interactions, such as clicks, file uploads, mouse events, and other interactions.

#### Implementation
```python
from selenium_swift.BrowserManager import *

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

# Define the MyBrowserManager1 class to manage download and upload actions
class MyBrowserManager1(ChromeBrowserManager):
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

# Start the BrowserManager and run the download and upload tasks
if __name__ == "__main__":
    BrowserManager.startBrowserManagers([MyBrowserManager1()])
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
2. **MyBrowserManager1 Class:**
    - This class extends `ChromeBrowserManager` and manages two separate tabs for downloading and uploading files. The methods prefixed with `tab_` signal to the BrowserManager that they will open a new tab.
    - `tab_download()`: Opens the download page and executes methods to download various file types, followed by waiting for the download to complete.
    - `tab_upload()`: Opens the upload page and executes methods to upload specified files. The sleep method is called to pause execution for a brief period, allowing the upload to complete.

#### Conclusion
By extending the `PageEvent` class, you can create specialized page handling classes that streamline file download and upload processes, making your web scraping tasks more efficient and organized. This structure also enhances readability and maintainability of your code.


