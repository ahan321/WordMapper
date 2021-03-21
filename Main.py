import PySimpleGUI as gui

gui.theme("DarkAmber")


layout = [[gui.Text("Please type in a word")],[gui.InputText()], [gui.Button("Okay"),gui.Button("Cancel")]]

window = gui.Window("WordMapper", layout)


while True:
    event,values = window.read()

    isWord = True
    for i in values[0]:
        if (i < ord("a") and i > ord("Z")) or (i < ord("A")) or (i > ord("z")):
            isWord = False
    
    if event == gui.WIN_CLOSED or event == "Cancel":
        shouldContinue = False
    elif event == "Okay":
        word = values[0]
        break
    elif values[0] == "":
        layout.append(gui.Text(text="You have not "))

if shouldContinue:
    lol = True

print(word)