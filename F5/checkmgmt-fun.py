__author__ = 'vmunde'

import cmdproxy
import datetime
import xlwt
import os


def timeStamped(fname, fmt='%Y-%m-%d-%H-%M-%S_{fname}'):
    return datetime.datetime.now().strftime(fmt).format(fname=fname)

creds = cmdproxy.Creds()

device = (raw_input("Enter the Device list you want to upgrade seperated by comma:")).strip()
devicelist = device.lower().split(",")

dict = {}

workbook = xlwt.Workbook()
worksheet = workbook.add_sheet('deviceinfo')

a = 0
b = 0
c = 0
d = 1
e = 0
f = 2
g = 0
h = 3
ha = []
def device_Stat(device):

    """

        :param device:
        :return state of device:
    """
    global ha
    connect = cmdproxy.Connection(device, creds)
    result = connect.showcmd('show running-config /sys db -hidden failover.state | grep value')
    hastatus = result.output()
    ha = hastatus.split("\n")
    ha1 = ha[0].replace('"','')
    hastat = ha1.replace('value','')
    hastat1 =  "".join(hastat.split())
    return hastat1

def show_mgmt(device):
    global creds
    connection = cmdproxy.Connection(device, creds)
    result = connection.showcmd('show running-config /sys management-ip')
    out =  result.output().split("\n")
    out1 = out[0].split(" ")
    out2 = out1[2].split("/")
    return out2[0]

def get_oob(device):
    dc = device.split("-")
    datacenter = dc[0]
    mycommand = "grep -i %s %s-3[789]t* | more" %(device, datacenter)
    os.chdir("/tftpboot/configs")
    outlist = os.popen(mycommand).read()
    if outlist:
        out = outlist.split(" ")
        oobd = out[0].split(".")
        oobdevice = oobd[0]
        oobport = out[3]
        oobnew =  oobdevice + ":"+ oobport
        print oobnew
        return oobnew
    else:
        print device+":count not find OOB info"


for dev in devicelist:
    show_mgmt(dev)
    worksheet.write(a,b,dev)
    worksheet.write(c,d,show_mgmt(dev))
    worksheet.write(e,f,get_oob(dev))
    worksheet.write(g,h,device_Stat(dev))
    a += 1
    c += 1
    e += 1
    g += 1
    
workbook.save(os.path.join("/mnt/gnsopssus/gnsopssus/complexity/reports/",timeStamped('devicelist.xls')))
