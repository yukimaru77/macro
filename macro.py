import subprocess
import os
import cmd
import re
import subprocess
import sys
import datetime
import time
import cv2
import numpy as np
from subprocess import PIPE

def get_devices_id(*args):
    Nox_Ids=[]
    for i in args:
      subprocess.Popen(f"Nox.exe -clone:Nox_{i}", shell=True)
      time.sleep(3)#デーモンが起動していない時のadb devicesのエラーを防ぐ。
      proc = subprocess.run("adb devices", shell=True,stdout=PIPE, stderr=PIPE, text=True)

      id=proc.stdout.split("\n")[1]
      while id==proc.stdout.split("\n")[1]:
          print(id)
          proc = subprocess.run("adb devices", shell=True,stdout=PIPE, stderr=PIPE, text=True)
          time.sleep(1)
      id=proc.stdout.split("\n")[1].replace("\tdevice","")
      Nox_Ids.append(id)
      time.sleep(5)
    print(Nox_Ids)
    return Nox_Ids

class Nox():
    pics={}
    def __init__(self, id):
        self.id=id
        self.x=0
        self.y=0
        self.cache=0

    def touch(self,x=-100,y=-100,t=60,sleep_time=0.5):
      if(x==-100):
        x=self.x
      if(y==-100):
        y=self.y

      subprocess.call(f"adb -s {self.id} shell input touchscreen swipe {x} {y} {x} {y} {t}", shell=True)
      time.sleep(sleep_time)
    
    def swipe(self,x1,y1,x2,y2,t):

        subprocess.call(f"adb -s {self.id} shell input touchscreen swipe {x1} {y1} {x2} {y2} {t}", shell=True)

    def screencap(self,file_name):
        subprocess.call(f"adb -s {self.id} shell screencap -p /sdcard/{file_name}{self.id.split(':')[1]}.png", shell=True)
        subprocess.call(f"adb -s {self.id} pull /sdcard/{file_name}{self.id.split(':')[1]}.png", shell=True)

    def app_start(self, app="jp.co.mixi.monsterstrike/.SplashActivity"):
        subprocess.call(f"adb -s {self.id} shell am start -n {app}", shell=True)

    def app_end(self, app="jp.co.mixi.monsterstrike"):
        subprocess.call(f"adb -s {self.id} shell am force-stop {app}", shell=True)

    def send_file(self, local_file_path, device_file_path):
        subprocess.call(f'adb -s {self.id} push "{local_file_path}" "{device_file_path}"', shell=True)

    def chage(self,i,j):
        self.send_file(f"C:\\Users\\yukit\\data\\data{i}\\{j}\\data10.bin","/data/data/jp.co.mixi.monsterstrike/")
    def send_event_from_file(self, path):
        ABS_MT_POSITION_X = 53
        ABS_MT_POSITION_Y = 54
        BTN_TOUCH = 330 #ちなみに最後の項が0ならDOWN、0ならUP
        V_INPUT = "/dev/input/event4"
        r = re.compile(r'\[   ([0-9\.]+)\] ([0-9a-f]+) ([0-9a-f]+) ([0-9a-f]+)') #getevent -t のログを解析するための正規表現
        text_file = open(path, "rt")
        cmd_strs=[]
        tmp=0
        before_time=0
        for line in text_file:
            m = r.search(line)
            if m:
              if tmp==0:
                before_time=float(m.group(1))
                tmp=1

              # イベント抽出 & 10進に変換
              match_type = int(m.group(2), 16)
              match_event = int(m.group(3), 16)
              match_value = int(m.group(4), 16)
              if match_event == BTN_TOUCH:
                wait_time= float(m.group(1))-before_time
                before_time= float(m.group(1))
                cmd_strs.append(wait_time)
              # イベント生成
              cmd_strs.append(f"adb -s {self.id} shell sendevent {V_INPUT} {match_type} {match_event} {match_value}")

        dt_now = datetime.datetime.now()
        for cmd_str in cmd_strs:
            if type(cmd_str)==str:
              subprocess.call(cmd_str, shell=True)
            else:
              dt_next = dt_now + datetime.timedelta(microseconds=int(cmd_str*1000000))
              diff = (dt_next-dt_now).microseconds - (datetime.datetime.now()-dt_now).microseconds #dt_nowをひかないと自国の桁上りが偶然重なると条件がバグる
              if diff > 0:
                time.sleep(float(diff)/1000000)
              dt_now = datetime.datetime.now()

    """def is_img(self,path,threshold,center=False,cap_cache=False,cache=False):
        print("aaaaaaaaaaaa")
        if(cache==False):
          subprocess.call(f"adb -s {self.id} shell screencap -p /sdcard/screen.png", shell=True)
          subprocess.call(f"adb -s {self.id} pull /sdcard/screen.png", shell=True)
          if(cap_cache==True):
            subprocess.call(f"adb -s {self.id} shell screencap -p /sdcard/screen{self.id.split(':')[1]}.png", shell=True)
            subprocess.call(f"adb -s {self.id} pull /sdcard/screen{self.id.split(':')[1]}.png", shell=True)
            self.cache=cv2.cvtColor(cv2.imread(f"cache/screen{self.id.split(':')[1]}.png"), cv2.COLOR_BGR2GRAY)
          img_rgb = cv2.imread('screen.png')
          #img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
          template = cv2.imread(path,0)
          res = cv2.matchTemplate(img_rgb,template,cv2.TM_CCOEFF_NORMED)
          loc = np.where( res >= threshold)
          print(np.amax(res)>=threshold)
          if np.amax(res)>=threshold:
              loc=np.where(res==np.amax(res))[::-1]
              for pt in zip(*loc):
                if center==False:
                  h, w = template.shape
                  self.x,self.y=pt[0]+w/2,pt[1]+h/2
                else:
                  self.x,self.y=pt
                break
              return True
          else:
              self.x,self.y=[0,0]
              return False
        else:
          template = cv2.imread(path,0)
          res = cv2.matchTemplate(self.cache,template,cv2.TM_CCOEFF_NORMED)
          loc = np.where( res >= threshold)
          if np.amax(res)>=threshold:
              loc=np.where(res==np.amax(res))[::-1]
              for pt in zip(*loc):
                if center==False:
                  h, w = template.shape
                  self.x,self.y=pt[0]+w/2,pt[1]+h/2
                else:
                  self.x,self.y=pt
                break
              return True
          else:
              self.x,self.y=[0,0]
              return False"""
    def is_img(self,path,threshold,x1=0,y1=0,x2=599,y2=999,center=False):
      print(len(Nox.pics))
      if  path is not Nox.pics:
        template = cv2.imread("pictures/"+path)
        template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        Nox.pics.update({path : template})
      else:
        template = Nox.pics[path]
        print("キャッシュ")
      subprocess.call(f"adb -s {self.id} shell screencap -p /sdcard/screen.png", shell=True)
      subprocess.call(f"adb -s {self.id} pull /sdcard/screen.png pictures/", shell=True)
      img_rgb = cv2.imread("pictures/"+'screen.png')
      img_rgb = img_rgb[y1:y2, x1:x2, : ]
      img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
      #print(path)

      res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
      loc = np.where( res >= threshold)
      #print(np.amax(res)>=threshold)
      if np.amax(res)>=threshold:
          loc=np.where(res==np.amax(res))[::-1]
          for pt in zip(*loc):
            if center==False:
              h, w = template.shape
              self.x,self.y=pt[0]+w/2+x1,pt[1]+h/2+y1
            else:
              self.x,self.y=pt[0]+x1,pt[1]+y1
            break
          return True
      else:
          self.x,self.y=[0,0]
          return False

    def img_touch(self,path,threshold,x1=0,y1=0,x2=599,y2=999,center=False,sleep_time=0.5):
      print(len(Nox.pics))
      if  path is not Nox.pics:
        template = cv2.imread("pictures/"+path)
        template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        Nox.pics.update({path : template})
      else:
        template = Nox.pics[path]
        print("キャッシュ")
      subprocess.call(f"adb -s {self.id} shell screencap -p /sdcard/screen.png", shell=True)
      subprocess.call(f"adb -s {self.id} pull /sdcard/screen.png pictures/", shell=True)
      img_rgb = cv2.imread("pictures/"+'screen.png')
      img_rgb = img_rgb[y1:y2, x1:x2, : ]
      img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
      #print(path)
      res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
      loc = np.where( res >= threshold)
      #print(np.amax(res)>=threshold)
      if np.amax(res)>=threshold:
          loc=np.where(res==np.amax(res))[::-1]
          for pt in zip(*loc):
            if center==False:
              h, w = template.shape
              self.x,self.y=pt[0]+w/2+x1,pt[1]+h/2+y1
            else:
              self.x,self.y=pt[0]+x1,pt[1]+y1
            break
          self.touch(sleep_time=sleep_time)
          return True
      else:
          self.x,self.y=[0,0]
          return False

class Nox_devices():
    def __init__(self,*args):
       self.devices=args
    
    def touch(self,x=-100,y=-100,t=60,sleep_time=0.5):
        for i in self.devices:
          i.touch(x,y,t,sleep_time)
    def swipe(self,x1,y1,x2,y2,t):
        for i in self.devices:
          i.swipe(x1,y1,x2,y2,t)
    def screencap(self,file_name):
        for i in self.devices:
          i.screencap(file_name)
    def app_start(self, app="jp.co.mixi.monsterstrike/.SplashActivity"):
        for i in self.devices:
          i.app_start(app)
    def app_end(self, app="jp.co.mixi.monsterstrike"):
        for i in self.devices:
          i.app_end(app)     
    def send_file(self, local_file_path, device_file_path):
        for i in self.devices:
          i.send_file(local_file_path, device_file_path)
    def chage(self,i,j):      
        for k in self.devices:
          k.chage(i,j)
          j=j+1 #binをずらす
    def send_event_from_file(self, path):
        for i in self.devices:
          i.send_event_from_file(path)      
    def is_img(self,path,threshold,x1=0,y1=0,x2=600,y2=1001,center=False):
        check=[]
        for i in self.devices:
          check.append(i.is_img(path,threshold,x1,y1,x2,y2,center))
        return check    
    def img_touch(self,path,threshold,x1=0,y1=0,x2=600,y2=1001,center=False,sleep_time=0.5):
        check=[]
        for i in self.devices:
          check.append(i.img_touch(path,threshold,x1,y1,x2,y2,center,sleep_time))
        return check   