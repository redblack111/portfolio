# portfolio
Salesforce Attachment Downloader program:

The purpose of this program is to download selected attachments, based on a SOQL query, to a local folder.

Author:      Rex Black

Date:        09/12/19

Description: This program runs a query for attachments, and downloads them to a local file folder.

Requirements:

    * SF user account with "API Enabled" permissions
    * Valid SF credentials    
         -username, password and token         
    * Valid SOQL query, with finite number of elements returned

Required installations:

    * Python 3    
    * Libraies:    
          -simple_salesforce - https://github.com/simple-salesforce/simple-salesforce          
          -requests - https://pypi.org/project/requests/2.22.0/#files
          
Notes:

    * To run in Production, remove ', domain='test' from the Salesforce credential
    * Use query with a reasonable result set. Thousands of records could take hours to complete.
