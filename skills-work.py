#!/usr/bin/python
# added coments
# a change
from __future__ import print_function
import requests
import csv
from xml.dom import minidom
from collections import Counter
from xml.etree import ElementTree
import xml.etree.ElementTree as ET
import requests
from getpass import getpass
from requests.auth import HTTPBasicAuth
from requests.exceptions import HTTPError
    
# Open the file containing the records. making a change to the comments here. make more changes. I made more changes
def get_res_data(csvFile = 'resources.csv'):
    xmlFile = 'myData.xml'
    xmlData = open(xmlFile, 'w')
#    xmlData.write('<?xml version="1.0"?>' + "\n")
#     there must be only one top-level tag
#    xmlData.write('<csv_data>' + "\n")
    csvData = csv.reader(open(csvFile))
    rowNum = 0
    for row in csvData:
        if rowNum == 0:
            tags = row
            # replace spaces w/ underscores in tag names
            for i in range(len(tags)):
                tags[i] = tags[i].replace(' ', '_')
        else:
            xmlData.write('<resource>' + "\n")
            for i in range(len(tags)):
                xmlData.write('<' + tags[i] + '>' \
                            + row[i] + '</' + tags[i] + '>' + "\n")
            xmlData.write('</resource>' + "\n")
        rowNum +=1
    
#    xmlData.write('</csv_data>' + "\n")
    xmlData.close()
##########################################################################################
## get_data()
## prompts for filename ,URL, Username and pass. Creates an XML file with the resources.
##
##
## TODO: SSL verification.
##
##
##
##########################################################################################
def get_data():
# get the name of the file to work with.
    xmlFile = str(raw_input("Please enter the output filename: "))
    # open the aforementioned file for writing.
    xmlData = open(xmlFile, 'w')
    # so many questions so little time! URL please?
    url = str(raw_input("Please enter the URL: "))
    # more questions!
    username = str(raw_input("Please enter the username: "))
    # secure way to get the password.
    passwd = getpass('Please enter the password: '	)
 #   # By using a context manager, you can ensure the resources used by
 #   # the session will be released after use
    with requests.Session() as session:
        session.auth = (username, passwd)
        auth_header = session.get(url)
        
    payload = ""
    headers = {
        'Content-Type': "application/xml",
        'Accept': "application/xml",
        'Cache-Control': "no-cache",
        'Content-Length': "178",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
        }
#send the request for data to the server.
    response = requests.request("GET", url=url, verify=False, data=payload, headers=headers, auth=HTTPBasicAuth(username, passwd))

# write the response from the server to the file we learned about at the begining of this mess. this is a string.
    xmlData.write(response.text)
    xmlData.close() # Close the file
    
# read the file and write it in pretty xml format. I'm so purty!!!
    doc = minidom.parse(xmlFile)
    with open(xmlFile,'w') as outfile:
        outfile.write(doc.toprettyxml())
    print("Done. Please check the file ",xmlFile, " for your 0utput~!\n")

#END get_data()

##########################################################################################
## post_data()
## prompts for filename ,URL, username and pass. uploads changes to the server.
##
##
## TODO: SSL verification.
##
##
##
##########################################################################################
def post_data():

 # get the name of the file to work with.
    xmlFile = str(raw_input("Please enter the input filename: "))
    # open the aforementioned file for reading.
    xmlData = open(xmlFile, 'r')
    # so many questions so little time! URL please?
    url = str(raw_input("Please enter the authentication URL: "))
    # more questions!
    username = str(raw_input("Please enter the username: "))
    # secure way to get the password.
    passwd = getpass('Please enter the password: '    )
 #   # By using a context manager, you can ensure the resources used by
 #   # the session will be released after use
    with requests.Session() as session:
        session.auth = (username, passwd)
        auth_header = session.get(url)
# HTML put header
    headers = {
        'Content-Type': "application/xml",
        'Accept': "application/xml",
        'Cache-Control': "no-cache",
        'Content-Length': "178",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
        } # end header
 # Open and Parse files
    xmlFile = 'myData.xml'
    xmlData = open(xmlFile, 'r')
#    xmlPostFile = 'postData.xml'
#    xmlData = open(xmlPostFile,'r')
    tree = ET.parse(xmlFile)
 # get the root element
    root = tree.getroot()
 # start at the resource level
    for elem in root.iter('resource'):
        # URL string
        url = elem.find('self').text
        print(url)
        # resource record
        xmlstr = ET.tostring(elem)
        print(xmlstr)

#send the request for data to the server.
        response = requests.request("PUT", url=url, data=xmlstr, headers=headers, auth=HTTPBasicAuth(username, passwd))
        print(response.text)
# write the response from the server to myData
#        xmlData.write('whatiput.txt')
#    xmlData.close() # Close the file
    

    print("Done. Please check the file whatiput.txt for your 0utput~!\n")
    
#END post_data()

def menu():
    print("What would you like to do?")
    print("[0] for quit")
    print("[1] Get data from UCCX server")
    print("[2] Put data to the UCCX server")
    print("[3] for CSV to XML")
    m = int(raw_input("Enter choice: "))
    return m

def main():
    print("This program was created as a way to manipulate skills using a CSV file")
    print("Simply follow the prompts.")
    print("Enj0y")
    m=''
    choice = menu()
    while True:
        if (choice > 4):
            print("Choice is invalid")
            break
        if (choice == 0):
            print("Good Bye")
            break
        if (choice == 1):
            x = get_data()
            break
        if (choice == 2):
            x = post_data()
            break
#            x = convert_file()
            # print(x)
#        break
        if (choice == 3):
            #print("Sorry not implemented yet")
            #break
            x = create_dest_pattern()
            # print(x)
if __name__ == "__main__":
    main()



