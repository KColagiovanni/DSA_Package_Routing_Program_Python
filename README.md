# Package Routing Program - Data Structures and Algorithms

## Description
This project uses a user defined data structure (hash table) and an algorithm (greedy algorithm) to deliver packages with a few constraints, described below.

### Scenario
The Kevin Flynn Colagiovanni Ultimate Parcel Service (KFCUPS) needs to determine an efficient route and delivery distribution
for their daily local deliveries (DLD) because packages are not currently being consistently delivered by their promised
deadline. The Salt Lake City DLD route has three trucks, two drivers, and an average of 40 packages to deliver each day.
Each package has specific criteria and delivery requirements that are listed in the attached “Package File.csv” file.

The task is to determine an algorithm, write code, and present a solution where all 40 packages will be delivered on
time while meeting each package’s requirements and keeping the combined total distance traveled under 140 miles for all
three trucks. The specific delivery locations are shown on the attached “SLC downtown map.docx” file and distances to
each location are given in the attached “Distance Table.csv” file. The intent is to use the program for this specific
location and also for many other major cities. As such, detailed comments to have been used to make the code easy to follow 
and to justify the decisions htat were made while writing the scripts.

The supervisor should be able to see, at assigned points, the progress of each truck and its packages by any of the
variables listed in the “Package File.csv” file including what has been delivered and at what time the delivery occurred.

### Assumptions
•  Each truck can carry a maximum of 16 packages, and the ID number of each package is unique.
•  The trucks travel at an average speed of 18 miles per hour and have an infinite amount of gas with no need to stop.
•  There are no collisions.
•  Three trucks and two drivers are available for deliveries. Each driver stays with the same truck as long as that
truck is in service.
•  Drivers leave the hub no earlier than 8:00 a.m., with the truck loaded, and can return to the hub for packages if
needed.
•  The delivery and loading times are instantaneous (i.e., no time passes while at a delivery or when moving packages to
a truck at the hub). This time is factored into the calculation of the average speed of the trucks.
•  There is up to one special note associated with a package.
•  The delivery address for package #9, Third District Juvenile Court, is wrong and will be corrected at 10:20 a.m.
KFCUPS is aware that the address is incorrect and will be updated at 10:20 a.m. However, KFCUPS does not know the
correct address (410 S. State St., Salt Lake City, UT 84111) until 10:20 a.m.
•  The distances provided in the “Distance Table” are equal regardless of the direction traveled.
•  The day ends when all 40 packages have been delivered.

<!-- ## Table of Contents (Optional) -->

## Requirements
A personal computer with Windows, Linux, or MacOS installed. (This program was designed using a Linux Ubuntu machine)
Language: Python 3.10
Libraries: No external modules are required.

## Cost
Free, besides a personal computer.

## How to Install and Run
### Getting Started
1. If it’s not already installed on your PC, download [Python 3.10](https://www.python.org/downloads/release/python-31014/)(The application may work with Python versions >= 3.8, but it was built, tested, and only guaranteed to work correctly using Python version 3.10)

2. Install Python, after a successful installation, continue to the next step.

   - [Install Python on Windows](https://www.geeksforgeeks.org/how-to-install-python-on-windows/)
   - [Install Python on Linux](https://www.geeksforgeeks.org/how-to-install-python-on-linux/)
   - [Install Python on Mac OS](https://docs.python.org/3/using/mac.html)

> [!Tip]
>  - In Windows OS, a command prompt window can be opened by pressing the windows key and typing `cmd`.
>  - In Lunux OS, a command prompt window can be opened by pressing Ctrl + Alt + t.
>  - I Mac OS, a command promt window can be opened by pressing {Comming Soon}.

3. In a command prompt window type: `python –version` or `python3 –version`  to ensure Python version 3.10 is installed and configured.
4. (Optional) If running the application in a virtual environment is desired, configure it and install the following libraries while it is activated. Also make sure the virtual environment is running while runing the program. For more info see: [Getting started with Virtual Environments](https://docs.python.org/3/library/venv.html)

### How to Use
1. Clone this project to any directory and make note of the path to it.
2. In a command prompt window, navigate to the directory where the project was cloned and go into that directory.
3. In a command prompt type `dir`(Windows) or `ls`(Unix), and verify that the “main.py”, “hash_table.py”, “kfc_time.py”, package_delivery.py, parse_package_data.py, Distance Table.csv, and “PAckage File.csv” files are there, if any of those files are not present, the project will not run. Delete the cloned repository and go back to step 1.
4. If typing `python –version` in the command prompt window displays `Python 3.11.X`, continue to step 4a. If typing `python3 –version` in the command prompt window displays `Python 3.11.X`, continue to step 4b.
    - a. In a command prompt window, type: “python main.py” and ensure the program starts.
    - b. In a command prompt window, type: “python3 main.py” and ensure the program starts. 
5. Once the application is running:
    - The user will be presented with multiple options:
        - Display package info and status' for all packages at a specified time. (Press 1, then the enter button)
          - The user will then be asked to enter a time (24h format).
          - Once a time is entered, a status of all the packages at the time entered will be displayed.
        - Display package info and status for a specific package at a specific time. (Press 2, then the enter button)
          - The user will be asked to enter a package id number.
          - The user will be asked to enter a time (24h format).
          - Once a package id and time is entered, a status of the specific package id at the time entered will be displayed.
        - See the program documentation. (Type "doc", then the enter button)
          - The user will be given options asking which file to display the documentation for, then the documenttation for the selected file will be displayed.
        - Quit the program. (Type "quit", then the enter button)

## More Info About the Development of This Project
A greedy algorithm has been chosen to create the program that delivers packages and is appropriate to use in this situation because it efficiently finds the shortest path between the current package and the remaining packages that have not been loaded and it is also easy to implement and maintain. Because it is a greedy algorithm, it is not optimal, but it meets the requirements.

A hash table (a.k.a. dictionary) has been chosen to be used with the greedy algorithm to store the package data and is appropriate to use because it is self-adjusting, and has fast add and lookup times.

  - The hash table accounts for the relationship between the data components being stored using a list for each package. The package ID is used as the key, and the remaining package data is added to a list and that list is used as the value to the corresponding package ID (key). The hash function is just a basic modulus function: package_id % table_size = package_id, and because the table_size is the same as the number of packages there are, there will never be a collision until the number of packages reaches 9223372036854775807 (Python 3.10 Documentation). 

### Pseudo Code - Greedy Algorithm (find_shortest_distance() method):

<h4>Prerequisites:</h4>
The packages are already manually loaded onto the trucks based on their individual requirements (manual_load() method).


<h4>Algorithm Overview:</h4>
Start with the first truck
Iterate through all packages on the truck using a for loop and find the one that has the shortest distance to the hub and append the package_id to an empty list called “ordered_truck_list”, append the distance to an empty list called “total_truck_dist”, and calculate the travel time, based on the distance traveled, to an empty list called “delivery_times_list”.
Iterate through the package list using a for loop and find the package that has the shortest distance from it to the previous package that was appended to the “ordered_truck_list” and append it to the “ordered_truck_list”, append the distance to the “total_truck_dist” list, and calculate the travel time, based on the distance traveled, and append it to the “delivery_times_list” list. Continue doing that, each time finding the shortest distance from the current package to the last package that was last loaded until the end of the package list is reached.
Finally, get the distance from the last package to the hub and, append it to the “total_truck_dist” list, and calculate the travel time, based on the distance traveled, and append it to the “delivery_times_list” list.
Repeat steps 1.1 through 1.4 for subsequent trucks.

<h4> Pseudo Code (Python):</h4>

```
ordered_truck_list = []
truck_distance_list = []
truck_travel_time_list = []
loaded_package_list = []

for package in manually_loaded_truck:

  # Find first package
  if ordered_truck_list is empty:
    minimum_distance = infinity

    for package in manually_loaded_truck_packages:
      if distance_to_hub < minimum_distance and package not in loaded_package_list:
        minimum_distance = distance_to_hub
        package_id = package
    ordered_truck_list.append(package_id)
    truck_distance_list.append(minimum_distance)
    truck_travel_time_list.append(calculate_travel_time(minimum_distance))
    loaded_package_list.append(package_id)

  #Find remaining packages
  else:
    minimum_distance = infinity
    for package in manually_loaded_truck_packages:
      if distance_to_previous_package < minimum_distance and package not in loaded_package_list:
        minimum_distance = distance_to_hub
        package_id = package
    ordered_truck_list.append(package_id)
    truck_distance_list.append(minimum_distance)
    truck_travel_time_list.append(calculate_travel_time(minimum_distance))
    loaded_package_list.append(package_id)

truck_distance_list.append(distance_from_last_package_to_hub)
truck_travel_time_list.append(calculate_travel_time(distance_from_last_package_to_hub))

while True:
  time_check = check_package_requirements(order_truck_list):
  if time_check is True (requirements met):
    if truck_num == 1:
      self.first_truck = ordered_truck_list
      self.total_dist_first_truck = truck_distance_list
      self.first_truck_delivery_times = truck_travel_time_list
      break
    if truck_num == 2:
      self.second_truck = ordered_truck_list
      self.total_dist_second_truck = truck_distance_list
      self.second_truck_delivery_times = truck_travel_time_list
      break
    if truck_num == 3:
      self.third_truck = ordered_truck_list
      self.total_dist_third_truck = truck_distance_list
      self.third_truck_delivery_times = truck_travel_time_list
      break
  else (requirements not met):
    ordered_truck_list = adjust_package_list(ordered_truck_list)
    continue
```

<h4>Development Tools:</h4>
PyCharm 2023.2.4 Community Edition was used for the IDE on a Lenovo ThinkPad P1 laptop with a Intel® Core™ i7-8850H CPU @ 2.60GHz × 12, 32GiB of RAM, 512GB SSD, builtin Intel graphics running two OS’s (dual boot). Ubuntu 22.04.3 is primarily used, the secondary OS is Windows 10. Python version 3.10 was used as the language.

<h4>Space-Time Complexity:</h4>

- Manual Loading: O(n^2)
- Greedy algorithm: O(n^2)
- Hash Table Class: O(n) when initializing and O(1) for each method
- Over All program: O(n^2)

<h4>Ability to Scale and Grow:</h4>
The capability of my solution to scale and adapt to a growing number of packages is adequate because methods(class functions) are used to automate repetitive tasks, loops are used strategically to make repetitive tasks more efficient, unnecessary variables are avoided and use locally within methods or classes when possible, data structures are used instead of variables when possible, all of which help my solution scale and adapt to a growing number of packages. (How To Write Efficient and Scalable Code - LInkedIn)

<h4>Ability to Maintain:</h4>
The software design will be easy and efficient to maintain because it has uniform style, structure, and formatting across all parts of it, the variables, methods, and classes all have meaningful names, comments are applied when needed and DocStrings are used with each method and class to help explain functionality, and error handling has been implemented to help handle any errors that may arise. (The Art of Writing Clean Code: A Key to Maintainable Software - Gary Espinosa)

<h4>Strengths and weaknesses of a hash table:</h4>
<h5>Strengths:</h5>

- Fast look up time. Look up elements with time complexity of O(1).
- Efficient lookup and deletion. Because of the fast access time to each element, looking up and deleting can happen very fast, thus efficiently.
- Space Efficiency. 
- Flexibility. Different data types can be stored as values.
- Collision Resolution. There are various different ways to address collisions.

<h5>Weaknesses:</h5>

- Inefficient when there are a lot of collisions. More time is spent addressing collisions than computations for the program.
- Collisions are hard to avoid for a large set of possible keys.
- A key cannot be a null value.
- Limited capacity and will eventually fill up.
- Can be complex to implement.
- Orders of elements are not maintained, which makes it difficult to retrieve elements in specific order.
(Geeks for Geeks, 28 Mar, 2023, Applications, Advantages and Disadvantages of Hash Data Structure)						

The Package ID was used as the choice of a key for efficient delivery management. 

### Future Improvements:

- Create a GUI or Web App to be used with the program instead of a command line interface.
- Implement Dijkstra's algorithm in addition to the greedy and compare the performance between the two.

### Reference List:

1.
- Author: Geeks for Geeks
  - Contributor: aayushi2402
  - Improved By: shreyasnaphad, nikhilbhoi9739
- Date: 23-Mar-2023
- Title: Applications, Advantages and Disadvantages of Hash Data Structure
- Source: [Geeks for Geeks - Applications, Advantages and Disadvantages of Hash Data Structure](https://www.geeksforgeeks.org/applications-advantages-and-disadvantages-of-hash-data-structure/)

2.
- Author: Python 3.10 documentation
- Date: Unknown
- Title/Section: sys — System-specific parameters and functions/ sys.maxsize - An integer giving the maximum value a variable of type Py_ssize_t can take. It’s usually 2**31 - 1 on a 32-bit platform and 2**63 - 1 on a 64-bit platform.
- Source: [Python 3.10 Documentation (`sys.axsize`)](https://docs.python.org/3.10/library/sys.html#sys.maxsize)
```
Example on my PC:
>>> import sys
>>> print(sys.maxsize)
9223372036854775807
>>>
```
3.
- Author: YouDigital - Salesforce & Full Stack Developers via LinkedIn
- Date: October 3, 2022
- Title: How To Write Efficient and Scalable Code
- Source: [How To Write Efficient and Scalable Code](https://www.linkedin.com/pulse/how-write-efficient-scalable-code-youdigital-com/)

4.
- Author: Gary Espinosa via Software Craft
- Date: 2-Jul-2023
- Title: The Art of Writing Clean Code: A Key to Maintainable Software
- Source: [The Art of Writing Clean Code: A Key to Maintainable Software](https://reflectoring.io/clean-code/#:~:text=Meaningful%20naming%20conventions%2C%20simple%20implementation,future%20to%20maintain%20and%20reuse.)
