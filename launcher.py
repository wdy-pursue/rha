import os
import subprocess
import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
import json
import sys
import shutil
from ttkbootstrap import Style
import tkinter.messagebox as msgbox
from bin.args_test import args_test
import io
import base64
from PIL import Image

def read_image(image_path):
    # 读取图片数据并返回
    with open(image_path, 'rb') as file:
        return file.read()

def write_image(image_path, data):
    # 将数据写入图片文件
    with open(image_path, 'wb') as file:
        file.write(data)


style = Style(theme='cosmo')
default_arg = {
    "configjson": "高清化test",
    "redraw_methods": 0,
    "redrawcamplitude": "0.4",
    "fixcount": 5,
    "control_methods": 1,
    "style":"cosmo"
}

try:
    f = open('launcher.json',encoding='utf8')
    args = json.load(f)
    default_arg.update(args)
    f.close()
except:
    pass
finally:
    args = default_arg
print("这个窗口是程序主窗口，请勿关闭")
t = 0
p = None
facecap=None
S_keys_input = ""
configdirPath = 'config'
is_4k = 0

configList = []
for item in sorted(os.listdir(configdirPath), key=lambda x: -os.path.getmtime(os.path.join(configdirPath, x))):
    if '.json' == item[-5:]:
        configList.append(item[:-5])
root = style.master
#root = tk.Tk()
root.resizable(False, False)
root.geometry('380x400+100+100')
root.title('Launcher')



theme_names = style.theme_names()#以列表的形式返回多个主题名
theme_selection = ttk.Frame(root, padding=(10, 10, 10, 0))
theme_selection.pack(fill='x', expand='YES')
lbl = ttk.Label(theme_selection, text="窗口主题:")
theme_cbo = ttk.Combobox(
        master=theme_selection,
        text=style.theme.name,
        values=theme_names,
)
theme_cbo.pack(padx=10, side='right')
style_name = args['style']
theme_cbo.current(theme_names.index(style_name))

theme_cbo_value = style_name
style.theme_use(theme_cbo_value)
theme_cbo.selection_clear()
    
lbl.pack(side='right')
def change_theme(event):
    theme_cbo_value = theme_cbo.get()
    style.theme_use(theme_cbo_value)
    theme_selected.configure(text="大鹅猫")
    theme_cbo.selection_clear()
theme_cbo.bind('<<ComboboxSelected>>', change_theme)


theme_selected = ttk.Label(
        master=theme_selection,
        text="大鹅猫",
        font="-size 24 -weight bold"
)
theme_selected.pack(side='left')





launcher = ttk.Frame(root)
launcher.pack(fill='x', expand=True)


def launch():
        global t

        args = {
            'configjson': configs.get(),
            'redraw_methods':redraw_methods.get(),
            'redrawcamplitude':redrawcamplitudetxt.get(),
            'fixcount': fixcounttxt.get(),
            'control_methods': control_methods.get(),
            'style': theme_cbo.get()
        }

        f = open('launcher.json', mode='w')
        json.dump(args, f)
        f.close()

#        run_args = [sys.executable, 'main.py']
        run_args = ['api/python.exe','main.py']
        run_args.append('--configjson')
        run_args.append(str(args['configjson']))
        run_args.append('--redraw_methods')
        run_args.append(str(args['redraw_methods']))
        run_args.append('--redrawcamplitude')
        run_args.append(str(args['redrawcamplitude']))
        run_args.append('--fixcount')
        run_args.append(str(args['fixcount']))
        run_args.append('--control_methods')
        run_args.append(str(args['control_methods']))
        run_args.append('--t')
        run_args.append(str(t))
        subprocess.Popen(run_args)

def open_config():
    start_directory = 'config'
    os.system("explorer.exe %s" % start_directory)


def redraw():
    global t
    t = 0
    launch()

def highdefinition():
    global t
    t = 1
    launch()

def reduce():
    resourcepath = "./缩放区/待缩放/"
    resultpath = "./草图/"
    for dirpath, dirnames, filenames in os.walk(resourcepath):
        for filepath in filenames:
            png_path = os.path.join(dirpath, filepath)
            basename = os.path.basename(dirpath)
            img = Image.open(png_path)
            # 缩小图片
            width, height = img.size
            img = img.resize((int(width / 2), int(height / 2)))
            # 保存图片
            if not os.path.exists(os.path.join(resultpath,basename)):
                os.makedirs(os.path.join(resultpath,basename))
            img.save(os.path.join(resultpath,basename,filepath))
    shutil.rmtree(resourcepath)
    os.makedirs(resourcepath)
    print("缩放完成")
open_png_btn = ttk.Button(launcher, text="打开配置文件夹",command=open_config)
open_png_btn.pack(side='bottom', fill='x', expand=True,  pady=5, padx=5)


open_emotions_btn = ttk.Button(launcher, text="开始高清化", command=highdefinition)
open_emotions_btn.pack(side='bottom', fill='x', expand=True,  pady=5, padx=5)

frameU = ttk.Frame(launcher)
frameU.pack(padx=10, pady=10, fill='both', side='top', expand=True)
frameB = ttk.Frame(launcher)
frameB.pack(padx=10, pady=10, fill='both', side='bottom', expand=True)
frameL = ttk.Frame(launcher)
frameL.pack(padx=10, pady=10, fill='both', side='left', expand=True)
frameR = ttk.Frame(launcher)
frameR.pack(padx=10, pady=10, fill='both', side='right', expand=True)

def on_select(event):
    S_keys_input = event.widget.get()

configs = tk.StringVar(value = args['configjson'])
ttk.Label(frameU, text="配置文件列表").pack(fill='x', expand=True)
config_combo = ttk.Combobox(frameU, textvariable=configs, value=configList)
config_combo.pack(fill='x', expand=True)
config_combo.bind("<<ComboboxSelected>>", on_select)

ttk.Label(frameU, text="高清化参数").pack(fill='x', expand=True)

ttk.Label(frameL, text="重绘幅度两种模式").pack(fill='x', expand=True)

redraw_methods = tk.IntVar(value=args['redraw_methods'])
ttk.Radiobutton(frameL, text='固定数值', value=0, variable=redraw_methods).pack(fill='x', expand=True)
ttk.Radiobutton(frameL, text='区间递增', value=1, variable=redraw_methods).pack(fill='x', expand=True)

ttk.Label(frameL, text="重绘幅度数值（或区间）").pack(fill='x', expand=True)

redrawcamplitudetxt = tk.StringVar(value=args['redrawcamplitude'])
redrawcamplitudeEnt = ttk.Entry(frameL, textvariable=redrawcamplitudetxt, state=False)
redrawcamplitudeEnt.pack(fill='x', expand=True)


ttk.Label(frameR, text="生成的张数").pack(fill='x', expand=True)

fixcounttxt = tk.IntVar(value=args['fixcount'])
fixcountEnt = ttk.Entry(frameR, textvariable=fixcounttxt, state=False)
fixcountEnt.pack(fill='x', expand=True)


ttk.Label(frameR, text="控制方法").pack(fill='x', expand=True)

control_methods = tk.IntVar(value=args['control_methods'])
ttk.Radiobutton(frameR, text='均衡', value=0, variable=control_methods).pack(fill='x', expand=True)
ttk.Radiobutton(frameR, text='更偏向提示词', value=1, variable=control_methods).pack(fill='x', expand=True)
ttk.Radiobutton(frameR, text='更偏向controlnet', value=2, variable=control_methods).pack(fill='x', expand=True)

def closeWindow():
    if p is not None:
        subprocess.run(['taskkill', '/F', '/PID', str(p.pid), '/T'], stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL)
    root.destroy()

def handle_focus_emotions(event):
    configList = []
    if event.widget == root:
        for item in sorted(os.listdir(configdirPath), key=lambda x: -os.path.getmtime(os.path.join(configdirPath, x))):
            if '.json' == item[-5:]:
                configList.append(item[:-5])
        config_combo.config(value=configList)
root.resizable(True, True)
root.bind("<FocusIn>", handle_focus_emotions)
root.protocol('WM_DELETE_WINDOW', closeWindow)
root.mainloop()
