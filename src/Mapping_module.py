'''
@author: ThePaloC
'''

class Mapping(object):
    
    def __init__(self,mapping_file,resources_folder):
        """
        Check if file exists and initialize path to mapping file
        """
        self.mapping_file = mapping_file
        self.resources_folder = resources_folder
        
        try:
            with open(resources_folder+mapping_file):
                pass
        except IOError:
            self.mapping_file = ''
    
    def get_mapping_file(self):
        return self.mapping_file
    
    def get_content_of_mapping_file(self):
        """
        Read mapping file line after line and then create list from them
        """
        mapping_file = open(self.mapping_file,'r')
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

    def creata_mapping_file(self,jira_issue_metadata, header) :
        """
        Method create mapping file with all default fields from screen
        and with custom fields which are also in header of CVS file.
        Result file looks like this 
        "key_from_CVS_file" : "key_from_Jira"
        """
        mapping_file = open('new.mapping','wb')
        mapping_file.write('# Unnecessary lines should be deleted.  \n')
        mapping_file.write('# Only custom fields have IDs.\n')
        mapping_file.write('# Header key : Jira field ID : Jira field name\n')
        meta = jira_issue_metadata
        low_header = []
        for h in header:
            h.lower()
            low_header.append(h)
        for m in meta['fields']:
            if 'customfield' in m:
                field_name = meta['fields'][m]['name']
                field_name.lower()
                #if meta['fields'][m]['name'] in header:
                if field_name in low_header:
                    mapping_file.write('"')
                    #mapping_file.write(meta['fields'][m]['name'])
                    i = low_header.index(field_name)
                    mapping_file.write(header[i])
                    mapping_file.write('" : "')
                    mapping_file.write(m)
                    mapping_file.write('" : "')
                    mapping_file.write(meta['fields'][m]['name'])
                    mapping_file.write('"')
                    mapping_file.write('\n')
                    continue
                else:
                    continue
            mapping_file.write('"" : "')
            mapping_file.write(m)
            mapping_file.write('"')
            mapping_file.write('\n')
        mapping_file.close()