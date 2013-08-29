'''
@author: ThePaloC
'''

from CSV_module import CSV
from Mapping_module import Mapping
from jira.client import JIRA
import os
from Jira_module import Jira
import datetime

class Main(object):
    def __init__(self,properties):
        """
        Initialize properties to access files and to access Jira
        :param properties: dictionary with all properties
        """
        self.properties = properties
        self.csv_file_new = properties['csv_file_new']
        self.csv_file_delete = properties['csv_file_delete']
        self.csv_file_update = properties['csv_file_update']
        self.mapping_file = properties['mapping_file']
        self.server = properties['server']
        self.username = properties['username']
        self.password = properties['password']
        self.datetime_format = properties['datetime_format']
        self.backup_folder = properties['backup_folder']
    
    def get_Csv_module(self):
        """
        csv = [new, update, delete]
        """
        csv_init = CSV(self.csv_file_new, self.csv_file_delete, 
                       self.csv_file_update)
        return csv_init    
    
    def get_Mapping_module(self):
        """
        Get access to mapping file from path given in properties
        """
        try :
            mapping = Mapping(self.mapping_file)
        except IOError :
            return 0
        return mapping
        
    def get_Jira(self):
        """
        Returns Jira instance running on server
        """
        options = {
            'server': self.server
        }
        jira = JIRA(options,basic_auth=(self.username,self.password))
        return jira
    
    def create_mapping_file_from_jira_metadata(self,jira_issue_metadata,
                                               header) :
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
    
    def move_to_backup(self,file):
        datetime_format = self.datetime_format
        file_sufix = datetime.datetime.now().strftime(datetime_format)
        file_name = os.path.basename(file)
        os.rename(file, self.backup_folder+file_name+'.'+file_sufix)
        print 'Moving file ' + file_name + ' to backup'
    
def main():
    properties = {
                  'csv_file_new' : '../resources/NewMRsOnlyExport.csv',
                  'csv_file_delete' : '../resources/DeletedMRsOnly.csv',
                  'csv_file_update' : '../resources/UpdatedMRsOnly.csv',
                   'mapping_file' : '../resources/new.mapping',
                  'server': 'http://localhost:2990/jira',
                  'username' : 'admin',
                  'password' : 'admin',
                  'datetime_format' : '%d-%m-%Y_%H-%M-%S',
                  'backup_folder' : '../backup/'
                  }
    #initialize priperties
    main = Main(properties)
    csv = main.get_Csv_module()
    mapping = main.get_Mapping_module()
    jira_module = Jira(main.get_Jira())

    print 'All set'
    
    csv_action = {'new' : '',
                  'update' : '',
                  'delete' : ''
                  }
    try :
        csv_action['new'] = csv.get_new_csv()
    except IOError :
        csv_action['new'] = ''
    try :
        csv_action['update'] = csv.get_update_csv()
    except IOError:
        csv_action['update'] = ''
    try :
        csv_action['delete'] = csv.get_delete_csv()
    except IOError:
            csv_action['delete'] = ''
    
    print 'Actions'
    print 'Do -> ' + str(csv_action)
    
    if csv_action['new'] != '' :
        print 'Creating new issues'
        #get all data necessary for creating issue
        header = csv.get_header(csv_action['new'])
        data_dict = csv.get_csv_dictionary(csv_action['new'])
        
        if mapping == 0:
            print "Missing mapping file"
            while( True ):
                #answer = raw_input('Create a new mapping file? [y/n]: ')
                answer = 'y'
                if (answer == 'y' or answer == 'n'):
                    if answer == 'y' :
                        #issue_key = raw_input('Key of mapping issue: ')
                        issue_key = 'PJ-2168'
                        meta =  main.get_Jira().editmeta(issue_key)
                        main.create_mapping_file_from_jira_metadata(meta, header)
                        os.rename('new.mapping',main.mapping_file)
                        mapping = Mapping(main.mapping_file)
                        break
                    else :
                        return
        mapp = mapping.get_mapping_dictionary()
        number_of_issues = data_dict['MR-ID']
        m = 0
        #create data for one issue and then call create issue method on them
        for issue in number_of_issues:
            data = {}
            for i in header:
                data[i] = data_dict[i][m]
            iss = jira_module.create_issue(header, data, mapp)
            print 'Created Issue: ' + str(iss)
            m = m + 1
        print 'Creating new issues finished'
        main.move_to_backup(csv_action['new'])
    if csv_action['update'] != '' :
        main.move_to_backup(csv_action['update'])
        pass
    if csv_action['delete'] != '' :
        print 'Deleting issues'
        #get all data necessary for creating issue
        data_dict = csv.get_csv_dictionary(csv_action['delete'])
        mapp = mapping.get_mapping_dictionary()
        number_of_issues = data_dict['MR-ID']
        customfield_id = mapp['MR-ID']['id']
        cf_id = customfield_id.split('_')[1]
        for issue in number_of_issues:
            jira = main.get_Jira()
            found_issue = jira.search_issues('cf['+ cf_id +']' + ' ~ "' + issue + '"')
            print 'Deleting issue ' + str(found_issue[0])
            found_issue[0].delete()
        main.move_to_backup(csv_action['delete'])
        
if __name__ == '__main__':
    main()
