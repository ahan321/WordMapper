import PySimpleGUI as gui

gui.theme("Black")

layout = [[gui.Text("Please type in a word")],[gui.InputText()], [gui.Button("Okay"),gui.Button("Cancel"),gui.Text(text = "", key = "ERROR", size = (28,1))]]

window = gui.Window("WordMapper", layout)


while True:
    event,values = window.read()

    isWord = True
    for i in values[0]:
        if (ord(i) < ord("a") and ord(i) > ord("Z")) or (ord(i) < ord("A")) or (ord(i) > ord("z")):
            isWord = False
    
    if event == gui.WIN_CLOSED or event == "Cancel":
        shouldContinue = False
    elif values[0] == "" or isWord == False:
        window["ERROR"].update(value = "You have not entered a word.")
        print(layout)
    elif event == "Okay":
        word = values[0]
        shouldContinue = True
        break

window.close()

if shouldContinue:
    
    mindMapLayout = []
    mindMapWindow = gui.Window("WordMapper", mindMapLayout)

print(word)