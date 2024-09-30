from selenium import webdriver
from selenium.webdriver.common.alert import Alert
import time

class AlertHandler:
    def __init__(self,driver) -> None:
        self.driver = driver
    def accept(self)->'AlertHandler':
        """Accepts the alert and prints its text."""
        return self.__handle_alert(action='accept')
    def cancel(self)->'AlertHandler':
        """Dismisses the alert."""
        return self.__handle_alert(action='dismiss')  
    
    def send_keys(self,text)->'AlertHandler':
        """Sends keys to the prompt alert and accepts it."""
        return self.__handle_alert(action='send_keys', text=text)
    def __handle_alert(self,action:str,text:str=None):
        id = driver.current_window_handle
        try:
            driver = self.driver
            alert = driver.switch_to.alert
            if action == 'accept':
                alert.accept()
                #print("Alert accepted")
            elif action == 'dismiss':
                alert.dismiss()
                #print("Alert dismissed")
            elif action == 'send_keys' and text is not None:
                alert.send_keys(text)
                alert.accept()
                #print(f"Sent keys: {text} to alert and accepted it...")
            driver.switch_to.window(id)
            return self
        except Exception:
            print('No Alert Found...')
            driver.switch_to.window(id)
            return self  
    def text(self)->str:
        """Returns the text of the alert if it exists."""
        try:
            # Switch to the alert box
            driver = self.driver
            id = driver.current_window_handle
            alert = driver.switch_to.alert
            text = alert.text
            driver.switch_to.window(id)
            return text
        except:
            print('No Alert Found...')
            return "" 

 
    

 