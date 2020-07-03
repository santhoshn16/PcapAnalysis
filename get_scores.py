from derivations import Get_Details
from getting_ip import Get_Ip
import Create_DIR
import json
import webbrowser
import os
class Scores:
  def __init__(self,obj_gp,obj_d):
    self.obj_d = obj_d
    self.obj_gp = obj_gp
    self.pcapfile = ''
    self.totalpackets = list()
    self.smallpackets = list()
    self.gappackets = list()
    self.bytesexchanged = list()
    self.T = list()
    self.Alpha = list()
    self.ratio = list()
    self.tcpconvlatest = list()
    self.timelatest = list()
    self.tcpconnfound = 0
    self.json_data = []

  def get_lists(self):
    self.tcpconvlatest,self.timelatest,self.tcpconnfound = self.obj_gp.get_lists()
    self.pcapfile,self.totalpackets,self.smallpackets,self.gappackets,self.bytesexchanged,self.T,self.Alpha,self.ratio = self.obj_d.get_lists()
    for i in range(self.tcpconnfound):
     self.json_data.append({})
     self.json_data[i]['tcpconnection'] = self.tcpconvlatest[i]
     self.json_data[i]['Totalpackets'] = self.totalpackets[i]
     self.json_data[i]['Smallpackets'] = self.smallpackets[i]
     self.json_data[i]['Gappackets'] = self.gappackets[i]
     self.json_data[i]['T'] = self.T[i]
     self.json_data[i]['Alpha'] = self.Alpha[i]
     self.json_data[i]['Bytes of data'] = self.bytesexchanged[i]
     self.json_data[i]['Ratio'] = self.ratio[i]
     self.json_data[i]['Time'] = self.timelatest[i]
    #print(json.dumps(self.json_data,indent = 4))
    os.chdir(os.path.join(Create_DIR.home_path,'results'))
    os.system('touch %s.json' %(self.pcapfile))
    for name in os.listdir(os.getcwd()):
     if self.pcapfile in name:
      with open(name,'w') as out:
       json.dump(self.json_data,out,indent=4)
    os.chdir(Create_DIR.home_path)
    self.populate_html()
    print('sucessfull')

  def populate_html(self):
    os.system("touch result")
    r=open("result","w")
    str1="Pcapname Totalpackets Smallpackets Gappackets T Alpha Bytesexchanged Ratio Time\n"
    r.write(str1)
    for i in range(self.tcpconnfound):
     str1 = str(self.tcpconvlatest[i])+" "+str(self.totalpackets[i])+" "+str(self.smallpackets[i])+" "+str(self.gappackets[i])+" "+str(self.T[i])+" "+str(self.Alpha[i])+" "+str(self.bytesexchanged[i])+" "+str(self.ratio[i])+" "+str(self.timelatest[i]+"\n")
     r.write(str1)
    r.close()
    os.system("touch result.html")
    filein = open("result", "r")
    fileout = open("result.html", "w")
    data = filein.read()
    data = data.split("\n")

    table = "<html>\n"+"<style>\n"+"table,th,td{\n"+"border:1px solid black;\n"+"border-collapse:collapse;\n"+"}\n"
    table = table + "th,td{\n"+"padding:10px;\n"+"text-align:center;\n"+"font-size:20;\n"+"}\n"+"</style>\n"
    table = table + "<table>\n"
    table = table + "<tr>\n"+"<caption><h2>Results based on consider points </h2></caption>\n"+"</tr>\n"

# Create the table's column headers
    header = data[0].split(" ")
    table += "  <tr>\n"
    for column in header:
     table += "    <th>{0}</th>\n".format(column.strip())
    table += "  </tr>\n"

# Create the table's row data
    for line in data[1:len(data)-1]:
     row = line.split(" ")
     table += "  <tr>\n"
     for column in row:
        table += "    <td >{0}</td>\n".format(column.strip())
     table += "  </tr>\n"

    table += "</table>\n"+"</html>\n"

    fileout.writelines(table)
    fileout.close()
    filein.close()
    os.system("rm result")
    os.system("cp result.html results/%s.html" %(self.pcapfile))
    webbrowser.open("result.html")
    
    
  

 
    



