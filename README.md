# secapi
This module provides an API that can be used to query metadata from sec
filings. These metadata can then be used to create a link to the actual filings
which can then be parsed.

## Technical information
The module was developed with python 2.7.18 and only uses build-in python packages as well
as the packages typing, requests, ratelimiter and [OpenDateRange](https://github.com/tlie03/OpenDateRange).

## Installation
``$ pip install secapi``

## What functionalities does the API provide?
### query filing metadata
The most important function ist the `get_filings` function
which takes one required and four optional search parameters.
The required parameter is the ticker symbol of the company 
whose filings are requested. If none of the optional arguments is 
set all filings of the given company will be returned.
The following arguments are optional.
* date_from : only filings that have been filed on this date or a current date
will be returned
* date_to : only filings that have been filed on this date or a former date
will be returned
* form_types : filters all filings based on a list of form types, so only filings
with a form type from the list will be returned
* filings_information: returns only the metadata points for each filing that
is included in the given list. This can be used to reduce the amount of data
and to get rid of irrelevant data.
A list of all possible data points can be found below

The return value will be a list of dictionaries. Each dictionary represents
one filing and holds multiple metadata points. Two of these metadata points
are the ticker symbol and the cik which are always part of the metadata.
By default, all other metadata points are contained in the dictionary, but
they can also be chosen via the filing_information parameter.
Below is a list of all possible metadata points:
* accessionNumber
* filingDate
* reportDate
* acceptanceDateTime
* act
* form
* fileNumber
* filmNumber
* items
* size
* isXBRL
* isInlineXBRL
* primaryDocument
* primaryDocDescription

These metadata can be used to create the links to the actual filings.
The process of finding a way to build the links from the metadata can be quite difficult, 
and requires a lot of experimentation and hacking. An example on how to
do this for the form4 filings can be found [below](#description-of-how-to-build-links-to-form4-filings)

### how to make requests to the sec server
The sec has restricted the access rate to their servers thereby it is not allowed
to do more than 10 requests per second. 


## Description of how to build links to form4 filings