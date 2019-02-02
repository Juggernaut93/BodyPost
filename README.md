# BodyPost
A Python Script for Distant Worlds 2 - Geology &amp; Biology Dept.

Original script by CMDR Flammenhand/ThePrinceOfEverbang.

Purpose:<br>
The tool has been developed as a support to the Geology and Organics department in the Distant Worlds 2 Expedition.<br>
When a scan is performed, the tool will open in the browser the scouting report form with most fields already filled in.<br>

The script has now three modes of operation:<br>
1) `run_continuously = True` and `useOCR = True`: the script will continuously (every 0.2 seconds) try to detect the results of a planet scan with FSS by reading the upper right part of the screen.
When the script reads "LOCATIONS" together with "GEOLOGICAL (X)", "BIOLOGICAL (X)", "THARGOID (X)" or "HUMAN (X)" (where X is a number) in the correct area of the screen, it will check the player Journal to read data about
the last scanned planet (system and body names, composition, etc.) and will open the form in the browser with every information already filled in. Please note that the OCR part is still work in progress,
and can sometimes mistake a 9 for a 3, or a 6 for a 5, that's why you'll have to rapidly check if the numbers put in are correct. If you scan a planet and the tool does not immediately open the form, it
means it hasn't recognized some character correctly; waiting a bit (no more than 1-2 seconds) usually solves the problem.
2) `run_continuously = True` and `useOCR = False`: the script will continuously run in background and it will open the browser for every landable planet scanned*. With these settings, the script will NOT use OCR and won't
be able to fill in the form the number of POIs found.<br>
2) `run_continuously = False`: the script will run for a single scan; in this case the script will only open the browser for the last body scanned (if landable)*.

The script will not open the form if you have scanned a star/brown dwarf/etc. or if the scanned planet is not landable (because in such cases it cannot have any POIs, so no form is needed).

*Note that the journal does NOT currently contain info about the number of POIs for each planet, so when OCR is *disabled* the script WILL open the form when scanning planets that are landable but do not have POIs.

Note also that you can change the interval at which the script checks the screen/journal by changing the `polling_interval` parameter at the start of the script.

How to "install":<br>
1: Install Python 3.x. https://www.python.org/<br>
2: Install Tesseract: https://github.com/UB-Mannheim/tesseract/wiki (the tool was tested with the Windows 64-bit 4.0.0.20181030 version).
Be sure to add the Tesseract folder in the PATH environment variable, as explained in the installation instructions here: https://github.com/UB-Mannheim/tesseract/wiki.<br>
3: Install the required libraries with the following command: `pip install Pillow python-opencv pytesseract mss`.<br>
4: Download/copy the script.<br>
5: Place it into the same folder that your Journal Files get written to.<br>
   Usually that's C:\Users\<username>\Saved Games\Frontier Developments\Elite Dangerous<br>
6: Open up the Script in a text editor and change your CMDR Name. It's the 8th Line, in the marks.<br>
7: If you want to disable continuous mode, set `run_continuously` to `False`. If you want to disable OCR, set `useOCR` to `False`.
   
Usage:<br>
If you have Python installed, double-clicking the python script should suffice. You can also bind it to a keymap - google is your friend. :)<br>
When running the script in continuous mode, you can interrupt it using Ctrl+C.
