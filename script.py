import PySimpleGUI as sg
import mouse
import time
import threading
import keyboard

cookiePos = (0, 0)
popup_open = False
stop_clicker = False

layout = [
    [sg.Button("Set Position", key="find_cookie", pad=(0, 0)), sg.Text("Current Position: " + str(cookiePos), justification='left', key="cookie_pos_text"), sg.Checkbox("Use mouse position", key="use_mouse", pad=(2, 0))],
    [sg.Button("START CLICKER", key="start_clicker", pad=(0, 10)),  sg.Text("F1 TO START | X TO STOP", justification='left', key="cookie_pos_text")],
    [sg.Checkbox("Lock Mouse Position", key="lock_mouse", pad=(0, 0))],
]

window = sg.Window("Clicccer", layout, element_justification='left', finalize=True)

def clicker_loop():
    global stop_clicker
    if window["lock_mouse"].get():
        while not stop_clicker:
            mouse.move(cookiePos[0], cookiePos[1])
            mouse.click()
            time.sleep(0.01)
    else:
        while not stop_clicker:
            mouse.click()
            time.sleep(0.01)

# Function to handle keyboard events
def keyboard_handler():
    global stop_clicker
    keyboard.wait('x')
    stop_clicker = True


# Function to show a custom instruction popup with a border
def show_instruction_popup():
    layout = [
        [sg.Frame('', [[sg.Text("Move your mouse to the position and click", pad=(10, 10))]], border_width=1)]
    ]
    popup = sg.Window("Instruction", layout, finalize=True, no_titlebar=True)
    popup.read(timeout=1500)
    popup.close()


def on_click(event):
    global popup_open, cookiePos
    if type(event) != mouse.ButtonEvent:
        return
    if event.event_type == mouse.UP:
        cookiePos = mouse.get_position()
        cookiePosText = "Position: " + str(cookiePos)
        window["cookie_pos_text"].update(cookiePosText)
        mouse.unhook_all()
        popup_open = False

while True:
    event, values = window.read(timeout=100)  # Set a short timeout to keep the loop responsive
    # End program if user closes window or
    if values["use_mouse"]:
        window["lock_mouse"].update(False)
        window["lock_mouse"].update(disabled=True)
        window["find_cookie"].update(disabled=True)
    else:
        window["lock_mouse"].update(disabled=False)
        window["find_cookie"].update(disabled=False)
    if event == "EXIT" or event == sg.WIN_CLOSED:
        break
    elif event == "find_cookie" and not popup_open:
        popup_open = True
        show_instruction_popup()
        mouse.hook(on_click)  # Start listening for mouse events
    elif event == "start_clicker" or keyboard.is_pressed('f1'):
        if not values["use_mouse"]:
            mouse.move(cookiePos[0], cookiePos[1])
        stop_clicker = False  # Reset stop flag
        threading.Thread(target=clicker_loop, daemon=True).start()  # Start clicker loop in a separate thread
        threading.Thread(target=keyboard_handler, daemon=True).start()  # Start keyboard event handler in a separate thread

window.close()

#for i in range(10000):
#    mouse.click('left')
