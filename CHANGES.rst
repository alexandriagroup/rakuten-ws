.. :changelog:

Python Rakuten Web Service changelog
==================================================

Version 0.5.2
-------------

Release on January 20th 2023

- Add python 3.11 compatibility
- Remove python 2 compat code
- Black code

Version 0.5.1
-------------

Release on August 22th 2020

- Fixed the recording of the response by scrubbing more information

Version 0.5.0
-------------

Release on August 22th 2020

- Added the new API RakutenPayOrder

Version 0.4.4
-------------

Release on November 6th 2019

- Fixed the parameters for `RmsService.items.update`
- Updated the API version of some endpoints

Version 0.4.3
-------------

Released on April 19th 2017

- Set `RmsOrderAPI.getOrder.isOrderNumberOnlyFlg` to False by default.

Version 0.4.3.dev0
------------------

**unreleased**

Version 0.4.2
-------------

Released on March 31st 2017

- Fixed `RmsOrderAPI.getOrder` and `RmsOrderAPI.updateOrder`

Version 0.4.1
-------------

Released on March 29th 2017

- Retrieve inventory information about multiple items at once (RmsInventoryAPI)

Version 0.4.0
-------------

Released on March 27th 2017

- Added support for RmsInventoryAPI

Version 0.3.0
-------------

Released on March 21st 2017

- Added support for RMS Category API

Version 0.2.1
-------------

Released on February 28th 2017

- Dropped upload_images function to keep the project as close as possible to Rakuten APIs
- Sorted xml keys recursively

Version 0.2.0
-------------

Released on February 22nd 2017

- Added support for RMS Cabinet API
- Added support for RMS Navigation API
- Added support for Python 3.6

Version 0.1.1
-------------

Released on January 13th 2017

- Included WSDL files in the Pypi package

Version 0.1.0
-------------

Released on January 03rd 2017

- First release on PyPI.
