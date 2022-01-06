# Package Delivery Algorithm
Package Delivery Problem.  A version of the traveling salesman problem.

Jason Philpy
Student ID:  001467497

C950 Core Algorithm Overview

Stated Problem

A delivery company is charged with distributing 40 packages in less than 140 miles while adhering to a number of package requirements such as delivery times, truck allotment limitations, and incorrect address updating.  There are three trucks but only two drivers that average a speed of 18 miles per hour. To solve this problem, I loaded the trucks based on delivery time priority and any other truck related requirement.  Then, I created a greedy algorithm to sort the truck’s packages.

Algorithm Overview

The greedy sorting algorithm works in the following manner.

Function: greedy_sort
Parameter:  Truck number (1, 2, or 3)
Set variable truck_packages = associated truck packages
Initialize an empty sorted list
Set initial truck location index to 0 (the hub)
While there is more than 1 package in truck_packages loop:
	Run _sort_row function (below) to get next closest package
	Assign the new truck location
	Add the found package to the sorted list
	Remove the package from the truck_packages list
Return the sorted list

Function: _sort_row
Parameters:  Packages left, location, truck number
Set initial shortest distance variable
Initialize variable for the next package to return
Iterate through each package in packages left:
	Set variable for distance to the package from current location
	If the shortest distance has not been set or the new distance is less than the shortest distance then assign the current distance to the shortest distance variable and the package to the next package variable
Return next package

The total time complexity for the greedy sort algorithm is O(N2).  In the first part of the algorithm greedy_sort, we set a number of variable (1), then run a loop based on the number of packages retrieved from the parameter (N).  Inside the loop, we run the _sort_row function which also iterates through the packages (N) as well as sets some variables (1).  Ultimately we end up with O(1 + N * (N + 1)) which equates to O(N2).  

Programing Environment

For this project, I developed the program using PyCharm 2021.2 Community Edition.  The language used is Python 2.7.  The hardware used was a 2015 MacBook Pro running macOS Big Sur version 11.5.2.

Space-Time Complexity

main.py:  O(N2)
	This file simply runs functions from other classes or files.  It calls sort_all_turcks O(N2) and main_menu_prompt O(1)

menu.py:  
	main_menu_prompt:  O(1)
	validate_pkg_input:  O(1)

truck_loader.py:
	get_hash_table, get_truck_one/two/three: O(1)
	Remaining script:  O(N2)

distance_calculator.py:
	Initial script: O(1)
	sort_all_trucks: O(N2)
	_get_distance:  O(1)
	get_package_status:  O(N)
	get_total_distance:  O(N)
	_update_package_status:  O(N)
	greedy_sort:  O(N2)
	_sort_row:  O(N)

hash_table.py:
	__init__:  O(N)
	_get_bucket: O(1)
	insert:  O(N)
	look_up:  O(N)
	remove:  O(1)
	get_count:  O(N)
	get_list:  O(N2)
	


Scaling and Adaptation

For a growing number of packages, the loading part of the program would need some adjustments.  For example, since trucks are limited 16 packages, more drivers and trucks would need to be added.  An admitted short coming is the hard coding of certain requirements like the incorrectly addressed package, delayed packages, etc.  Simple changes to set_third_truck_start_time could be made to have it dynamically set any truck’s start time. The greedy_sort algorithm itself is very scalable.  It can take any package details and sort them so long as the truck and distance data are provided.

Efficiency and Maintainability

There are number of organization choices intended to make the code base easy to maintain.  There is separation of duties that keeps the menu system, initializing of data and sorting/calculating all separate.  This way, changes can be made to one section and not affect the entire program.  It also makes it clear to people new to the code base where they need to go intuitively to make changes.

Strengths and Weaknesses of the Hash Table

The main strength of the hash table is that insertion and retrieval of data is very quick especially when the hashes are evenly distributed amongst the buckets.  The main weakness is retrieving data about the overall hash table can be cumbersome.  For instance, getting a list of all items or getting a count of those items requires us to iterate through each bucket independently to compile the data.

Core Algorithm Justification

The core algorithm which is a greedy algorithm, successfully delivers all of the packages in 117.2 miles which is under the required 140 miles.  This includes the mileage back to the hub after all of the packages are delivered.  The main advantage of the algorithm is that it works mostly with generic inputs so that a variety of data can be used and can be scaled up easily.  Another strength is that the algorithm is relatively simple and easy to understand.  This means that passing the code base on to another developer would be a rather painless procedure. Another algorithm that could have been chosen was a heuristic algorithm.  This algorithm may sacrifice the possible optimal or accurate solution in exchange for gaining improved execution speed. Another algorithm that could be used is dynamic programming.  This type of algorithm doesn’t attempt to solve the entire problem at once but rather breaks the problem into smaller pieces and solves them individually.


What I Would Do Differently

If I were to do this project again, I would add more parameters to my methods in order to make them even more generic.  For instance, I would add a truck start travel time parameter and travel distances to my get_package_status method so that it could be completely generic and would scale much easier.  I’d do the same with my greedy_sort method so that it would be completely independent from the rest of the project and would not need any updating in order to scale with more trucks or packages.

Data Structure Justification

The data structure used for the project is a hash table.  It uses the package ID’s (which are unique) for the key which is hashed and stores the data in the assigned bucket.  The look_up function of the hash table can be negatively affected by an increase in the number of packages if the number of buckets is not increased accordingly.  As the number of items in each bucket increases, so do the number of items that need to be searched in order to find the matching key.  However, if the number of buckets is adjusted beforehand, the items can be evenly distributed in the table and keep look up iterations to a minimum.  With the addition of more trucks and cities, we would require increasing the number of buckets in order to keep execution time down.  However, in either case, most of the hash table’s functions operate at a worst-case time complexity of O(N).  Another data structure that could have been used would be a stack.  The stack would have arranged for the last package to be on the bottom of the stack and the next package to be delivered on the top.  Then we would pop the top package off the stack as they were delivered.  Another data structure would be a graph.  In this data structure, each package location would be a vertex and the distance to the adjacent package address would be the edge.  This would require us to iterate through the vertices in order to determine appropriate edges for the structure.  
![image](https://user-images.githubusercontent.com/13845028/146462603-2b32655c-bad5-438d-8d52-c85cd87ad899.png)
