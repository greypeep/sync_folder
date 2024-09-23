# sync_folder
This code will synchronize through two files of your choice. On the default state it will end the synchronization process after the computer is shutdown. In case you want it to continue working after the computer shutdown,the batch file will have to be moved to the startup folder of windows. 

How to run:
-Edit the batch file so it works with the files that you want,the default state of the batch file  is:
----------------
@echo off 
start /b pythonw "path-to-script" "path-to-source-folder" "path-to-replica-folder" 10(time in seconds that takes replica to clone the source folder) "path-to-log"
exit
---------------

After adjusting the settings for the folders you want,execute the batch script and you should be good to go.
