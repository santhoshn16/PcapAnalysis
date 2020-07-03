import os
import subprocess

class Get_Files:
  def find_filenames(self):
    home_path = os.getcwd()
    try:
     files_path = os.path.join(home_path,'conversations')
     os.chdir(files_path)
    except:
     print('files not found')
    
    for name in os.listdir(files_path):
      protofound = 0
      if os.path.isfile(name):
        count = subprocess.check_output("tcpdump -vv -r %s \'(tcp[(tcp[12]>>2):2]<0xffff) and (tcp[(tcp[12]>>2):2]>0xfffa)\'|wc -l" %(name),shell=True)
        if(int(count) > 0) :
         os.system("cp %s protocol/telnet_%s" %(name,name))
         os.system('tshark -r %s -q -z follow,tcp,ascii,0 > tcpstream.txt' %(name))
         infile = open('tcpstream.txt','r')
         data = infile.read()
         data = data.strip()
         data = data.split('\n')
         password = ''
         for i in range(len(data)):
          if 'Password:' in data[i]:
           j = i+1
           while j<(len(data)):
            if int(data[j]) > 1:
             break
            if int(data[j]) == 1:
             password = password + data[j+1]
             j = j + 2
         os.system('echo %s>>credentials/telnet_%s.txt' %(password,name))
         os.system('rm tcpstream.txt')
         protofound=protofound+1 

        count = subprocess.check_output("tcpdump -vv -r %s \'tcp[(tcp[12]>>2):4] = 0x5353482D and (tcp[((tcp[12]>>2)+4):2] = 0x312E or tcp[((tcp[12]>>2)+4):2] = 0x322E)\'|wc -l" %(name),shell=True)
        if(int(count) > 0) :
         os.system("cp %s protocol/ssh_%s" %(name,name))
         protofound=protofound+1

        count = subprocess.check_output("tcpdump -vv -r %s \'tcp[(tcp[12]>>2):4] = 0x3232302d or tcp[(tcp[12]>>2):4] = 0x32323020 \'|wc -l" %(name),shell=True)
        if(int(count) > 0) :
         os.system("cp %s protocol/ftp_%s " %(name,name))
         os.system("cp %s protocol/smtp_%s" %(name,name))
         os.system("tcpdump -vvA -r %s | grep STOR | awk \'{ for (c=2;c<=NF;c++) print $c }\' | uniq >>file_names/names_ftp.txt" %(name))
         os.system("tcpdump -vvA -r %s | egrep -o \'USER [a-z0-9]*|PASS [a-z0-9]*\' | uniq >>credentials/ftp_%s.txt" %(name,name))
         protofound=protofound+1

        count = subprocess.check_output("tcpdump -vvA -r %s \'tcp[(tcp[12]>>2):4] = 0x524f5354 or tcp[20:4] = 0x47455420 or tcp[32:4] = 0x47455420 or tcp[32:4] = 0x524f5354 or tcp[((tcp[12:1] & 0xf0)>>2):4] = 0x48545450\'|wc -l" %(name),shell=True)
        if(int(count) > 0) :
         os.system("cp %s protocol/http_%s" %(name,name)) 
         os.system("tcpdump -vvA -r %s |  egrep -o \'GET [A-Za-z0-9\./\\=+\"  -]* HTTP\' | awk \'{ for (c=2;c<NF;c++) print $c }\' | uniq >>file_names/names_http.txt" %(name))
         os.system("tcpdump -vvA -r %s |  egrep -o \'POST [A-Za-z0-9\./\\=+\" -]* HTTP\' | awk \'{ for (c=2;c<NF;c++) print $c }\'| uniq >>file_names/names_http.txt" %(name))
         os.system("tshark -r %s -q --export-objects \'http,httpobjects/%s\'" %(name,name))
         protofound=protofound+1
  
        if protofound > 0 :
         os.system("rm %s" %(name))
