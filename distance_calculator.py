import csv
import datetime
from truck_loader import get_truck_one
from truck_loader import get_truck_two
from truck_loader import get_truck_three
from truck_loader import pkg_hash_table
import math

# distance_data is a list version of the raw data found csv files
with open('distanceData.csv') as raw_distance_data:
    distance_data = list(csv.reader(raw_distance_data, delimiter=','))

    # Start times for each of the trucks.  Truck 1 and 2 start times are known but truck 3 start time
    # is set based on how fast the truck 1 finishes the deliveries
    leave_time_one = datetime.timedelta(hours=int(8))
    leave_time_two = datetime.timedelta(hours=int(9), minutes=int(10))
    leave_time_three = datetime.timedelta()

    # Initializing some variables for sorted trucks and their distances
    first_distance_set = False
    second_distance_set = False
    third_distance_set = False
    sorted_truck_one = []
    sorted_truck_two = []
    sorted_truck_three = []
    truck_one_distances = []
    truck_two_distances = []
    truck_three_distances = []

    # O(N^2) Runs the greedy sort algorithm on each of the 3 trucks
    def sort_all_trucks():
        global sorted_truck_one
        sorted_truck_one = greedy_sort(1)
        global sorted_truck_two
        sorted_truck_two = greedy_sort(2)
        global sorted_truck_three
        sorted_truck_three = greedy_sort(3)
        set_third_truck_start_time()

    # O(1) Uses indexes to pull distance data from the csv file
    def _get_distance(row, column):
        found_distance = distance_data[row][column]
        if found_distance is '':
            found_distance = distance_data[column][row]
        found_distance = found_distance.replace('\xef\xbb\xbf', '')
        return float(found_distance)

    # O(N) Takes a package ID and a time and returns the associated packages status
    def get_package_status(package_id, time):
        truck_one_travel_time = time - leave_time_one
        truck_two_travel_time = time - leave_time_two
        truck_three_travel_time = time - leave_time_three
        # The following conditionals check if the time is before the truck's start time.  Otherwise,
        # the all of the packages current status don't need to be updated (they are default 'At Hub')
        if truck_one_travel_time.days >= 0:
            truck_one_travel_distance = float(truck_one_travel_time.seconds) / 60 / 60 * 18
            _update_package_status(truck_one_travel_distance, 1, leave_time_one)
            if truck_two_travel_time.days >= 0:
                truck_two_travel_distance = float(truck_two_travel_time.seconds) / 60 / 60 * 18
                _update_package_status(truck_two_travel_distance, 2, leave_time_two)
                if truck_three_travel_time.days >= 0:
                    truck_three_travel_distance = float(truck_three_travel_time.seconds) / 60 / 60 * 18
                    _update_package_status(truck_three_travel_distance, 3, leave_time_three)

        # Package ID 0 is given when a user selects 'all' from the menu, so this prints all package statuses,
        # otherwise, print out the specific package status that was requested
        if package_id == 0:
            for pkg in sorted_truck_one:
                print("Package " + str(pkg[0]) + " on Truck 1 " + pkg[8])
            for pkg in sorted_truck_two:
                print("Package " + str(pkg[0]) + " on Truck 2 " + pkg[8])
            for pkg in sorted_truck_three:
                print("Package " + str(pkg[0]) + " on Truck 3 " + pkg[8])
            print('\n')
        else:
            package_status = str(pkg_hash_table.look_up(package_id)[1][8])
            truck = str(pkg_hash_table.look_up(package_id)[1][11])
            print("Package " + str(package_id) + " on Truck " + truck + " " + package_status + "\n")

    # O(N) Adds up and returns all of the truck distances list for a grand total
    def get_total_distance():
        total_dist = 0
        for dist in truck_one_distances:
            total_dist += dist
        for dist in truck_two_distances:
            total_dist += dist
        for dist in truck_three_distances:
            total_dist += dist
        return total_dist

    # O(N) Takes distance (user time divided by average truck speed, 18 mile per hour), the truck and the truck's start
    # time to update all of the packages in that particular truck.
    def _update_package_status(distance, truck, start_time):
        total_dist = 0
        if truck == 1:
            for i in range(0, len(truck_one_distances) - 1):
                dist = truck_one_distances[i]
                total_dist += dist
                time_in_minutes = math.ceil(total_dist / 18 * 60)
                hours = int(math.floor(time_in_minutes / 60))
                minutes = int(time_in_minutes % 60)
                delivery_time = start_time + datetime.timedelta(hours=hours, minutes=minutes)
                if total_dist <= distance:
                    sorted_truck_one[i][8] = "Delivered at " + str(delivery_time)
                else:
                    sorted_truck_one[i][8] = "En Route. ETA: " + str(delivery_time)
                pkg_hash_table.insert(sorted_truck_one[i][0], sorted_truck_one[i])
        elif truck == 2:
            for i in range(0, len(truck_two_distances) - 1):
                dist = truck_two_distances[i]
                total_dist += dist
                time_in_minutes = math.ceil(total_dist / 18 * 60)
                hours = int(math.floor(time_in_minutes / 60))
                minutes = int(time_in_minutes % 60)
                delivery_time = start_time + datetime.timedelta(hours=hours, minutes=minutes)
                if total_dist <= distance:
                    sorted_truck_two[i][8] = "Delivered at " + str(delivery_time)
                else:
                    sorted_truck_two[i][8] = "En Route. ETA: " + str(delivery_time)
                pkg_hash_table.insert(sorted_truck_two[i][0], sorted_truck_two[i])
        elif truck == 3:
            for i in range(0, len(truck_three_distances) - 1):
                dist = truck_three_distances[i]
                total_dist += dist
                time_in_minutes = math.ceil(total_dist / 18 * 60)
                hours = int(math.floor(time_in_minutes / 60))
                minutes = int(time_in_minutes % 60)
                delivery_time = start_time + datetime.timedelta(hours=hours, minutes=minutes)
                if total_dist <= distance:
                    sorted_truck_three[i][8] = "Delivered at " + str(delivery_time)
                else:
                    sorted_truck_three[i][8] = "En Route. ETA: " + str(delivery_time)
                pkg_hash_table.insert(sorted_truck_three[i][0], sorted_truck_three[i])

    # O(N) This sets the third truck's start time. Since there are only 2 drives, this truck must start after the first
    # driver returns but no earlier that 10:20 so that the one corrected address package can be fixed at the hub.
    def set_third_truck_start_time():
        global leave_time_three
        total_dist = 0
        for dist in truck_one_distances:
            total_dist += dist
        time_in_minutes = math.ceil(total_dist / 18 * 60)
        hours = int(math.floor(time_in_minutes / 60))
        minutes = int((time_in_minutes - (60 * hours)) % 60)
        if hours < 2 or (hours == 2 and minutes < 20):
            leave_time_three = datetime.timedelta(hours=10, minutes=20)
        else:
            leave_time_three = datetime.timedelta(hours=hours, minutes=minutes)

    # O(N^2) This a greedy sorting algorithm. It takes the given starting point, iterates through all of possibilities
    # and chooses the shortest distance delivery address. It then repeats from the new address until all packages have
    # been chosen.
    def greedy_sort(truck_number):
        global first_distance_set
        global second_distance_set
        global third_distance_set
        if len(truck_one_distances) > 0:
            first_distance_set = True
        if len(truck_two_distances) > 0:
            second_distance_set = True
        if len(truck_three_distances) > 0:
            third_distance_set = True
        truck_packages = []
        if truck_number == 1:
            truck_packages = get_truck_one()
        if truck_number == 2:
            truck_packages = get_truck_two()
        if truck_number == 3:
            truck_packages = get_truck_three()
        sorted_list = []
        truck_location = 0
        while len(truck_packages) > 0:
            next_package = _sort_row(truck_packages, truck_location, truck_number)
            truck_location = next_package[9]
            sorted_list.append(next_package)
            truck_packages.remove(next_package)
        back_to_hub = _get_distance(sorted_list[len(sorted_list) - 1][9], 0)

        if truck_number == 1:
            if not first_distance_set:
                truck_one_distances.append(back_to_hub)
        if truck_number == 2:
            if not second_distance_set:
                truck_two_distances.append(back_to_hub)
        if truck_number == 3:
            if not third_distance_set:
                truck_three_distances.append(back_to_hub)
        return sorted_list

    # O(N) The main logic for the greedy algorithm. This loop searches through the possibilities and identifies
    # the shortest one.
    def _sort_row(packages_left, location, truck_number):
        shortest_distance = -1
        next_package = []
        priority_shortest = -1
        priority_package = []
        for package in packages_left:
            found_distance = _get_distance(location, package[9])
            if package[10]:
                if priority_shortest == -1 or found_distance < priority_shortest:
                    priority_shortest = found_distance
                    priority_package = package
            else:
                if shortest_distance == -1 or found_distance < shortest_distance:
                    shortest_distance = found_distance
                    next_package = package
        if priority_shortest != -1 and priority_package != []:
            shortest_distance = priority_shortest
            next_package = priority_package
        if truck_number == 1:
            if not first_distance_set:
                truck_one_distances.append(shortest_distance)
        if truck_number == 2:
            if not second_distance_set:
                truck_two_distances.append(shortest_distance)
        if truck_number == 3:
            if not third_distance_set:
                truck_three_distances.append(shortest_distance)
        return next_package
