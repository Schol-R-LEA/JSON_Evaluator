import os
import time
from tkinter import *
import tkinter as tk
from tkinter import ttk, PhotoImage, LabelFrame, Text, GROOVE, Button, Label, scrolledtext
from tkinter.scrolledtext import ScrolledText
import requests
import json
from xpto.makeReport import savetoxls
from TabSet import *


def tabZeroBanner(tabControl, tab_title, banner_specs):
    frmbtnspecs = ttk.Frame(tabControl.tabEntries[tab_title].tab)
    frmbtnspecs.pack(side="top")
    for box in banner_specs.keys():
        banner_specs[box]["label"] = Label(frmbtnspecs, 
                                           width=banner_specs[box]["width"], 
                                           text="{0}:".format(box), 
                                           justify=RIGHT, 
                                           anchor="e").grid(row=0, 
                                                            column=banner_specs[box]["column"], 
                                                            sticky=W, 
                                                            pady=2)
        banner_specs[box]["textbox"] = Text(frmbtnspecs, height=1, width=35, relief=GROOVE, borderwidth=2).grid(row=0, 
                                                                                                                column=banner_specs[box]["column"]+1, 
                                                                                                                sticky=NW, 
                                                                                                                pady=2)

    frmbtn = ttk.Frame(tabControl.tabEntries[tab_title].tab)
    frmbtn.pack(side="top", expand=1, fill="both")
    return frmbtnspecs, frmbtn

###########################################nova janela####################################

def gera_forms(parent, get_inp_cond_id, get_inp_cond_endpoint):
    parent.pack_forget()

    nome_endpoint, timeoutvar, url_endpoint = get_inp_cond_endpoint.split('<:>')
    nome_endpoint = nome_endpoint.replace('  ', '').strip()
    url_endpoint = url_endpoint.replace(' ', '').strip()
    timeoutvar = timeoutvar.replace(' ', '').strip()

    photoRun = PhotoImage(file=r'img/run.png')
    photoOK = PhotoImage(file=r'img/ok.png')
    photoNot = PhotoImage(file=r'img/notok.png')

    headers = {'Content-Type': 'application/json', 'chargingstation':'stat1'}

    tiporeq = ""
    payload = json.dumps({})
    expResp = ""

    lsttiporeq = []
    lsttitreq = []
    lstjsonreq = []
    lstexpectresq = []

    varconfbook = open("Confs/json_dumps.txt", "r").readlines()
    tabControl = TabSet(tabmain1, frmmain)
    tab_titles = packTabs(tabControl, varconfbook)
    tabControl.pack(expand=1, fill="both")

    def runpost(resp_json,reqtxt,tiporeq):
        try:
            getconfval = reqtxt.get(1.0, "end-1c")
            if len(getconfval)>1:
                resp_json.delete('1.0', END)
                resp_json.insert(tk.INSERT, str(url_endpoint+tiporeq)+", headers="+str(headers)+", data=json.dumps("+str(getconfval)+"), timeout="+str(timeoutvar)+"\n\n\n")
                reqjson = requests.request("POST", str(url_endpoint+tiporeq), headers=headers, data=json.dumps(getconfval), timeout=int(timeoutvar))
                statReason = ("Request:\n\n" + getconfval + "\n\nStatus:\n\n" + str(reqjson.status_code) + " - " + str(reqjson.reason) + "\n\nResponse:\n\n" + str(reqjson.text))
                resp_json.insert(tk.INSERT, statReason)
                
        except Exception as e:
            from OCPP.main import log_error
            resp_json.insert(tk.INSERT, "\n\n"+str(e)+"\n\n")
            log_error(e, "runpost")


    def ChangConfWI(tipreq,reqtxt,lblexp):
        #try:
        reqtxt.delete('1.0', END)
        lblexp.delete('1.0', END)
        reqtxt.insert(tk.INSERT, lstjsonreq[tipreq])
        lblexp.insert(tk.INSERT, str(lstexpectresq[tipreq]))
        #except Exception as e:
        #   from OCPP.main import log_error
        #  log_error(e, "ChangConfWI")


    def makesubmenu(tab_title):
        tab = tabControl.tabEntries[tab_title].tab
        frm_json_case_button = ttk.Frame(tab)
        frm_json_case_button.grid(column=0, row=0, rowspan=99)
        
        frm_txt_json_case = ttk.Frame(tab)
        frm_txt_json_case.grid(column=1, row=0)
        
        url_show=ttk.Label(frm_txt_json_case, text=nome_endpoint + "  @  " + str(url_endpoint + tab_title) + "  @  " + get_inp_cond_id)
        url_show.grid(column=1, row=0, columnspan=99, padx=10, pady=10)
        
        ttk.Label(frm_txt_json_case, text="Request:").grid(column=2, row=1, padx=10, pady=10)
        reqst_input = ScrolledText(frm_txt_json_case, width=75, height=10, wrap=tk.WORD)
        reqst_input.grid(column=2, row=2, padx=10, pady=10, ipady=35)
        
        ttk.Label(frm_txt_json_case, text="Expected Response:").grid(column=2, row=3, rowspan=1, padx=10, pady=10)
        lblexpect = ScrolledText(frm_txt_json_case, width=75, height=10, wrap=tk.WORD)
        lblexpect.grid(column=2, row=4, padx=10, pady=10, ipady=15)
        
        resp_json_input = ScrolledText(frm_txt_json_case, width=75, height=10, wrap=tk.WORD)
        resp_json_input.grid(column=4, row=2, padx=10, pady=10, ipady=35)
        
        ttk.Button(frm_txt_json_case, text="Run", image=photoRun,command=lambda resp_json=resp_json_input, reqtxt=reqst_input, tiporeq=tab_title: runpost(resp_json, reqtxt, tiporeq)).grid(column=3, row=2, padx=10, pady=10, ipady=65)
        ttk.Label(frm_txt_json_case, text="Response:").grid(column=4, row=1, padx=10, pady=10)
        ttk.Label(frm_txt_json_case, text="Response / OBS:").grid(column=3, row=3, columnspan=5, padx=10, pady=10)
        resp_kiblog = ScrolledText(frm_txt_json_case, width=95, height=10)
        resp_kiblog.grid(column=3, row=4, padx=10, columnspan=5, rowspan=10, pady=10, ipady=120)
        
        frm_but_oknot = ttk.Frame(frm_txt_json_case)
        frm_but_oknot.grid(column=2, row=5, padx=1, pady=1)
        
        ttk.Button(frm_but_oknot, width="15", text="OK", image=photoOK, command=lambda: savetoxls(jsonresponse)).grid(column=0, row=0,padx=1, pady=15)
        ttk.Button(frm_but_oknot, width="15", text="Not Ok", image=photoNot).grid(column=1, row=0, padx=1, pady=15)
        
        # generate the column 0 buttons
        for i, button_name in enumerate(tabControl.tabEntries[tab_title].subentries.keys()):
            button = ttk.Button(frm_json_case_button,
                                width="20",
                                text=button_name,
                                command=lambda lblexp=lblexpect, reqtxt=reqst_input, cont=i: ChangConfWI(int(cont),reqtxt,lblexp))
            button.grid(column=0, row=i, padx=10, pady=10)
            tabControl.tabEntries[tab_title].subentries[button_name].button = button


        return reqst_input, lblexpect, resp_json_input,resp_kiblog

    ################################################# tab 0
    banner = {
        "Vendor": {"label": None, "textbox": None, "width": 8, "column": 0},
        "chargeBoxSerialNumber": {"label": None, "textbox": None, "width": 20, "column": 2},
        "Model": {"label": None, "textbox": None, "width": 8, "column": 4},
        "Firmware Version": {"label": None, "textbox": None, "width": 16, "column": 6}
    }

    frmbtnspecs, frmbtn = tabZeroBanner(tabControl, tab_titles[0], banner)


    var_expect_result = open("Confs/expectresult.txt", "r").readlines()
    for coll, line in enumerate(var_expect_result):
            x, y, y1 ,y2 ,y3 ,y4 ,y5 = line.split('<->')
            y_respexpt=(y+"\n\n"+y1+"\n\n"+y2+"\n\n"+y3+"\n\n"+y4+"\n\n"+y5).replace(' ', '').strip()
            lbl = Label(frmbtn, text=x.replace(' ', '').strip()).grid(column=coll, row=0, padx=10, pady=10)
            lbl = Label(frmbtn, text="Response / OBS:").grid(column=coll, row=1, padx=10, pady=10)
            kiblogbn = ScrolledText(frmbtn, width=25, height=20)
            kiblogbn.grid(column=coll, row=2, padx=10, pady=10, ipady=25)
            ttk.Button(frmbtn, width="5", text="OK", image=photoOK).grid(column=coll, row=3, padx=1, pady=1)
            ttk.Button(frmbtn, width="5", text="Not Ok", image=photoNot).grid(column=coll, row=4, padx=1, pady=1)
            lblspec = Label(frmbtn, text=y_respexpt, justify='left', anchor=N)
            lblspec.grid(column=coll, row=5, rowspan=55, sticky=N, padx=20, pady=20)

    for i in range(1, len(tab_titles)):
        makesubmenu(tab_titles[i])

###########################################FIM nova janela####################################

if __name__ == "__main__":
    tabmain1 = Tk()
    w, h = tabmain1.winfo_screenwidth(), tabmain1.winfo_screenheight()
    tabmain1.geometry("%dx%d+0+0" % (w, h))

    frmmain = Label(tabmain1, text='')
    frmmain.pack(side='top', fill='x', expand=False)

    gera_forms(frmmain, "stat1","nome_end<:>30<:>http://something.com/?")

    tabmain1.mainloop()
