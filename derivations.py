import os
import subprocess

class Get_Details:
  def __init__(self,pcapfile):
    self.pcapfile = pcapfile
    self.totalpackets = list()
    self.smallpackets = list()
    self.gappackets = list()
    self.bytesexchanged = list()
    self.T = list()
    self.Alpha = list()
    self.server = list()
    self.client = list()
    self.ratio = list()
 
  def get_lists(self):
    return self.pcapfile,self.totalpackets,self.smallpackets,self.gappackets,self.bytesexchanged,self.T,self.Alpha,self.ratio

  def get_src_dst(self):
    with open('ip/ipsrc.txt','r') as f:
      data = f.read()
      src=data.split('\n')
    with open('ip/ipdst.txt','r') as f:
      data = f.read()
      dst=data.split('\n')
    return src,dst

  def calculate_metrics(self):
    src,dst = self.get_src_dst()
    for i in range(len(src)-1):
      temp5 = str(src[i])
      temp,temp1 = temp5.split(':')
      temp1=int(temp1)
      temp2 = str(dst[i])
      temp3,temp4 = temp2.split(':')
      temp4=int(temp4)
      print("\n\ntcp conversation number ",i)
      print("\n\n")

      os.system("tcpdump -r %s \'src host %s and tcp port %i and len <= 80\'| egrep -o 'ack [0-9]+'|  awk \'{print $2}\' | sed \'1d\' >server.txt" %(self.pcapfile,temp,temp1) )
      os.system("tcpdump -r %s \'src host %s and tcp port %i and len <= 80\'| egrep -o 'ack [0-9]+'|  awk \'{print $2}\' | sed \'1d\' >client.txt" %(self.pcapfile,temp3,temp1) )
      os.system('tcpdump -r %s \'src host %s and tcp port %i\' | egrep -o \'length [0-9]*\' | awk \'{ print $2 } \' | sed \'1d\' > length.txt ' %(self.pcapfile,temp3,temp1))
      os.system('tcpdump -tt -r %s \'src host %s and tcp port %i\' | egrep -o \'[0-9]+.[0-9]+ I\' | awk \'{print $1}\' | sed \'1d\' > timestamps.txt ' %(self.pcapfile,temp3,temp1) )
      os.system("tcpdump -r %s \'host %s or %s and tcp port %i\' -w conversations/%s-%s.pcap" %(self.pcapfile,temp,temp3,temp1,temp5,temp2))
      spc = int(subprocess.check_output("tcpdump -r %s \'host %s or %s and tcp port %i and len<=80\' | wc -l " %(self.pcapfile,temp,temp3,temp1),shell=True))
      self.smallpackets.append(int(spc))
      tpc = int(subprocess.check_output("tcpdump -r %s \'host %s or %s and tcp port %i \' | wc -l " %(self.pcapfile,temp,temp3,temp1),shell=True))
      self.totalpackets.append(int(tpc))
      
      gap = self.calculate_gap()
      self.bytesexchanged.append(self.server[i]+self.client[i]) 
      if(self.client[i]==0):
        self.ratio.append(self.server[i])
      else:
        self.ratio.append(int(self.server[i]/self.client[i]))
      self.gappackets.append(gap)
      os.system("cp server.txt data/%s-%s.txt" %(temp5,temp2))
      os.system("cp client.txt data/%s-%s.txt" %(temp2,temp5))
      print("\n\nprinting gap packets")
      print("for "+temp5+" <-> "+temp2+" is ",gap,"\n\n")
      self.T.append(float("{:.2f}".format((spc-gap-1)/tpc)))
      self.calculate_alpha()
    os.system("rm server.txt client.txt length.txt timestamps.txt")

  def calculate_gap(self):
    gap = 0
    ack_server = list()
    with open('server.txt','r') as f:
     data = f.read()
     data = data.split('\n')
     ack_server = data
     c = 0
     for j in range(len(data)-2):
      if(int(data[j+1])-int(data[j])) > 1400 :
       c = c+ int((int(data[j+1])-int(data[j]))/1500)
     if len(data) == 0:
       num = 0
     elif len(data) == 1:
       num = 0 
     else: 
       num = int(data[len(data)-2]) - int(data[0])
     self.server.append(int(data[len(data)-2])) 
     num = int(num/1400)
     gap = gap + num - c

    with open('client.txt','r') as f:
     data = f.read()
     data = data.split('\n')
     if len(data) == 0:
       num = 0
     elif len(data) == 1:
       num = 0 
     else: 
       num = int(data[len(data)-2]) - int(data[0])
     self.client.append(int(data[len(data)-2])) 
     num = int(num/1400)
     gap = gap + num

    return gap


  def calculate_alpha(self):
    timestamps = list()
    length = list()
    with open('length.txt','r') as f:
     data = f.read()
     data = data.split('\n')
     for line in data :
      if line == '':
       break
      line = line.strip()
      length.append(int(line))
    with open('timestamps.txt','r') as f:
     data = f.read()
     data = data.split('\n')
     for line in data :
      if line == '':
       break
      line = line.strip()
      timestamps.append(float(line))
    c = 0
    ct = 0
    for i in range(len(length)-1) :
     if length[i] <=20 & length[i+1]<=20 :
      c = c+1
      if timestamps[i+1]-timestamps[i] < 2.0 :
       ct = ct + 1
    self.Alpha.append(float("{:.2f}".format(ct/c)))









