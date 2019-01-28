# BodyPost
A Python Script for Distant Worlds 2 - Geology &amp; Biology Dept.

Original script by CMDR Flammenhand/ThePrinceOfEverbang

Purpose:<br>
The script will read the Elite: Dangerous Player Journal files and when a scan is performed it will open in the browser the scouting report form with most fields already filled in.<br>
The script has two modes of operation:<br>
1) It can continuously run in background and it will open the browser for every landable planet scanned.
2) It can be run for a single scan; in this case the script will only open the browser for the last body scanned (if landable).

The script will not open the form if you have scanned a star/brown dwarf/etc. or if the scanned planet is not landable (because it such cases it cannot have any POIs, so no form is needed).
Note that the journal does NOT currently contain info about the number of POIs for each planet, so the script WILL open the form when scanning planets that are landable but do not have POIs.

How to "install":<br>
1: Install Python 3.x. https://www.python.org/<br>
2: Download/copy the script.<br>
3: Place it into the same folder that your Journal Files get written to.<br>
   Usually that's C:\Users\<username>\Saved Games\Frontier Developments\Elite Dangerous<br>
4: Open up the Script in a text editor and change your CMDR Name. It's the 7th Line, in the marks.<br>
5: If you want to disable continuous mode, set `run_continuously` to False.
   
Usage:<br>
If you have Python installed, double-clicking the python script should suffice. You can also bind it to a keymap - google is your friend. :)<br>
When running the script in continuous mode, you can interrupt it using Ctrl+C.
