print('Hi from calculate_distance.py')

import csv

with open('./data/distance_data.csv', newline='') as distance_data:

    distance_data = csv.reader(distance_data, delimiter=',')

    def convert_to_float(num):
        if num != '':
            return float(num)

    def sum_list(list_input):
        sum = 0
        for value in list_input:
            if value != None:
                sum += value
        return round(sum, 2)

    for distance in list(distance_data):
        converted = map(convert_to_float, (distance))
        summed = sum_list(list(converted))
        # print(summed)

with open('./data/distance_name_data.csv', newline='') as distance_name_data:

    distance_name_data = csv.reader(distance_name_data, delimiter=',')

    # for name in list(distance_name_data):
    #     print(name)