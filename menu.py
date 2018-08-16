import webbrowser
import Tkinter as Tk

def initmenu(window):
    """
    Creates the menu bar
    """
    menubar = Tk.Menu(window)
    menu = Tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Help", menu=menu)
    menu.add_command(label="eactivities", command=_openeacivities)
    menu.add_command(label="About", command=_opencredits)
    return menubar


def _opencredits():
    """
    Creates a windows showing the credits, from menu bar
    """
    credits_window = Tk.Tk()
    credits_window.title('CSV Analyser')
    canvas = Tk.Canvas(credits_window, bg="white", width=400, height=150,
                       bd=0, highlightthickness=0)
    canvas.create_text(200, 30, fill="darkblue", font="Times 20 italic bold",
                       text="CSV Analyser (v1.0)")
    canvas.create_text(150, 70, fill="black", font="Times 14",
                       text="CSV Analyser was created by")
    canvas.create_text(292, 70, fill="black", font="Times 14 bold",
                       text="Kelvin")
    canvas.create_text(130, 110, fill="black", font="Times 14 underline",
                       text="Email:")
    canvas.create_text(225, 110, fill="black", font="Times 14",
                       text="kc3014@ic.ac.uk")
    canvas.pack()


def _openeacivities():
    """
    Creates the eactivities window from menu bar
    """
    eactivities_window = Tk.Tk()
    eactivities_window.title('eactivities')
    canvas = Tk.Canvas(eactivities_window, bg="white", width=400, height=150,
                       bd=0, highlightthickness=0)
    canvas.create_text(200, 30, fill="darkblue", font="Times 20 italic bold",
                       text="Links to eactivities")
    button1 = Tk.Button(eactivities_window, fg="blue", font="Times 14 underline", text="eactivities.union.ic.ac.uk",
                        command=lambda: webbrowser.open('https://eactivities.union.ic.ac.uk/'), anchor=Tk.W)
    button1_window = canvas.create_window(100, 60, anchor=Tk.NW, window=button1)

    button2 = Tk.Button(eactivities_window, fg="blue", font="Times 14 underline",
                        text="eactivities > finance/transactions",
                        command=lambda: webbrowser.open('https://eactivities.union.ic.ac.uk/finance/transactions'),
                        anchor=Tk.W)
    button2_window = canvas.create_window(100, 110, anchor=Tk.NW, window=button2)
    canvas.pack()