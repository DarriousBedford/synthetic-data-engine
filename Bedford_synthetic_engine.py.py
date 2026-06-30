## Name: Darrious Bedford
## 6/8/2026
## Course: ISAN 3305
## Assignment: Capstone - Synthetic Data Engine
## Description: This project  reads a csv  copunts how oftn it shows up in each column two differnt ways to make sure
                ## i didnt mess up the phrasing, then makes a fake version of the data using the same odds,
                ##    and checks how close the fake data is to the real data 
import tkinter
from tkinter import filedialog
import random

# opens the file app to allow you to select the file you will be using

def request_file_path():

    root = tkinter.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title = 'Select a CSV File',
        filetypes = [('CSV Files', '*.csv')])
    root.destroy()
    return file_path

# takes the file and dumps it to create one big string

def read_file_blob(file_path):
    input_file = open(file_path, 'r')
    blob = input_file.read()
    input_file.close()
    return blob

# checks and makes sure the file isn't empty and the quotes in the file are all correct

def validate_blob(blob):
    quote_count = 0
    char_index = 0

    while char_index < len(blob):
        if blob[char_index] == '"':
            quote_count = quote_count + 1
        char_index = char_index + 1

    if len(blob) == 0:
        print("Error: File is empty.")
        return False
    elif quote_count % 2 != 0: 
        print("ERROR: Asymmetric quotation boundraies detected (odd quote count).")
    
        return False
    else:
        return True

# shows the first three lines of the file to make sure everything is corect

def preview_first_lines(blob):
    lines = blob.split('\n')
    count = 0

    while count < 3 and count < len(lines):
        print(lines[count])
        count = count + 1

# ask the user if there is a header to the file comes out as a true or false

def ask_header_exists():
    response = input("Does this file have a header row? (yes/no): ")
    response_lower = response.lower()
    if response_lower == "yes":
        return True

    else:
        return False

# turns th eraw data into rows and columns

def build_matrix(blob):
    full_matrix = []
    lines = blob.split('\n')
    line_index = 0
    while line_index < len(lines):
        current_line = lines[line_index]
        if current_line != "":
            row_values = current_line.split(',')
            trimmed_row = []
            value_index = 0
            while value_index < len(row_values):
                trimmed_value = row_values[value_index].strip()
                trimmed_row.append(trimmed_value)
                value_index = value_index + 1
            full_matrix.append(trimmed_row)
        line_index = line_index + 1
    return full_matrix

# takes the header off the top so it doesn't mess up the code when counting

def split_header(full_matrix, has_header):
    header_row = []
    data_matrix = []
    if has_header == True:
        header_row = full_matrix[0]
        row_index = 1
        while row_index < len(full_matrix):
            data_matrix.append(full_matrix[row_index])
            row_index = row_index + 1
    else:
        data_matrix = full_matrix
    return header_row, data_matrix

# counts the amount of times each value shows up for each column straight from the raw data/text

def build_profile_streaming(blob, has_header):
    lines = blob.split('\n')
    profile_a = []
    start_index = 0
    if has_header == True:
        start_index = 1

    column_count_known = False
    line_index = start_index
    while line_index < len(lines):
        current_line = lines[line_index]
        if current_line != "":
            row_values = current_line.split(',')

            if column_count_known == False:
                col_index = 0
                while col_index < len(row_values):
                    profile_a.append({})
                    col_index = col_index +1
                column_count_known = True

            col_index2 = 0
            while col_index2 < len(row_values):
                value = row_values[col_index2]
                this_dict = profile_a[col_index2]
                if value in this_dict:
                    this_dict[value] = this_dict[value] + 1

                else:
                    this_dict[value] = 1  
                col_index2 = col_index2 + 1

        line_index = line_index + 1

    return profile_a

# counts again the same way using the clean matrix instead basically a double check

def build_profile_from_matrix(data_matrix):
    profile_b = []
    if len(data_matrix) > 0:
        col_count = len(data_matrix[0])
        c = 0
        while c < col_count:
            profile_b.append({})
            c = c + 1
    row_index = 0
    while row_index < len(data_matrix):
        col_index = 0
        while col_index < len(data_matrix[row_index]):
            value = data_matrix[row_index][col_index]
            this_dict = profile_b[col_index]
            if value in this_dict:
                this_dict[value] = this_dict[value] + 1
            else:
                this_dict[value] = 1

            col_index = col_index + 1
        row_index = row_index + 1

    return profile_b

# checks if both methods of counting agree/ = each other

def compare_profiles(profile_a, profile_b):

    if profile_a == profile_b:
        print("SUCCESS: Method 3A and Method 3B match.")
        return True
    else:
        print("CRITICAL ERROR: Data integrity verification failed.")
        print("Method 3A results:")
        print(profile_a)
        print("Method 3B results:")
        print(profile_b)
        return False

# basically asks how many fake rows there is 

def get_synthetic_row_count():
    row_count = input("How many synthetic rows would you like to generate? ")
    row_count = int(row_count)
    return row_count

# asks you what is the name of the file

def get_output_filename():
    filename = input("What is the File Name? ")
    return filename

# builds you the fake rows using the weighted random of the picks based on the real data

def generate_synthetic_matrix(profile_list, synthetic_row_count):
    synthetic_matrix = []
    row_counter = 0
    while row_counter < synthetic_row_count:
        new_row = []
        col_index = 0
        while col_index < len(profile_list):
            column_dict = profile_list[col_index]
            weighted_pool = []

            for key in column_dict:
                freq = column_dict[key]
                repeat_counter = 0
                while repeat_counter < freq:
                    weighted_pool.append(key)
                    repeat_counter = repeat_counter + 1

            random_index = random.randint(0, len(weighted_pool) - 1)
            chosen_value = weighted_pool[random_index]
            new_row.append(chosen_value)
            col_index = col_index + 1
        synthetic_matrix.append(new_row)
        row_counter = row_counter + 1
    return synthetic_matrix

# writes out the fake data to make a new csv

def write_synthetic_file(output_filename, header_row, synthetic_matrix):
    output_file = open(output_filename, 'w')

    if len(header_row) > 0:
        header_line = ",".join(header_row)
        output_file.write(header_line)
        output_file.write("\n")

    row_index = 0
    while row_index < len(synthetic_matrix):
        line = ",".join(synthetic_matrix[row_index])
        output_file.write(line)
        output_file.write("\n")
        row_index = row_index + 1

    output_file.close()

# turns the raw data counts and truns them into percentages

def calculate_percentages(profile_list, total_count):
    percentage_list = []
    col_index = 0
    while col_index < len(profile_list):
        column_dict = profile_list[col_index]
        percent_dict = {}
        for key in column_dict:
            percent_value = column_dict[key] / total_count * 100      
            percent_dict[key] = percent_value
        percentage_list.append(percent_dict)                           
        col_index = col_index + 1
    return percentage_list

#prints out and makes a orginal vs "fake"(synthetic) and puts them side by side so you can easily see how close they are 

def print_variance_report(original_pct_list, synthetic_pct_list):
    print("=== STATISTICAL DISTRIBUTION AUDIT REPORT ===")
    col_index = 0
    while col_index < len(original_pct_list):
        print("--- Column", col_index, "---")
        original_dict = original_pct_list[col_index]
        for key in original_dict:
            original_pct = original_dict[key]
            synthetic_pct = 0
            if key in synthetic_pct_list[col_index]:
                synthetic_pct = synthetic_pct_list[col_index][key]
            delta = abs(original_pct - synthetic_pct)

            original_rounded = round(original_pct, 2)
            synthetic_rounded = round(synthetic_pct, 2)
            delta_rounded = round(delta, 2)

            print(key, "| Original:", original_rounded, "% | Synthetic:", synthetic_rounded, "% | Delta:", delta_rounded)
        col_index = col_index + 1

# its the main calls everything simple chapter 5 things

def main():
    file_path = request_file_path()
    if file_path == "":
        print("No file selected. Exiting.")
        return
    blob = read_file_blob(file_path)
    blob_is_valid = validate_blob(blob)
    if blob_is_valid == False:
        return
    
    preview_first_lines(blob)
    has_header = ask_header_exists()
    full_matrix = build_matrix(blob)
    header_row, data_matrix = split_header(full_matrix, has_header)
    profile_a = build_profile_streaming(blob, has_header)
    profile_b = build_profile_from_matrix(data_matrix)
    profiles_match = compare_profiles(profile_a, profile_b)
    if profiles_match == False:
        return
    
    synthetic_row_count = get_synthetic_row_count()
    output_filename = get_output_filename()
    synthetic_matrix = generate_synthetic_matrix(profile_b, synthetic_row_count)
    write_synthetic_file(output_filename, header_row, synthetic_matrix)
    original_total = len(data_matrix)
    synthetic_profile = build_profile_from_matrix(synthetic_matrix)
    synthetic_total = len(synthetic_matrix)
    original_pct_list = calculate_percentages(profile_b, original_total)
    synthetic_pct_list = calculate_percentages(synthetic_profile, synthetic_total)
    print_variance_report(original_pct_list, synthetic_pct_list)

main()
