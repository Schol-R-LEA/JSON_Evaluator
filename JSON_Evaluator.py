import os
import time
from tkinter import *
import tkinter as tk
from tkinter import ttk, PhotoImage, LabelFrame, Text, GROOVE, Button, Label, scrolledtext
from tkinter.scrolledtext import ScrolledText
import requests
import json


global get_inp_cond_endpoint, get_inp_cond_id
tabmain1 = Tk()
w, h = tabmain1.winfo_screenwidth(), tabmain1.winfo_screenheight()
tabmain1.geometry("%dx%d+0+0" % (w, h))


frmmain = Label(tabmain1, text='')
frmmain.pack(side='top', fill='x', expand=False)
###########################################nova janela####################################

def gera_forms(get_inp_cond_id, get_inp_cond_endpoint):

    nome_endpoint, timeoutvar, url_endpoint = get_inp_cond_endpoint.split('<:>')
    nome_endpoint = nome_endpoint.replace('  ', '').strip()
    url_endpoint = url_endpoint.replace(' ', '').strip()
    timeoutvar = timeoutvar.replace(' ', '').strip()


    photRun = PhotoImage(file=r'img/run.png')
    photoOK = PhotoImage(file=r'img/ok.png')
    photoNot = PhotoImage(file=r'img/notok.png')

    headers = {'Content-Type': 'application/json', 'chargingstation':'stat1'}

    tiporeq = ""
    payload = json.dumps({})
    expResp = ""

    varconfbook = open("Confs/json_dumps.txt", "r").readlines()
    lsttiporeq = []
    lsttitreq = []
    lstjsonreq = []
    lstexpectresq = []




    def makesubmenu(tipo_de_conf, framename):
        cont = 0
        rowcont=0

        frm_json_case_button = ttk.Frame(framename)
#        frm_json_case_button.grid(column=0, row=0, rowspan=99)

        frm_txt_json_case = ttk.Frame(framename)
#        frm_txt_json_case.grid(column=1, row=0)

        url_show=ttk.Label(frm_txt_json_case, text=nome_endpoint + "  @  " + str(url_endpoint + tipo_de_conf) + "  @  " + get_inp_cond_id)
#        url_show.grid(column=1, row=0, columnspan=99, padx=10, pady=10)

        ttk.Label(frm_txt_json_case, text="Request:").grid(column=2, row=1, padx=10, pady=10)
        reqst_input = ScrolledText(frm_txt_json_case, width=75, height=10, wrap=tk.WORD)
#        reqst_input.grid(column=2, row=2, padx=10, pady=10, ipady=35)

        ttk.Label(frm_txt_json_case, text="Expected Response:").grid(column=2, row=3, rowspan=1, padx=10, pady=10)
        lblexpect = ScrolledText(frm_txt_json_case, width=75, height=10, wrap=tk.WORD)
#        lblexpect.grid(column=2, row=4, padx=10, pady=10, ipady=15)



        resp_json_input = ScrolledText(frm_txt_json_case, width=75, height=10, wrap=tk.WORD)
#        resp_json_input.grid(column=4, row=2, padx=10, pady=10, ipady=35)
        ttk.Button(frm_txt_json_case, text="Run", image=photRun,command=lambda resp_json=resp_json_input, reqtxt=reqst_input, tiporeq=tipo_de_conf: runpost(resp_json, reqtxt, tiporeq)).grid(column=3, row=2, padx=10, pady=10, ipady=65)
        ttk.Label(frm_txt_json_case, text="Response:").grid(column=4, row=1, padx=10, pady=10)

        ttk.Label(frm_txt_json_case, text="Response / OBS:").grid(column=3, row=3, columnspan=5, padx=10, pady=10)
        resp_kiblog = ScrolledText(frm_txt_json_case, width=95, height=10)
        resp_kiblog.grid(column=3, row=4, padx=10, columnspan=5, rowspan=10, pady=10, ipady=120)

        frm_but_oknot = ttk.Frame(frm_txt_json_case)
        frm_but_oknot.grid(column=2, row=5, padx=1, pady=1)

        ttk.Button(frm_but_oknot, width="15", text="OK", image=photoOK, command=lambda: savetoxls(jsonresponse)).grid(column=0, row=0,padx=1, pady=15)
        ttk.Button(frm_but_oknot, width="15", text="Not Ok", image=photoNot).grid(column=1, row=0, padx=1, pady=15)


        for line in varconfbook:
            if tipo_de_conf in line:
                tabbxx, tiporeq, titreq, jsonreq, expectresq = line.split('<->')
                lsttiporeq.append(tiporeq)
                lsttitreq.append(titreq)
                lstjsonreq.append(jsonreq)
                lstexpectresq.append(expectresq)

                ttk.Button(frm_json_case_button, width="20", text=titreq, command=lambda lblexp=lblexpect, reqtxt=reqst_input, cont=cont: ChangConfWI(int(cont),reqtxt,lblexp)).grid(column=0, row=rowcont, padx=10, pady=10)
                rowcont += 1

            cont += 1

        return lsttiporeq, lsttitreq, lstjsonreq, lstexpectresq, reqst_input, lblexpect, resp_json_input,resp_kiblog



    def ChangConfWI(tipreq,reqtxt,lblexp):
    #try:
        reqtxt.delete('1.0', END)
        lblexp.delete('1.0', END)
        reqtxt.insert(tk.INSERT, lstjsonreq[tipreq])
        lblexp.insert(tk.INSERT, str(lstexpectresq[tipreq]))
    #except Exception as e:
     #   from OCPP.main import log_error
      #  log_error(e, "ChangConfWI")>


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



#######Gera tabuladores##################################
    tabControl = ttk.Notebook(tabmain1)


    style = ttk.Style()
    style.theme_create("stl_obrigator", parent="alt", settings={
        "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0]}},
        "TNotebook.Tab": {
            "configure": {"padding": [5, 1], "background": "#fd6262"},
            "map": {"background": [("selected", "#fd2b2b")],
                    "expand": [("selected", [1, 1, 1, 0])]}}})

    style.theme_create("stl_facult", parent="alt", settings={
        "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0]}},
        "TNotebook.Tab": {
            "configure": {"background": "#62fd72"},
            "map": {"background": [("selected", "#02d417")],
                    "expand": [("selected", [1, 1, 1, 0])]}}})

    style.theme_use("stl_obrigator")
    tab0 = ttk.Frame(tabControl)
    tabControl.add(tab0, text="Messages")

    lst_menu= []
    lst_tipo=[]
    for line in varconfbook:
        if len(line) > 1:
#            aaaaaa, tipo,nome,bbbbb,ccccc,ddddddd = line.split('<->')
            aaaaaa, tipo,nome,bbbbb,ccccc = line.split('<->')
            if nome not in lst_menu:
                lst_menu.append(nome)
                lst_tipo.append(tipo)


    x = 0
    tab1 = None
    tab2 = None
    tab3 = None
    tab4 = None
    tab5 = None
    tab6 = None
    tab7 = None
    tab8 = None
    tab9 = None
    tab10 = None
    tab11 = None
    tab12 = None
    tab13 = None

    for nome,tipo in zip(lst_menu, lst_tipo):
        if "Obrigatorio" in tipo:
            style.theme_use("stl_obrigator")
        else:
            style.theme_use("stl_facult")

        if x == 1:
            tab1 = ttk.Frame(tabControl)
            tabControl.add(tab1, text=nome.strip())
            tabControl.pack(expand=1, fill="both")
            makesubmenu(nome.strip(), tab1)
        elif x == 2:
            tab2 = ttk.Frame(tabControl)
            tabControl.add(tab2, text=nome.strip())
            tabControl.pack(expand=1, fill="both")
            makesubmenu(nome.strip(), tab2)

        elif x == 3:
            tab3 = ttk.Frame(tabControl)
            tabControl.add(tab3, text=nome.strip())
            tabControl.pack(expand=1, fill="both")
            makesubmenu(nome.strip(), tab3)

        elif x == 4:
            tab4 = ttk.Frame(tabControl)
            tabControl.add(tab4, text=nome.strip())
            tabControl.pack(expand=1, fill="both")
            makesubmenu(nome.strip(), tab4)

        elif x == 5:
            tab5 = ttk.Frame(tabControl)
            tabControl.add(tab5, text=nome.strip())
            tabControl.pack(expand=1, fill="both")
            makesubmenu(nome.strip(), tab5)

        elif x == 6:
            tab6 = ttk.Frame(tabControl)
            tabControl.add(tab6, text=nome.strip())
            tabControl.pack(expand=1, fill="both")
            makesubmenu(nome.strip(), tab6)

        if x == 7:
            tab7 = ttk.Frame(tabControl)
            tabControl.add(tab7, text=nome.strip())
            tabControl.pack(expand=1, fill="both")
            makesubmenu(nome.strip(), tab7)

        elif x == 8:
            tab8 = ttk.Frame(tabControl)
            tabControl.add(tab8, text=nome.strip())
            tabControl.pack(expand=1, fill="both")
            makesubmenu(nome.strip(), tab8)

        elif x == 9:
            tab9 = ttk.Frame(tabControl)
            tabControl.add(tab9, text=nome.strip())
            tabControl.pack(expand=1, fill="both")
            makesubmenu(nome.strip(), tab9)

        elif x == 10:
            tab10 = ttk.Frame(tabControl)
            tabControl.add(tab10, text=nome.strip())
            tabControl.pack(expand=1, fill="both")
            makesubmenu(nome.strip(), tab10)

        elif x == 11:
            tab11 = ttk.Frame(tabControl)
            tabControl.add(tab11, text=nome.strip())
            tabControl.pack(expand=1, fill="both")
            makesubmenu(nome.strip(), tab11)

        elif x == 12:
            tab12 = ttk.Frame(tabControl)
            tabControl.add(tab12, text=nome.strip())
            tabControl.pack(expand=1, fill="both")
            makesubmenu(nome.strip(), tab12)

        elif x == 13:
            tab13 = ttk.Frame(tabControl)
            tabControl.add(tab13, text=nome.strip())
            tabControl.pack(expand=1, fill="both")
            makesubmenu(nome.strip(), tab13)

        elif x > 13:
            messagebox.showinfo("Menu Testes OCPP", "Nao é possivel adicionar mais tabuladores.\n\n o numero maximo de tabuladores permitidos é 13, \n\n por favor reveja o seu ficheiro de configuracao (json_dumps.txt)")
            tabControl.update()
            break
        x += 1

############################################################################################################


    ################################################# tab1

    frmbtnspecs = ttk.Frame(tab1)
#    frmbtnspecs.pack(side="top")

    lbl = Label(frmbtnspecs, width=8, text="Vendor:", justify=RIGHT, anchor="e").grid(row=0, column=0, sticky=W, pady=2)
    inp_cond_vendor = Text(frmbtnspecs, height=1, width=35, relief=GROOVE, borderwidth=2)
    inp_cond_vendor.grid(row=0, column=1, sticky=NW, pady=2)

    lbl = Label(frmbtnspecs, width=20, text="chargeBoxSerialNumber:", justify=RIGHT, anchor="e").grid(row=0, column=2, sticky=W, pady=2)
    inp_cond_sn = Text(frmbtnspecs, height=1, width=35, relief=GROOVE, borderwidth=2)
    inp_cond_sn.grid(row=0, column=3, sticky=NW, pady=2)

    lbl = Label(frmbtnspecs, width=8, text="Model:", justify=RIGHT, anchor="e").grid(row=0, column=4, sticky=W, pady=2)
    inp_cond_model = Text(frmbtnspecs, height=1, width=35, relief=GROOVE, borderwidth=2)
    inp_cond_model.grid(row=0, column=5, sticky=NW, pady=2)
    lbl = Label(frmbtnspecs, width=16, text="Firmware Version:", justify=RIGHT, anchor="e").grid(row=0, column=6, sticky=W, pady=2)
    inp_cond_firmware = Text(frmbtnspecs, height=1, width=35, relief=GROOVE, borderwidth=2)
    inp_cond_firmware.grid(row=0, column=7, sticky=NW, pady=2)

    frmbtn = ttk.Frame(tab1)
#    frmbtn.pack(side="top", expand=1, fill="both")

    coll = int(0)
    specvar = int(1)

    var_expect_result = open("Confs/expectresult.txt", "r").readlines()
    for line in var_expect_result:
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
            coll += 1
            specvar += 1






    ########## FIM tab1 ################ FIM tab1 ################ FIM tab1 ############ FIM tab1 ############ FIM tab1




    makesubmenu("Change",tab2)

    makesubmenu("Cache",tab3)

    makesubmenu("Get",tab4)

    makesubmenu("something", tab5)





###########################################FIM nova janela####################################
gera_forms("stat1","nome_end<:>30<:>http://something.com")

if __name__ == "__main__":
    tabmain1.mainloop()
