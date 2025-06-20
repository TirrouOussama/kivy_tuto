from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.properties import (
    StringProperty,
    ObjectProperty,
    NumericProperty,
    ReferenceListProperty,
    ListProperty,
)
from kivy.graphics import Rectangle, Color, Line, Bezier, Ellipse, Triangle
from kivy.utils import platform
from kivy.core.window import Window
import threading
import re
import time
import sqlite3

from supperwidget.suppertextinput import SupperTextinput

Builder.load_file("supperwidget/suppertextinput.kv")

from supperwidget.supperbutton import SupperButton

Builder.load_file("supperwidget/supperbutton.kv")

from supperwidget.supperlabel import SupperLabel

Builder.load_file("supperwidget/supperlabel.kv")


Window.size = (608, 1080)  ##### delete this if u package for mobile

login_catch = ""


######################### Detached threads
def try_login(ml, ps, mc):
    global login_catch
    print("called")
    time.sleep(3)

    login_catch = "Valid_log"
    # login_catch = "Whatever to simulate"
    # login_catch ......

    ## login_catch = http
    ## login_catch = sockets
    ## depends on how u want to send and rcv


######################### Detached threads end


class initialscreen(Widget):
    l01_angle = NumericProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.l01_angle = 0

    def on_size(self, *args):
        if self.width > 100:
            self.ids.l01.pos[0] = (self.width * 0.5) - 32
            Clock.schedule_interval(self.loading, 1 / 30)
            self.ids.lock.pos[0] = 0
            theapp.access_screen.login("Saved")

    def loading(self, *args):
        if self.l01_angle < 360:
            self.l01_angle += 10

        if self.l01_angle >= 360:
            self.l01_angle = 0

    def stop_loading(self):
        Clock.unschedule(self.loading)
        self.ids.lock.pos[0] = self.width * 1.1


class access_screen(Widget):
    l01_angle = NumericProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.login_timeout = 0
        self.l01_angle = 0

    def loading(self, *args):
        if self.l01_angle < 360:
            self.l01_angle += 10

        if self.l01_angle >= 360:
            self.l01_angle = 0

    def stop_loading(self):
        Clock.unschedule(self.loading)
        self.ids.lock.pos[0] = self.width * 1.1

    def check_creds(self, ml, ps):
        if ml != None and ps != None:
            if re.match(
                r"""^(?:[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+
                (?:\.[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+)*|
                "(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|
                \\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@
                (?:(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?\.)+
                [a-zA-Z]{2,}|localhost)$""",
                ml,
                re.VERBOSE,
            ):
                if (
                    any(c.islower() for c in ps)
                    and any(c.isupper() for c in ps)
                    and any(c.isdigit() for c in ps)
                    and re.search(r"[^\w]", ps)
                ):
                    return True

                else:
                    self.ids.login_error_lbl.text = "Password Format is Wrong"
                    return False

            else:
                self.ids.login_error_lbl.text = "Email Format is Wrong"
                return False

        else:
            return False

    def login(self, with_what):
        if with_what == "input":
            Clock.schedule_interval(self.loading, 1 / 30)
            self.ids.lock.pos[0] = 0

            print("called with input")
            res = self.check_creds(self.ids.log_mail.text, self.ids.log_pass.text)
            if res == True:
                # use hashlib to hash password or all data
                self.call_thread(
                    self.ids.log_mail.text, self.ids.log_pass.text, theapp.mac
                )

            elif res == False:
                pass

        #############################################
        elif with_what == "Saved":
            print("called with Saved")
            res = self.fetch_saved_creds()
            if res != None:
                print("diff than None")
                if res[0][3] == 1:  # 1 for remember me 0 for not remembering
                    # use hashlib to hash password or all data
                    self.call_thread(res[0][0], res[0][2], res[0][1])

                elif res[0][3] == 0:
                    print("remember", res[0][3])
                    theapp.screenm.current = "access_screen"

            elif res == None:
                print("Equal to None")
                theapp.screenm.current = "access_screen"

    def call_thread(self, ps, ml, mc):
        self.ids.login_error_lbl.text = ""
        Clock.schedule_interval(self.wait_login, 0.2)
        self.login_timeout = 0
        attempt = threading.Thread(
            target=try_login,
            args=(ml, ps, theapp.mac),
        )
        attempt.start()

    def wait_login(self, *args):
        global login_catch
        print(login_catch)
        if self.login_timeout < 75:  ## 0.2 * 72  = 15 sec timeout
            if login_catch != "":
                if login_catch == "Account Does Not Exist":
                    self.ids.login_error_lbl.text = login_catch
                    Clock.unschedule(self.wait_login)
                    theapp.initialscreen.stop_loading()
                    self.stop_loading()

                elif login_catch == "Password Wrong":
                    self.ids.login_error_lbl.text = login_catch
                    Clock.unschedule(self.wait_login)
                    theapp.initialscreen.stop_loading()
                    self.stop_loading()  ## this is repitive u
                    ## type more to avoid this

                elif login_catch == "Valid_log":
                    theapp.global_email = self.ids.log_mail.text
                    theapp.global_pass = self.ids.log_pass.text
                    self.ids.login_error_lbl.text = ""
                    theapp.screenm.current = "main_screen"
                    if self.ids.remember_me.active == True:
                        self.insert_saved_cred(
                            self.ids.log_mail.text,
                            theapp.mac,
                            self.ids.log_pass.text,
                            1,
                        )

                    Clock.unschedule(self.wait_login)
                    theapp.initialscreen.stop_loading()
                    self.stop_loading()

                else:
                    self.ids.login_error_lbl.text = "Something Went Wrong! Try Again"
                    Clock.unschedule(self.wait_login)

                    theapp.initialscreen.stop_loading()
                    self.stop_loading()

        elif self.login_timeout >= 75:
            self.ids.login_error_lbl.text = "Time Out Please Try Again"
            Clock.unschedule(self.wait_login)
            theapp.initialscreen.stop_loading()
            self.stop_loading()

    def create_saved_creds_db(self):
        try:
            conn = sqlite3.connect("saved_creds.db")
            cursor = conn.cursor()

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS creds (
                    email TEXT,
                    mac TEXT,
                    password TEXT,
                    remember INTEGER
                )
            """
            )

            conn.commit()
            conn.close()

        except:
            pass

    def fetch_saved_creds(self):
        try:
            conn = sqlite3.connect("saved_creds.db")
            cursor = conn.cursor()

            cursor.execute("SELECT email, mac, password, remember FROM creds")
            rows = cursor.fetchall()

            conn.close()
            return rows
        except:
            return None

    def insert_saved_cred(self, email, mac, password, remember):
        self.create_saved_creds_db()

        conn = sqlite3.connect("saved_creds.db")
        cursor = conn.cursor()

        cursor.execute("DELETE FROM creds")

        cursor.execute(
            """
            INSERT INTO creds (email, mac, password, remember)
            VALUES (?, ?, ?, ?)
        """,
            (email, mac, password, remember),
        )

        conn.commit()
        conn.close()


class main_screen(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def logout(self):
        ## u can make the same call with
        ## another outer thread to logout if u need to pass this to server
        theapp.screenm.current = "access_screen"
        theapp.access_screen.insert_saved_cred("", "", "", 0)  ## to clear saved creds


class theapp(App):
    def build(self):
        self.global_email = ""  ## these variable could be hashed and stored locally
        self.global_pass = ""  ## on the machine and could be use for further handshakes or token retrieving
        self.mac = None

        self.screenm = ScreenManager()

        self.initialscreen = initialscreen()
        screen = Screen(name="initialscreen screen")
        screen.add_widget(self.initialscreen)
        self.screenm.add_widget(screen)

        self.access_screen = access_screen()
        screen = Screen(name="access_screen")
        screen.add_widget(self.access_screen)
        self.screenm.add_widget(screen)

        self.main_screen = main_screen()
        screen = Screen(name="main_screen")
        screen.add_widget(self.main_screen)
        self.screenm.add_widget(screen)

        return self.screenm

    def on_start(self):
        self.get_mac()

    def get_mac(self):
        from plyer import uniqueid

        try:
            mac = uniqueid.id
            if mac:
                self.mac = mac  # m getting this on start u could avoid this logic
                return mac
        except:
            ### the app shoud exit if u dont retrieve it also we not checking
            print("Couldn't Retrieve Mac Adress")


if __name__ == "__main__":
    theapp = theapp()
    theapp.run()
