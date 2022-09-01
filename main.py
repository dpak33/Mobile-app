from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import json, glob
# See video 249 for use of terminal to import path to textfiles
from datetime import datetime
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from pathlib import Path
import random
import smtplib
from Hoverable import HoverBehavior




Builder.load_file('design.kv')
# In our python script, we create empty classes with the same name as the roots in our design.kv file.

class LoginScreen(Screen):
    def sign_up(self):
        self.manager.current = 'sign_up_screen'
        # manager above is a property of Screen - the parent -, which is inherited from Screen when fed into child
        # LoginScreen class.
    def password_unknown(self):
        self.manager.current = 'forgot_password_screen'

    def login(self, uname, pword):
 # We need to open and verify relevant json file to see if user present. The
# information is contained in a large dictionary of keys and values.
        with open('users.json') as file:
            users = json.load(file)
     # You can call the dictionary value using the below keys as indices:
        if uname in users and users[uname]['password'] == pword:
            self.manager.current = 'login_screen_success'
        else:
            self.ids.login_wrong.text = 'Wrong username or password!'



#Because the rootwidget keeps a record of all the screens in the app, it inherits ScreenManager as a parameter
class RootWidget(ScreenManager):
    pass

# The below class needs to be created as SignUpScreen is not a class in the kivi library, so needs to exist
# as a python file in order to be instantiated in the rootwidget of the design.kv file.
class SignUpScreen(Screen):
    def add_user(self, uname, pword):
        with open('users.json') as file:
            users = json.load(file)
        # We create a template dictionary in the user.json file
        # and when the user enters their input, the json file will
        # format that input according to the template and it will become
        # visible in the terminal. We need to add further values as below
        # to upload user data. We import datetime and pre-convert to string.
        users[uname] = {'username': uname, 'password': pword,
                        'created': datetime.now().strftime('%Y-%m-%d %H-%M-%S')}
        with open('users.json', 'w') as file:
            json.dump(users,file)
# The json. dumps() method allows us to convert a python object into an
# equivalent JSON object. Or in other words to send the data from python to
# json at the working directory.
        self.manager.current = 'sign_up_screen_success'
# Notice the above is replicated at the rootwidget and in main kivi design code
# and in a relevant class below.

class ForgotPasswordScreen(Screen):
    def change_password(self, user_name, new_pass):
        with open("users.json") as file:
            users = json.load(file)
        users[user_name] = {'username': user_name, 'password': new_pass,
                            'created': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

        if users[user_name]['username'] == user_name:
            with open("users.json", "w") as file:
                users[user_name]['password'] = new_pass
                json.dump(users, file)
            self.ids.password_status.text = "Password changed successfully"
            import time
            time.sleep(1)
            self.manager.current = "login_screen"
        else:
            self.ids.password_status.text = "Try Again"






class SignUpScreenSuccess(Screen):
    def revert_to_main(self):
#So that when you press the login button, it will send you back to original scr.
# We can change direction of screen shuffle using self.manager.transition.direction = 'right
        self.manager.current = 'login_screen'

class LoginScreenSuccess(Screen):
    def log_out(self):
        self.manager.current = 'login_screen'

    def get_quote(self, philosopher):
        philosopher = philosopher.lower()
# The inbuilt glob module below accesses text from the
# relevant quotes files.
        available_quotes = glob.glob('quotes/*txt')
 # We use a list comprehension to iterate through the quotes folder.
        available_quotes = [Path(filename).stem for filename in available_quotes]
        if philosopher in available_quotes:
            with open(f'quotes/{philosopher}.txt') as file:
                quotes = file.readlines()
# Once we have the quotes, we can share them with our
# enlightenme button label in LoginScreenSuccess
            self.ids.quote.text = random.choice(quotes)
        else:
            self.ids.quote.text = 'Please try one of the options given.'

    def get_bio(self, philosopher):
        philosopher = philosopher.lower()
        available_bios = glob.glob('biographies/*txt')
        available_bios = [Path(filename).stem for filename in available_bios]
        if philosopher in available_bios:
            with open(f'biographies/{philosopher}.txt') as file:
                biographies = file.readlines()
            self.ids.biography.text = random.choice(biographies)
        else:
            self.ids.biography.text = 'Please try one of the options given.'

class MainApp(App):
    def build(self):
        return RootWidget()
    # We are returning the RootWidget object rather than the class.

# ImageButton inherits from other classes below:
class ImageButton(ButtonBehavior, HoverBehavior, Image):
    pass


if __name__ == '__main__':
    MainApp().run()