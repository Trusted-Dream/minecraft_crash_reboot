import subprocess as prc
import re
import time
import os
import sys
import concurrent.futures
import tkinter as tk
import socket

class Minecraft():

    def __init__(self):
        self.dir = os.path.dirname(os.path.abspath(__file__)) + '\\'
        self.setting_file = self.dir + "setting.txt"
        self.log_file = self.dir + "crash_log.txt"

    def settings(self):
        self.root = tk.Tk()
        self.root.title(u"バッチファイル名を入力")
        self.root.geometry("400x100")

        msg = (
            u'バッチファイル名を入力してください。\n尚、'
            'このファイルはバッチファイルと同じ位置に設置してください。'
        )

        self.Label = tk.Label(text=msg)
        self.Label.pack()

        self.EditBox = tk.Entry(width=500)
        self.EditBox.insert(tk.END,"start.bat")
        self.EditBox.pack()
    
        self.Button = tk.Button(text="OK",command=self.tkinter_action,width=10)
        self.Button.pack()
        self.root.mainloop()

    def tkinter_action(self):
        self.input_msg = self.EditBox.get()
        self.root.destroy()

    def proc_check(self):
        cmd = 'tasklist |findstr "java" |findstr -v "javaw"'
        tasklist = prc.Popen(cmd, shell=True, stdout=prc.PIPE)
        output = tasklist.communicate()[0].decode('utf-8').split()
        if output != []:
            return output[1]

    def port_check(self):
        pid = self.proc_check()
        if pid == None:
            return None
        cmd = f'netstat -nao |findstr "0.0.0.0" |findstr {pid}'
        port = prc.Popen(cmd, shell=True, stdout=prc.PIPE)
        try:
            output = port.communicate()[0].decode('utf-8').split()[1].split(':')[1]
        except:
            return None
        return output
        
def main():
    mic = Minecraft()
    if not os.path.isfile(mic.log_file):
        with open(mic.log_file, mode="w"):pass
    if not os.path.isfile(mic.setting_file):
        mic.settings()
        batch_name = mic.input_msg
        with open(mic.setting_file, mode="w") as f: f.write(mic.dir + batch_name)
        
    with open(mic.setting_file, mode="r") as f: batch_name = f.read()
    
    while True:
        check = mic.port_check()
        if check == None:
            error_time = time.strftime("%Y/%m/%d %H:%M:%S ", time.strptime(time.ctime()))
            error_msg = f"{error_time} --- サーバダウンを検知したため、再起動実施しました。\n"
            prc.Popen("taskkill /F /IM cmd.exe", shell=True, stdout=prc.PIPE)
            time.sleep(1)
            prc.Popen("start " + batch_name, shell=True, stdout=prc.PIPE)
            for i in range(60):
                check = mic.port_check()
                if check != None: break
                time.sleep(1)
            else:
                error_msg = f"{error_time} --- サーバ再起動に失敗しました。プログラムを終了します。\n"
                with open(mic.log_file, mode="a") as f: f.write(error_msg)
                print (error_msg,end="")
                sys.exit()
                
            with open(mic.log_file, mode="a") as f: f.write(error_msg)
            print (error_msg,end="")
            time.sleep(30)
            
        time.sleep(10)
    
if __name__ == "__main__":
    main()
