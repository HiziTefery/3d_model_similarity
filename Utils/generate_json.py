import json
import csv

data = []
path = '../screenshots/'
with open('/home/hizi/Downloads/train_ordered.csv', 'rb') as csvfile:
    raw = csv.reader(csvfile, delimiter=' ', quotechar='|')

    for row in raw:
        print ', '.join(row)
        files = []
        row_data = row[0].split(',')
        for x in range(1, 13):
            files.append(path + row_data[0] + '/' + 'image_' + str(x) + '.jpeg')
        data.append({'files': files, '_categories': [row_data[1]]})

with open('images.json', 'w') as outfile:
    for row in data:
        outfile.write(json.dumps(row) + '\n')

