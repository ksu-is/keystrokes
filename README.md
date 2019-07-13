# Keystrokes - A Python project for Penetration Testers 
Python script “keystrokes” extracts the user keystrokes in real-time. The keystrokes can be saved locally so they can be viewed at a later time. This application can be used by penetration testers or security consultants in order to test operational security in order to ensure the compliance with the information security frameworks such as PCI-DSS, FedRamp, and NIST SP-800. The scope of this tool deals with the social engineering and exploitation aspect of the penetration test which is outlined in penetration testing guidance document published by FedRamp and PCI-DSS. This tool should only be deployed after the information gathering phase has been completed on the target along with intended purpose which aligns with the scope of the penetration test. This tool can further assist with acquiring keystrokes of local administrator which can assist us in creation of another admin account for a successful penetration test. This tool can assist with the extraction of almost all windows applications.


This script displays user keystrokes in a terminal.

Note:
  - This code only works on Windows systems
  - It is important to note that additional libraries are needed to run this code which is not covered in class such as:
  	- pyHook
	- pythoncom

Not working:
  - Ctrl + C is not working so the program cannot quit by itself
  - Output in .txt format is not working
  - There are some exceptions being generated but no major bugs. 
