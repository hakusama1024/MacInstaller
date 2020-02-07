# MacInstaller

This script is use to install dmg to guest mac os from host os. 
example:

xbai@mac-xbai:~/Desktop/MacInstaller$ prlctl list -a
UUID                                    STATUS       IP_ADDR         NAME
{168c789e-caa6-4b83-bb84-a1f18c26e1f3}  stopped      -               Clone_2 of VM macOS Mojave
{edbe0c40-83dc-4505-8941-bac038897648}  stopped      -               VM macOS Mojave
{14c73b9b-c677-4647-9fe8-ad71f2b23b53}  paused       -               macOS Catalina


xbai@mac-xbai:~/Desktop/MacInstaller$ prlctl exec {14c73b9b-c677-4647-9fe8-ad71f2b23b53} /Volumes/SharedFolders/ShareTest/installpkg.py

the steps are 
1. put dmg files and script in the share folder, make sure you could see that in the guest os. 
2. In the guest os enable the prltoolsd
   System Prefrences -> Security & Privacy -> Full Disk Access 
3. Check the share forlder path from guest os then run the script


   
