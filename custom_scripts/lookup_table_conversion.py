#takes xlsx file listado.xlsx and converts to yml file with just the names column and stores in data folder as person_names.yml

import pandas as pd
import yaml
import os
import sys
import re

# Add the current directory to the path so that the script can find the data folder
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

# Path to the lookup table file
yml_filecreation_path = '../data/person_names.yml'
yml_departments_path = '../data/departments.yml'
yml_office_numbers_path = '../data/officenumbers.yml'
excel_file_path = '../data/listado.xlsx'
person_names = 'person_names' # name of the lookup table
department_names = 'department_names'
office_numbers = 'office_numers'

def generate_all_possible_names(input_string):
    """
    Generates all possible names by adding or removing single characters from the input string.

    Parameters:
    input_string (str): The input string to generate possible names from.

    Returns:
    list: A list of all possible names generated from the input string.
    """

    # Initialize list with input string
    possible_names = [input_string]

    # Add all possible names with one character added
    for i in range(len(input_string)):
        for letter in 'abcdefghijklmnopqrstuvwxyz':
            possible_names.append(input_string[:i+1] + letter + input_string[i+1:])

    # Add all possible names with one character removed
    for i in range(len(input_string)):
        possible_names.append(input_string[:i] + input_string[i+1:])

    return possible_names



print('running lookuptable conversion')

def get_departments(dep_column):

        # convert pandas column to set to remove duplicates
        departments = set(dep_column)
        # convert set to list
        departments = list(departments)
        # remove nan values
        departments = [x for x in departments if str(x) != 'nan']
        print('departments', departments)
        return departments

def generate_similar_permutations_of_string(word):
        list_of_new_names = []
        counter = 0
        for each_character_of_word in word:
                new_name = word[:counter]
                new_name += (each_character_of_word)
                new_name += (word[counter:])
                list_of_new_names.append(new_name)
                counter += 1
        return list_of_new_names

# data_list = ['MATTEO FABBRI', 'DILIP HARISH']


def lookup_table_conversion():

        df = pd.read_excel(excel_file_path)
        department_column = df[df.columns[1]]
        office_column = df[df.columns[2]]
        #include the first column from the excel file
        df = df[df.columns[0]]
       
        #print('department_column', department_column)
        # convert the names column from last name, first name to first name last name format using the regular expression
        # if isinstance(x, str) is a check to make sure that the value is a string
        df = df.apply(lambda x: re.sub(r'([^,]+),\s*(.+)', r'\2 \1', x) if isinstance(x, str) else x)

        # Drop any rows that have a NaN value in the first column
        df = df.dropna()

        # Convert the DataFrame to a list and return only values and remove empty spaces in the end of the string
        data = df.values.tolist()
        data_list = [x.strip() for x in data] # remove empty spaces in the end of the string

        # print first 5 rows of the list
        # print(data_list[:5])

        departments = get_departments(department_column)
        
        # list_of_new_names = []
        # for name in data_list:
        #         list_of_new_names += generate_similar_permutations_of_string(name)
        # for full_name in data_list:
        #         for each_word_of_name in full_name.split(' '):
        #                 list_of_new_names += generate_similar_permutations_of_string(each_word_of_name)       
        
        # print(list_of_new_names)

        
        #Write the YAML string to a file in the lookup_tables folder the way the rasa docs say to do it
        with open(yml_filecreation_path, 'w') as outfile:

                def write_to_yml_file(name):
                        outfile.write("\n      - " + str(name))

                outfile.write("\nversion: \"2.0\"\nnlu:\n  - lookup: "+person_names+"\n    examples: |")
                
                for full_name in data_list:
                        # write_to_yml_file(full_name)
                        [write_to_yml_file(name) for name in generate_similar_permutations_of_string(full_name)]
                        # [write_to_yml_file(each_word_of_name) for each_word_of_name in full_name.split(' ')]
                        for full_name_edited in generate_similar_permutations_of_string(full_name):
                                [write_to_yml_file(each_word_of_name) for each_word_of_name in full_name_edited.split(' ') if each_word_of_name != '']
                                
        
        # with open(yml_departments_path, 'w') as outdeptfile:

        #         def write_to_yml_file(name):
        #                 outdeptfile.write("\n      - " + name)

        #         outdeptfile.write("\nversion: \"2.0\"\nnlu:\n  - lookup: "+department_names+"\n    examples: |")
                
        #         for dept in departments:
        #                 write_to_yml_file(dept)
        #                 [write_to_yml_file(each_word_of_name) for each_word_of_name in dept.split(':')]

        # with open(yml_office_numbers_path, 'w') as outofficeNumfile:

        #         def write_to_yml_file(name):
        #                 # convert name from float to str
        #                 name = str(name)
        #                 outofficeNumfile.write("\n      - " + name)

        #         outofficeNumfile.write("\nversion: \"2.0\"\nnlu:\n  - lookup: "+office_numbers+"\n    examples: |")
                
        #         for offnum in office_column:
        #                 write_to_yml_file(offnum)
        
        print('finished lookuptable conversion')


if __name__ == '__main__':
        # try:
                lookup_table_conversion()
        # except Exception as e:
        #         print(e)