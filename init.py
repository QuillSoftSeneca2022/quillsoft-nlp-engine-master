import os
import tkinter.filedialog
from PoC_Knowledge_Graph import draw_graph_kg
from PoC_Semantic_Relations import draw_graph_sr

def display_title_bar():
              
    print("\t**********************************************")
    print("\t**********  QUILLSOFT - NLP Engine  **********")
    print("\t**********************************************")
    
def explore():
    pathname = tkinter.filedialog.askopenfilename()
    return pathname

### MAIN PROGRAM ###
# Clears the terminal screen, and displays a title bar.
os.system('cls')
choice = ''
display_title_bar()
while choice != 'q':    
    
    display_title_bar()
    print("\n[1] Knowledge Graph - Triples.")
    print("[2] Knowledge Graph - Hearst Patterns.")
    print("[q] Quit.")
    
    choice = input("What would you like to do? ")
    
    # Respond to the user's choice.
    if choice == '1':
        print("\n***Leave it empty to visualize all relations***")
        print("What Relation do you want to visualize? (e.g.: is, has, use): ")
        relation = input()
        path = explore()
        draw_graph_kg(path, relation)
    elif choice == '2':
        path = explore()
        draw_graph_sr(path)
    elif choice == 'q':
        print("\nBye!!!.")
    else:
        print("\nI didn't understand that choice.\n")