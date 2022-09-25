import re
import tkinter as tk
from tkinter import filedialog
import csv
import pandas as pd
from IPython.display import display

sanitize_dict = {}


# Row Sanitize Functions
def id_col_preprocess(value):
    regex = "[^0-9]"
    clean_str = re.sub(regex, '', value)
    return clean_str


def price_levy_col_preprocess(value):
    regex = "[^0-9]"
    clean_str = re.sub(regex, '', value)
    if not clean_str and not clean_str.strip():
        clean_str = "0"
    return clean_str


def engine_col_preprocess(value):
    clean_str = [value, '']
    return clean_str


def do_nothing(value):
    print("not implemented")
    return value


def init(root):
    global sanitize_dict
    # init windows stuff
    root = tk.Tk()
    root.withdraw()
    # add all definitions
    sanitize_dict = {'ID': id_col_preprocess, 'Price': price_levy_col_preprocess, 'Levy': price_levy_col_preprocess,
                     'Manufacturer': do_nothing, 'Model': do_nothing, 'Prod_year': do_nothing, 'Category': do_nothing,
                     'Leather_interior': do_nothing, 'Fuel_type': do_nothing, 'Engine_volume': engine_col_preprocess,
                     'Mileage': do_nothing, 'Cylinders': do_nothing, 'Gear_box_type': do_nothing,
                     'Drive_wheels': do_nothing, 'Doors': do_nothing, 'Wheel': do_nothing, 'Color': do_nothing,
                     'Airbags': do_nothing}


def scrub_txt_file(root):
    # THIS SECTION SCRUBS SPECIAL CHARACTERS FROM THE ENTIRE FILE
    # get the file path
    print("Asking for original data file path")
    file_path = filedialog.askopenfilename()
    print("Replacing all special characters for clean read")
    bad_string = open(file_path, encoding="utf8").read()
    # create regex that only gets basic characters
    regex = "[^a-zA-Z0-9\n\.\,\- ]"
    clean_str = re.sub(regex, ' ', bad_string)
    # write out sanitized file
    print("Asking for cleaned data file save location")
    clean_file = save_file(clean_str, root)
    print("Printing save location:")
    print(clean_file)
    # THIS SECTION CALLS THE SANITIZE METHODS
    first_row = True
    df_1 = []
    tmp_a_1 = []
    with open(clean_file, 'rt', encoding="utf8") as f:
        # list to store the names of columns
        list_of_column_names = []
        reader = csv.reader(f, delimiter=';')
        # loop to iterate through the rows of csv
        for row in reader:
            if first_row:
                # adding the first row
                row_temp = str(row)
                row_temp = row_temp.replace('"', '')
                row_temp = row_temp.replace('.', '')
                row_temp = row_temp.replace(']', '')
                row_temp = row_temp.replace('[', '')
                row_temp = row_temp.replace('\'', '')
                row_temp = row_temp.replace(' ', '_')
                row_temp = [x.strip() for x in row_temp.split(',')]
                list_of_column_names = row_temp
                list_of_column_names.append("Turbo")
                first_row = False
                # breaking the loop after the
                # first iteration itself
            else:
                temp_values = {}
                row_temp = str(row)
                row_temp = row_temp.replace('\'', '')
                row_temp = row_temp.replace(']', '')
                row_temp = [x.strip() for x in row_temp.split(',')]
                for xcol in range(len(list_of_column_names)-1):
                    if list_of_column_names[xcol] == 'Engine_volume':
                        # account for turbo expansion
                        t1 = sanitize_dict[list_of_column_names[xcol]](row_temp[xcol])
                        temp_values[list_of_column_names[xcol]] = [t1[0]]
                        temp_values[list_of_column_names[len(list_of_column_names)-1]] = [t1[1]]
                    else:
                        temp_values[list_of_column_names[xcol]] = \
                            [sanitize_dict[list_of_column_names[xcol]](row_temp[xcol])]
                tmp_a_1.append(temp_values)
        df_1 = pd.json_normalize(tmp_a_1)
        display(df_1)



def save_file(out_string,root):
    fd = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
    if fd is None:
        return
    fd.write(out_string)
    fd.close()
    return fd.name


def main():
    # sets up the variables needed for run
    print("Setting Up Variables")
    root = ''
    sanitize_dict = ''
    init(root)
    print("Entering scrubbing methods")
    #scrub the output
    scrub_txt_file(root)


if __name__ == "__main__":
    main()