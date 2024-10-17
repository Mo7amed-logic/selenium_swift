# selenium_swift
<img src="https://raw.githubusercontent.com/Mo7amed-logic/selenium_swift/refs/heads/master/selen_img1.webp" alt="selenium_swift" width="300"/>

**`selenium_swift`** is a powerful Python package designed to accelerate and simplify web scraping tasks using Selenium. With a focus on speed, accuracy, and ease of use, `selenium_swift` offers advanced features that cater to both beginners and experienced developers.

## Key Features

- **Advanced Element Handling**: Interact with web elements effortlessly using a high-level API. The `Element` class supports synchronous and asynchronous operations, making actions like clicking, sending keys, and capturing screenshots straightforward.

- **Frame Management**: The `Frame` class simplifies working with iframes by providing methods to switch and focus on specific frames, ensuring precise element interactions within complex page structures.

- **CAPTCHA Solving**: Easily integrate CAPTCHA-solving capabilities using `2Captcha` and Tesseract OCR. The package includes asynchronous functions to handle image CAPTCHAs and improve automation in scraping tasks. **Coming soon**: A new feature will allow for complex CAPTCHAs to be solved remotely by a human using the socket library. This feature will enable real-time CAPTCHA solving, allowing users to send CAPTCHAs for human resolution during automation.

- **Remote Server Capabilities**: Connect to remote WebDriver instances to execute your scraping tasks on servers. This feature enables distributed scraping, allowing you to run multiple instances across different environments for enhanced performance and resource utilization.

- **Web Downloading**: Utilize built-in features to download files directly from web pages. The `WebDownloader` class facilitates file downloading through simple method calls, making it easy to gather resources from the web.

- **JSON Handling**: The `JsonHandler` class simplifies saving and loading JSON data. This feature allows users to easily store scraped data in JSON format, enhancing data management and usability.

- **Mouse Control**: The `MouseController` class provides advanced mouse control functionalities, allowing you to simulate mouse movements and clicks. This feature is useful for interacting with dynamic web content, such as drag-and-drop actions and hover effects.

- **Alert Handling**: The `AlertHandler` class simplifies the process of managing browser alerts and pop-ups. Easily accept, dismiss, or retrieve messages from alerts during your scraping tasks, allowing for a smoother automation experience.

- **Chrome Extension Integration**: Utilize the `ChromeExtension` class to manage and interact with Chrome extensions directly within your scraping tasks, enhancing your automation capabilities.

- **Flexible WebDriver Options**: Configure WebDriver settings easily with the `WebOption` class, including headless mode, proxy settings, and custom profiles, allowing you to tailor your WebDriver to suit specific scraping needs.

- **Automatic Driver Management**: The `WebService` class handles WebDriver installations for Chrome, Firefox, and Edge BrowserManagers, leveraging `webdriver-manager` for seamless driver management.

- **Asynchronous and Synchronous Support**: Choose between async programming with `asyncio` or traditional synchronous methods, optimizing performance and flexibility based on your project requirements.

- **User-Friendly API**: Designed for simplicity and efficiency, `selenium_swift` abstracts complex Selenium operations, making web scraping accessible to beginners while providing powerful tools for advanced users.

## Installation

Install `selenium_swift` from PyPI using pip:

```bash
pip install selenium-swift
```
## Usage Example

### Example 1:Scraping Quotes and Tables with selenium_swift

In this example, we will scrape data, specifically quotes, from a website and a table from another website using the `selenium_swift` package. We will create two classes, `PageQuote` and `PageTable`, that extend from `PageScrape` to handle the specific scraping tasks.

##### Step 1: Create the `PageQuote` Class:
First, we define the `PageQuote` class, which will be responsible for scraping quotes from a web page:
```python
class PageQuote(PageScrape):
    dataQuotes = []

    async def onResponse(self, **arg):
        self.set_implicite_timeout(2)  # Set an implicit timeout for element searches
        quotes = await self.find_elements('css_selector', '.quote')  # Find all quote elements
        texts = (await quotes.find_element('css_selector', '.text')).text  # Extract quote texts
        authors = (await quotes.find_element('css_selector', 'small.author')).text  # Extract authors
        tags = (await quotes.find_elements('css_selector', 'a.tag')).text  # Extract tags
        data = [{'text': text, 'author': author, 'tags': tags} 
                for text, author, tags in zip(texts, authors, tags)]  # Compile data into a list of dictionaries
        PageQuote.dataQuotes.append(data)  # Append the data to the class variable
```
##### Explanation:
- **Class Declaration:** `PageQuote` inherits from `PageScrape`, enabling it to handle scraping tasks easily.

- **Data Storage:** The `dataQuotes` class variable stores all scraped quote data.

- **onResponse Method:** This asynchronous method is triggered when the page responds. It sets an implicit timeout and uses CSS selectors to find and extract text from the quote elements. The quotes, authors, and tags are collected and formatted into a list of dictionaries, which is then appended to `dataQuotes`.

##### Step 2: Create the `PageTable` Class
Next, we create the `PageTable` class to scrape table data from another website:
```python
class PageTable(PageScrape):
    dataTables = []

    async def onResponse(self, **arg):
        rows_table = await self.find_elements('css_selector', 'table tr')  # Find all table rows
        PageTable.dataTables.append(rows_table.text)  # Append the table row texts to the class variable

```
#### Explanation:
- Similar to `PageQuote`, the `PageTable` class inherits from `PageScrape`.
- The `dataTables` class variable holds the scraped table data.
- The `onResponse` method finds all rows in the table using a CSS selector and stores their text in `dataTables`.


#### Step 3: Create Your Browser Class
Now, we create a `Browser` class that extends from either `ChromeBrowser`, `FirefoxBrowser`, or `EdgeBrowser`. In this case, we'll use `ChromeBrowser`:

```python
class Browser(ChromeBrowser):
    def __init__(self):
        super().__init__(ChromeOption(), ChromeService())
    
    async def tab_1(self):
        for i in range(1, 4):
            await PageQuote(f'https://quotes.toscrape.com/page/{i}/').crawl()  # Scrape quotes from pages 1 to 3
    
    async def tab_2(self):
        for i in range(4, 7):
            await PageQuote(f'https://quotes.toscrape.com/page/{i}/').crawl()  # Scrape quotes from pages 4 to 6
    
    async def tab_3(self):
        for i in range(7, 11):
            await PageQuote(f'https://quotes.toscrape.com/page/{i}/').crawl()  # Scrape quotes from pages 7 to 10
    
    async def tab_4(self):
        await PageTable(f'https://the-internet.herokuapp.com/challenging_dom').crawl()  # Scrape table data
    
    def onClose(self):
        print('Browser closed ....')
        save_json_data(PageQuote.dataQuotes, 'quotes.json')  # Save scraped quotes to a JSON file
        save_json_data(PageTable.dataTables, 'table.json')  # Save scraped table data to a JSON file

```
#### Explanation:
- **Class Declaration:** `Browser` inherits from `ChromeBrowser` to leverage Chrome for scraping.

- **Initialization:** The constructor calls the parent class constructor to set up the browser options and service.

- **Tab Methods:** Each method (e.g., `tab_1`, `tab_2`, etc.) begins with the prefix "tab". This naming convention is crucial because it ensures that the browser recognizes these methods as asynchronous tabs, allowing them to open in separate browser tabs.

- **onClose Method:** This method is called when the browser closes, saving the scraped data to JSON files.

#### Step 4: Run the Browser Manager
Finally, we create the `main` function to start the browser:
```python
async def main():
    await BrowserManager.startBrowsers([Browser()])  # Start the browser manager with our custom browser class

if __name__ == '__main__':
    asyncio.run(main())  # Execute the main function

```
#### Explanation:
- The `main` function starts the `BrowserManager`, which handles the opening and management of the browser instances defined in the `Browser` class.
The script is executed using `asyncio.run(main())`, which ensures the asynchronous tasks are properly awaited.

### Summary
In this example, you have learned how to:
1. Create classes that extend the `PageScrape` class for scraping specific data types (quotes and tables).

2. Define a custom browser class that manages asynchronous tab operations, allowing multiple web pages to be scraped simultaneously.

3. Use the `BrowserManager` to initialize and manage the browser instances.
By following this example, you can effectively use the selenium_swift package to automate web scraping tasks with minimal effort. Customize the class methods and CSS selectors as needed to fit your specific scraping needs!
### Complete Example

```python
from selenium_swift.browser import *
from selenium_swift.json_handler import save_json_data
import asyncio

# Step 1: Create PageQuote Class
class PageQuote(PageScrape):
    dataQuotes = []

    async def onResponse(self, **arg):
        self.set_implicite_timeout(2)
        quotes = await self.find_elements('css_selector', '.quote')
        texts = (await quotes.find_element('css_selector', '.text')).text
        authors = (await quotes.find_element('css_selector', 'small.author')).text
        tags = (await quotes.find_elements('css_selector', 'a.tag')).text
        data = [{'text': text, 'author': author, 'tags': tags} 
                for text, author, tags in zip(texts, authors, tags)]
        PageQuote.dataQuotes.append(data)

# Step 2: Create PageTable Class
class PageTable(PageScrape):
    dataTables = []

    async def onResponse(self, **arg):
        rows_table = await self.find_elements('css_selector', 'table tr')
        PageTable.dataTables.append(rows_table.text)

# Step 3: Create Browser Class
class Browser(ChromeBrowser):
    def __init__(self):
        super().__init__(ChromeOption(), ChromeService())
    
    async def tab_1(self):
        for i in range(1, 4):
            await PageQuote(f'https://quotes.toscrape.com/page/{i}/').crawl()
    
    async def tab_2(self):
        for i in range(4, 7):
            await PageQuote(f'https://quotes.toscrape.com/page/{i}/').crawl()
    
    async def tab_3(self):
        for i in range(7, 11):
            await PageQuote(f'https://quotes.toscrape.com/page/{i}/').crawl()
    
    async def tab_4(self):
        await PageTable(f'https://the-internet.herokuapp.com/challenging_dom').crawl()
    
    def onClose(self):
        print('Browser closed ....')
        save_json_data(PageQuote.dataQuotes, 'quotes.json')
        save_json_data(PageTable.dataTables, 'table.json')

# Step 4: Run the Browser Manager
async def main():
    await BrowserManager.startBrowsers([Browser()])

if __name__ == '__main__':
    asyncio.run(main())
```

### Example 2: File Downloads and Uploads with selenium_swift
In this example, we will create a custom browser class, `MyBrowser`, which will handle downloading and uploading files using the `selenium_swift` package. The browser class extends `ChromeBrowser`, allowing us to leverage Chrome's capabilities for automation.

#### Step 1: Create the `MyBrowser` Class
We start by defining the `MyBrowser` class. This class takes parameters for the download path, file extension to download, and a flag for file upload:

```python
class MyBrowser(ChromeBrowser):
    def __init__(self, download_path, extension, upload_file):
        self.extension = extension  # File extension to download (e.g., '.txt')
        self.download_path = download_path  # Path where files will be downloaded
        self.upload_file = upload_file  # Flag indicating whether to perform file upload
        super().__init__(ChromeOption('download.default_directory=' + download_path), ChromeService())

```
#### Explanation:

- **Class Declaration:** `MyBrowser` extends `ChromeBrowser`, allowing it to use Chrome's capabilities for scraping.
- **Initialization:** The constructor accepts three parameters: `download_path`, extension, and `upload_file`. It sets up the download directory and initializes the browser with these options.
- **Chrome Options:** The `download.default_directory` option specifies where downloaded files will be stored.

#### Step 2: Define the tab_download_files Method
Next, we create a method to handle downloading files from a specified page:
```python
async def tab_download_files(self):
    page = await self.get('https://the-internet.herokuapp.com/download')  # Navigate to the download page
    a_tags = await page.find_elements('tag_name', 'a')  # Find all anchor tags
    for tag in a_tags:
        if tag.text.endswith(self.extension):  # Check if the tag text ends with the specified extension
            tag.click()  # Click on the link to download the file
    
    if self.extension == '.txt':
        await BrowserManager.startBrowsers([MyBrowser(self.download_path, '.pdf', False)])  # Start another browser instance to download PDF

    await page.wait_for_Download(self.download_path)  # Wait for the download to complete

```
#### Explanation:

- **Method Declaration:** The `tab_download_files` method is defined as an asynchronous function.
- **Page Navigation:** It navigates to a specific URL where files can be downloaded.
- **Element Selection:** It retrieves all anchor (`<a>`) tags on the page to find links for files.
- **File Downloading:** For each anchor tag, if the text ends with the specified file extension (like `.txt`), it triggers a click to start the download.
- **Conditional Browsing:** If the specified extension is `.txt`, it starts another browser instance to download a PDF file, demonstrating how you can initiate multiple downloads in parallel.
- **Wait for Download:** The method waits for the download process to complete before proceeding.

#### Step 3: Define the tab_upload_files Method
Now, we implement a method for uploading files:
```python
async def tab_upload_files(self):
    if not self.upload_file:  # Check if upload is required
        return
    page = await self.get('https://the-internet.herokuapp.com/upload')  # Navigate to the upload page
    (await page.find_element('id', 'file-upload')).send_file(r'c:\Users\progr\Downloads\js_events_list.pdf')  # Upload the specified file
    await page.sleep(2)  # Wait for a moment to ensure the upload is processed

```
#### Explanation:

- **Method Declaration:** The `tab_upload_files` method is also asynchronous.
- **Conditional Upload:** It checks if the `upload_file` flag is set to `True`. If not, the method returns early.
- **Page Navigation:** The method navigates to a designated upload page.
- **File Uploading:** It finds the file input element by its ID and uses `send_file` to upload a specified file from the local path.
- **Sleep:** A short wait is included to ensure that the upload completes before moving on.
### Why Use await `page.sleep()` Instead of time.sleep()
1. **Non-blocking Behavior:** 
    - `time.sleep()` is a blocking call, meaning that when it’s executed, the entire program stops executing for the specified duration. This can cause the browser to become unresponsive and can lead to inefficiencies in asynchronous tasks.
    - In contrast, `await page.sleep()` is a non-blocking call. It allows other tasks to run while waiting for the sleep duration to complete. This is crucial in an asynchronous environment, where you want to keep the event loop active to handle multiple operations concurrently.
2. **Maintaining Asynchronous Flow:**
    - Using `await page.sleep()` allows the program to maintain its asynchronous flow. While one task is paused (like waiting for a file upload to finish), other tasks can continue executing. This is especially important when you have multiple browser tabs open that are performing different tasks simultaneously.
    - For example, if one tab is waiting for a file upload to complete, another tab can continue scraping data or downloading files without being held up by the sleep function.

#### Step 4: Run the Browser Manager
Finally, we create the `main` function to start multiple instances of `MyBrowser`, each configured for different file downloads:

```python
async def main():
    await BrowserManager.startBrowsers([
        MyBrowser(r'd:\text_download', '.txt', True),  # Download .txt files
        MyBrowser(r'd:\images_download', '.jpg', False),  # Download .jpg files
        MyBrowser(r'd:\images_download', '.png', False)  # Download .png files
    ], 'parallel', 3)  # Start browsers in parallel with a limit of 3 concurrent instances

if __name__ == '__main__':
    asyncio.run(main())  # Execute the main function

```
#### Explanation:

- **Main Function:** The `main` function uses `BrowserManager` to start multiple instances of `MyBrowser`.
- **Instances:** Each instance is configured with its own download path, file extension to download, and upload flag.
- **Parallel Execution:** The `BrowserManager` is instructed to run the browsers in parallel, with a limit of 3 concurrent instances.
- **Execution:** The script is executed using `asyncio.run(main())`, ensuring that all asynchronous tasks are handled properly.

### Complete Example
Below is the complete code for the MyBrowser class and the usage example:
```python
from selenium_swift.browser import *
import asyncio

class MyBrowser(ChromeBrowser):
    def __init__(self, download_path, extension, upload_file):
        self.extension = extension
        self.download_path = download_path 
        self.upload_file = upload_file
        super().__init__(ChromeOption('download.default_directory=' + download_path), ChromeService())

    async def tab_download_files(self):
        page = await self.get('https://the-internet.herokuapp.com/download')
        a_tags = await page.find_elements('tag_name', 'a')
        for tag in a_tags:
            if tag.text.endswith(self.extension):
                tag.click()
        
        if self.extension == '.txt':
            await BrowserManager.startBrowsers([MyBrowser(self.download_path, '.pdf', False)])

        await page.wait_for_Download(self.download_path)

    async def tab_upload_files(self):
        if not self.upload_file:
            return
        page = await self.get('https://the-internet.herokuapp.com/upload')
        (await page.find_element('id', 'file-upload')).send_file(r'c:\Users\progr\Downloads\js_events_list.pdf')
        await page.sleep(2)

async def main():
    await BrowserManager.startBrowsers([
        MyBrowser(r'd:\text_download', '.txt', True),
        MyBrowser(r'd:\images_download', '.jpg', False),
        MyBrowser(r'd:\images_download', '.png', False)
    ], 'parallel', 3)

if __name__ == '__main__':
    asyncio.run(main())
```
### Summary
In this example, you learned how to:

1. Create a custom browser class that manages file downloads and uploads using the `selenium_swift` package.
2. Use asynchronous methods to handle tasks like downloading multiple file types and uploading files with conditional checks.
3. Start multiple instances of the custom browser in parallel, demonstrating how to efficiently manage multiple download tasks simultaneously.
By following this example, you can effectively automate file handling tasks with the `selenium_swift` package. Customize the parameters and methods as needed to fit your specific automation requirements!