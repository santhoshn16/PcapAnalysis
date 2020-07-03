import os
home_path = os.getcwd()
def create_dir():


   if os.path.exists('conversations'):
    os.system('rm -r conversations')
    os.mkdir('conversations')
   else:
    os.mkdir('conversations')
   os.makedirs('conversations/protocol')
   os.makedirs('conversations/intersting_conv')
   os.makedirs('conversations/file_names')
   os.makedirs('conversations/httpobjects')
   os.makedirs('conversations/credentials')
 
   if os.path.exists('ip'):
    os.system('rm -r ip')
    os.mkdir('ip')
   else:
    os.mkdir('ip')
  
   if os.path.exists('data'):
    os.system('rm -r data')
    os.mkdir('data') 
   else:
    os.mkdir('data')

   if not os.path.exists('results'):
    os.mkdir('results')

     
