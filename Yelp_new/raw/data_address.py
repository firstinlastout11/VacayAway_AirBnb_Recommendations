import csv

csv_reader = csv.reader(open('final_yelp_extracted.csv', mode='r'), delimiter=',')
writer = csv.writer(open('yelp_address.csv', mode='w', newline=''))
writer.writerow(["address"])

line_count = 0
for row in csv_reader:
    if line_count == 0:
        print(f'Column names are {", ".join(row)}')
        line_count += 1
    else:
        parse = row[1]
        display_address = parse[parse.find("display_address"):].split(":")
        display_address=display_address[1].replace("'","").replace("[","").replace("]","").replace("}","")
        print(display_address)
        writer.writerow([display_address])
        line_count += 1
print(f'Processed {line_count} lines.')




