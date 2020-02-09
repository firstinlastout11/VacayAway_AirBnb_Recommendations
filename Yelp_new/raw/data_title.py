import csv


csv_reader = csv.reader(open('yelp_title.csv', mode='r'), delimiter=',')
csv_title = csv.reader(open('yelp_cate_dict.csv', mode='r'), delimiter=',')
writer = csv.writer(open('yelp_cate2.csv', mode='w', newline=''))
writer.writerow(["categories 1" , "categories 2"])

dict_title = {}
for row in csv_title:
        origin = row[0]
        level_one = row[1]
        level_two = row[2]
        dict_title[origin] = [row[1], row[2]]




line_count = 0
for row in csv_reader:
    if line_count == 0:
        line_count += 1
    else :
        unique_title1=set()
        unique_title2=set()
        if row:
            parse = row[0]
            parse_split = parse.split(', ')
            for split in parse_split:

                if dict_title.get(split) is None:
                    print('error:title not found.')
                    title_list = ['NULL','NULL']
                else:
                    title_list = dict_title.get(split)
                unique_title1.add(title_list[0])
                unique_title2.add(title_list[1])
                print(unique_title1)
            word_count=0
            for i in unique_title1:
                 if word_count==0:
                    title1=i
                    word_count=word_count+1
                 else:
                    title1=title1+', '+i

            word_count=0
            for i in unique_title2:
                 if word_count==0:
                    title2=i
                    word_count=word_count+1
                 else:
                    title2=title2+', '+i

        else:
            title1 = 'NULL'
            title2 = 'NULL'
        writer.writerow([title1,title2])
        print([title1,title2])
        line_count += 1
        print(line_count)
print(f'Processed {line_count} lines.')
print(dict_title.get('Desserts'))




