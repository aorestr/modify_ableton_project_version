import PySimpleGUI as sg
from main import run_script

FONT = font = ("Arial", 12)
sg.theme("DarkAmber")

# Rows
als_row = [sg.Text("Select Ableton '.als' file: ", size=(20, 1)), sg.InputText(key="-ALS-"), sg.FileBrowse()]
version_row = [sg.Text("Select Ableton version: ", size=(20, 1)), sg.InputText(key="-VERSION-")]
buttons_row = [sg.Button("Run"), sg.Button("Cancel")]
xml_row = [sg.Checkbox("Removed XML file after extraction?", key="-XML-", default=True)]
output_row = [sg.Output(size=(40, 7), key="-OUTPUT-")]
layout = [
    [
        sg.Column([als_row, version_row, xml_row, buttons_row]),
        sg.Column([output_row, ])
    ]
]

# Window
window = sg.Window("Modify Ableton project version", layout, font=FONT)

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == "Run":
        try:
            run_script(values["-ALS-"], values["-VERSION-"], remove_xml=values["-XML-"])
        except Exception as e:
            print(e)
    if event == sg.WIN_CLOSED or event == "Cancel":
        break

window.close()
