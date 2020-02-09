import csv

overall_title_set = set()
csv_reader = csv.reader(open('final_yelp_extracted2.csv', mode='r'), delimiter=',')
writer = csv.writer(open('yelp_title.csv', mode='w', newline=''))
writer.writerow(["categories"])

line_count = 0
for row in csv_reader:
    if line_count == 0:
        print(f'Column names are {", ".join(row)}')
        line_count += 1
    else:
        parse = row[1]
        parse_split = parse.split(', ')
        title_list=""
        for split in parse_split:
            if "title" in split:
                title = split[split.index(':')+3:].replace("'}","").replace("]","")
                #overall title set
                overall_title_set.add(title)
                if  title_list=="":
                    title_list = title
                else:
                    title_list = title_list + ", " + title
        print(title_list)
        writer.writerow([title_list])
        line_count += 1
print(f'Processed {line_count} lines.')
#print(overall_title_set)

set_writer = csv.writer(open('yelp_cate_dict.csv', mode='w', newline=''))
for row in list(overall_title_set):
    set_writer.writerow([row])

