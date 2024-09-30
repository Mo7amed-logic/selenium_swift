from setuptools import setup, find_packages

# Read the README.md for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='selenium_swift', 
    version='0.1.0',  
    author='Mo7amed-logic',  
    author_email='medhasnaoui833@gmail.com',  
    description='A high-performance async web scraping and automation framework using Selenium.',
    long_description=long_description,   
    long_description_content_type="text/markdown",  
    url='https://github.com/Mo7amed-logic/selenium_swift',   
    packages = find_packages(exclude=["tests*", "examples*"]),  # Automatically find packages, excluding tests and examples
    install_requires=[
        'selenium>=4.0.0',                 # Required for core Selenium functionality
        'aiohttp>=3.7.4',                  # Used for asynchronous operations
        'webdriver-manager>=3.5.0',        # Manages browser drivers for Selenium
        'undetected-chromedriver>=3.0.0',  # Bypasses detection by websites
        'requests>=2.25.1',                # For HTTP requests to external services (e.g., fetching resources)
        'Pillow>=8.0.0', 
    ],
    classifiers=[
        'Development Status :: 4 - Beta',   
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',  # Use the MIT License (you can change this if you prefer another)
        'Operating System :: OS Independent',
        'Framework :: AsyncIO',  # Since your package heavily uses async
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Web Scraping',
    ],
    python_requires='>=3.6',  # Ensure compatibility with Python 3.6 and above
    include_package_data=True,  # To include non-code files, such as documentation or examples
    #entry_points={
    #    'console_scripts': [
    #        'selenium_swift=selenium_swift.browser:main',  # Optional: command-line tool setup
    #    ],
    #},
    project_urls={  # Additional links, such as documentation and issues page
        'Bug Reports': 'https://github.com/Mo7amed-logic/selenium_swift/issues',
        'Source': 'https://github.com/Mo7amed-logic/selenium_swift',
        #'Documentation': 'https://github.com/Mo7amed-logic/selenium_swift/wiki',  # Example
    },
)
