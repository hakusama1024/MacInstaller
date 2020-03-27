# MacInstaller

This script is use to install tableau mac software to guest mac os from host os. 

example:
this command will list the current existing guest os. 

xbai@mac-xbai:~/Desktop/MacInstaller$ prlctl list -a

      UUID                                    STATUS       IP_ADDR         NAME

      {168c789e-caa6-4b83-bb84-a1f18c26e1f3}  stopped      -               Clone_2 of VM macOS Mojave

      {edbe0c40-83dc-4505-8941-bac038897648}  stopped      -               VM macOS Mojave

      {14c73b9b-c677-4647-9fe8-ad71f2b23b53}  paused       -               macOS Catalina

This command is choosing one guest os and install all the dmg packages from the share folder. 

xbai@mac-xbai:~/Desktop/MacInstaller$ prlctl exec {14c73b9b-c677-4647-9fe8-ad71f2b23b53} /Volumes/SharedFolders/ShareTest/installpkg.py

Before running the script make sure to  install parallels tools.  
Also note that, as in the above example, the path to the script needs to be the path that where the guest OS would see it.

the steps are 
1. put dmg files and script in the share folder, make sure you could see that in the guest os. 

2. In the guest os enable the prltoolsd
          
      System Prefrences -> Security & Privacy -> File Disk Access -> prltoolsd 
      
3. Check the share forlder path from guest os then run the script

______________________________________________________________________________________
# Usage for vm auto update 

1. you will need update the vmlist file with your vm template uuid

2. add following command into you crontab 
    
      
>  crontab -e

      eg. runs every day 2AM

      
>  \* 2 * * * /usr/local/bin/python3 /Users/xbai/Desktop/environment-deployment/MacInstaller/autoVmUpdate.py

3. install prlsdkapi library. 
   [sdk](https://www.parallels.com/download/pvsdk/)

4. daily update log will save to vmUpdateLog. 