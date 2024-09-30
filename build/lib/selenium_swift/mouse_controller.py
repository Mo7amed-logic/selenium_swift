from selenium.webdriver.common.action_chains import ActionChains
from typing import Literal

class MouseController:
    """
    A class to control mouse actions using Selenium's ActionChains.

    This class provides methods to perform various mouse operations, 
    such as moving the mouse, clicking, and dragging.

    Parameters
    ----------
    page : web_driver
        driver: The Selenium WebDriver instance.
    """
    def __init__(self, driver):
        """
        Initializes the MouseController class with a Selenium WebDriver instance.
        
        Args:
            driver: The Selenium WebDriver instance.
        """
        self.driver = driver 
        self.actions = ActionChains(self.driver )

    def move_to(self, x: int, y: int):
        """
        Move the mouse to the absolute position (x, y).
        
        Args:
            x: The x-coordinate to move the mouse to.
            y: The y-coordinate to move the mouse to.
        """
        self.actions.move_by_offset(x, y).perform()
        return self 

    def move_to_element(self, element):
        """
        Move the mouse to the specified web element, with an optional delay.
        
        Args:
            element: The WebElement to move the mouse to.
        """
        self.actions.move_to_element(element._info['e']).perform()
        return self
    def move_by(self, dx: int, dy: int):
        """
        Move the mouse by the relative offset (dx, dy).
        
        Args:
            dx: The x-coordinate offset to move the mouse by.
            dy: The y-coordinate offset to move the mouse by.
        """
        self.actions.move_by_offset(dx, dy).perform()

    def click(self, button: Literal['left', 'right'] = 'left'):
        """
        Perform a mouse click with the specified button.
        
        Args:
            button: The mouse button to click ('left', 'right').
        """
        if button == 'left':
            self.actions.click().perform()
        elif button == 'right':
            self.actions.context_click().perform()
        else:
            raise ValueError(f"Unsupported button type: {button}")
        return self

    def mouse_down(self, button: Literal['left', 'right'] = 'left'):
        """
        Press the specified mouse button down.
        
        Args:
            button: The mouse button to press down ('left', 'right').
        """
        if button == 'left':
            self.actions.click_and_hold().perform()
        elif button == 'right':
            self.actions.context_click().click_and_hold().perform()   # Custom right-click hold implementation
        else:
            raise ValueError(f"Unsupported button type: {button}")
        return self
    def mouse_up(self, button: Literal['left', 'right'] = 'left'):
        """
        Release the specified mouse button.
        
        Args:
            button: The mouse button to release ('left', 'right').
        """
        if button == 'left':
            self.actions.release().perform()
        elif button == 'right':
            self.actions.context_click().release().perform()  # Custom right-click release implementation
        else:
            raise ValueError(f"Unsupported button type: {button}")
        return self 
    def double_click(self):
        """
        Perform a double-click action.
        """
        self.actions.double_click().perform()
        return self
