from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from dd_email import DailyDigestEmail
from dd_scheduler import DailyDigestScheduler
from dd_content import engine
import pandas as pd
import config




class DailyDigest:
    global value

    def __init__(self, root, top):

        # ************************************************** ROOT WINDOW **************************************************
        self.__root = root
        # self.__root.resizable(width=FALSE, height=FALSE)
        self.__root.title("Daily Digest")
        title_label = ttk.Label(
            self.__root,
            text=" \U0001F4DC TREEOLIVE NEWSLETTER \U0001F4DC",
            font="Algerian 32 bold",
            justify=CENTER,
        )
        title_label.pack(padx=5, pady=5)

        self.__style = ttk.Style()
        self.__style.configure("TButton", font=("Arial", 12, "bold"))
        self.__style.configure("Header.TLabel", font=("Arial", 18, "bold"))

        tabControl = ttk.Notebook(root)

        tab1 = ttk.Frame(tabControl)
        tab2 = ttk.Frame(tabControl)

        tabControl.add(tab1, text="Daily Digest")
        # tabControl.add(tab2, text="Make Announcement")
        tabControl.pack(expand=1, fill="both")

        # TODO: GUI listbox for recipients
        recipients_frame = ttk.Frame(tab1)
        recipients_frame.pack(padx=5, pady=5)
        self.__add_recipient_var = StringVar()
        self.__recipient_list_var = Variable()
        self.__build_gui_recipients(
            recipients_frame, self.__add_recipient_var, self.__recipient_list_var
        )

        # TODO: GUI elements to schedule delivery time
        schedule_frame = ttk.Frame(tab1)
        schedule_frame.pack(padx=5, pady=5)
        self.__hour_var = StringVar()
        self.__minute_var = StringVar()
        self.__build_gui_schedule(schedule_frame, self.__hour_var, self.__minute_var)

        # TODO: GUI checkboxes of content to include in email
        contents_frame = ttk.Frame(tab1)
        contents_frame.pack(padx=5, pady=5)
        self.__verse_var = IntVar()
        self.__weather_var = IntVar()
        self.__devotions_var = IntVar()
        self.__wikipedia_var = IntVar()
        self.__build_gui_contents(
            contents_frame,
            self.__verse_var,
            self.__weather_var,
            self.__devotions_var,
            self.__wikipedia_var,
        )

        # TODO: GUI fields for sender email/password credentials
        sender_frame = ttk.Frame(tab1)
        sender_frame.pack(padx=5, pady=5)
        self.__sender_email_var = StringVar()
        self.__sender_password_var = StringVar()
        self.__build_gui_sender(
            sender_frame, self.__sender_email_var, self.__sender_password_var
        )

        # TODO: GUI field for controls
        controls_frame = ttk.Frame(tab1)
        controls_frame.pack(padx=5, pady=5)
        self.__build_gui_controls(controls_frame)

        # TODO: set initial values for variables
        self.__email = DailyDigestEmail()

        self.__add_recipient_var.set("")
        self.__recipient_list_var.set(self.__email.recipients_list)

        self.__hour_var.set("07")  # defaul send time
        self.__minute_var.set("30")

        self.__verse_var.set(self.__email.content["verse"]["include"])
        self.__weather_var.set(self.__email.content["weather"]["include"])
        self.__devotions_var.set(self.__email.content["devotions"]["include"])
        self.__wikipedia_var.set(self.__email.content["wikipedia"]["include"])

        self.__sender_email_var.set(self.__email.sender_credentials["email"])
        self.__sender_password_var.set(self.__email.sender_credentials["password"])

        # TODO: GUI textbox for making announcement
        announcement_frame = ttk.Frame(tab2)
        announcement_frame.pack(padx=5, pady=5)
        self.__lbl = ttk.Label(tab2, text="")
        self.__lbl.pack()
        self.__build_gui_announcement(announcement_frame)
        self.__input_announcement = inputtxt.get(1.0, "end-1c")

        # TODO: initialize scheduler
        self.__scheduler = DailyDigestScheduler()
        self.__scheduler.start()
        self.__root.protocol(
            "WM_DELETE_WINDOW", self.__shutdown
        )  # shuts down the scheduler

        # ************************************************** LOGIN WINDOW **************************************************

        self.__top = top
        self.__top.title("Login")
        self.__top.geometry("800x400+300+150")
        self.__top.resizable(width=FALSE, height=FALSE)

        login_frame = ttk.Frame(self.__top)
        login_frame.pack(padx=5, pady=5)
        self.__input_name_var = StringVar()
        self.__input_password_var = StringVar()
        self.__build_gui_login(
            login_frame, self.__input_name_var, self.__input_password_var
        )
        self.__top.protocol("WM_DELETE_WINDOW", self.__shutdown)

    """
    Build GUI elements to for making announcements 
    """

    def __build_gui_announcement(self, master):
        # TODO: create GUI widgets
        header = ttk.Label(master, text="Announce to members:", style="Header.TLabel")
        spacer_frame = ttk.Frame(master)
        global inputtxt
        inputtxt = Text(master, height=20, width=60)
        sendbutton = ttk.Button(
            master, text="Send", command=lambda: self.__post_announcement()
        )

        # TODO: place GUI widgets using grid geometry manager
        header.grid(row=0, column=0)
        inputtxt.grid(row=1, column=0)
        spacer_frame.grid(row=2, column=0, pady=5)
        sendbutton.grid(row=4, column=0)

    # ********************* LOGIN WINDOW METHODS
    """
    Build GUI elements to for inputting login username and password 
    """

    def __build_gui_login(self, master, input_name_var, input_password_var):
        # TODO: create GUI widgets
        header = ttk.Label(master, text="Login", style="Header.TLabel", justify=CENTER)
        spacer_frame_1 = ttk.Frame(master)  # used as GUI spacer
        spacer_frame_2 = ttk.Frame(master)
        name_label = ttk.Label(master, text="Username")
        password_label = ttk.Label(master, text="Password")

        name_entry = ttk.Entry(master, width=40, textvariable=input_name_var)
        password_entry = ttk.Entry(
            master, width=40, show="*", textvariable=input_password_var
        )
        login_btn = ttk.Button(
            master, text="sign in", command=lambda: self.__validate_login()
        )
        login_btn.place(x=50, y=200)
        cancel_btn = ttk.Button(
            master, text="cancel", command=lambda: self.__shutdown()
        )
        # TODO: place GUI widgets using grid geometry manager
        header.grid(row=0, padx=5, pady=5)
        name_label.grid(row=4, column=0)
        name_entry.grid(row=4, column=1)
        spacer_frame_1.grid(row=5, column=0, pady=5)
        password_label.grid(row=6, column=0)
        password_entry.grid(row=6, column=1)
        spacer_frame_2.grid(row=7, column=0, pady=5)
        login_btn.grid(row=8, column=0)
        cancel_btn.grid(row=8, column=1)

    # ********************* ROOT WINDOW METHODS

    """
    Build GUI elements to add/remove recipients 
    """

    def __build_gui_recipients(self, master, add_recipient_var, recipient_list_var):
        # TODO: create GUI widgets
        header = ttk.Label(master, text="Recipients:", style="Header.TLabel")
        spacer_frame = ttk.Frame(master)
        recipients_entry = ttk.Entry(master, width=40, textvariable=add_recipient_var)
        recipients_scrollbar = ttk.Scrollbar(master, orient=VERTICAL)
        recipients_scrollbar.grid(row=4, column=1, sticky=N + S + W + E)
        recipients_listbox = Listbox(
            master,
            listvariable=recipient_list_var,
            selectmode="multiple",
            width=40,
            height=5,
        )
        recipients_listbox.configure(yscrollcommand=recipients_scrollbar.set)
        recipients_scrollbar.config(command=recipients_listbox.yview)

        add_button = ttk.Button(
            master, text="Add Recipient", command=self.__add_recipient
        )
        remove_button = ttk.Button(
            master,
            text="Remove Selected",
            command=lambda: self.__remove_selected_recipients(
                recipients_listbox.curselection()
            ),
        )

        # TODO: place GUI widgets using grid geometry manager
        header.grid(row=0, column=0)
        recipients_entry.grid(row=1, column=0)
        add_button.grid(row=2, column=0)
        spacer_frame.grid(row=3, column=0, pady=5)
        recipients_listbox.grid(row=4, column=0)
        remove_button.grid(row=5, column=0)

    """
    Build GUI elements to schedule send time
    """

    def __build_gui_schedule(self, master, hour_var, minute_var):
        # TODO: create GUI widgets
        header = ttk.Label(master, text="Scheduled Time (24hr):", style="Header.TLabel")
        hour_spinbox = ttk.Spinbox(
            master,
            from_=0,
            to=23,
            textvariable=hour_var,
            wrap=True,
            width=3,
            justify=CENTER,
            font="Arial 12",
        )
        minute_spinbox = ttk.Spinbox(
            master,
            from_=0,
            to=59,
            textvariable=minute_var,
            wrap=True,
            width=3,
            justify=CENTER,
            font="Arial 12",
        )
        # TODO: place GUI widgets using grid geometry manager
        header.grid(row=0, column=0, columnspan=2)
        hour_spinbox.grid(row=1, column=0, sticky=E, padx=2, pady=5)
        minute_spinbox.grid(row=1, column=1, sticky=W, padx=2, pady=5)

    """
    Build GUI elements to select content to include
    """

    def __build_gui_contents(
        self, master, verse_var, weather_var, devotions_var, wikipedia_var
    ):
        # TODO: create GUI widgets
        header = ttk.Label(master, text="Digest Contents:", style="Header.TLabel")
        verse_checkbox = ttk.Checkbutton(
            master, text="Daily Verse", onvalue=True, offvalue=False, variable=verse_var
        )
        weather_checkbox = ttk.Checkbutton(
            master,
            text="Weather Forecast",
            onvalue=True,
            offvalue=False,
            variable=weather_var,
        )
        devotions_checkbox = ttk.Checkbutton(
            master,
            text="Day's lesson",
            onvalue=True,
            offvalue=False,
            variable=devotions_var,
        )
        wikipedia_checkbox = ttk.Checkbutton(
            master,
            text="Wikipedia Article",
            onvalue=True,
            offvalue=False,
            variable=wikipedia_var,
        )

        # TODO: place GUI widgets using grid geometry manager
        header.grid(row=0, column=0, columnspan=2)
        verse_checkbox.grid(row=1, column=0, sticky=W)
        weather_checkbox.grid(row=2, column=0, sticky=W)
        devotions_checkbox.grid(row=1, column=1, sticky=W)
        wikipedia_checkbox.grid(row=2, column=1, sticky=W)

    """
    Build GUI elements to configure sender credentials
    """

    def __build_gui_sender(self, master, sender_email_var, sender_password_var):
        # TODO: create GUI widgets
        header = ttk.Label(master, text="Sender Credentials:", style="Header.TLabel")
        email_label = ttk.Label(master, text="Email:")
        email_entry = ttk.Entry(master, width=40, textvariable=sender_email_var)
        password_label = ttk.Label(master, text="Password:")
        password_entry = ttk.Entry(
            master, width=40, show="*", textvariable=sender_password_var
        )

        # TODO: place GUI widgets using grid geometry manager
        header.grid(row=0, column=0, columnspan=2)
        email_label.grid(row=1, column=0, pady=2, sticky=E)
        email_entry.grid(row=1, column=1, pady=2, sticky=W)
        password_label.grid(row=2, column=0, pady=2, sticky=E)
        password_entry.grid(row=2, column=1, pady=2, sticky=W)

    """
    Build GUI elements to update settings & manually send digest email
    """

    def __build_gui_controls(self, master):
        # TODO: create GUI widgets
        update_button = ttk.Button(
            master, text="Update Settings", command=self.__update_settings
        )
        send_button = ttk.Button(master, text="Manual Send", command=self.__manual_send)

        # TODO: place GUI widgets using grid geometry manager
        update_button.grid(row=0, column=0, padx=5, pady=5)
        send_button.grid(row=0, column=1, padx=5, pady=5)

    # ******************* BUTTONS

    """
    Callback function to add recipient
    """

    def __add_recipient(self):
        new_recipient = self.__add_recipient_var.get()

        if new_recipient != "":
            recipient_list = self.__recipient_list_var.get()
            if recipient_list != ("",):
                self.__recipient_list_var.set(recipient_list + (new_recipient,))
            else:
                self.__recipient_list_var.set((new_recipient,))
            self.__add_recipient_var.set("")  # clear entry field

    """
    Callback function to send/post announcement
    """

    def __post_announcement(self):
        print("Sending email announcement...")
        # global inp
        # inp = inputtxt.get(1.0, "end-1c")
        self.__email.send_email_announcement()
        self.__lbl.config(text="Email sent")

    """
    Callback function to remove selected recipient(s)
    """

    def __remove_selected_recipients(self, selection):
        recipient_list = list(self.__recipient_list_var.get())
        for index in reversed(selection):
            recipient_list.pop(index)
        self.__recipient_list_var.set(recipient_list)

    """
    Callback function to update settings
    """

    def __update_settings(self):
        print("Updating settings...")
        self.__email.recipients_list = list(self.__recipient_list_var.get())
        self.__email.content["verse"]["include"] = self.__verse_var.get()
        self.__email.content["weather"]["include"] = self.__weather_var.get()
        self.__email.content["devotions"]["include"] = self.__devotions_var.get()
        self.__email.content["wikipedia"]["include"] = self.__wikipedia_var.get()

        self.__email.sender_credentials = {
            "email": self.__sender_email_var.get(),
            "password": self.__sender_password_var.get(),
        }

        self.__scheduler.schedule_daily(
            int(self.__hour_var.get()),
            int(self.__minute_var.get()),
            self.__email.send_email_digest,
        )

    """
    Callback function to manually send digest email
    """

    def __manual_send(self):
        # note: settings are not updated before manual send
        print("Manually sending email digest...")
        self.__email.send_email_digest()

    """
    Callback function to validate login username and password
    """

    def __validate_login(self):
        df = pd.read_sql(
            """SELECT username, password FROM administrators;""", con=engine
        )
        admin_name = df["username"].tolist()
        admin_password = df["password"].tolist()

        temp_name = ""
        temp_pswrd = ""

        for i in admin_name:
            if self.__input_name_var.get() == i:
                temp_name = i
                name = i
                break
            else:
                name = self.__input_name_var.get()

        for i in admin_password:
            if self.__input_password_var.get() == i:
                temp_pswrd = i
                pswrd = i
                break
            else:
                pswrd = self.__input_password_var.get()

        if name == temp_name and pswrd == temp_pswrd:
            messagebox.showinfo("Valid login", "Success. Press Ok to continue")

            self.__root.deiconify()
            self.__top.destroy()

        else:
            messagebox.showwarning(
                "Invalid login", "Failed login attempt. Please Try again"
            )

    """
    Shutdown the scheduler before closing the GUI window
    Also Callback function to cancel login attempt and close program
    """

    def __shutdown(self):
        print("Shutting down the scheduler...")
        self.__scheduler.stop()
        self.__scheduler.join()
        self.__top.destroy()
        self.__root.destroy()  # close the GUI


value = "Welcome to Treeolive"


if __name__ == "__main__":
    config.create_database()
    root = Tk()
    top = Toplevel()
    app = DailyDigest(root, top)
    value = inputtxt.get(1.0, "end-1c")
    root.withdraw()
    root.mainloop()
