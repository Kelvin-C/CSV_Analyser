# |**********************************************************************;
# * Project           : csv_analyser
# *
# * Author            : Kelvin-C
# *
# * Program name      : gui.py
# *
# * Python Version    : 2.7.14
# *
# * Date created      : 25 September 2017
# *
# * Purpose           : A gui which allows .csv files to be analysed.
# *
# * Revision History  : v1.0
# *
# |**********************************************************************;



import Tkinter as Tk
import tkFileDialog
import tkFont
import csv
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
import webbrowser

class GUIMain():
    def __init__(self):
        """
        Main GUI Window
        This class controls everything that occurs on the main window.
        """
        self.window = Tk.Tk()
        self.window.title('CSV Analyser')
        if os.path.exists(os.getcwd()+'/csv'):
            os.chdir(os.getcwd()+'/csv')
        else:
            os.chdir(os.getcwd())
        self.output_dir = os.getcwd()
        self.file_dropdown_name = Tk.StringVar(self.window)
        self.column_dropdown_name = Tk.StringVar(self.window)
        self.column_variables = []
        self.CheckVar = []
        self.CheckVar_graph = []
        self.__plots = []
        self.excel_path = Tk.StringVar(self.window)
        self.__initgrid()
        self.window.mainloop()

    def __initgrid(self):
        """
        Displays the rest of the GUI.
        The widgets are made row by row.
        """
        sizex = 400
        sizey = 100
        posx = 100
        posy = 100
        self.window.wm_geometry("%dx%d+%d+%d" % (sizex, sizey, posx, posy))
        self.__maxrow = 2
        self.__maxcolumn = 3
        self.__row0()
        self.__row1()
        self.__nothingrow(frame=self.window, row=1, rowspan=1)
        self.__initmenu()
        self.window.config(menu=self.menubar)

    def __safeinitgrid(self):
        """
        Displays the rest of the GUI when the .csv file is successfully loaded.
        The widgets are made row by row.
        """
        sizex = 750
        sizey = 365
        posx = 100
        posy = 100
        self.window.wm_geometry("%dx%d+%d+%d" % (sizex, sizey, posx, posy))

        self.headings, self.csv_table = self._opencsv(self.excel_path.get())

        column_index = np.where(np.array(self.headings) == self.column_dropdown_name.get())[0]
        if not not column_index:   #if column_index is not empty
            self.column_variables = self._combine_elements(self.headings, self.csv_table, column_index[0])

        self.__maxrow = len(self.headings)+2
        self.__maxcolumn = 3
        self.__row0()
        self.__row1()
        self.__row2()
        self.__initmenu()
        self.window.config(menu=self.menubar)

        #Creates scroll window for the checklists
        self.scrollwindow, self.canvas = self._initframe(self.window)
        self.canvas.config(width=400, height=180)
        self.canvas.create_window(0, 0, window=self.scrollwindow, anchor='nw')
        self.__row3()
        self.__nothingrow(self.scrollwindow, rowspan=2)
        self.window.update()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        self.__keybinds()
        self.__lastrow()


    def __initmenu(self):
        """
        Creates the menu bar
        """
        self.menubar = Tk.Menu(self.window)
        menu = Tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Help", menu=menu)
        menu.add_command(label="eactivities", command=self._openeacivities)
        menu.add_command(label="About", command=self._opencredits)

    def _opencredits(self):
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
        canvas.create_text(60, 110, fill="black", font="Times 14 underline",
                           text="Email:")
        canvas.create_text(200, 110, fill="blue", font="Times 14 underline",
                           text="kelvin.chan14@imperial.ac.uk")
        canvas.pack()

    def _openeacivities(self):
        """
        Creates the eactivities window from menu bar
        """
        eactivities_window = Tk.Tk()
        eactivities_window.title('eactivities')
        canvas = Tk.Canvas(eactivities_window, bg="white", width=400, height=170,
                           bd=0, highlightthickness=0)
        canvas.create_text(200, 30, fill="darkblue", font="Times 20 italic bold",
                           text="Links to eactivities")
        button1 = Tk.Button(eactivities_window, fg="blue", font="Times 14 underline", text="eactivities.union.ic.ac.uk",
                            command=lambda: webbrowser.open('https://eactivities.union.ic.ac.uk/'), anchor=Tk.W)
        button1_window = canvas.create_window(100, 60, anchor=Tk.NW, window=button1)

        button2 = Tk.Button(eactivities_window, fg="blue", font="Times 14 underline", text="eactivities > finance/transactions",
                            command=lambda: webbrowser.open('https://eactivities.union.ic.ac.uk/finance/transactions'), anchor=Tk.W)
        button2_window = canvas.create_window(100, 110, anchor=Tk.NW, window=button2)
        canvas.pack()

    def _initframe(self, window):
        """
        Generates the overall frame for the scrollbar.
        """

        # initiate scrollbars
        vscrollbar = Tk.Scrollbar(window)
        hscrollbar = Tk.Scrollbar(window)

        # create canvas in window
        canvas = Tk.Canvas(window, background="#D2D2D2", yscrollcommand=vscrollbar.set, xscrollcommand=hscrollbar.set)

        # Create the frame which will hold the widgets
        frame = Tk.Frame(canvas)

        # configure the scrollbar to move canvas screen
        vscrollbar.config(command=canvas.yview, orient=Tk.VERTICAL)
        vscrollbar.pack(side=Tk.RIGHT, fill=Tk.Y)
        hscrollbar.config(command=canvas.xview, orient=Tk.HORIZONTAL)
        hscrollbar.pack(side=Tk.BOTTOM, fill=Tk.X)

        # pack canvas after scrollbars to allow scrollbars to be at correct places.
        canvas.pack(fill="both", expand=True)
        return frame, canvas

    def __keybinds(self):
        self.canvas.focus_set()
        self.canvas.bind("<1>", lambda event: self.canvas.focus_set())
        self.canvas.bind("<Left>", lambda event: self.canvas.xview_scroll(-1, "units"))
        self.canvas.bind("<Right>", lambda event: self.canvas.xview_scroll(1, "units"))
        self.canvas.bind("<Up>", lambda event: self.canvas.yview_scroll(-1, "units"))
        self.canvas.bind("<Down>", lambda event: self.canvas.yview_scroll(1, "units"))
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Shift-MouseWheel>", self._sidescroll)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(-1 * (event.delta / 120), "units")

    def _sidescroll(self, event):
        self.canvas.xview_scroll(-1 * (event.delta / 120), "units")

    def _opencsv(self, excel_path):
        """
        Opens the .csv file and stores the headings and elements into lists.
        """
        csv_table = []
        with open(excel_path, 'r') as file:
            report = csv.reader(file)
            headings = report.next()
            for row in report:
                csv_table += row,
        return headings, csv_table

    def __nothingrow(self, frame, row=0, rowspan=1):
        """
        Creates a row with empty space
        """
        nothing_frame = Tk.Frame(frame)
        nothing_frame.grid(row=row, rowspan=rowspan)
        for i in range(rowspan):
            nothing_label = Tk.Label(nothing_frame, text="")
            nothing_label.pack()
        nothing_frame.pack()
        return

    def __nothingwidget(self, frame, width=40, pack=False, side=Tk.TOP, fill=Tk.NONE, expand=False, padx=0, pady=0, background="#D2D2D2"):
        """
        Creates a widget of empty space.
        """
        text = " "*width
        nothing_label = Tk.Label(frame, text=text)
        if pack == True:
            nothing_label.pack(side=side, fill=fill, expand=expand, padx=padx, pady=pady, background=background)
            return
        return nothing_label

    def __refresh(self):
        """
        Refreshes the window.
        Tests whether the .csv file can be opened.
        If .csv can be opened, jumps to __safeinitgrid to load more functions about the .csv file.
        """
        self.excel_path.set(self.output_dir + "/" + self.file_dropdown_name.get())
        try:
            open(self.excel_path.get(), "r")
        except:
            for widget in self.window.winfo_children():
                widget.destroy()
            self.__initgrid()
            self.window.update()
        else:
            for widget in self.window.winfo_children():
                widget.destroy()
            self.__safeinitgrid()

    def __row0(self):
        """
        Title row
        """
        row0 = Tk.Frame(self.window)
        row0.grid(row=0, column=0)#, columnspan=self.__maxcolumn)

        helv36 = tkFont.Font(family='Helvetica', size=12, weight=tkFont.BOLD)
        self.__windowtitle = Tk.Label(row0, text="CSV Analyser", font=helv36)
        row0.pack(fill=Tk.X)
        self.__windowtitle.pack(fill=Tk.X)

    def __row1(self):
        """
        Row of the .csv entry box and the browse/refresh buttons
        """
        self.window.rowconfigure(1, minsize=50)
        row1 = Tk.Frame(self.window)
        row1.grid(row=1, column=0, sticky='EWNS')
        self.excel_path_label = Tk.Label(row1, text="CSV Location")
        self.excel_path_entry = Tk.Entry(row1, bd=5, textvariable=self.excel_path)
        self.excel_path_browse = Tk.Button(row1, text="Browse", command=self._askfile)
        #self.refreshbutton = Tk.Button(row1, text="Refresh", command=self.__refresh)

        row1.pack(fill=Tk.X)
        self.excel_path_label.pack(side=Tk.LEFT, padx=10)
        self.excel_path_entry.pack(side=Tk.LEFT, fill=Tk.X, expand=True)
        self.excel_path_browse.pack(side=Tk.LEFT, padx=10)
        #self.refreshbutton.pack(side=Tk.LEFT, padx=10)

    def __row2(self):
        """
        When .csv can be loaded, a drop-down list is used so a .csv file can be chosen if multiple .csv files are chosen.
        """
        row2 = Tk.Frame(self.window)
        row2.grid(row=2, column=1, sticky='EWNS')
        file_dropdown = Tk.OptionMenu(row2, self.file_dropdown_name, *self.filenames, command=lambda _: self.__refresh())
        row2.pack(fill=Tk.X)
        file_dropdown.pack()

    def __row3(self):
        """
        This functions creates all widgets for the 3rd row.
        self.__nothing is used to create empty spaces.
        Checklists are made in self._createchecklist function
        """
        row3 = Tk.Frame(self.scrollwindow)
        row3.grid(row=0, sticky='EWNS')

        nothing1 = self.__nothingwidget(frame=row3)

        table_checklist = Tk.Frame(row3)
        helv36 = tkFont.Font(family='Helvetica', size=10, weight=tkFont.BOLD)
        checklist_heading = Tk.Label(table_checklist, text="Columns to draw in table", font=helv36)
        checklist_heading.pack()
        self.CheckVar = self._createchecklist(table_checklist, self.headings, 1, self.CheckVar)
        nothing2 = self.__nothingwidget(frame=row3)

        graph_checklist_frame = Tk.Frame(row3)
        column_dropdown = Tk.OptionMenu(graph_checklist_frame, self.column_dropdown_name, *self.headings, command=lambda _: self.__refresh())
        column_dropdown.pack()
        column_dropdown_heading = Tk.Label(graph_checklist_frame, text="Variables to include in graph", font=helv36)
        column_dropdown_heading.pack()
        self.CheckVar_graph = self._createchecklist(graph_checklist_frame, self.column_variables[1:], 1,  self.CheckVar_graph)

        nothing3 = self.__nothingwidget(frame=row3, width=1000)

        row3.pack(fill=Tk.X)
        nothing1.pack(fill=Tk.BOTH, side=Tk.LEFT, expand=True)
        table_checklist.pack(fill=Tk.Y, side=Tk.LEFT)
        nothing2.pack(fill=Tk.BOTH, side=Tk.LEFT, expand=True)
        graph_checklist_frame.pack(fill=Tk.Y,side=Tk.LEFT)
        nothing3.pack(fill=Tk.BOTH, side=Tk.LEFT, expand=True)
        return

    def __lastrow(self):
        """
        This row controls the buttons to plot graphs and tables.
        """
        lastrow = Tk.Frame(self.window)
        lastrow.grid(row=self.__maxrow)

        nothing0 = self.__nothingwidget(frame=lastrow, width=25)
        tick_button = Tk.Button(lastrow, text="Tick/untick all", command=self._tickuntick)
        nothing1 = self.__nothingwidget(frame=lastrow, width=10)
        table_button = Tk.Button(lastrow, text="Plot Table", command=self._plottable)
        nothing2 = self.__nothingwidget(frame=lastrow, width=20)
        plot_button = Tk.Button(lastrow, text="Plot Graph", command=self._plotgraph)
        nothing3 = self.__nothingwidget(frame=lastrow, width=10)
        remove_plot_button = Tk.Button(lastrow, text="Delete Last Plot", command=self._removegraph)
        nothing4 = self.__nothingwidget(frame=lastrow, width=20)

        lastrow.pack(fill=Tk.X)
        nothing0.pack(fill=Tk.X, side=Tk.LEFT, expand=True)
        tick_button.pack(side=Tk.LEFT)
        nothing1.pack(fill=Tk.X, side=Tk.LEFT, expand=True)
        table_button.pack(side=Tk.LEFT)
        nothing2.pack(fill=Tk.X, side=Tk.LEFT, expand=True)
        plot_button.pack(side=Tk.LEFT)
        nothing3.pack(fill=Tk.X, side=Tk.LEFT, expand=True)
        remove_plot_button.pack(side=Tk.LEFT)
        nothing4.pack(fill=Tk.X, side=Tk.LEFT, expand=True)

    def _askfile(self):
        """
        This function is used when 'browse' button is clicked on. A file will be chosen and further checks in __refresh
        will be done to see if it's a .csv file.
        """
        self.output_files = tkFileDialog.askopenfilenames(filetypes=(("csv files", "*.csv"), ("all files", "*.*")), title="Choose the .csv file(s)")
        if not self.output_files:
            self.__refresh()
        else:
            self.output_dir = '/'.join(self.output_files[0].split('/')[:-1])
            self.filenames = map(lambda file: file.split('/')[-1], self.output_files)
            self.excel_path_entry.delete(0, 'end')
            self.excel_path_entry.insert(0, self.output_dir)
            self.file_dropdown_name.set(self.filenames[0])
            self.column_dropdown_name.set("Variables to plot")
            self.__refresh()

    def _createchecklist(self, frame, list, default_value, CheckVar=[]):
        """
        Creates a checklist.
        """
        old_CheckVar = CheckVar
        new_CheckVar = []
        if len(list) == len(old_CheckVar):
            for i in range(len(list)):
                temp = Tk.IntVar(frame)
                temp.set(old_CheckVar[i].get())
                new_CheckVar.append(temp)
                check = Tk.Checkbutton(frame, text=list[i], variable=new_CheckVar[i], onvalue=1, offvalue=0)
                check.pack(fill=Tk.X)
        else:
            for i in range(len(list)):
                temp = Tk.IntVar(frame)
                temp.set(default_value)
                new_CheckVar.append(temp)
                check = Tk.Checkbutton(frame, text=list[i], variable=new_CheckVar[i], onvalue=1, offvalue=0)
                check.pack(fill=Tk.X)
        return new_CheckVar

    def _combine_elements(self, headings, csv_table, column):
        """
        Finds all variables in a given column of the csv_table and outputs them into a list
        """
        i = column
        csv_table_transpose = np.transpose(csv_table)
        column_elements = csv_table_transpose[i]

        column_elements = list(set(column_elements))
        column_elements = np.append(np.array([headings[i]]), column_elements)
        return column_elements

    def _tickuntick(self):
        """
        Unticks all boxes in the checklist when the untick box is clicked.
        """
        num = self.CheckVar[0].get()
        rev_num = not int(bool(num))
        for i in range(len(self.CheckVar)):
            self.CheckVar[i].set(rev_num)
        return

    def _plottable(self):
        """
        Creates the GUITable class and produces a table with the class
        """
        GUITable(self.excel_path.get(), self.CheckVar, self.file_dropdown_name.get())
        return

    def _removegraph(self):
        """
        Remove the last graph that was plotted
        """
        if len(self.__plots) > 0:
            plot = self.__plots[-1]
            lines = plot.pop(0)
            lines.remove()
            del lines
            self.__plots = self.__plots[:-1]
            plt.show()
        else:
            return

    def _plotgraph(self):
        """
        This function deals with plotting the graph.
        """

        #delete rows in table that aren't ticked
        csv_table, headings = self._deleterows(self.CheckVar_graph, self.column_variables, self.csv_table)

        # sort csv_table into date ascending order
        csv_table = self._timesort(csv_table, column_index=0, delimiter='/')

        csv_table = np.array(csv_table)

        # sum the amounts with the same dates
        dates = np.array([])
        amount = []
        for i in range(len(csv_table)):
            if csv_table[i][0] in dates:
                date_loc = np.where(dates == csv_table[i][0])[0][0]
                amount[date_loc] += float(csv_table[i][-1].replace(',', ''))
            else:
                dates = np.append(dates, csv_table[i][0])
                amount += [float(csv_table[i][-1].replace(',', ''))]

        # accumulative amount over time
        accum_amount = []
        for i in range(len(amount)):
            accum_amount += [sum(amount[0:i + 1])]

        if plt.fignum_exists(1):
            self.__plotdates(dates, accum_amount)
        else:
            plt.figure(1)
            self.__plotdates(dates, accum_amount)
            plt.ylabel('Amount (%s)' % unichr(163))
            plt.grid()
        plt.title('+'.join(headings))
        plt.legend(loc='best')
        plt.show()
        return

    def __plotdates(self, dates_list, y_list):
        """
        This function plots the graph with dates in the x-axis.
        """
        x = [dt.datetime.strptime(date, '%d/%m/%Y').date() for date in dates_list]
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=2))
        line = plt.plot(x, y_list, label=self.file_dropdown_name.get())
        self.__plots.append(line)
        plt.gcf().autofmt_xdate()
        plt.xlabel("Date")
        return

    def _deleterows(self, CheckVar, column_variables, csv_table):
        """
        This function deletes the rows, in csv_table, with the variables in column_variables.
        """
        CheckVarGet = map(lambda value: value.get(), CheckVar)
        CheckVarGet = np.array(CheckVarGet)
        headings = column_variables[1:]

        if 0 in CheckVarGet:
            deletenames_indices = np.where(CheckVarGet == 0)[0]
            for i in range(len(deletenames_indices)):
                checklist_heading = column_variables[0]
                checklist_column = np.where(np.array(self.headings) == checklist_heading)[0]
                csv_table_transpose = np.transpose(csv_table)
                csv_table = np.delete(csv_table, np.where(csv_table_transpose[checklist_column[0]] == column_variables[deletenames_indices[i] + 1]), 0)
            headings = np.delete(headings, deletenames_indices)
        return csv_table, headings

    def _timesortDMY(self, time1, time2, delimiter='/'):
        """
        Sorts two times in time ascending order.
        Format is DD/MM/YYYY (hence DMY in function name)

        Returns True if time1 is earlier than time2
        Returns False if time1 is later than time2
        """
        time1_parts = map(int, time1.split(delimiter))
        time2_parts = map(int, time2.split(delimiter))

        # time1 year is lower than time2
        if time1_parts[2] < time2_parts[2]:
            return True

        # time1 year is same as time2
        elif time1_parts[2] == time2_parts[2]:
            if time1_parts[1] < time2_parts[1]:  # time1 month is lower than time2
                return True
            elif time1_parts[1] == time2_parts[1]:  # time1 month is same as time2
                if time1_parts[0] <= time2_parts[0]:  # time1 day is lower/same as time2
                    return True
                else:
                    return False  # time1 day is higher than time2
            else:  # time1 month is higher than time2
                return False

        # time1 year is higher than time2
        else:
            return False

    def _numbersort(self, num1, num2):
        num1 = int(num1)
        num2 = int(num2)

        if num1 <= num2:
            return True
        else:
            return False

    def _timesort_OLD(self, list, column_index=0, delimiter='/'):
        """
        Sorts a 2D list into time order.
        list = list variable name
        column index = which column of the list contains the times?
        delimiter = the character(s) which separated the DD MM YYYY
        """
        timesort = self._timesortDMY
        j = column_index
        new_list = [list[0]]
        for i in range(1, len(list)):
            stop_k_loop = 0
            for k in range(i):
                if stop_k_loop == 0:
                    if timesort(list[i][j], new_list[k][j], delimiter) == True:
                        new_list.insert(k, list[i])
                        stop_k_loop = 1
                    elif timesort(list[i][j], new_list[k][j], delimiter) == False:
                        if k == i - 1:
                            new_list.append(list[i])
                            stop_k_loop = 1
        return new_list

    def _timesort(self, table, column_index=0, delimiter='/', reverse=False):
        dates = np.transpose(table)[column_index]
        dates_parts = list(map(lambda date: date.split(delimiter), dates))
        sort_column = list(map(lambda parts: ''.join(parts[::-1]), dates_parts))

        csv_table = [n for _, n in sorted(zip(sort_column, table), key=lambda pair: pair[0], reverse=reverse)]
        return csv_table

    def _cidnumbersort(self, list, column_index=3):
        """
        Sort CID numbers in ascending/descending order.
        """
        numbersort = self._numbersort
        j = column_index
        new_list = [list[0]]
        for i in range(1, len(list)):
            stop_k_loop = 0
            for k in range(i):
                if stop_k_loop == 0:
                    if numbersort(list[i][j], new_list[k][j]) == True:
                        new_list.insert(k, list[i])
                        stop_k_loop = 1
                    elif numbersort(list[i][j], new_list[k][j]) == False:
                        if k == i - 1:
                            new_list.append(list[i])
                            stop_k_loop = 1

        for i in range(len(new_list)):
            new_list[i][j] = self._cid_addzeros(new_list[i][j])
        return new_list

    def _cid_addzeros(self, cid):
        cid_length = len(cid)
        true_cid_length = 8
        add_zeros = true_cid_length - cid_length
        cid = '0'*add_zeros + cid
        return cid

    def _generalnumbersort_OLD(self, list, column_index=2):
        numbersort = self._numbersort
        j = column_index
        new_list = [list[0]]
        for i in range(1, len(list)):
            stop_k_loop = 0
            for k in range(i):
                if stop_k_loop == 0:
                    if numbersort(list[i][j], new_list[k][j]) == True:
                        new_list.insert(k, list[i])
                        stop_k_loop = 1
                    elif numbersort(list[i][j], new_list[k][j]) == False:
                        if k == i - 1:
                            new_list.append(list[i])
                            stop_k_loop = 1
        return new_list

    def _generalnumbersort(self, table, column_index, reverse=False):
        """
        Sort the table according the numbers in column 'column_index'.
        """

        #Create a new list of the column and remove the commas in the numbers of the new list
        sort_column = list(map(lambda n: ''.join(n.split(',')), np.transpose(table)[column_index]))

        #Convert the numbers from string to float
        sort_column = list(map(lambda n: float(n), sort_column))

        #Sort the original table according to the list of floats.
        csv_table = [n for _, n in sorted(zip(sort_column, table), key=lambda pair: pair[0], reverse=reverse)]
        return csv_table

class GUITable(GUIMain):
    def __init__(self, excel_path, CheckVar, filename):
        """
        This GUI controls and displays the information regarding the table that it creates.
        This class is created when 'Plot Table' button is clicked on.

        CheckVar stores information about which columns to plot (from the checklist)
        """
        self.headings, self.csv_table = self._opencsv(excel_path)
        self.filename = filename

        CheckVarGet = map(lambda value: value.get(), CheckVar)
        CheckVarGet = np.array(CheckVarGet)
        self.headings = np.delete(self.headings, np.where(CheckVarGet == 0)[0])
        self.csv_table_original = np.delete(self.csv_table, np.where(CheckVarGet == 0)[0], 1)
        self.csv_table = self.csv_table_original

        self.column_variables = []

        self.window = Tk.Tk()
        self.window.title(filename)
        sizex = 1000
        sizey = 600
        posx = 100
        posy = 100
        self.window.wm_geometry("%dx%d+%d+%d" % (sizex, sizey, posx, posy))

        self.CheckVar = self.__initiateCheckVar()

        self.column_dropdown_name = Tk.StringVar(self.window)
        self.column_dropdown_name.set("Headings")

        self.__initwindow()

    def __initwindow(self):
        """
        Initiates the frame and its widgets. This is ran when window is refreshed.
        """

        self.__updatecolumndropdown()

        self.frame, self.canvas = self._initframe(self.window)
        self.canvas.create_window(0, 0, window=self.frame, anchor='nw')
        self.__insertheadings(self.frame, self.headings, self.csv_table)
        self.__insertelements(self.frame, self.headings, self.csv_table)
        self.__insertdropdown(self.frame, len(self.headings)+1, self.headings)
        self.__insertchecklist(self.frame, len(self.headings)+1)
        self.__insertfilename(self.frame, len(self.headings)+2)
        self.window.update()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        self.__keybinds()
        self.window.mainloop()

    def __updatecolumndropdown(self):
        """
        Allows the variables of the column given in the dropdown list to be stored for the checklist.
        """
        column_index = np.where(np.array(self.headings) == self.column_dropdown_name.get())[0]
        if len(column_index) > 0:  # if column_index is not empty
            self.column_variables = self._combine_elements(self.headings, self.csv_table, column_index[0])

    def __keybinds(self):
        """
        Sets the keybinds for the window.
        """
        self.canvas.focus_set()
        self.canvas.bind("<1>", lambda event: self.canvas.focus_set())
        self.canvas.bind("<Left>", lambda event: self.canvas.xview_scroll(-1, "units"))
        self.canvas.bind("<Right>", lambda event: self.canvas.xview_scroll(1, "units"))
        self.canvas.bind("<Up>", lambda event: self.canvas.yview_scroll(-1, "units"))
        self.canvas.bind("<Down>", lambda event: self.canvas.yview_scroll(1, "units"))
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Shift-MouseWheel>", self._sidescroll)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(-1 * (event.delta / 120), "units")

    def _sidescroll(self, event):
        self.canvas.xview_scroll(-1 * (event.delta / 120), "units")


    def __insertheadings(self, frame, headings, csv_table):
        """
        Insert headings to the table.
        The headings are buttons which can be pressed to order the dates.
        """
        helv36 = tkFont.Font(family='Helvetica', size=8, weight=tkFont.BOLD)

        frame.rowconfigure((0, len(csv_table) + 1), weight=1)  # make buttons stretch when
        frame.columnconfigure((0, len(headings) + 1), weight=1)  # when window is resized

        for j in range(len(headings)):
            button_var = Button()
            heading_button = Tk.Button(frame, text=headings[j], font=helv36, relief='ridge',
                                command=lambda index=j, button=button_var, heading_name=headings[j]: self._sort(
                                    frame=frame, headings=headings, csv_table=csv_table, button=button,
                                    column_index=index, heading_name=heading_name))
            heading_button.grid(row=0, column=j, columnspan=1, sticky='EWNS')
        return

    def __insertelements(self, frame, headings, csv_table):
        """
        Insert the elements to the table
        """
        csv_table, _ = self._deleterows(self.CheckVar, self.column_variables, csv_table)

        element_rows_length = len(csv_table)
        heading_length = len(headings)

        for i in range(element_rows_length):
            for j in range(heading_length):
                element = Tk.Label(frame, text=csv_table[i][j], font='Arial 10', bg='white', relief='groove')
                element.grid(row=i + 1, column=j, columnspan=1, sticky='EWNS')

        #Add the total amount row, showing the total value of all transactions.
        if 'Amount' in headings:
            amount_index = np.where(headings == 'Amount')[0][0]

            # Remove the comma in the numbers in the 'Amount' column and sums the column.
            total = str(sum(list(map(lambda n: float(''.join(n.split(','))), np.transpose(csv_table)[amount_index]))))

            element = Tk.Label(frame, text=total, font='Arial 10 bold', bg='white', relief='groove')
            element.grid(row=element_rows_length+2, column=amount_index, columnspan=1, sticky='EWNS')

            if 'Description' in headings:
                description_index = np.where(headings == 'Description')[0][0]

                element = Tk.Label(frame, text='Total Amount', font='Arial 10 bold', bg='white', relief='groove')
                element.grid(row=element_rows_length+2, column=description_index, columnspan=1, sticky='EWNS')
        return

    def __insertdropdown(self, frame, column, list):
        """
        Inserts a dropdown list
        """
        dropdown_frame = Tk.Label(frame)
        dropdown_frame.grid(row=0, rowspan=1, column=column, sticky='EWNS')

        helv36 = tkFont.Font(family='Helvetica', size=8, weight=tkFont.BOLD)
        column_dropdown = Tk.OptionMenu(dropdown_frame, self.column_dropdown_name, *list, command=lambda _: self.__refresh_optionmenu())
        column_dropdown.config(font=helv36)
        column_dropdown.pack()
        return

    def __insertchecklist(self, frame, column):
        """
        Inserts a checklist at the end of the table.
        """
        self.finalcolumn_frame = Tk.Label(frame)
        self.finalcolumn_frame.grid(row=1, rowspan=5000, column=column, sticky='EWNS')

        self.checklist_frame = Tk.Frame(self.finalcolumn_frame)
        self.CheckVar = self._createchecklist(self.checklist_frame, self.column_variables[1:], default_value=1, CheckVar=self.CheckVar)

        self.untickbutton = Tk.Button(self.finalcolumn_frame, text="Tick/Untick All", command=self.__tickuntickall)

        self.refreshbutton = Tk.Button(self.finalcolumn_frame, text="Refresh", command=self.__refresh)

        self.checklist_frame.pack()
        self.untickbutton.pack()
        self.refreshbutton.pack()
        return

    def __insertfilename(self, frame, column):
        """
        Insert a label displaying the name of .csv file
        """
        filename_label_frame = Tk.Frame(frame)
        filename_label_frame.grid(row=0, rowspan=1, column=column, sticky='EWNS')

        helv36 = tkFont.Font(family='Helvetica', size=8, weight=tkFont.BOLD)
        filename_label = Tk.Label(filename_label_frame, text=self.filename, font=helv36)
        filename_label.pack()
        return

    # def __insertuntickbox(self, frame, column):
    #     """
    #     Inserts a button to untick all boxes in the checklist.
    #     """
    #     untickbox_frame = Tk.Frame(frame)
    #     untickbox_frame.grid(row=1, rowspan=1, column=column, sticky='EWNS')
    #
    #     return

    def __refresh_optionmenu(self):
        """
        This function resets the table checklist when the optionmenu is clicked.
        """
        self.CheckVar = self.__initiateCheckVar()
        for widget in self.finalcolumn_frame.winfo_children():
            widget.destroy()
        self.__updatecolumndropdown()
        self.__insertchecklist(self.frame, len(self.headings) + 1)
        self.window.update()

    def __refresh(self):
        """
        Refreshes the window, jumps to __initwindow() and recreates the table.
        """
        for widget in self.window.winfo_children():
            widget.destroy()
        self.__initwindow()

    def __tickuntickall(self):
        """
        Unticks all boxes in the checklist when the untick box is clicked.
        """
        if len(self.CheckVar) > 0:
            num = self.CheckVar[0].get()
            rev_num = not int(bool(num))
            for i in range(len(self.CheckVar)):
                self.CheckVar[i].set(rev_num)
        return

    def __initiateCheckVar(self):
        """
        Initiate self.CheckVar, needed for _inserteleements()
        """
        CheckVar = []
        temp = Tk.IntVar(self.window)
        temp.set(1)
        CheckVar.append(temp)
        return CheckVar

    def _sort(self, frame, headings, csv_table, button, column_index, heading_name):
        """
        Sort the columns in order
        """

        date_headings = ['Date']
        number_headings = ['CID/Card Number', 'Order No', 'Amount', 'Unit Price', 'Quantity', 'Gross Price']
        text_headings = ['Description', 'Funding', 'Account', 'Activity', 'Document', 'Login', 'First Name',
                         'Surname', 'Email', 'Product Name']

        reverse = button.ascending

        if heading_name in date_headings:
            csv_table = self._timesort(csv_table, column_index=column_index, delimiter='/', reverse=reverse)
        elif heading_name in number_headings:
            csv_table = self._generalnumbersort(csv_table, column_index=column_index, reverse=reverse)
        elif heading_name in text_headings:
            csv_table = sorted(csv_table, key=lambda l: l[column_index], reverse=reverse)
        else:
            return
        self.__insertelements(frame, headings, csv_table)
        Button.reverse(button)
        return

class Button():
    def __init__(self):
        """
        Class to see if the dates have been ordered or reversed.
        """
        self.ascending = False

    def reverse(self):
        """
        This function is used when the date orders had been reversed/ordered
        """
        self.ascending = not self.ascending
        return self.ascending

class CheckButton():
    def __init__(self):
        self.IntVar = Tk.IntVar()

    def get(self):
        return self.IntVar.get()

