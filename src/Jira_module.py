'''
@author: ThePaloC
'''

class Jira (object):
    
    def __init__(self,jira_instance):
        self.jira_instance = jira_instance
    
    def get_Jira(self):
        return self.jira_instance
    
    def create_issue(self,header,issue_data,mapping_data):
        """
        Method create issue in Jira. First it creates issue_dict dictionary
        with all attributes, then is dictionary passed to Jira API and then
        finaly send to Jira
        :param header: Header from CSV file as a list. ['MR-Tag','MR-ID',...]
        :param issue_data: Data from CSV file as a dictionary. {'k1':'v1','k2':}
        :param mapping_data: Mapping dictionary.
        """
        issue_dict = {
                      'project' : {'key': 'CIA'},
                      'issuetype' : {'name' : 'New Feature'}
                      }
        for i in header:
            m_key = i
            if m_key in mapping_data.keys():
                m_value = mapping_data[m_key]['id']
                m_value_name = mapping_data[m_key]['name']
                """
                Some fields require user to define specific value, name or id.
                For example, RA is select list
                """
                if m_value.startswith('customfield'):
                    if m_value_name == 'RA':
                        issue_dict[m_value] = {'value' : issue_data[i]}
                        continue
                if m_value == 'reporter':
                    issue_dict[m_value] = {'name' : issue_data[i]}
                    continue
                issue_dict[m_value] = issue_data[i]
        jira = self.get_Jira()
        new_issue = jira.create_issue(fields=issue_dict)
        return new_issue
