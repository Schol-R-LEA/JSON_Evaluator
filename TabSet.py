from tkinter import *
import tkinter as tk
from tkinter import ttk, Label


class TabSet(ttk.Notebook):
    def __init__(self, root, parent):
        super().__init__(root)
        self.root = root
        self.parent = parent
        self.tabEntries = dict()

    def add(self, title, **kwargs):
        if title not in self.tabEntries.keys():
            self.tabEntries[title] = TabEntry(title)
        if "tab" in kwargs.keys():
            if self.tabEntries[title].tab != None:
                raise TabSetDuplicateTabException(title)
            else:
                self.tabEntries[title].tab = kwargs["tab"]
                super().add(self.tabEntries[title].tab, text=title)
        if "subentry" in kwargs.keys():
            self.tabEntries[title].add(kwargs["subentry"])
        if "button_name" in kwargs.keys():
            self.tabEntries[title].subentries[kwargs["button_name"]] = TabSubentry(kwargs["button_name"], kwargs["json_request"], kwargs["expected_response"])




class TabEntry:
    def __init__(self, tab_title):
        self.tab_title = tab_title
        self.tab = None
        self.subentries = dict()
    
    def add(self, subentry):
        if subentry.button_name not in self.subentries.keys():
            self.subentries[subentry.button_name] = subentry
        else:
            raise TabEntryDuplicateSubentryException(self.tab_title, subentry.button_name)


class TabSubentry:
    def __init__(self, button_name, json_request, expected_response):
        self.button_name = button_name
        self.button = None
        self.json_request = json_request
        self.expected_response = expected_response


class TabSetDuplicateTabException(Exception):
    def __init__(self, title):
        self.title = title


class TabEntryDuplicateSubentryException(Exception):
    def __init__(self, title, button):
        self.title = title
        self.button = button


def packTabs(tab_set, test_file):
    """Destructures a list of lines into a collection fo TabEntry objects,
    each of which containing a list of one or more subentries, and
    inserting the entries into a TabSet.
    Returns a list of tab names."""
    tab_titles = list()
    for line in test_file:
        tab_count, tab_title, button_name, json_request, expected_response = line.split('<->')
        tab_title = tab_title.strip()
        tab_set.add(tab_title,
                    button_name=button_name.strip(),
                    json_request=json_request.strip(),
                    expected_response=expected_response.strip())
        if tab_title not in tab_titles:
            tab_titles.append(tab_title)
            tab_set.add(tab_title, tab=tk.Frame(tab_set))
            ttk.Label(tab_set.tabEntries[tab_title].tab, text=tab_title)            
    tab_set.pack(expand=1, fill="both")
    return tab_titles

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Tab Widget")
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry("%dx%d+0+0" % (w, h))
    frame = Label(root, text='')
    frame.pack(side='top', fill='x', expand=False)    
    tabControl = TabSet(root, frame) 
    varconfbook = open("Confs/json_dumps.txt", "r").readlines()
    packTabs(tabControl, varconfbook)
    tabControl.pack(expand=1, fill="both")
    root.mainloop()
