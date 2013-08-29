'''
@author: ThePaloC
'''

class Mapping(object):
    
    def __init__(self,mapping_file_path):
        """
        Check if file exists and initialize path to mapping file
        """
        with open(mapping_file_path):
            pass
        self.mapping_file_path = mapping_file_path
    
    def get_content_of_mapping_file(self):
        """
        Read mapping file line after line and then create list from them
        """
        mapping_file = open(self.mapping_file_path,'r')
        mapping_content = [] 
        for line in mapping_file:
            if line.startswith('#'):
                continue
            mapping_content.append(line)
        mapping_file.close()
        return mapping_content
    
    def get_mapping_dictionary(self):
        """
        Read file and makes dictionary from mapping values
        """
        content = self.get_content_of_mapping_file()
        dictionary = {}
        error = False
        """
        Split every reasonable line with ':' and remove " from begining and
        end of each word.
        """
        for line in content:
            if len(line) <= 2 or line.startswith('#'):
                continue
            else:
                l = line.split(':')
                h_field = l[0]
                j_id_field = l[1]
                j_name_field = ''
                if len(l) > 2 :
                    j_name_field = l[2]
                trun_h_field = h_field[h_field.find('"')+1:h_field.rfind('"')]
                x = j_id_field.find('"')
                y = j_id_field.rfind('"')
                trun_j_id_field = j_id_field[x+1:y]
                x = j_name_field.find('"')
                y = j_name_field.rfind('"')
                trun_j_name_field = j_name_field[x+1:y]
                """
                If there is empty string in mapping file, don't return anything
                and print error to console
                """
                if trun_h_field == '' or trun_j_id_field == '':
                    error = True
                    print 'Error in mapping file ' + self.mapping_file_path
                    print '-> ' + trun_h_field +' : '+ trun_j_id_field +' : '\
                                + trun_j_name_field  
                dictionary[trun_h_field] = { 
                                            'id' : trun_j_id_field ,
                                            'name' : trun_j_name_field
                                            } 
        if error :
            return 0
        else :
            return dictionary
