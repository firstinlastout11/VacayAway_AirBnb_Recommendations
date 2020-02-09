# Imports
import json
import time
import sys
import csv
import requests
import pandas as pd
import time

def scrape_data(search_string, date_availabilityStart, date_availabilityEnd, bool_save, bool_verbose):
  # 1 - Send a POST request to the OAuth Server
  ## construct request
  url = "https://ws.homeaway.com/oauth/token"

  payload = ""
  headers = {
      'Authorization': "Basic NzViNDgyOTktZGEyNS00YWNkLThiYjctM2EyMTJkMWVmOTljOmEyN2M1YmNlLWRhOTYtNGEwNS1hYzRmLTE3NDBkMDFiYWJjNQ==",
      'cache-control': "no-cache",
      'Postman-Token': "f60f6d42-07c7-4b8f-aaa5-f0a03d307012"
      }

  ## send POST request
  #print("| - - POST - - |")
  #print("Sending POST request to", url)
  #print("Authorization:", headers['Authorization'])
  #print("Postman Token:", headers['Postman-Token'])
  response = requests.request("POST", url, data=payload, headers=headers)
  #print("| - - SUCCESS - - |")
  # #print(response.text)

  ## extract `access_token`
  access_token = response.json()['access_token']
  #print("Access Token is", access_token)

  # 2 - Send GET requests to obtain listings information and extract to DataFrame
  def parseEntry(entries, i):
      tmp_data = pd.DataFrame(
          data=[entries[i]['listingId'],
                entries[i]['priceQuote']['amount'],
                entries[i]['priceQuote']['averageNightly'],
                entries[i]['priceQuote']['fees'],
                entries[i]['priceQuote']['rent'],
                entries[i]['location']['lat'],
                entries[i]['location']['lng'],
                entries[i]['location']['city'],
                entries[i]['location']['state'],
                entries[i]['location']['country'],
                entries[i]['reviewCount'],
                entries[i]['reviewAverage'],
                entries[i]['bathrooms'],
                entries[i]['bedrooms'],
                entries[i]['listingUrl'],
                entries[i]['bookWithConfidence']
               ], 
          index=[
              'listing_id',
              'price_amt',
              'price_avg_nightly',
              'price_fees',
              'price_rent',
              'latitude',
              'longitude',
              'city',
              'state',
              'country',
              'review_count',
              'review_average',
              'bathrooms',
              'bedrooms',
              'listing_url',
              'book_with_confidence'
          ]
      ).transpose()
      return(tmp_data)

  ## Initialize `data` DataFrame
  data = pd.DataFrame(columns=[
          'listing_id',
          'price_amt',
          'price_avg_nightly',
          'price_fees',
          'price_rent',
          'latitude',
          'longitude',
          'city',
          'state',
          'country',
          'review_count',
          'review_average',
          'bathrooms',
          'bedrooms',
          'listing_url',
          'book_with_confidence'
      ])

  ## Extract data
  boolParse = True
  i = 0
  while(boolParse):
      time.sleep(1)
      i += 1 # increment pageNum counter by 1
      # construct GET request
      url = "https://ws.homeaway.com/public/search"

      val_pageSize = 25
      val_pageNum = i

      #date_availabilityStart = "2019-07-01"
      #date_availabilityEnd = "2019-07-09"

      querystring = {"q":search_string,
                     "availabilityStart": date_availabilityStart,
                     "availabilityEnd":date_availabilityEnd,
                     "pageSize":str(val_pageSize),
                     "page":str(val_pageNum)}
      

      payload = ""
      headers = {
          'Authorization': "Bearer " + access_token,
          'cache-control': "no-cache",
          'Postman-Token': "9a32c226-9a48-417f-b062-5070f405af71"
          }


      # send GET request
      if(bool_verbose):
        print("| - - GET - - |")
        print("| - - Sending POST request to", url)
        print("| - - Authorization:", headers['Authorization'])
        print("| - - Postman Token:", headers['Postman-Token'])
        print("| - - - - Query Params - - - - |")
        print("| - - - - - - q:", querystring['q'])
        print("| - - - - - - availabilityStart:", querystring['availabilityStart'])
        print("| - - - - - - availabilityEnd:", querystring['availabilityEnd'])
        print("| - - - - - - pageSize:", querystring['pageSize'])
        print("| - - - - - - page:", querystring['page'])
      response = requests.request("GET", url, data=payload, headers=headers, params=querystring).json()
      #print("| - - SUCCESS - - |")
      
      # parse GET response to get entries
      entries = response['entries']
      numEntries = len(response['entries']) # calculate number of entries

      if numEntries > 0:
          # extract pertinent entries into a DataFrame
          if(bool_verbose):
            print("| - - Parsing pertinent entries - - |")
          for j in range(numEntries):
              data = data.append(parseEntry(entries,j))
              #if(bool_verbose):
                #print("| - - - - Row", j, "- - - - |")
      else:
          boolParse = False
          if(bool_verbose):
            print("| - - COMPLETE - - |")

  # 3 - save output dataframe to CSV
  data = data.reset_index(drop=True)

  if(bool_save):
    data.to_csv("homeaway_data.csv")
  return(data)