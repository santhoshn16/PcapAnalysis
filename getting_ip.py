import os

class Get_Ip:
  def __init__(self,pcapname):
    self.pcapname = pcapname
    self.field = [3,5]
    self.tcpconvlatest = list()
    self.timelatest = list()
    self.tcpconnfound = 0

  def get_lists(self):
    return self.tcpconvlatest,self.timelatest,self.tcpconnfound

  def extract_ip(self):
    tcpconv = list()
    time = list()
    src = list()
    dst = list()
    os.system("tcpdump -nr %s \'tcp[tcpflags] & (tcp-syn|tcp-ack) = (tcp-syn|tcp-ack)\' | awk \'{print \"timestamp  \"$1\" from source \"$5\" to destination \"$3}\' | tr : ' ' >ip/ip.txt " %(self.pcapname))
    for i in self.field:
      os.system("tcpdump -nr %s \'tcp[tcpflags] & (tcp-syn|tcp-ack) = (tcp-syn|tcp-ack)\' | awk \'{print $%i}\'| tr : ' ' | tr . ' ' | awk \'{print $1\".\"$2\".\"$3\".\"$4\":\"$5}\' >ip/field%i.txt " %(self.pcapname,i,i))

    os.system("mv ip/field3.txt ip/ipdst.txt")
    os.system("mv ip/field5.txt ip/ipsrc.txt")

    os.system("tshark -r %s -q -z conv,tcp | tail -n +6 | head -n -1 | awk \'{print $1\"-\"$3\" \"$11}\' >ip/time.txt" %(self.pcapname))
    with open('ip/time.txt','r') as f:
      data = f.read()
      addr = data.split('\n')
      for i in range(len(addr)-1):
        temp = str(addr[i])
        temp1,temp2  = temp.split(' ')
        tcpconv.append(temp1)
        time.append(temp2)

    with open('ip/ipsrc.txt','r') as f:
      data = f.read()
      src=data.split('\n')
    with open('ip/ipdst.txt','r') as f:
      data = f.read()
      dst=data.split('\n')

    for i in range(len(src)-1):
      temp = str(src[i])
      temp1,temp2 = temp.split(':')
      temp3 = str(dst[i])
      temp4,temp5 = temp3.split(':')
      for j in range(len(tcpconv)):
        if (temp1 in tcpconv[j]) & ( temp2 in tcpconv[j])& (temp4 in tcpconv[j]) &  (temp5 in tcpconv[j]):
          #self.tcpconvlatest.append([])
          self.tcpconvlatest.append(tcpconv[j])
          #self.tcpconvlatest[i].append(time[j])
          self.timelatest.append(time[j])
          break
    self.tcpconnfound = len(self.tcpconvlatest)
    
    



    
