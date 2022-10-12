# Job-Invoice-Automation
Automatic Job Invoice Generation with all the information required.

I have a part time tutoring job where I had to track my working hours to create an invoice for the pay. I had to manually note down my working hours and create an invoice with all the details every month. So, I decided to automate the task. The project is implemented using Python and all the neccessary code is available here in this repository!

Basically, I noted down my tutoring class schedule and created them as recurring events on my phone calendar and then extracted those events as a data from the calendar using Google API. I utilized Python to exract and transform the calendar data as per my needs. I used the final information for the invoice creation. The invoice generation on liquid platform is automated using Selenium and other libraries.

Once, the invoice is generated, I can mail my Boss to pay me my salary :)

Note:
I have deleted credentials.json and token.json, which is neccessary for extracting data using Google API but I haven't updated here as it is generated for my credentials. Please look into the references to how to set up google api connection and how to generate these files.


REFERENCES:

1. Google Calendar API: https://www.youtube.com/watch?v=qwqJcyLQSSQ&ab_channel=DAIMTODeveloperTips

2. Google Calendar API: https://www.youtube.com/watch?v=1JkKtGFnua8&list=PL3JVwFmb_BnTO_sppfTh3VkPhfDWRY5on&ab_channel=JieJenn

3. Selenium Web Driver for Automation bot: https://www.youtube.com/watch?v=Xjv1sY630Uc&list=PLzMcBGfZo4-n40rB1XaJ0ak1bemvlqumQ&ab_channel=TechWithTim
