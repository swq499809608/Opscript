#/usr/bin/env python

import os,sys,time,re,traceback


class ceph_depoloy(object):
    def __init__(self):
        version = 1.0 

    #Log insert 
    def LOG(self,info):
        logfile = '/tmp/ceph-deploy.log'
        files = open(logfile,'a')
        try:
            files.write('%s : %s \n'%(time.ctime(),info))
        except IOError:
            files.close()
        files.close()
    def diskDell(self,disk,count):
        try:
            keys = os.popen("fdisk %s" %disk,"w")
            keys.write('d \n')
            keys.write('w \n')
            #key = os.popen("parted %s" %disk,"w")
            #key.write('rm \n')
            #key.write('1 \n')
            #key.write('quit')
            keys.flush()
        except:
            LOG.error(traceback.format_exc())
    #Disk format /dev/sd*
    def diskFormat(self,disk,count):
        try:
            disk_cap = int(os.popen("fdisk  -l %s|grep 'Disk %s'|awk '{print $5}'" %(disk,disk)).readlines()[0].strip())
            if (disk_cap / 1000 /1000 /1000) >= 2001:
                os.system("parted -s %s rm 1" %disk)
                os.system("parted -s %s mklabel gpt" %disk)
                os.system("parted -s %s mkpart primary xfs 0 100%%" %disk)
                print disk,count
                #key = os.popen("parted %s" %disk,"w")
                #key.write('rm \n')
                #key.write('1 \n')
                #key.write('mklabel gpt \n')
                #key.write('yes \n')
                #key.write('mkpart \n')
                #key.write('p \n')
                #key.write('\n \n')
                #key.write('0 \n')
                #key.write('100% \n')
                #key.write('i \n')
                #akey.write('q \n')
                #key.flush()
            else:
                keys = os.popen("fdisk %s" %disk,"w")
                keys.write('d \n')
                keys.write('n \n')
                keys.write('p \n')
                keys.write('1 \n')
                keys.write('\n \n')
                keys.write('\n \n')
                keys.write('w')
                keys.flush()
            time.sleep(1)
            os.system("""mkdir -p /data%s""" %count)
            os.system("""mkfs.xfs -f -i size=1024 %s1 """ %disk)
            self.LOG("""cmd: mkfs.xfs -f -i size=1024 %s1 """ %disk)
            
            fp = open('/etc/fstab','r')
            for i in fp:
                if not re.search('sdb',i):
                    cmds = """%s1				/data%s			xfs	defaults	 1 2 """ %(disk,count)
                    os.system("echo %s >> /etc/fstab" %cmds)
                    break
            self.LOG("Disk  %s format partion" %disk )
        except:
            self.LOG(traceback.format_exc())

    
    #Get disk tag 
    def disk_tag(self):
        disk_tags = list()
        disk_part = list()
        for ch in xrange(0x42, 0x5B): 
            disk_tags.append("sd%s" %unichr(ch).lower())
            disk_part.append("/dev/sd%s1" %unichr(ch).lower())
        return disk_tags

    def work(self):
        disks = list()
        disk_tags = self.disk_tag()
        
        devs = os.listdir('/dev/')
        count = 0 
        for d in disk_tags:
            if d in devs:
                count += 1
                disk = '/dev/%s' %d 
                self.diskFormat(disk.strip(),count)
                time.sleep(1)
 
 
if __name__ == "__main__":
    sc = ceph_depoloy()
    sc.work()
    
