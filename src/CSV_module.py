'''
@author: ThePaloC
'''

import csv
import os

class CSV(object):
    def __init__(self,csv_new_file,csv_delete_file, csv_update_file,
                 resources_folder):
        """
        Check if file exists and initialize path for CSV file
        """
        self.csv_new_file = csv_new_file
        self.csv_delete_file = csv_delete_file
        self.csv_update_file = csv_update_file
        self.resources_folder = resources_folder
        self.delimiter = '\t'

    def find_file(self,action_type):
        """
        Find file in current dir (src) that ends with .csv.
        Then according to action find file that stars with new/update/delete.
        Finding file name is not case sensitive. 
        """
        file_list =  os.listdir(self.resources_folder)
        for f in file_list:
            if f.endswith(".csv"):
                low = f.lower()
                if low.startswith(action_type):
                    if action_type == 'new':
                        self.csv_new_file = self.resources_folder + f
                    if action_type == 'update':
                        self.csv_update_file = self.resources_folder + f
                    if action_type == 'delete':
                        self.csv_delete_file = self.resources_folder + f
        
    def get_new_csv(self):
        try:
            with open(self.csv_new_file):
                pass
        except IOError:
            self.csv_new_file = ''
            self.find_file('new')
            
        return self.csv_new_file
    
    def get_update_csv(self):
        try:
            with open(self.csv_update_file):
                pass
        except IOError:
            self.csv_update_file = ''
            self.find_file('upadte')
            
        return self.csv_update_file
    
    def get_delete_csv(self):
        try:
            with open(self.csv_delete_file):
                pass
        except IOError:
            self.csv_delete_file = ''
            self.find_file('delete')
            
        return self.csv_delete_file
    
    def get_content(self, csv_file):
        """
        Put all lines from CSV file to LIST. Each list in THE LIST is the line
        """
        content = []
        with open(csv_file, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=self.delimiter)
            for row in reader:
                content.append(row)
        return content
        
    
    def get_header(self, csv_file):
        """
        Method gets first line from CSV file, which is Header
        """
        with open(csv_file, 'rb') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=self.delimiter)
            header = reader.fieldnames  
        return header
    
    def get_csv_dictionary(self, csv_file):
        """
        Method create dictionary with all data from CSV file. Format should be:
        {
        'MR-Tag' : ['PJ-1','PJ-2','PJ-3',...]
        'MR-ID' : [1,2,3,...]
        'Revision' : ['PA5','PA1','PA3',...]
        ... 
        }
        So first element in each list, in whole dictionary is one line in CSV
        """
        content = self.get_content(csv_file)
        
        header = self.get_header(csv_file)

        dictionary = {}
        for h in header:
            dictionary[h] = []
        i = 0
        for line in content[1:]:
            for item in line:
                dictionary[str(header[i])].append(item)
                i += 1
            i = 0
        
        return dictionary
        
