#!/usr/bin/env python
#-*-coding:UTF-8-*-
"""
@Item   :  Rsync Backup
@Author :  Villiam Sheng
@Group  :  Open Group
@Date   :  2016-08-11
@Funtion:
           Check file MD5 value, if the same upload to FTP
"""

from ftplib import FTP  

import ftplib, os,time,sys,traceback,socket,hashlib

host = '192.168.1.1'
name = 'anyween'
pswd = "anyween"
port  = 21
#Source File path
SFILE = '/data/vsftp/club/'
BAKFILE = '/data/vsftp/club_bak/'
#Log path 
LOGFILE = '/var/log/vsftp.upload.log'
#Ftp Timeout 30 
TIMEOUT = 30
ftp = FTP()


class Vsftp(object):
    def __init__ (self):
        version  = 0

    #Log Func, insert info to logfile path 
    def log (self,info):
        if not os.path.exists(LOGFILE):
            os.system("touch %s"%LOGFILE)

        fopen = open(LOGFILE,'a')
        fopen.write("%s INFO  %s \n" %(time.ctime(),info))
        
    #md5 file to src
    def md5file (self,fname):
        filemd5 = ""
        try:
            file = open(fname, "rb")
            md5 = hashlib.md5()
            strs = ""
            while True:
                strs = file.read(8096)
                if not strs:
                    break
                md5.update(strs)
            filemd5 = md5.hexdigest()
            file.close()
            return filemd5
        except Exception,e:
            self.log(traceback.format_exc())
            return False
        
    #Upload file to remote ftp srever 
    def FtpUpload (self):
        try:
            session=ftplib.FTP(host,name ,pswd)
            self.log("%s login ok" % host)
        except:
            self.log("%s login failed" %host)

        try:
            for d  in  os.listdir(SFILE):

                #Md5sum file,mfile: Calculation before
                #mmfile: After the calculation
                fname = "%s%s"%(SFILE,d)
                mfile =  self.md5file(fname)
                time.sleep(3)
                mmfile = self.md5file(fname)

                if mfile == mmfile:
                    files = open(fname,'rb')
                    session.storbinary('STOR '+d,files) 
                    files.close()

                    session.set_debuglevel(0)
                    self.log("Send the file %s successfully" %(fname))
                    os.system("mv %s %s"%(fname, BAKFILE))
                    self.log("Remove local file %s successfully" %fname)
                else:
                    self.log("The file is on the cross,the file is not the same")
                    self.log("file md5 %s, mfile:%s ,mmfile %s"%(fname,mfile,mmfile))
        except:
            self.log(traceback.format_exc())
        
        session.quit()

    
    def work (self):
        self.FtpUpload()

if __name__ == '__main__':
    while True:
        time.sleep(60)
        
        if os.listdir(SFILE):
            start = Vsftp()
            start.work()