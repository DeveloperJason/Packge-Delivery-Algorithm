import csv
from hash_table import HashTable

#  address_data and pkg_data are list versions of the raw data found csv files
with open('addressData.csv') as raw_address_data:
    address_data = list(csv.reader(raw_address_data, delimiter=','))
with open('packageData.csv') as pkg_data_csv:
    pkg_data = csv.reader(pkg_data_csv, delimiter=',')

    # set up empty tables for the packages and trucks
    pkg_hash_table = HashTable()
    truck_one = HashTable()
    truck_two = HashTable()
    truck_three = HashTable()

    # loop through data from the csv and assign it to the proper list
    for row in pkg_data:
        hasBeenAllocated = False
        package_id = int(row[0].replace('\xef\xbb\xbf', ''))
        address = row[1]
        city = row[2]
        state = row[3]
        zip_code = row[4]
        deadline = row[5]
        weight = row[6]
        special_notes = row[7]
        status = 'At Hub'
        location_index = 0
        priority = False
        truck = 1

        if deadline != 'EOD':
            priority = True

        # This takes the address data from the package data csv and finds it in the address data csv and stores its
        # index to quickly search for the data later
        for index in range(0, len(address_data)):
            if address in address_data[index][0] and zip_code in address_data[index][0]:
                location_index = index

        package = [package_id, address, city, state, zip_code, deadline, weight,
                   special_notes, status, location_index, priority, truck]

        # Filters for the special notes/requirements of the packages
        if 'Wrong address listed' in package[7]:
            package[1] = '410 S State St'
            package[11] = 3
            truck_three.insert(package[0], package)
            hasBeenAllocated = True
        if truck_two.get_count() <= 16 and \
                ('Can only be on truck 2' in package[7] or 'Delayed on flight' in package[7]):
            package[11] = 2
            truck_two.insert(package[0], package)
            hasBeenAllocated = True
        if package[0] == 19:
            package[11] = 1
            truck_one.insert(package[0], package)
            hasBeenAllocated = True

        # Puts all of the more immediate deadline packages on truck 1
        if truck_one.get_count() <= 16 and package[5] != 'EOD' and \
                (package[7] == '' or 'Must be delivered' in package[7]):
            package[11] = 1
            truck_one.insert(package[0], package)
            hasBeenAllocated = True

        # Balances trucks 2 and 3 with the remaining packages
        if not hasBeenAllocated:
            if truck_two.get_count() <= truck_three.get_count():
                package[11] = 2
                truck_two.insert(package[0], package)
            else:
                package[11] = 3
                truck_three.insert(package[0], package)

        pkg_hash_table.insert(package_id, package)

    # Getters for the tables
    def get_hash_table():
        return pkg_hash_table

    def get_truck_one():
        return truck_one.get_list()

    def get_truck_two():
        return truck_two.get_list()

    def get_truck_three():
        return truck_three.get_list()
