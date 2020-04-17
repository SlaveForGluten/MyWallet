# MyWallet

This program is a web-scraper and a database manager to help me conveniently access and edit data using Tkinter GUI. It scraps net for info about GPW (Warsaw Stock Market) companies, current price, quarterly reports, etc. and currency rates for set currencies (most popular currencies to PLN).
It also allows you to set an alarm (when the share reaches set price) and receive on-screen notifications and/or email and/or SMS message (for SMS you need to have an API key). It allows you to add shares to your 'wallet'. Keeps the history of your transactions. Calculates your total costs, profit, annual rate of return and many more.
The program is still under development and has some issues that I am fixing gradually.
There is some dummy data inputted to help you see the program's functionality.

It features:
1. Liquid asset page
- adding, deleting and editing assets in five currencies (EUR, GBP, USD, CHF, PLN)
 with a short note, you can add negative numbers if you owe someone.
- each entry is displayed on scrollable canvas, with a summary on top
- to edit or delete entries right-click on it (you need to click on empty space as labels are not bound to event)
2. Shares page
- lets you add, edit or delete Shares, lets you add an alarm to share
- on top of the scrollable canvas - summary of your wallet (wallet worth, wallet net profit, up to seven biggest share packets in your wallet with their profile name, total worth, net profit, percentage of your wallet)
- bellow summary there is detailed info on every share packet you own with its current price, profit, the annual rate of return and more
- to edit or delete entries right-click on it (you need to click on empty space as labels are not bound to event)
- during editing share, if you add 'Exit price' and 'Exit date' this share is then transferred to 'Past transactions'
3. Past transactions page
- this page (unlike others) is only accessible through Shares page 
- on this page you can see shares you sold, they are displayed on scrollable canvas with a summary on top
4. Watched shares
- here you add companies you want to see detailed info on (quarterly reports, average price, net profit, etc.)
- from here you can also add an alarm to share
5. Summary page
- display summary of every currency
- display total shares worth
- display total wealth in PLN (foreign currencies to polish zloty by current exchange rate)
6. Settings page
- you can add your details to receive email or SMS
- set how often web gets scraped to update info on share price and currency rates

Known bugs (and crimes against 'best practice'):
- takes looooong time to start when on-line (i am working on it)
- to secure input, I restricted the share names to those in a 'gpw_profiles.txt' file,
I want to at least do an auto-fill in entry-fields or make it more user friendly otherwise
- ambiguous function names
- there is a lot of data tossing back and forth
- change list() to dict() where possible
- adding share when not on-line is not possible

Note: 
I decided to make this program because when buying shares my bank didn't show me all the details ie.
net profit (they didn't include tax, bank commission or dividends). On the bank website, when I bought, let us say 100 shares of KGHM in March and then 100 more in December, they would get merged in one packet with average price. This made difficult for me to calculate the annual rate of return. Then they wanted me to pay for showing me data on companies which I can find on-line. Also, I have accounts in different banks and currencies and wanted to have everything in one place. 
Feel free to copy, use, modify. If you have any ideas on how this could work better please share. Peace.   
