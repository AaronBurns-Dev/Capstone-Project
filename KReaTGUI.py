"""
Author: Praveen Rai
Date: 03/14/2019

Module for user interface. Needs kivy.require('1.9.0')
"""

#IMPORTS
import kivy 
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.graphics import Line

import re
import datetime
from KReaTLogger import *
from KReaTEmail import sendMyEmail
from KReaTDatabaseManager import DataBaseManager as realTimeDB

#GLOBALS
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
USER_TYPE = 'UNKNOWN'
TEACHER = 'Teacher'
STUDENT = 'Student'
NOTAPPLICABLE = 'NA'
NEW_ACC_CREAT_SUBJECT = 'Welcome To KReaT'
NEW_ACC_CREAT_MSG = 'Welcome to KReaT- Kids Reading Tracker. Start Logging Your Reading Hours!'
PASS_CHANGE_SUBJECT = 'Alert-Password Change'
PASS_CHANGE_MSG = 'Your password has been changed. Please contact help desk if this was not done by your!'
READING_HOURS_LOGGED_SUBJECT = 'Reading Hours Updated'
READING_HOURS_LOGGED_MSG = 'Your reading hours have been logged in KReaT. Keep up the good work!'

# You can create your kv code in the Python file
Builder.load_string("""
# Custom button
<CustButton@Button>:
    font_size: 18

<CustomPopup>:
    id: CustomPopUp
    size_hint:.3, .2
    auto_dismiss: False
    title: "Message"
    Button:
        text: "OK"
        on_press:root.dismiss()

<UserSelectScreen>:
    BoxLayout
        id: UserSelectLayout
        orientation: 'vertical'
        padding: [10,50,10,50]
        spacing: 50

        Label:
            text: 'KReaT\u2122 Kids Reading Tracker'
            font_size: 24
            halign: 'center'
            size_hint: (1, 1)       

        BoxLayout:
            orientation: 'vertical'
            CustButton:
                id: teacherSelectButton
                text: "TEACHER ENTER"
                halign: 'center'
                size_hint: (1, 0.5)                
                on_press:
                    root.onTeacherSelectButtonPress()
        BoxLayout:
            orientation: 'vertical'
            CustButton:
                id: studentSelectButton
                text: "STUDENT ENTER"
                halign: 'center'
                size_hint: (1, 0.5)                
                on_press:
                    root.onStudentSelectButtonPress()
        BoxLayout:
            orientation: 'vertical'
            CustButton:
                id: userExitButton
                text: "EXIT KREAT"
                halign: 'center'
                size_hint: (1, 0.5)                
                on_press:
                    root.onUserExitButtonPress()
                    
        BoxLayout:
            orientation: 'vertical'
            Label:
                text: 'KReaT is designed by rai@uwm.edu for INFOST-790 at UWM. Any usage outside course work requires consent.'
                font_size: 8
                halign: 'center'
                size_hint: (1, 1)
                    
<LoginScreen>:
    BoxLayout
        id: LoginLayout
        orientation: 'vertical'
        padding: [10,50,10,50]
        spacing: 50

        Label:
            text: 'KReaT\u2122 Kids Reading Tracker'
            font_size: 24
            halign: 'center'
            size_hint: (1, 1)            

        BoxLayout:
            orientation: 'vertical'
            Label:
                text: 'Email Id'
                font_size: 18
                halign: 'center'
                size_hint: (1, 1)                

            TextInput:
                id: login
                multiline:False
                font_size: 18
                halign: 'center'
                size_hint: (1, 1)
                write_tab:False 
                hint_text: 'something@gmail.com'

        BoxLayout:
            orientation: 'vertical'
            Label:
                text: 'Password'
                halign: 'center'
                font_size: 18
                size_hint: (1, 1)                

            TextInput:
                id: password
                multiline:False
                password:True
                font_size: 18
                halign: 'center'
                size_hint: (1, 1)
                write_tab:False
                hint_text: 'password'

        BoxLayout:
            orientation: 'vertical'
            CustButton:
                id: userLoginButton
                text: "LOGIN"
                halign: 'center'
                size_hint: (1, 0.5)                
                on_press:
                    root.onUserLoginButtonPress()
        BoxLayout:
            orientation: 'horizontal'
            CustButton:
                id: createNewAccButton
                text: "CREATE NEW ACCOUNT"
                size_hint: (1, 0.5)
                halign: 'left'
                on_press:
                    root.onCreateNewAccButtonPress()
                    
            CustButton:
                id: exitButton
                text: "EXIT"
                halign: 'right'
                size_hint: (1, 0.5)
                on_press:
                    root.onExitButtonPress()


<CreateUserScreen>:
    BoxLayout
        id: CreateUserLayout
        orientation: 'vertical'
        padding: [10,50,10,50]
        spacing: 50

        Label:
            text: 'KReaT\u2122 New Account'
            font_size: 24
            halign: 'center'
            size_hint: (1, 1)            

        BoxLayout:
            orientation: 'horizontal'
            Label:
                text: 'Email Id'
                font_size: 18
                halign: 'left'
                size_hint: (1, 0.5)                

            TextInput:
                id: login
                multiline:False
                font_size: 12
                size_hint: (1, 0.5)
                write_tab:False
                hint_text: 'something@gmail.com'

            Label:
                text: 'Date'
                halign: 'center'
                font_size: 18
                size_hint: (1, 0.5)

            TextInput:
                id: datetime
                multiline:False
                font_size: 12
                hint_text: 'YYYY-MM-DD'
                readonly:True
                size_hint:(1, 0.5)
                write_tab:False
                
            Label:
                text: 'Password'
                halign: 'right'
                font_size: 18
                size_hint: (1, 0.5)                

            TextInput:
                id: password
                multiline:False
                password:True
                font_size: 12
                size_hint: (1, 0.5)
                write_tab:False
                hint_text: 'password'

        BoxLayout:
            orientation: 'horizontal'
            Label:
                text: 'Name'
                halign: 'left'
                font_size: 18
                size_hint:(1, 0.5)

            TextInput:
                id: username
                multiline:False
                font_size: 12
                hint_text: 'Adam Smith'
                write_tab:False
                size_hint:(1, 0.5)

            Label:
                text: 'Class'
                halign: 'center'
                font_size: 18
                size_hint:(1, 0.5)

            TextInput:
                id: userclass
                multiline:False
                font_size: 12
                hint_text: 'NA For Teacher'
                write_tab:False
                size_hint:(1, 0.5)

            Label:
                text: 'School Name'
                halign: 'right'
                font_size: 18
                size_hint:(1, 0.5)

            TextInput:
                id: schoolname
                multiline:False
                font_size: 12
                hint_text: 'XYZ School'
                write_tab:False
                size_hint:(1, 0.5)
                
        BoxLayout:
            orientation: 'horizontal'
            CustButton:
                id: createUserAccButton
                text: "CREATE ACCOUNT"
                halign: 'left'
                size_hint: (1, 0.6)                
                on_press:
                    root.onCreateUserAccButtonPress()
                    
            CustButton:
                id: cancelButton
                text: "CANCEL"
                halign: 'right'
                size_hint: (1, 0.6)
                on_press:
                    root.manager.transition.direction = 'right'
                    root.manager.current = 'LoginScreen'

        BoxLayout:
            orientation: 'vertical'
            Label:
                text: ''
                font_size: 24
                halign: 'center'
                size_hint: (1, 1)

                
<StudentLandingScreen>:
    BoxLayout:
        id: StudentLandingLayout
        orientation: 'vertical'
        padding: [10,50,10,50]
        spacing: 50

        Label:
            text: 'My KReaT\u2122'
            font_size: 24
            halign: 'center'
            size_hint: (1, 1)

        BoxLayout:
            orientation: 'horizontal'
            CustButton:
                id: studentStatsListButton
                text: 'Select Statistics Entry'
                halign: 'center'
                size_hint: (1,0.5)

        BoxLayout:
            orientation: 'horizontal'
            Label:
                text: 'Author'
                font_size: 18
                halign: 'left'
                size_hint: (1, 0.5)                

            TextInput:
                id: authorName
                multiline:False
                font_size: 12
                size_hint: (1, 0.5)
                write_tab:False
            Label:
                text: 'Genre'
                font_size: 18
                halign: 'center'
                size_hint: (1, 0.5)                

            TextInput:
                id: bookGenre
                multiline:False
                font_size: 12
                size_hint: (1, 0.5)
                write_tab:False
            Label:
                text: 'Hours'
                font_size: 18
                halign: 'center'
                size_hint: (1, 0.5)
                write_tab:False

            TextInput:
                id: readingHours
                multiline:False
                font_size: 12
                size_hint: (1, 0.5)
                write_tab:False

        BoxLayout:
            orientation: 'horizontal'
            Label:
                id: totalHoursLabel
                text: 'Total Hours:'
                font_size: 18
                halign: 'center'
                size_hint: (1, 0.5)

        BoxLayout:
            orientation: 'horizontal'                  
            CustButton:
                id: logHoursStudentLandingScreen
                text: "START LOGGING HOURS"
                halign: 'center'
                size_hint: (1, 0.5)
                on_press:
                    root.onLogHoursButtonPress()
        BoxLayout:
            orientation: 'horizontal'                  
            CustButton:
                id: logoutButtonStudentLandingScreen
                text: "LOGOUT"
                halign: 'left'
                size_hint: (1, 0.5)
                on_press:
                    root.manager.transition.direction = 'right'
                    root.manager.current = 'LoginScreen'
            CustButton:
                id: refreshStudentAccountButton
                text: "REFRESH"
                halign: 'center'
                size_hint: (1, 0.5)
                on_press:
                    root.onRefreshStudentAccountButtonPress()
            CustButton:
                id: updateStudentAccountButton
                text: "UPDATE ACCOUNT"
                halign: 'right'
                size_hint: (1, 0.5)
                on_press:
                    root.onUpdateStudentAccountPress()

<TeacherLandingScreen>:
    BoxLayout:
        id: TeacherLandingScreenLayout
        orientation: 'vertical'
        padding: [10,50,10,50]
        spacing: 50

        Label:
            text: 'My KReaT\u2122'
            font_size: 24
            halign: 'center'
            size_hint: (1, 1)

        BoxLayout:
            orientation: 'horizontal'
            CustButton:
                id: studentListButton
                text: 'Select Student'
                halign: 'center'
                size_hint: (1,0.5)

        BoxLayout:
            orientation: 'horizontal'
            Label:
                text: 'Student Name'
                font_size: 18
                halign: 'left'
                size_hint: (1, 0.5)                

            TextInput:
                id: studentName
                multiline:False
                font_size: 12
                size_hint: (1, 0.5)
                write_tab:False
            Label:
                text: 'Student Class'
                font_size: 18
                halign: 'center'
                size_hint: (1, 0.5)                

            TextInput:
                id: studentClass
                multiline:False
                font_size: 12
                size_hint: (1, 0.5)
                write_tab:False
            Label:
                text: 'Student School'
                font_size: 18
                halign: 'center'
                size_hint: (1, 0.5)
                write_tab:False

            TextInput:
                id: studentSchool
                multiline:False
                font_size: 12
                size_hint: (1, 0.5)
                write_tab:False

        BoxLayout:
            orientation: 'horizontal'
            CustButton:
                id: studentStatsListButton
                text: 'Select Statistics Entry'
                halign: 'center'
                size_hint: (1,0.5)

        BoxLayout:
            orientation: 'horizontal'
            Label:
                text: 'Author'
                font_size: 18
                halign: 'left'
                size_hint: (1, 0.5)                

            TextInput:
                id: authorName
                multiline:False
                font_size: 12
                size_hint: (1, 0.5)
                write_tab:False
            Label:
                text: 'Genre'
                font_size: 18
                halign: 'center'
                size_hint: (1, 0.5)                

            TextInput:
                id: bookGenre
                multiline:False
                font_size: 12
                size_hint: (1, 0.5)
                write_tab:False
            Label:
                text: 'Hours'
                font_size: 18
                halign: 'center'
                size_hint: (1, 0.5)                

            TextInput:
                id: readingHours
                multiline:False
                font_size: 12
                size_hint: (1, 0.5)
                write_tab:False

        BoxLayout:
            orientation: 'horizontal'
            Label:
                id: totalHoursLabel
                text: 'Total Hours:'
                font_size: 18
                halign: 'left'
                size_hint: (1, 0.5)
            Label:
                id: classStandingLabel
                text: 'Class Standing (out of 10):'
                font_size: 18
                halign: 'right'
                size_hint: (1, 0.5)
                
        BoxLayout:
            orientation: 'horizontal'                 
            CustButton:
                id: logoutTeacherLandingScreen
                text: "LOGOUT"
                halign: 'left'
                size_hint: (1, 0.5)
                on_press:
                    root.manager.transition.direction = 'right'
                    root.manager.current = 'LoginScreen'
            CustButton:
                id: refreshTeacherAccountButton
                text: "REFRESH"
                halign: 'center'
                size_hint: (1, 0.5)
                on_press:
                    root.onRefreshTeacherAccountButtonPress()
            CustButton:
                id: updateTeacherAccountButton
                text: "UPDATE ACCOUNT"
                halign: 'right'
                size_hint: (1, 0.5)
                on_press:
                    root.onUpdateTeacherAccountPress()

<UpdateAccountScreen>:
    BoxLayout
        id: UpdateAccountLayout
        orientation: 'vertical'
        padding: [10,50,10,50]
        spacing: 50

        Label:
            text: 'KReaT\u2122 Kids Reading Tracker'
            font_size: 24
            halign: 'center'
            size_hint: (1, 1)            

        BoxLayout:
            orientation: 'vertical'
            Label:
                text: 'Email Id'
                font_size: 18
                halign: 'center'
                size_hint: (1, 1)                

            TextInput:
                id: login
                multiline:False
                font_size: 18
                halign: 'center'
                size_hint: (1, 1)
                hint_text: 'something@gmail.com'
                write_tab:False

        BoxLayout:
            orientation: 'vertical'
            Label:
                text: 'New Password'
                halign: 'center'
                font_size: 18
                size_hint: (1, 1)                

            TextInput:
                id: password
                multiline:False
                password:True
                font_size: 18
                halign: 'center'
                size_hint: (1, 1)
                write_tab:False
                hint_text: 'password'

        BoxLayout:
            orientation: 'horizontal'
            CustButton:
                id: updateAccounButton
                text: "UPDATE"
                halign: 'left'
                size_hint: (1, 0.5)                
                on_press:
                    root.onUpdateAccountButtonPress()
            CustButton:
                id: cancelUpdateAccount
                text: "CANCEL"
                halign: 'right'
                size_hint: (1, 0.5)
                on_press:
                    root.onCancelUpdateAccountButtonPress()

        BoxLayout:
            orientation: 'vertical'
            Label:
                text: ''
                font_size: 24
                halign: 'center'
                size_hint: (1, 1)

<LoggingHourScreen>:
    BoxLayout
        id: LoggingHourLayout
        orientation: 'vertical'
        padding: [10,50,10,50]
        spacing: 50

        Label:
            text: 'KReaT\u2122 Logger'
            font_size: 24
            halign: 'center'
            size_hint: (1, 1)

        BoxLayout:
            orientation: 'horizontal'
            Label:
                text: 'Title'
                font_size: 18
                halign: 'left'
                size_hint: (1, 0.5)                

            TextInput:
                id: booktitle
                multiline:False
                font_size: 12
                size_hint: (1, 0.5)
                write_tab:False

            Label:
                text: 'Author'
                font_size: 18
                halign: 'center'
                size_hint: (1, 0.5)

            TextInput:
                id: bookauthor
                multiline:False
                font_size: 12
                size_hint: (1, 0.5)
                write_tab:False

            Label:
                text: 'Genre'
                font_size: 18
                halign: 'right'
                size_hint: (1, 0.5)                

            CustButton:
                id: bookGenreListButton
                text: 'Select'
                font_size: 12
                size_hint: (1,0.5)

        BoxLayout:
            orientation: 'horizontal'
            Label:
                text: 'Start Time'
                font_size: 18
                halign: 'left'
                size_hint: (1, 0.5)                

            TextInput:
                id: starttime
                multiline:False
                font_size: 12
                size_hint: (1, 0.5)
                hint_text: 'HH:MM'
                write_tab:False
                on_text:
                    root.onStartTimeTextEntered()
            Label:
                text: 'End Time'
                font_size: 18
                halign: 'center'
                size_hint: (1, 0.5)                

            TextInput:
                id: endtime
                multiline:False
                font_size: 12
                size_hint: (1, 0.5)
                hint_text: 'HH:MM'
                write_tab:False
                on_text:
                    root.onEndTimeTextEntered()

            Label:
                text: 'Calculated Hours'
                font_size: 18
                halign: 'right'
                size_hint: (1, 0.5)                

            TextInput:
                id: calchours
                multiline:False
                font_size: 12
                size_hint: (1, 0.5)
                readonly:True
                write_tab:False
                
        BoxLayout:
            orientation: 'horizontal'
            CustButton:
                id: updateLogButton
                text: "UPDATE"
                halign: 'left'
                size_hint: (1, 0.5)                
                on_press:
                    root.onUpdateLogButtonPress()
            CustButton:
                id: cancelLogging
                text: "DONE"
                halign: 'right'
                size_hint: (1, 0.5)
                on_press:
                    root.onCancelLoggingButtonPress()

        BoxLayout:
            orientation: 'vertical'
            Label:
                text: ''
                font_size: 24
                halign: 'center'
                size_hint: (1, 1)
""")

# Create all helper functions
#Function to read genre for file
def getGenreFromFile():
    lcl_lst = []
    with open('GENRE_CSV_LIST') as f:
        for line in f:
            line = line.strip('\r\n')
            lcl_lst = line.split(',')
    return(lcl_lst)

#Function to return today's date in specific format.
def todayDate():
    return datetime.datetime.now().strftime("%Y-%m-%d")

#Function to validate specific date format.
def validateDate(date_string):
    lclReturn = True
    try:
        datetime.datetime.strptime(date_string, "%Y-%m-%d")
    except ValueError:
        lclReturn = False
    finally:
        return lclReturn
    
#Function to validate email address.
#Regex tester: https://www.regextester.com/1924
def validateEmail(email_id):
    lclReturn = False
    if(email_id):
        rex = re.compile("[^@]+@[^@]+\.[^@]+")
        if(rex.match(email_id)):
            lclReturn = True
    return (lclReturn)

#Function to validate string.
def validateString(str_value):
    lclReturn = False
    if(str_value):
        rex = re.compile("^$|\s")
        if(not rex.match(str_value)):
            lclReturn = True

    return (lclReturn)

#Function to validate time format
def validateTimeFormat(time_value):
    lcl_return = True
    if(time_value):
        try:
            datetime.datetime.strptime(time_value, '%H:%M')
            lcl_return = True
        except ValueError:
            lcl_return = False
        finally:
            return(lcl_return)
    
#Function to set user type
def setUserType(user_type):
    global USER_TYPE
    USER_TYPE = user_type


#Function to get user type
def getUserType():
    return(USER_TYPE)


#Function to set screen name
def setScreenNames(current_screen):
    global CURRENT_SCREEN
    CURRENT_SCREEN = current_screen

#Function to get screen names
def getScreenNames():
    return(CURRENT_SCREEN)

#Function to set user id
def setUserID(email_id):
    global EMAIL_ID
    EMAIL_ID = email_id

#Function to get user id
def getUserID():
    return(EMAIL_ID)

#Function to get hours between two time
def getTimeDiffInHours(time1,time2):
    lcl_diff = 0.25
    lcl_t1 = 0
    lcl_t2 = 0
    try:
        lcl_t1 = datetime.datetime.strptime(time1,'%H:%M')
        lcl_t2 = datetime.datetime.strptime(time2,'%H:%M')
        lcl_diff = lcl_t2 - lcl_t1
        lcl_diff = (lcl_diff.seconds/3600)
    except:
        KREATDEBUG("getTimeDiffInHours: failed to get time diff!")
    finally:
        return (lcl_diff)

        
# Create a class for all screens in which you can include
# helpful methods specific to that screen
class CustomDropDown(DropDown):
    pass

class CustomPopup(Popup):

    def setTitle(self, msg):
        self.title = msg
    

#UserSelect screen class
class UserSelectScreen(Screen):

    def __init__(self,*args, **kwargs):
        super(UserSelectScreen, self).__init__(*args, **kwargs)

    def onTeacherSelectButtonPress(self):
        setUserType(TEACHER)
        screen_manager.current = 'LoginScreen'
        KREATDEBUG("onTeacherSelectButtonPress: Teacher Enter!")

    def onStudentSelectButtonPress(self):
        setUserType(STUDENT)
        screen_manager.current = 'LoginScreen'
        KREATDEBUG("onStudentSelectButtonPress: Student Enter!")

    def onUserExitButtonPress(self):
        KREATDEBUG("onExitButtonPress: Successfully Exiting KReaT!")
        App.get_running_app().stop()
        Window.close()

    
#Login screen class
class LoginScreen(Screen):

    def __init__(self,*args, **kwargs):
        super(LoginScreen, self).__init__(*args, **kwargs)

        self.db_mgr = DATABASE_MGR
        self.pass_word_expired = False

    def on_enter(self):
        self.ids.login.text = ""
        self.ids.password.text = ""
        
    def onUserLoginButtonPress(self):
        KREATDEBUG("onUserLoginButtonPress: User Type " + getUserType())
        
        loginSuccessful = False
        #Check for format
        loginSuccessful = validateEmail(self.ids.login.text.strip())
        if(loginSuccessful == False):
            p = CustomPopup()
            p.setTitle("Email Id Format Incorrect")
            p.open()
        else:
            loginSuccessful = validateString(self.ids.password.text.strip())
            if(loginSuccessful == False):
                p = CustomPopup()
                p.setTitle("Password empty!")
                p.open()
            else:
                #Validate against the database
                loginSuccessful = self.validateLoginCredentialWithDB(getUserType(),self.ids.login.text.strip(),self.ids.password.text.strip())

                if(loginSuccessful == False):
                    p = CustomPopup()
                    p.setTitle("Incorrect Login Password")
                    p.open()
                else:
                    if(self.pass_word_expired == True):
                        p = CustomPopup()
                        p.setTitle("Password has expired. Please Update!")
                        p.open()

                    setUserID(self.ids.login.text.strip())    
                    self.ids.login.text = ""
                    self.ids.password.text = ""
                    if(getUserType() == TEACHER):
                        screen_manager.current = 'TeacherLandingScreen'
                    else:
                        screen_manager.current = 'StudentLandingScreen'
                    KREATDEBUG("onUserLoginButtonPress: Logged In Successfully!")

    def validateLoginCredentialWithDB(self, user_type, email_id, pass_word):
        lcl_return = False
        try:
            lcl_type, lcl_pass_word, lcl_date = self.db_mgr.getUserAccount(email_id)
            if(lcl_type == user_type) and (lcl_pass_word == pass_word):
                lcl_return = True
                self.pass_word_expired = False
                if(self.isPasswordExpired(lcl_date) == True):
                    self.pass_word_expired = True
                    KREATDEBUG("validateLoginCredentialWithDB: pass word has expired!")
        except:
            KREATDEBUG("validateLoginCredentialWithDB: Failed to read credentials from db!")
        finally:
            return(lcl_return)
        
    def onCreateNewAccButtonPress(self):
        self.ids.login.text = ""
        self.ids.password.text = ""
        screen_manager.current = 'CreateUserScreen'
        KREATDEBUG("onCreateNewAccButtonPress: Switching to create user account screen!")
    
    def onExitButtonPress(self):
        KREATDEBUG("onExitButtonPress: Successfully Exiting KReaT!")
        App.get_running_app().stop()
        Window.close()

    def isPasswordExpired(self, date_time):
        lcl_date = datetime.datetime.now()+ datetime.timedelta(days=365)
        lcl_date = lcl_date.strftime("%Y-%m-%d")
        return(lcl_date < date_time)        
        
        
#CreateUser screen class
class CreateUserScreen(Screen):

    def __init__(self, *args, **kwargs):
        super(CreateUserScreen, self).__init__(*args, **kwargs)

        self.db_mgr = DATABASE_MGR
        self.ids.datetime.text = todayDate()

    def on_enter(self):
        self.ids.login.text = ""
        self.ids.password.text = ""
        
    def onCreateUserAccButtonPress(self):
        credOk = False
        
        credOk = validateEmail(self.ids.login.text.strip())

        if(credOk == False):
            p = CustomPopup()
            p.setTitle("Email Id Format Incorrect")
            p.open()
        else:
            credOk = (validateString(self.ids.password.text.strip()) == True) and (validateString(self.ids.schoolname.text.strip()) == True) and (validateString(self.ids.username.text.strip()) == True)
            if(getUserType() == STUDENT) and (credOk == True):
                credOk = validateString(self.ids.userclass.text.strip())    
            if(credOk == False):
                p = CustomPopup()
                p.setTitle("Missing Or Empty Values. Please Enter All The Details!")
                p.open()
            else:
                #Create new account
                if(self.createNewUserAcc(getUserType(),self.ids.login.text.strip(),self.ids.password.text.strip(),self.ids.schoolname.text.strip(),self.ids.userclass.text.strip(),self.ids.username.text.strip()) == True):
                    p = CustomPopup()
                    p.setTitle("New Account Created Successfully. Please Re-Login!")
                    p.open()
                    sendMyEmail(NEW_ACC_CREAT_SUBJECT, NEW_ACC_CREAT_MSG, self.ids.login.text.strip())
                    self.ids.login.text = ""
                    self.ids.password.text = ""
                    screen_manager.current = 'LoginScreen'
                    KREATDEBUG("onReturnToLoginButtonPress: Switching back to login screen!")
                else:
                    p = CustomPopup()
                    p.setTitle("Failed To Create New Account. Re-try Or Call Help Desk!")
                    p.open()
                


    def createNewUserAcc(self, user_type, email_id, pass_word, school_name, user_class, user_name):
        lcl_return = False
        if(user_type == STUDENT):
            lcl_return = self.db_mgr.createUserAccount(email_id,pass_word,user_type,school_name,user_class,user_name)
        else:
            lcl_return = self.db_mgr.createUserAccount(email_id,pass_word,user_type,school_name,NOTAPPLICABLE,user_name)
        return(lcl_return)


#StudentLanding screen class        
class StudentLandingScreen(Screen):
    
    def __init__(self, *args, **kwargs):
        super(StudentLandingScreen, self).__init__(*args, **kwargs)

        self.db_mgr = DATABASE_MGR
        self.myStatsDropDown = CustomDropDown()
        self.myStatsList = {}
        
    def on_enter(self):
        lcl_text = ""
        lcl_total_hours = 0
        try:
            self.myStatsList = self.db_mgr.getUserStatistics(getUserID())
        except:
            KREATDEBUG("on_enter: failed to read statistics for " + getUserID())
        else:
            self.myStatsDropDown.clear_widgets()
            self.ids.studentStatsListButton.text = "Select Statistics Entry"
            self.ids.authorName.text = ""
            self.ids.bookGenre.text = ""
            self.ids.readingHours.text = ""
            if(self.myStatsList is not None):
                for item in self.myStatsList:
                    lcl_text = self.myStatsList[item]['Title'] + "," + self.myStatsList[item]['Date'] + "," + self.myStatsList[item]['Start Time']
                    lcl_total_hours = lcl_total_hours + float(self.myStatsList[item]['Hours'])
                    btn = Button(text=lcl_text, id=item, size_hint_y=None, height=44)
                    btn.bind(on_release=lambda btn: self.myStatsDropDown.select(btn.text))
                    btn.bind(on_release=lambda btn: self.updateScreenStatsFields(btn.id))
                    self.myStatsDropDown.add_widget(btn)
                

        self.ids.studentStatsListButton.bind(on_release=self.myStatsDropDown.open)
        self.myStatsDropDown.bind(on_select=lambda instance, x: setattr(self.ids.studentStatsListButton, 'text', x))
                        
        self.ids.totalHoursLabel.text = ("Total Hours: %0.2f" %(lcl_total_hours))            

    def updateScreenStatsFields(self, unique_id):
        KREATDEBUG("updateScreenStatsFields: updating screen for " + getUserID())
        if(self.myStatsList is not None):
            self.ids.authorName.text = self.myStatsList[unique_id]['Author']
            self.ids.bookGenre.text = self.myStatsList[unique_id]['Genre']
            self.ids.readingHours.text = ("%0.2f" %(self.myStatsList[unique_id]['Hours']))
        
    def onRefreshStudentAccountButtonPress(self):
        self.ids.authorName.text = ""
        self.ids.bookGenre.text = ""
        self.ids.readingHours.text = ""
        self.myStatsDropDown.clear_widgets()
        self.ids.studentStatsListButton.text = "Select Statistics Entry"
        lcl_text = ""
        lcl_total_hours = 0
        try:
            self.myStatsList = self.db_mgr.getUserStatistics(getUserID())
        except:
            KREATDEBUG("onRefreshStudentAccountButtonPress: failed to read statistics for " + getUserID())
        else:
            if(self.myStatsList is not None):
                for item in self.myStatsList:
                    lcl_text = self.myStatsList[item]['Title'] + "," + self.myStatsList[item]['Date'] + "," + self.myStatsList[item]['Start Time']
                    lcl_total_hours = lcl_total_hours + float(self.myStatsList[item]['Hours'])
                    btn = Button(text=lcl_text, id=item, size_hint_y=None, height=44)
                    btn.bind(on_release=lambda btn: self.myStatsDropDown.select(btn.text))
                    btn.bind(on_release=lambda btn: self.updateScreenStatsFields(btn.id))
                    self.myStatsDropDown.add_widget(btn)
    
    def onUpdateStudentAccountPress(self):
        setScreenNames('StudentLandingScreen')
        screen_manager.current = 'UpdateAccountScreen'
        KREATDEBUG("onUpdateStudentAccountPress: Switching to update account screen!")

    def onLogHoursButtonPress(self):
        setScreenNames('StudentLandingScreen')
        screen_manager.current = 'LoggingHourScreen'
        KREATDEBUG("onLogHoursButtonPress: Switching to logging hours screen!")

#TeacherLanding screen class
class TeacherLandingScreen(Screen):
    
    def __init__(self, *args, **kwargs):
        super(TeacherLandingScreen, self).__init__(*args, **kwargs)

        self.db_mgr = DATABASE_MGR
        self.studentListDropDown = CustomDropDown()
        self.studentStatsDropDown = CustomDropDown()
        self.AllLoginCredentialList = {}
        self.studentStatsList = {}
        self.studentIDClassDict = {}
        self.classHourDict = {}
        self.entireClassHours = 0
        try:
            self.AllLoginCredentialList = self.db_mgr.getAllLoginCredentials()
        except:
            KREATDEBUG("TeacherLandingScreen: Failed to get all login credentials!")
        else:
            if(self.AllLoginCredentialList is not None):
                for item in self.AllLoginCredentialList:
                    if(self.AllLoginCredentialList[item]['Type'] == STUDENT):
                        self.studentIDClassDict[item] = self.AllLoginCredentialList[item]['Class']
                        if(self.classHourDict.get(self.AllLoginCredentialList[item]['Class']) is None):
                            self.classHourDict[self.AllLoginCredentialList[item]['Class']] = 0
                        btn = Button(text=self.AllLoginCredentialList[item]['Name'], id=item, size_hint_y=None, height=44)
                        btn.bind(on_release=lambda btn: self.studentListDropDown.select(btn.text))
                        btn.bind(on_release=lambda btn: self.updateScreenProfileFields(btn.id))
                        self.studentListDropDown.add_widget(btn)


        self.ids.studentListButton.bind(on_release=self.studentListDropDown.open)
        self.studentListDropDown.bind(on_select=lambda instance, x: setattr(self.ids.studentListButton, 'text', x))

        self.studentStatsDropDown.clear_widgets()
        self.entireClassHours = self.getEntireClassTotalHours()
            
    def on_enter(self):
        self.ids.studentName.text = ""
        self.ids.studentClass.text = ""
        self.ids.studentSchool.text = ""

        self.ids.authorName.text = ""
        self.ids.bookGenre.text = ""
        self.ids.readingHours.text = ""
        self.studentStatsDropDown.clear_widgets()
        self.ids.studentListButton.text = "Select Student"
        self.ids.studentStatsListButton.text = "Select Statistics Entry"
        self.ids.totalHoursLabel.text = "Total Hours:"
        self.ids.classStandingLabel.text = "Class Standing (out of 10):"
        
    def onUpdateTeacherAccountPress(self):
        setScreenNames('TeacherLandingScreen')
        screen_manager.current = 'UpdateAccountScreen'
        KREATDEBUG("onUpdateTeacherAccountPress: Switching to update account screen!")

    def updateScreenProfileFields(self, student_email):
        KREATDEBUG("updateScreenProfileFields: updating screen for " + student_email)

        lcl_text = ""
        lcl_total_hours = 0
        lcl_class_standing = 10
        self.ids.studentName.text = self.AllLoginCredentialList[student_email]['Name']
        self.ids.studentClass.text = self.AllLoginCredentialList[student_email]['Class']
        self.ids.studentSchool.text = self.AllLoginCredentialList[student_email]['School']

        try:
            self.studentStatsList = self.db_mgr.getUserStatistics(student_email)
        except:
            KREATDEBUG("TeacherLandingScreen: failed to read student statistics!")
        else:
            self.studentStatsDropDown.clear_widgets()
            self.ids.studentStatsListButton.text = "Select Statistics Entry"
            self.ids.authorName.text = ""
            self.ids.bookGenre.text = ""
            self.ids.readingHours.text = ""
            if(self.studentStatsList is not None):
                for item in self.studentStatsList:
                    lcl_text = self.studentStatsList[item]['Title'] + "," + self.studentStatsList[item]['Date'] + "," + self.studentStatsList[item]['Start Time']
                    lcl_total_hours = lcl_total_hours + float(self.studentStatsList[item]['Hours'])
                    btn = Button(text=lcl_text, id=item, size_hint_y=None, height=44)
                    btn.bind(on_release=lambda btn: self.studentStatsDropDown.select(btn.text))
                    btn.bind(on_release=lambda btn: self.updateScreenStatsFields(btn.id))
                    self.studentStatsDropDown.add_widget(btn)
                

        self.ids.studentStatsListButton.bind(on_release=self.studentStatsDropDown.open)
        self.studentStatsDropDown.bind(on_select=lambda instance, x: setattr(self.ids.studentStatsListButton, 'text', x))
                        
        self.ids.totalHoursLabel.text = ("Total Hours: %0.2f" %(lcl_total_hours))
        if(self.entireClassHours is not 0) and (self.entireClassHours is not None):
            lcl_class_standing = int((lcl_total_hours / self.entireClassHours) *10)
        self.ids.classStandingLabel.text = ("Class Standing (out of 10): %d" %(lcl_class_standing))
        
    def updateScreenStatsFields(self, unique_id):
        if(self.studentStatsList is not None):
            self.ids.authorName.text = self.studentStatsList[unique_id]['Author']
            self.ids.bookGenre.text = self.studentStatsList[unique_id]['Genre']
            self.ids.readingHours.text = ("%0.2f" %(self.studentStatsList[unique_id]['Hours']))


    def getEntireClassTotalHours(self):
        lcl_total_class_hours = 0
        lcl_stat_list = {}
        if(self.studentIDClassDict is not None) and (self.classHourDict is not None):
            for student_id in self.studentIDClassDict.keys():
                try:
                    lcl_total_class_hours = 0
                    lcl_stat_list = self.db_mgr.getUserStatistics(student_id)
                except:
                    KREATDEBUG("getEntireClassTotalHours: failed to get statistics for " + str(student_id))
                    continue
                else:
                    if(lcl_stat_list is not None):
                        for item in lcl_stat_list:
                            lcl_total_class_hours = lcl_total_class_hours + float(lcl_stat_list[item]['Hours']) 
                        self.classHourDict[self.studentIDClassDict[student_id]] = self.classHourDict[self.studentIDClassDict[student_id]] + lcl_total_class_hours
        KREATDEBUG("Total Hours For Entire Class %f" %(self.classHourDict[self.studentIDClassDict[student_id]]))
        return(self.classHourDict[self.studentIDClassDict[student_id]])
                
        
    def onRefreshTeacherAccountButtonPress(self):
        self.ids.studentName.text = ""
        self.ids.studentClass.text = ""
        self.ids.studentSchool.text = ""

        self.ids.authorName.text = ""
        self.ids.bookGenre.text = ""
        self.ids.readingHours.text = ""
        self.studentStatsDropDown.clear_widgets()
        self.ids.studentListButton.text = "Select Student"
        self.ids.studentStatsListButton.text = "Select Statistics Entry"
        self.studentIDClassDict = {}
        self.classHourDict={}
        self.ids.totalHoursLabel.text = "Total Hours:"
        self.ids.classStandingLabel.text = "Class Standing (out of 10):"
        try:
            self.AllLoginCredentialList = self.db_mgr.getAllLoginCredentials()
        except:
            KREATDEBUG("TeacherLandingScreen: Failed to get all login credentials!")
        else:
            self.studentListDropDown.clear_widgets()
            for item in self.AllLoginCredentialList:
                if(self.AllLoginCredentialList[item]['Type'] == STUDENT):
                    self.studentIDClassDict[item] = self.AllLoginCredentialList[item]['Class']
                    if(self.classHourDict.get(self.AllLoginCredentialList[item]['Class']) is None):
                        self.classHourDict[self.AllLoginCredentialList[item]['Class']] = 0
                    btn = Button(text=self.AllLoginCredentialList[item]['Name'], id=item, size_hint_y=None, height=44)
                    btn.bind(on_release=lambda btn: self.studentListDropDown.select(btn.text))
                    btn.bind(on_release=lambda btn: self.updateScreenProfileFields(btn.id))
                    self.studentListDropDown.add_widget(btn)

        self.entireClassHours = self.getEntireClassTotalHours()
        
#UpdateAccount screen class
class UpdateAccountScreen(Screen):
    def __init__(self, *args, **kwargs):
        super(UpdateAccountScreen, self).__init__(*args, **kwargs)

        self.db_mgr = DATABASE_MGR

    def on_enter(self):
        self.ids.login.text = ""
        self.ids.password.text = ""
        
    def onUpdateAccountButtonPress(self):
        loginSuccessful = False
        #Check for format
        loginSuccessful = validateEmail(self.ids.login.text.strip())
        if(loginSuccessful == False):
            p = CustomPopup()
            p.setTitle("Email Id Format Incorrect")
            p.open()
        else:
            loginSuccessful = validateString(self.ids.password.text.strip())
            if(loginSuccessful == False):
                p = CustomPopup()
                p.setTitle("Password empty!")
                p.open()
            else:
                #Update password
                if(self.db_mgr.updateUserPassword(self.ids.login.text.strip(),self.ids.password.text.strip()) == True):
                    p = CustomPopup()
                    p.setTitle("Your Password Has Been Updated Successfully!")
                    p.open()
                    sendMyEmail(PASS_CHANGE_SUBJECT, PASS_CHANGE_MSG, self.ids.login.text.strip())
                    self.ids.login.text = ""
                    self.ids.password.text = ""
                    screen_manager.current = 'LoginScreen'
                    KREATDEBUG("onUpdateAccountButtonPress: Switching to login screen!")                    
                else:
                    p = CustomPopup()
                    p.setTitle("Failed To Update Your Password. Re-try With Correct Email Id Or Call Help Desk!")
                    p.open()


    def onCancelUpdateAccountButtonPress(self):
        screen_manager.current = getScreenNames()
            
#LoggingHour screen class
class LoggingHourScreen(Screen):
    def __init__(self, *args, **kwargs):
        super(LoggingHourScreen, self).__init__(*args, **kwargs)

        self.db_mgr = DATABASE_MGR
        self.bookGenreDropDown = CustomDropDown()
        self.bookGenreList = getGenreFromFile()
        self.bookGenreListRead = False
        if(not self.bookGenreList):
            KREATDEBUG('LoggingHourScreen: failed to reade genre list from file')
        else:
            self.bookGenreListRead = True
            for genre_value in self.bookGenreList:
                btn = Button(text=str(genre_value), size_hint_y=None, height=44)
                btn.bind(on_release=lambda btn: self.bookGenreDropDown.select(btn.text))
                self.bookGenreDropDown.add_widget(btn)
        self.ids.bookGenreListButton.bind(on_release=self.bookGenreDropDown.open)
        self.bookGenreDropDown.bind(on_select=lambda instance, x: setattr(self.ids.bookGenreListButton, 'text', x))

    def on_enter(self):
        self.ids.bookauthor.text = ""
        self.ids.booktitle.text = ""
        self.ids.starttime.text = ""
        self.ids.endtime.text = ""
        self.ids.calchours.text = ""
        if(self.bookGenreListRead == True):
            self.ids.bookGenreListButton.text = 'Select'
        else:
            self.ids.bookGenreListButton.text = 'Other'            
        
    def onUpdateLogButtonPress(self):
        lcl_calc_hours = 0
        lcl_flag = False
        lcl_flag = (validateString(self.ids.bookauthor.text.strip()) == True) and (validateString(self.ids.booktitle.text.strip()) == True) and (validateString(self.ids.starttime.text.strip()) == True) and (validateString(self.ids.endtime.text.strip()) == True) and (self.ids.bookGenreListButton.text.strip() != 'Select')
        if(lcl_flag == False):
            p = CustomPopup()
            p.setTitle("One Or More Entries Empty. Please Enter Correctly!")
            p.open()
        else:
            if(validateTimeFormat(self.ids.starttime.text.strip()) == False) or (validateTimeFormat(self.ids.endtime.text.strip()) == False):
                p = CustomPopup()
                p.setTitle("Time Format Incorrect. Please Enter Correctly!")
                p.open()
            else:
                lcl_calc_hours = getTimeDiffInHours(self.ids.starttime.text.strip(),self.ids.endtime.text.strip())
                self.ids.calchours.text = ("%0.2f" %(lcl_calc_hours))
                self.updateLogginStatistics(getUserID(), self.ids.booktitle.text.strip(),self.ids.bookauthor.text.strip(),self.ids.bookGenreListButton.text.strip(),todayDate(),self.ids.starttime.text.strip(),self.ids.endtime.text.strip(),lcl_calc_hours)

    def updateLogginStatistics(self, email_id, book_title, book_author, book_genre, reading_date, start_time, end_time, calc_hours):
        try:
            self.db_mgr.uploadUserStatistics(email_id, book_title, book_author, book_genre, reading_date, start_time, end_time, calc_hours)
        except:
            KREATDEBUG("updateLogginStatistics: failed to upload logging statistics!")
        else:
            KREATDEBUG("updateLogginStatistics: uploaded logging statistics!")
            p = CustomPopup()
            p.setTitle("Successfully Uploaded Reading Hours!")
            p.open()
            sendMyEmail(READING_HOURS_LOGGED_SUBJECT, READING_HOURS_LOGGED_MSG, getUserID())

        
    def onCancelLoggingButtonPress(self):
        screen_manager.current = getScreenNames()


    def onStartTimeTextEntered(self):
        if(validateTimeFormat(self.ids.starttime.text.strip()) == True) and (validateTimeFormat(self.ids.endtime.text.strip()) == True):
            lcl_calc_hours = getTimeDiffInHours(self.ids.starttime.text.strip(),self.ids.endtime.text.strip())
            self.ids.calchours.text = ("%0.2f" %(lcl_calc_hours))

    def onEndTimeTextEntered(self):
        if(validateTimeFormat(self.ids.starttime.text.strip()) == True) and (validateTimeFormat(self.ids.endtime.text.strip()) == True):
            lcl_calc_hours = getTimeDiffInHours(self.ids.starttime.text.strip(),self.ids.endtime.text.strip())
            self.ids.calchours.text = ("%0.2f" %(lcl_calc_hours))
        
# Set window size
Window.size = (WINDOW_WIDTH, WINDOW_HEIGHT)
Window.top = 10
Window.left = 10
Window.clearcolor = (0.136, 0.191, 0.25, 1)
Window.minimum_height = WINDOW_HEIGHT
Window.minimum_width = WINDOW_WIDTH 

# Get handle to database
global DATABASE_MGR
DATABASE_MGR = realTimeDB()

# The ScreenManager controls moving between screens
screen_manager = ScreenManager()
 
# Add the screens to the manager and then supply a name
# that is used to switch screens
screen_manager.add_widget(UserSelectScreen(name="UserSelectScreen"))
screen_manager.add_widget(LoginScreen(name="LoginScreen"))
screen_manager.add_widget(CreateUserScreen(name="CreateUserScreen"))
screen_manager.add_widget(TeacherLandingScreen(name="TeacherLandingScreen"))
screen_manager.add_widget(StudentLandingScreen(name="StudentLandingScreen"))
screen_manager.add_widget(UpdateAccountScreen(name="UpdateAccountScreen"))
screen_manager.add_widget(LoggingHourScreen(name="LoggingHourScreen"))

 
class KREATApp(App):
 
    def build(self):
        return screen_manager
 
kreat_app = KREATApp()
kreat_app.run()
