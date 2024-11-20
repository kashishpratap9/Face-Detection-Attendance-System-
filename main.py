import os.path
import subprocess
import tkinter as tk
import tempfile
import datetime
import cv2
print(cv2.__version__)
from PIL import Image
from PIL import ImageTk
import util


class App:
    def __init__(self):
        self.main_window = tk.Tk()
        #window
        self.main_window.geometry("1200x520+250+100")
        #button/button_location
        self.login_button_main_window= util.getbutton(self.main_window,'login','green',self.login)
        self.login_button_main_window.place(x=750, y=300)
        self.register_new_user_button_main_window = util.getbutton(self.main_window, 'register new user', 'grey', self.register_new_user, fg='black')
        self.register_new_user_button_main_window.place(x=750, y=400)
        self.webcam_label=util.get_img_label(self.main_window)
        self.webcam_label.place(x=10, y=0, width=700, height=500)
        self.add_webcam(self.webcam_label)

        self.db_dir='C:/Users/kashish pratap/PycharmProjects/FaceRecoginitationSystem/Attendance'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)
        self.log_path= 'C:/Users/kashish pratap/PycharmProjects/FaceRecoginitationSystem/log.txt'

    def add_webcam(self, label):
        if 'cap' not in self.__dict__:
             self.cap=cv2.VideoCapture(1) # 2 for external webcam
        self.label_=label
        self.process_webcam()
        # read frame from the webcam


    def process_webcam(self):
        ret, frame = self.cap.read()
        self.most_recent_capture_arr= frame

        img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)
        self. most_recent_capture_pil=Image.fromarray(img_)

        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)

        self.label_.imgtk = imgtk
        self.label_.configure(image=imgtk)

        self.label_.after(20, self.process_webcam)

    def login(self):
        temp_dir = tempfile.gettempdir()
        unknown_img_path = os.path.join(temp_dir, 'unknown.jpg')
        #logic for face recgonition
        cv2.imwrite(unknown_img_path,  self.most_recent_capture_arr)
        output=str(subprocess.check_output(['face_recognition', self.db_dir ,unknown_img_path]))

        name=output.split(',')[1][:-5]
        print(name)

        if name in ['unknown_person' , 'no_persons_found']:
            util.msg_box('Ups...','Unknown user,.Please register new user or Try again')
        else:
            util.msg_box('Welcome Back !', 'Welcome,' f'{name}.jpg')
            with open(self.log_path, 'a') as f:
                f.write('{} {}\n'.format(name, datetime.datetime.now()))
                f.close()




        os.remove(unknown_img_path)


    def register_new_user(self):
        self.register_new_user_window = tk.Toplevel(self.main_window)
        self.register_new_user_window.geometry("1200x520+270+100")  # Set geometry for the secondary window
        self.register_new_user_window.title("Register New User")

        self.accept_button_register_new_user_window = util.getbutton(self.register_new_user_window, 'Accept', 'green', self.accept_register_new_user_window)
        self.accept_button_register_new_user_window .place(x=750, y=300)

        self.tryagain_button_register_new_user_window = util.getbutton(self.register_new_user_window, 'Try Again', 'red',self.tryagain_register_new_user, fg='black')
        self.tryagain_button_register_new_user_window .place(x=750, y=400)

        self.capture_label = util.get_img_label(self.register_new_user_window)
        self.capture_label.place(x=10, y=0, width=700, height=500)

        self.add_img_to_label(self.capture_label)


        self.entry_text_register_new_user= util.get_entry_text(self.register_new_user_window)
        self.entry_text_register_new_user.place(x=750, y=150)

        self.text_label_register_new_user=util.get_text_label(self.register_new_user_window, "Please,input username")
        self.text_label_register_new_user.place(x=750, y=150)
    def add_img_to_label(self,label):
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        label.imgtk = imgtk
        label.configure(image=imgtk)
        self.register_new_user_capture= self.most_recent_capture_arr.copy()

    def accept_register_new_user_window(self):
        # name =self.entry_text_register_new_user.get(1.0,"end-1c")
        # cv2.imwrite(os.path.join(self.db_dir,'{}.jpg'.format(name)), self.register_new_user_capture)
        name = self.entry_text_register_new_user.get(1.0, "end-1c").strip()
        if self.register_new_user_capture is not None and name:
            cv2.imwrite(os.path.join(self.db_dir, f'{name}.jpg'), self.register_new_user_capture)
            util.msg_box("Success", "User was register successfully")

        else:
            print("No image captured or username is empty.")

        self.register_new_user_window.destroy()

    def tryagain_register_new_user(self):
        self.register_new_user_window.destroy()

    def start(self):
        self.main_window.mainloop()


if __name__ == "__main__":
    app = App()
    app.start()
