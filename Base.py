import Create_DIR 
from derivations import Get_Details
from getting_ip import Get_Ip
from getting_filenames import Get_Files
from get_scores import Scores

pcapname = input("enter pcap name")
Create_DIR.create_dir()
gp = Get_Ip(pcapname)
gp.extract_ip()
d = Get_Details(pcapname)
d.calculate_metrics()
Get_Files().find_filenames()
Scores(gp,d).get_lists()
print('sucessfull')

