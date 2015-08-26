"""
Utility module for Discdex.
Module handling the processes for sorting and creating indexing entries.
"""

import re, sys, os


def create_indexing_entry(results, current_suffix, path_to_device, device_name):
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
        current_suffix: string. The current filetype being listed.
        path_to_device: string. The path to the currently indexed storage device.
        device_name: string. The user supplied name for the device.

    return:
        entries: list. All the files with their stats as string.
    """
    entries = []

    for result in results:
        file_base_name = os.path.basename(result)

        if current_suffix == '*':
            suffix = (re.split('\.', file_base_name))[-1]
        
        else:
            suffix = current_suffix

        name = re.split('.' + suffix, file_base_name)[0] # Get file name without suffix.
        # path_and_name_to_file = re.split(path_to_device, result)[1]   # Not used in later versions of Discdex.

        path_to_file = re.split(path_to_device, os.path.dirname(result))[-1]    # Get the relative path to file from device root.
        path_to_file += "/"

        entries.append('\n'
            + path_to_device + '\t'                     # System path to device
            + device_name  + '\t'                       # Device name
            + path_to_file + '\t'                       # Path to file
            + name + '\t'                               # Name of file
            + suffix + '\t'                             # File type
            + str(os.path.getmtime(result)) + '\t'      # Date modified
            + str(os.path.getsize(result))              # Size
            )

    return entries


def sort_list_of_tuples(data, sort_mode):
    """
    Take the file name and device name from index file entries and sort them according to sort_mode.
    [1] Alphabetical order.
    [2] Alphabetical order grouped by device name.
    http://www.pythoncentral.io/how-to-sort-python-dictionaries-by-key-or-value/
    http://www.thegeekstuff.com/2014/06/python-sorted/

    parameters:
        data: list. A list to be sorted.
        sort_mode: integer. The method of sorting.

    return:
        sorted_list: list. A list of the sorted entries.
    """

    def key_by_name(item):
        return item[1].lower()  # Sort by File name with disregard to upper-lower case.

    def key_by_location(item):
        return item[0]  # Sort by location

    if sort_mode == "1":
        return sorted(data, key=key_by_name)
        # return sorted(data, key=lambda tup: tup[1])

    elif sort_mode == "2" and len(data) > 0:
        ticker = 0; i = 0; j = 0
        arr = sorted(data, key=key_by_location)
        arr2 = []; arr3 = []; arr4 = []
        tmp_dev = arr[0][0]

        for dev in arr:
            i += 1
            ticker += 1

            if tmp_dev != dev[0]:
                print("Drive %s has %s entries."
                    % (tmp_dev, ticker))
                ticker = 0
                tmp_dev = dev[0]
                arr2 = arr[j:i - 1]
                arr3 = sorted(arr2, key=key_by_name)
                arr4 += arr3
                j = i

        print("Device %s has %s entries."
            % (tmp_dev, ticker))
        arr2 = arr[j:]
        arr3 = sorted(arr2, key=key_by_name)
        arr4 += arr3

        return arr4

    else:

        return None
        

def stringify_list_of_tuples(data, sort_mode):
    """
    Make strings from tuple pairs according to sorting order.
    [1] Alphabetical order.
    [2] Alphabetical order grouped by device name.

    parameters:
        data: list. A list of tuples to be stringified.
        sort_mode: integer. The method of sorting.

    return:
        entries: list. A list of the stringified entries.
        ticker: integer. A count of all the items listed.
    """
    ticker = 0  # Keep count of the number of entries.
    entries = []

    if sort_mode == "1":

        for item in data:
            ticker += 1
            entries.append("\n" + item[1] + "\t\t" + item[0])

    elif sort_mode == "2":
        tmp_dev = data[0][0]
        entries.append("\n\n\n" + tmp_dev + "\n- - - - - - -")

        for dev in data:
            ticker += 1

            if tmp_dev != dev[0]:
                entries.append("\n\n\n" + dev[0] + "\n- - - - - - -")
                tmp_dev = dev[0]

            entries.append("\n" + dev[1])

    return entries, ticker
