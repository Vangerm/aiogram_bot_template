import csv
import random


promocodes = ['8qqLp7BH',
            'uodK3MGq',
            'OF5JCH7E',
            'BnoIiEB3',
            'E8FAxIJC',
            '6BtOYWRM',
            'XupjpWwf',
            '1jqQ0VU5',
            'ScPOWOvh',
            '1syyOM2l']

def write_promocode(data):
    with open('data_micro/data_dk.csv', 'w', newline='', encoding='utf-8') as file:
        fieldnames = ['last_name', 'dk', 'discount', 'promocode']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(data)

def main():
    with open('data_micro/data_dk.csv', newline='\n', encoding='utf-8') as f:

        # data = list()
        # for _, row in enumerate(list(csv.DictReader(f))):
        #     print(row)
        #     if row['promocode'] == '':
        #         data.append(row)
        # print(data)
        data = list(csv.DictReader(f))
        for id, row in enumerate(data):
            print(row)
            if row['last_name'] == 'Новикова' and row['dk'] == '668776142':
                if row['promocode'] == '':
                    promocode = random.choice(promocodes)
                    data[id]['promocode'] = promocode
                    # write_promocode(data)
                else:
                    promocode = row['promocode']
    print(promocode)


main()
