from .page_event import PageEvent
import os 
 
class ChromeExtension(PageEvent):
    """
    A class to manage a Chrome extension.

    Inherits from the PageEvent class to utilize event-driven mechanisms
    for handling Chrome extensions.

    Parameters
    ----------
    extension_path : str
        The file system path to the Chrome extension directory. 
        Example for Windows 10: 
        '...\\Default\\Extensions\\majdfhpaihoncoakbjgbdhglocklcgno\\x.x.x...'
        Example for Linux/Mac: 
        '.../Default/Extensions/majdfhpaihoncoakbjgbdhglocklcgno/x.x.x...'
    
    extension_id : str
        The unique identifier of the Chrome extension. 
        Example: 'majdfhpaihoncoakbjgbdhglocklcgno'

    Attributes
    ----------
    extension_path : str
        The path to the Chrome extension.
    
    url_extension : str
        The URL to access the popup of the Chrome extension.

    Methods
    -------
    __init__(extension_path: str, extension_id: str):
        Initializes the ChromeExtension with the provided path and ID,
        constructing the URL for the extension's popup page.
    """
    def __init__(self, extension_path: str,extension_id) -> None:
        """
        Initializes the ChromeExtension with the provided path and ID,
        constructing the URL for the extension's popup page.

        Parameters
        ----------
        extension_path : str
            The file system path to the Chrome extension directory.
        extension_id : str
            The unique identifier of the Chrome extension.
        """
        self.extension_path = extension_path
        #extension_id = os.path.basename(extension_path)  # Handles path separators for any OS
        url_extension = f'chrome-extension://{extension_id}/src/popup/popup.html'
        
        super().__init__(url_extension)


 
