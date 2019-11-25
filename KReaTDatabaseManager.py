"""
Author: Praveen Rai
Date: MAR 19, 2019

Module with firebase API.
"""

#IMPORTS
from binascii import hexlify, unhexlify
from KReaTLogger import *
from KReaTFirebase import FireBaseRESTAPI

#GLOBALS
DOT = '_dot_'
HASH= '_has_'
EMPERCENT = '_emp_'
DOLLAR = '_dol_'
EXCLAIMATION = '_exl_'
ASTERIK = '_ast_'
PERCENT = '_per_'


class DataBaseManager():
    def __init__(self):
        self.restapi = FireBaseRESTAPI()


    def createUserAccount(self, email_id, pass_word, user_type, school_name, user_class, user_name):
        lcl_id = None
        lcl_data = None
        lcl_return = False
        lcl_date = None
        lcl_pass_word = ""
        try:
            lcl_id = email_id
            lcl_id = self.getCleanEmailId(email_id)
            lcl_date = self.todayDate()
            lcl_pass_word = pass_word
            
            lcl_data = {"Name": user_name, "Type": user_type, "Password": lcl_pass_word, "School": school_name, "Class": user_class, "Date": lcl_date}
            lcl_pass_word = self.getEncodedPassword(pass_word)
            lcl_data['Password'] = lcl_pass_word
            
            if(self.restapi.setData('LoginCredentials',lcl_id, lcl_data) == True):
                KREATDEBUG("Created user account with data " + str(lcl_data))
                lcl_return = True
        except:
            KREATDEBUG("Failed to create user account with data " + str(lcl_data))
        finally:
            return(lcl_return)


    def getUserAccount(self, email_id):
        lcl_type = None
        lcl_pass_word = None
        lcl_date = None
        try:
            lcl_id = email_id
            lcl_id = self.getCleanEmailId(email_id)
            
            lcl_query = 'LoginCredentials/'+lcl_id+'/Type'
            lcl_type = self.restapi.getData(lcl_query)
            
            lcl_query = 'LoginCredentials/'+lcl_id+'/Password'
            lcl_pass_word = self.restapi.getData(lcl_query)
            lcl_pass_word = self.getDecodedPassword(lcl_pass_word)

            lcl_query = 'LoginCredentials/'+lcl_id+'/Date'
            lcl_date = self.restapi.getData(lcl_query)

        except:
            KREATDEBUG("Failed to get user account with email " + email_id)

        finally:
            return(lcl_type,lcl_pass_word, lcl_date)

    def getCleanEmailId(self, email_id):
        lcl_id = email_id
        lcl_id = lcl_id.replace('.',DOT)

        if('#' in lcl_id):
            lcl_id = lcl_id.replace('#',HASH)
        
        if('&' in lcl_id):
            lcl_id = lcl_id.replace('&',EMPERCENT)

        if('$' in lcl_id):
            lcl_id = lcl_id.replace('$',DOLLAR)

        if('!' in lcl_id):
            lcl_id = lcl_id.replace('!',EXCLAIMATION)

        if('*' in lcl_id):
            lcl_id = lcl_id.replace('*',ASTERIK)

        if('%' in lcl_id):
            lcl_id = lcl_id.replace('%',PERCENT)

        return(lcl_id)

    def updateUserPassword(self, email_id, new_pass_word):
        lcl_return = False
        lcl_id = self.getCleanEmailId(email_id)
        lcl_date = self.todayDate()
        lcl_pass_word = new_pass_word
        
        lcl_data = {"Password":lcl_pass_word, "Date":lcl_date}
        lcl_pass_word = self.getEncodedPassword(new_pass_word)
        lcl_data['Password']=lcl_pass_word
        
        try:
            lcl_return = self.restapi.updateData('LoginCredentials',lcl_id,lcl_data)
        except:
            KREATDEBUG("Failed to update password!")
        else:
            lcl_return = True
        finally:
            return(lcl_return)

        
    def uploadUserStatistics(self, email_id, book_title, book_author, book_genre, reading_date, start_time, end_time, calc_hours):
        lcl_return = False
        lcl_id = self.getCleanEmailId(email_id)
        lcl_data = {"Title": book_title, "Author": book_author, "Genre": book_genre, "Date": reading_date, "Start Time": start_time, "End Time": end_time, "Hours":calc_hours}

        try:
            lcl_return = self.restapi.pushData('ReadingTracker/'+lcl_id,lcl_data)
        except:
            KREATDEBUG("Failed to upload stats!")
        else:
            lcl_return = True
        finally:
            return (lcl_return)

    def getUserStatistics(self,email_id):
        lcl_return = {}
        lcl_id = self.getCleanEmailId(email_id)
        
        try:
            lcl_return = self.restapi.getData('ReadingTracker/'+lcl_id)
        except:
            KREATDEBUG("Failed to get user stats!")
        finally:
            return(lcl_return)

    def getAllLoginCredentials(self):
        lcl_return = {}
        try:
            lcl_return = self.restapi.getData('LoginCredentials')
        except:
            KREATDEBUG("Failed to get login credential!")
        finally:
            return(lcl_return)

        
    def todayDate(self):
        return datetime.datetime.now().strftime("%Y-%m-%d")

    def getEncodedPassword(self, pass_word):
        lcl_pass = ""
        lcl_pass = hexlify(pass_word.encode('utf8'))
        return (lcl_pass.decode('utf8'))

    def getDecodedPassword(self, enc_pass_word):
        lcl_pass = ""
        lcl_pass = unhexlify(enc_pass_word.encode('utf8'))
        return (lcl_pass.decode('utf8'))
    
# Test functions to create users.
if __name__ == '__main__':
    db_mgr = DataBaseManager()
    db_mgr.createUserAccount("Something.#.Mooh@gmail.com","Patanahin","Teacher","BVM", "XI", "MeraNaamJoker Smith")
    print(db_mgr.getUserAccount("Something.#.Mooh@gmail.com"))
    db_mgr.updateUserPassword("Something.#.Mooh@gmail.com","KyunNahinPata")
    print(db_mgr.getUserAccount("Something.#.Mooh@gmail.com"))
    db_mgr.uploadUserStatistics("Something.#.Mooh@gmail.com","1","2","3","4","5","6","7")
    all_val = db_mgr.getUserStatistics("Something.#.Mooh@gmail.com")
    print(all_val)
    for item in all_val:
        print(all_val[item])

    all_val = db_mgr.getAllLoginCredentials()
    for item in all_val:
        print(all_val[item]['Name'], item)
    
