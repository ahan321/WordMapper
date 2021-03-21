import PySimpleGUI as gui
from mapper.word_map import save_word_map

gui.theme("reddit")

shouldContinue = True
while shouldContinue:
    
    layout = [[gui.Text("Please type in a word")],
            [gui.InputText()],
            [gui.Button("Okay"),gui.Button("Cancel"),gui.Text(text = "", key = "ERROR", size = (28,1))]]

    window = gui.Window("WordMapper", layout)
    while True:
        
        event,values = window.read()
        isWord = True
        
        for i in values[0]:
            if (ord(i) < ord("a") and ord(i) > ord("Z")) or (ord(i) < ord("A")) or (ord(i) > ord("z")):
                isWord = False
        
        if event == gui.WIN_CLOSED or event == "Cancel":
            shouldContinue = False
            break
        elif values[0] == "" or isWord == False:
            window["ERROR"].update(value = "You have not entered a word.")
            print(layout)
        elif event == "Okay":
            word = values[0]
            save_word_map(word)
            shouldContinue = True
            break

    window.close()

    if shouldContinue:
        
        mapLayout = [[gui.Image(filename = "test-output/graph.gv.png", key = "IMAGE")],
                    [gui.Button("Exit"), gui.Button("Back")]]
        
        mapLayoutCentered = [gui.Column(mapLayout, element_justification = "center")]

        window = gui.Window("WordMapper", mapLayoutCentered)

        while True:
            event,values = window.read()

            if event == gui.WIN_CLOSED or event == "Exit":
                shouldContinue = False
                break
            elif event == "Back":
                break

    window.close()