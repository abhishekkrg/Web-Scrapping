import requests
import json
from time import sleep
import csv

#query = {'q' : 'intitle:"flowers for algernon",inauthor:keyes'}
#data = requests.get('https://www.googleapis.com/books/v1/volumes', query)

with open('filecompletelist.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)

    with open('names.csv', 'w') as csvfile1:
        fieldnames = ['S.No', 'Book Name', 'Book Code', 'Author', 'Category/Genre', 'Summary', 'Team Member']
        writer = csv.DictWriter(csvfile1, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:


            bookname = row['Book Name']
            print("")

            data = ''
            while data == '':

                try:

                    bookname=bookname.upper().strip()
                    matchbookname=bookname
                    print(matchbookname)
                    query = {'q' : bookname}
                    data = requests.get('https://www.googleapis.com/books/v1/volumes', query)


                    json_data = data.json()
                    print(json_data)
                    for key in json_data.keys():
                        if key =='items':

                            for item in json_data['items']:
                                try:
                                    isauthor=False
                                    iscategories=False
                                    isdescription=False

                                    #print(item)
                                    title = item['volumeInfo']['title']
                                    matchtitle = title.upper().strip()
                                    if matchtitle ==matchbookname:
                                        #print(item)
                                        for key in item['volumeInfo'].keys():
                                            if key == 'authors':
                                                isauthor =True
                                            if key == 'categories':
                                                iscategories =True
                                            if key == 'description':
                                                isdescription =True

                                        print(item['volumeInfo']['title'])


                                        authorslist=''
                                        categorylist=''
                                        Summary=''
                                        if isauthor:
                                            print(item['volumeInfo']['authors'])

                                            for authors in item['volumeInfo']['authors']:
                                                if authorslist == '':
                                                    authorslist = authors
                                                else:
                                                    authorslist = authorslist + ' and ' + authors

                                        if iscategories :
                                            print(item['volumeInfo']['categories'])
                                            for categories in item['volumeInfo']['categories']:
                                                if categorylist=='':
                                                    categorylist =categories
                                                else:
                                                    categorylist = categorylist + ' and ' + categories

                                        if isdescription:
                                            print(item['volumeInfo']['description'])
                                            Summary =item['volumeInfo']['description']



                                        datdict = {'S.No': row['S.No'], 'Book Name': row['Book Name'],
                                                   'Book Code': row['Book Code'],
                                                   'Author': authorslist,
                                                   'Category/Genre': categorylist,
                                                   'Summary':Summary,
                                                   'Team Member': row['Team Member ']}
                                        writer.writerow(datdict)
                                        print('end')
                                        print('')
                                except Exception as e:
                                    print('exception in reading details -')
                                    print(e)

                        else:
                            print("No items ")



                except Exception as e1:
                    print('exception in connection-')
                    print(e1)
                    sleep(120)
                    print("Was a nice sleep, now let me continue...")
                continue

                # print("Reading next book - Let me take some rest")
                # sleep(120)