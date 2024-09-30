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

Example 1:
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

