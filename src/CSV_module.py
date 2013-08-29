'''
@author: ThePaloC
'''

import csv

class CSV(object):
    def __init__(self,csv_new_file_path,csv_delete_file_path,
                 csv_update_file_path):
        """
        Check if file exists and initialize path for CSV file
        """
        self.csv_new_file_path = csv_new_file_path
        self.csv_delete_file_path = csv_delete_file_path
        self.csv_update_file_path = csv_update_file_path
        
    def get_new_csv(self):
        with open(self.csv_new_file_path):
            pass
        return self.csv_new_file_path
    
    def get_update_csv(self):
        with open(self.csv_update_file_path):
            pass
        return self.csv_update_file_path
    
    def get_delete_csv(self):
        with open(self.csv_delete_file_path):
            pass
        return self.csv_delete_file_path
    
    def get_content(self, csv_file):
        """
        Put all lines from CSV file to LIST. Each list in THE LIST is the line
        """
        content = []
        with open(csv_file, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                content.append(row)
        return content
        
    
    def get_header(self, csv_file):
        """
        Method gets first line from CSV file, which is Header
        """
        with open(csv_file, 'rb') as csvfile:
            reader = csv.DictReader(csvfile)
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
        
