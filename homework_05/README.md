# Homework: Module 5 - Asynchronous programming

## Task

The public API of PrivatBank allows you to get information about the cash exchange rates of PrivatBank and the NBU on the selected date. The archive stores data for the last 4 years.

Write a console utility that returns the EUR and USD exchange rate of PrivatBank for the last few days. Set the limit that the utility can find out the exchange rate no more than for the last 10 days. To request the API, use Aiohttp client. Follow SOLID principles when writing an assignment. Correctly handle errors during network requests.

Example of execution:

py .\main.py 2

Result:

[
  {
    '03.11.2022': {
      'EUR': {
        'sale': 39.4,
        'purchase': 38.4
      },
      'USD': {
        'sale': 39.9,
        'purchase': 39.4
      }
    }
  },
  {
    '02.11.2022': {
      'EUR': {
        'sale': 39.4,
        'purchase': 38.4
      },
      'USD': {
        'sale': 39.9,
        'purchase': 39.4
      }
    }
  }
]

## Additional Task

* add the ability to select additional currencies in the program's response through the passed parameters of the console utility;
* take websockets chat from the lecture material and add the ability to enter the exchange command. It shows users the current exchange rate in text format. Choose the presentation format at your own discretion;
* expand the attached exchange command to be able to view exchange rates in the chat for the last few days. Example exchange 2;
* use the aiofile and aiopath packages to add logging to the file when the exchange command was executed in chat.
