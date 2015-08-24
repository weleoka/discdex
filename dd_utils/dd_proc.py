"""
Utility module for Discdex.
Module handling the processes for sorting and creating indexing entries.
"""

import re, sys, os


def create_indexing_entry(results, current_file_type, path_to_device, device_name):
    """
    Create indexing entry/string of file metadata and append to list.
    Data should include:
        - Path to device (supplied by user at prompt)
        - Location device name (supplied by user at prompt)
        - Path to file
        - Name of file
        - File type
        - Date modified
        - Size

    parameters:
        results: list. All the files found with relevant metadata.
        current_file_type: string. The current filetype being listed.
        path_to_device: string. The path to the currently indexed storage device.
        device_name: string. The user supplied name for the device.

    return:
        entries: list. All the files with their stats as string.
    """
    entries = []

    for result in results:
        file_base_name = os.path.basename(result)

        if current_file_type == '*':
            file_type = (re.split('\.', file_base_name))[-1]  # This is so that a file type can be assigned to the current entry.
        
        else:
            file_type = current_file_type

        name = re.split('.' + file_type, file_base_name)[0]
        path_and_name_to_file = re.split(path_to_device, result)[1]

        try:
            path_to_file = re.split(path_to_device, os.path.dirname(result))[-1] # re.split(name, path_and_name_to_file)[0]
            path_to_file = path_to_file + "/"

        except:
            path_to_file = 'ERROR: bad character range'
            print("\n Problem with name of file: %s "
                % (path_and_name_to_file))

            pass

        entries.append('\n'
            + path_to_device + '\t'                        # System path to device
            + device_name  + '\t'                       # Device name
            + path_to_file + '\t'                           # Path to file
            + name + '\t'                                   # Name of file
            + file_type + '\t'                                  # File type
            + str(os.path.getmtime(result)) + '\t'  # Date modified
            + str(os.path.getsize(result))              # Size
            )

    return entries


def sort_list_of_tuples(data, sorting_option):
    """
    Take the file name and device name from index file entries and sort them according to sorting_option.
    [1] Alphabetical order.
    [2] Alphabetical order grouped by device name.
    http://www.pythoncentral.io/how-to-sort-python-dictionaries-by-key-or-value/
    http://www.thegeekstuff.com/2014/06/python-sorted/

    parameters:
        data: list. A list to be sorted.
        sorting_option: integer. The method of sorting.

    return:
        sorted_list: list. A list of the sorted entries.
    """

    def key_by_name(item):
        return item[1].lower()  # Sort by File name with disregard to upper-lower case.

    def key_by_location(item):
        return item[0]  # Sort by location

    if sorting_option == "1":
        return sorted(data, key=key_by_name)
        # return sorted(data, key=lambda tup: tup[1])

    elif sorting_option == "2" and len(data) > 0:
        ticker = 0; i = 0; j = 0
        arr = sorted(data, key=key_by_location)
        arr2 = []; arr3 = []; arr4 = []
        current_location = arr[0][0]

        for location in arr:
            i += 1
            ticker += 1

            if current_location != location[0]:
                print("Drive %s has %s entries."
                    % (current_location, ticker))
                ticker = 0
                current_location = location[0]
                arr2 = arr[j:i - 1]
                arr3 = sorted(arr2, key=key_by_name)
                arr4 += arr3
                j = i

        print("Drive %s has %s entries."
            % (current_location, ticker))
        arr2 = arr[j:]
        arr3 = sorted(arr2, key=key_by_name)
        arr4 += arr3

        return arr4

    else:

        return None
        

def stringify_list_of_tuples(data, sorting_option):
    """
    Make strings from tuple pairs according to sorting order.
    [1] Alphabetical order.
    [2] Alphabetical order grouped by device name.

    parameters:
        data: list. A list of tuples to be stringified.
        sorting_option: integer. The method of sorting.

    return:
        entries: list. A list of the stringified entries.
        ticker: integer. A count of all the items listed.
    """
    ticker = 0  # Keep count of the number of entries.
    entries = []

    if sorting_option == "1":

        for item in data:
            ticker += 1
            entries.append("\n" + item[1] + "\t\t" + item[0])

    elif sorting_option == "2":
        current_location = data[0][0]
        entries.append("\n\n\n" + current_location + "\n- - - - - - -")

        for location in data:
            ticker += 1

            if current_location != location[0]:
                entries.append("\n\n\n" + location[0] + "\n- - - - - - -")
                current_location = location[0]

            entries.append("\n" + location[1])

    return entries, ticker
