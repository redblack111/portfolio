""" Author:  Rex Black
Date:        09/11/19
Description: This script will run a query for attachments, downloads them to a local file folder.

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
    * To run in Production, remove ', domain='test' from the Salesforce credential"""

import logging
import os
import sys
import codecs
import requests
from simple_salesforce import Salesforce

#import argparse

ACCOUNT_TO_FILE_CSV = './attachments.csv'

# Connect to Salesforce
session = requests.Session()
# Enter credentials
sf = Salesforce(username='rblack@prokarma.com.full', password='Nevar11!sal',
                security_token='nfPf9iiN7vyzg8cAXxI118aWU', domain='test')

auth_id = 'Bearer ' + sf.session_id
req_headers = {'Authorization': auth_id}

# Enter query here
query = ('SELECT Id, ParentId, Name, Body FROM Attachment '
         'WHERE ParentId in (SELECT Id FROM Account) limit 10000')
#query = "SELECT Id, ParentId, Name, Body FROM Attachment"
    # Over 100,000 Ids returned, and generates 'OPERATION_TOO_LARGE' error
result = sf.query(query)

total_records = result.get('totalSize', 0)

if not total_records:
    logging.info('No Attachments Found')
    sys.exit('No Attachments Found')
print(total_records, 'Attachments Found')

# Continue with download decision y/n
proceed = str(input('Proceed with download?:(y/n)'))
print(proceed)
if proceed != 'y':
    sys.exit("'y' was not entered, exiting...")

logging.debug("Starting to download %d attachments", total_records)

acc_to_file = []

# Enter local storage directory
storage_dir = 'c:\\temp\\'
sf_pod = sf.base_url.replace("https://", "").split('.salesforce.com')[0]

# Loop to download each record
records = result.get('records', {})
for record in records:
    body_uri = record.get('Body')
    if not body_uri:
        logging.warning("No body URI for file id %s", record.get('Id', ''))
        continue

    remote_file = record.get('Name')
    remote_file_lower = remote_file.lower()

    remote_path = "https://{0}.salesforce.com{1}".format(sf_pod, body_uri)
    local_file = '%s_%s' % (record.get('Id'), remote_file)
    local_path = os.path.join(storage_dir, local_file)
#    local_path = storage_dir + local_file
    logging.info("Downloading %s to %s", remote_file, local_path)
    logging.debug("Remote URL: %s", remote_path)

    resp = session.get(remote_path, headers=req_headers)
    if resp.status_code != 200:
        logging.error("Download failed [%d]", resp.status_code)
        continue

    with open(local_path, 'wb') as out_file:
        out_file.write(resp.content)

    logging.debug("Account ID: %s", record.get('ParentId'))
    acc_to_file.append((record.get('ParentId'), local_file))

    with codecs.open(ACCOUNT_TO_FILE_CSV, 'wb', 'utf-16') as csv_file:
        csv_file.write('ParentId,FileName\n')
        csv_file.write('\n'.join('"%s","%s"' % l for l in acc_to_file))

    print("Starting Downloader...")

# End of loop, Wrap-up
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='attachments_downloader.log',
                    filemode='w')

print("\nDownloads Complete")
