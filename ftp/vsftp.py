#!/usr/bin/env python
#-*-coding:UTF-8-*-
"""
@Item   :  Rsync Backup
@Author :  Villiam Sheng
@Group  :  System Group
@Date   :  2016-08-11
@Funtion:
           Check file MD5 value, if the same upload to FTP
"""

from ftplib import FTP  

import ftplib, os,time,sys,traceback,socket,hashlib

host = '192.168.10.100'
name = 'autohome'
pswd = "3e25cbe5f"
port  = 21
#Source File path
SFILE = '/data/vsftp/club/'
BAKFILE = '/data/vsftp/club_bak/'
#Log path 
LOGFILE = '/var/log/vsftp.upload.log'
#Ftp Timeout 30 
TIMEOUT = 30
ftp = FTP()

def LOG (info):
    if not os.path.exists(LOGFILE):
        os.system("touch %s"%LOGFILE)

    fopen = open(LOGFILE,'a')
    fopen.write("%s INFO  %s \n" %(time.ctime(),info))

class Vsftp(object):
    def __init__ (self):
        version  = 0

    #Log Func, insert info to logfile path 
    def log (self,info):
        if not os.path.exists(LOGFILE):
            os.system("touch %s"%LOGFILE)

        fopen = open(LOGFILE,'a')
        fopen.write("%s INFO  %s \n" %(time.ctime(),info))
        
 
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
            LOG(traceback.format_exc())
            return False
        

    def FtpUpload (self):
        try:
            session=ftplib.FTP(host,name ,pswd)
        except socket.error:
            pass
            #sys.exit()
            #print traceback.format_exc()
            #session=ftplib.FTP(host,name ,pswd)
    
                    

        try:
            for d  in  os.listdir(SFILE):
                #Md5sum file,mfile: Calculation before
                #mmfile: After the calculation
                fname = "%s%s"%(SFILE,d)
                mfile =  self.md5file(fname)
                #time.sleep(1)
                mmfile = self.md5file(fname)

                if mfile == mmfile:
                    files = open(fname,'rb')
                    session.storbinary('STOR '+d,files) 
                    files.close()

                    session.set_debuglevel(0)
                    LOG("Send the file %s successfully" %(fname))
                    os.system("mv %s %s"%(fname, BAKFILE))
                    LOG("Remove local file %s successfully" %fname)
                    session.close()
                else:
                    LOG("The file is on the cross,the file is not the same")
                    LOG("file md5 %s, mfile:%s ,mmfile %s"%(fname,mfile,mmfile))
        except:
            print  braceback.format_exc()
            LOG(traceback.format_exc())
        
        session.quit()

    
    def work (self):
        self.FtpUpload()

if __name__ == '__main__':
    try:
        pid = os.fork()
        if pid > 0 :
            sys.exit(0)
        os.setsid()
        os.chdir('/')
        sys.stdin = open("/dev/null","r+")
        sys.stdout = os.dup(sys.stdin.fileno())
        sys.stderr = os.dup(sys.stdin.fileno())

        LOG("Vsftp start")
        while True:
            try:
                session=ftplib.FTP(host,name ,pswd)
                if os.listdir(SFILE) and session.port == 21:
                    start = Vsftp()
                    start.work()
                else:
                    time.sleep(30)
                    LOG("No file download ...")
            except:
                time.sleep(30)
                LOG("Vsftp service network anomalies, restart the ipsec services")
                continue
    except IOError,e:
        LOG(traceback.format_exc())