import customtkinter as ctk
import threading
import socket

ctk.set_appearance_mode("system")

# App configureation
app = ctk.CTk()
app.title("TCP Chat Client")

w = 480
h = 720
ws = app.winfo_screenwidth()
hs = app.winfo_screenheight()
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)

app.geometry('%dx%d+%d+%d' % (w, h, x, y))
app.resizable(False, False)


HOST = "127.0.0.1"
PORT = 8081
ADDR = HOST, PORT
FORMAT = "utf-8"
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

nickname = None
stop_thread = False
connected = False

# Gui Functions


def showMsg(message: str) -> None:
    msg_history.configure(state="normal")
    msg_history.insert("end", text=f"{message}\n")
    msg_history.yview(ctk.END)
    msg_history.configure(state="disabled")


def getMessage() -> None:
    message = msg_entry.get()
    if message and message != "":
        msg_entry.delete(0, "end")
        showMsg(f"{nickname}: {message}")
        send(message)


# client functions
def receive() -> None:
    global stop_thread
    print("Thread Started")
    while True:
        if stop_thread == True:
            break
        try:
            message = client.recv(1024).decode(FORMAT)
            if message != "nick?" and message != "pass?" and message != "refused?":
                showMsg(message)
            if message == "nick?":
                nickname = aksForNick()
                client.send(nickname.encode(FORMAT))

            if message == "pass?":
                password = askForPassword()
                client.send(password.encode(FORMAT))
            if message == "refused?":
                app.quit()

        except:
            stop_thread = True
            client.close()
            break


def send(message: str):
    if message != "!dc":
        client.send(message.encode(FORMAT))
    else:
        client.send("!dc".encode(FORMAT))
        client.close()
        app.quit()


def stop() -> bool:
    global stop_thread
    if connected:
        stop_thread = True
        client.send("!dc".encode(FORMAT))
        client.close()
    app.destroy()
    return True


def aksForNick() -> str:
    nickname_dialog = ctk.CTkInputDialog(title="Pick a Nick name", text="Pick a nickname")
    nickname_dialog.geometry('%dx%d+%d+%d' % (300, 100, x, y))
    nickname = nickname_dialog.get_input()
    while nickname == None or nickname == "":
        nickname_dialog = ctk.CTkInputDialog(title="Pick a Nick name", text="Pick a nickname")
        nickname_dialog.geometry('%dx%d+%d+%d' % (300, 100, x, y))
        nickname = nickname_dialog.get_input()
    return nickname


def askForPassword() -> str:
    password_dialog = ctk.CTkInputDialog(title="Enter admin password", text="Enter admin password")
    password_dialog.geometry('%dx%d+%d+%d' % (300, 100, x, y))
    password = password_dialog.get_input()
    while password == None or password == "":
        password_dialog = ctk.CTkInputDialog(title="Enter admin password", text="Enter admin password")
        password_dialog.geometry('%dx%d+%d+%d' % (300, 100, x, y))
        password = password_dialog.get_input()
    return password


def setEntrySate(state: str):
    msg_entry.configure(state=state)


# Frame
frame = ctk.CTkFrame(master=app)
frame.pack(fill="both", expand=1, side="top", padx=20, pady=10)

# Title
labell = ctk.CTkLabel(
    frame, text="Test labell", fg_color="gray", text_color="white", corner_radius=10)
labell.pack(fill="x", padx=20, pady=10)

# Message history
msg_history = ctk.CTkTextbox(frame, corner_radius=8)
msg_history.insert("1.0", "Message History\n")
msg_history.pack(fill="both", expand=1, padx=20, pady=10)
msg_history.configure(state="disabled")

# Message entry
msg_entry = ctk.CTkEntry(
    frame, corner_radius=8, fg_color="gray")
msg_entry.focus_force()
msg_entry.pack(fill="x", padx=10, pady=10)

# Send message button
send_button = ctk.CTkButton(frame, text="Send")
send_button.pack(side="right", padx=10, pady=10)
send_button.configure(command=getMessage)

setEntrySate("disabled")
try:
    client.connect(ADDR)
    connected = True
    setEntrySate("normal")

    receive_thread = threading.Thread(target=receive)
    print("Thread created")
    receive_thread.start()
except Exception as e:
    print(e)
    showMsg("[ERROR]: Can't connect")


app.deiconify()
app.protocol("WM_DELETE_WINDOW", stop)
app.mainloop()
