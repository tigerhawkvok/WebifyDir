##    This program is free software: you can redistribute it and/or modify
##    it under the terms of the GNU Lesser General Public License as published by
##    the Free Software Foundation, either version 3 of the License, or
##    (at your option) any later version.
##
##    This program is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU Lesser General Public License for more details.
##
##    You should have received a copy of the GNU Lesser General Public License
##    along with this program.  If not, see <http://www.gnu.org/licenses/>.
##
## Library components: OptiPNG 0.6.3, Cosmin Truta
## PNGcrush 1.2.5, Glenn Randers-Pehrson
## CSSTtidy 1.3, Florian Schmitz
## convert.exe via ImageMagick 6.5.7, ImageMagick Studio LLC
## Peazip portable 32-bit 2.7.1, Giorgio Tani
##
## OptiPNG batch compression script, Python code. 
## Released under CC-GNU LGPL 2.1 by Philip Kahn.
## Code for Python 3.0+  
## To revert, change PRINT statements and change INPUT to RAW_INPUT for security purposes.
import os, math, time



print("Python 3.0+ PNG batch file compression, with IE PNG corrections. \n(CC-GNU) Philip Kahn, 2009. See source for copyright information and directory for component licenses.")

## Edit the batch file output directory here. 
## Each "\" in the path must be escaped to "\\".

rundir = os.environ.get("APPDATA") + "\\WebifyDir"
writedir = rundir + "\\pngcrushbatch.bat"

print("\nPlease enter the full directory path. This may be case sensitive. Do not use quotes.")
scandir = input("Path: ")

quick = input("Press 'Q'[enter] here for a quick webify directory with default options\n    Compress PNGs\n    Strip PNGs of color profile information\n    Compress CSS\n    Compress JPGs to 90% quality\nPress 'P'[enter] to classic PNG-only compression.\nOtherwise, press any key to continue.")

if quick.lower() != 'q':
    print("\nPlease input a compression level from 1-8, where 8 is highest.")
    print("Be aware high levels of compression may be very slow.")
    print("For details on compression levels, see the OptiPNG documentation.")
    olevel = input("Select a level (Default: 7): ")
    if olevel == "1": opngoptions = "-o1"
    elif olevel == "2": opngoptions = "-o2"
    elif olevel == "3": opngoptions = "-o3"
    elif olevel == "4": opngoptions = "-o4"
    elif olevel == "5": opngoptions = "-o5"
    elif olevel == "6": opngoptions = "-o6"
    elif olevel == "7": opngoptions = "-o7"
    elif olevel == "8": opngoptions = "-zc1-9 -zm1-9 -zs0-3 -f0-5"
    else: 
        print ("\nNo option or invalid option selected. Using compression level 7.")
        opngoptions = "-o7"
        olevel="7"
        opngoptions = "-o7"
    if quick.lower()!='p':
        print("By default this program strips color profile information from PNGs for cross-browser display.")
        colorstrip = input("Please enter 'N' if you wish to skip this step. Otherwise, press any key to continue. ")
        jq = input("Would you like to compress the JPGs in this folder? [Y/N]: ")
        if jq.lower() == 'y':
            jqual = input("Please enter the JPG compression quality you desire. Lower is more highly compressed. \n(90% default): ")
            try:
                int(jqual) + 1
            except TypeError:
                print("Invalid number. Defaulting to 90%")
                jqual = 90

        cq = input("Would you like to compress the CSS files in this directory? [Y/N]: ")
    else:
        jq='n'
        colorstrip='n'
        cq='n'
        jqual='100'

else:
    opngoptions = '-o7'
    jq = 'y'
    jqual = str(90)
    cq = 'y'
    colorstrip = 'y'
    olevel='7, and JPG compression at ' + jqual + ' percent quality.'

if cq and jq == 'y':
    extend = ", CSS files, and JPG files"
elif cq == 'y':
    extend = " and CSS files"
elif jq == 'y':
    extend = " and JPG files"
else:
    extend = ""

print("\n" + scandir + " is being \nsearched for PNG files" + extend + ".")
print("\nPNG compression will take place at compression level " + olevel + ". Please wait.\n")

i = 0
f = open(writedir,'w')
writetime = str(time.time())
backbase = "\\backup_" + writetime
f.write("@echo off")
if quick.lower() != 'p':
    f.write("\nmkdir \"" + scandir + backbase + "\"")
    f.write("\nmkdir \"" + scandir + backbase + "\\backup_pngs\"")
    jpgdir = scandir + backbase + "\\backup_jpgs_" + writetime # Lossy compression, versioning
    if jq.lower() == 'y': f.write("\nmkdir \"" + jpgdir + "\"")
    if cq.lower() == 'y': f.write("\nmkdir \"" + scandir + backbase + "\\backup_css\"")
for root, dirs, files in os.walk(scandir): 
    for file in files:
        # make search case insensitive
        fname=file.lower()
        ext=fname[-3:]
        if "png" == ext:
            ## backup PNGs for all but classic mode
            if quick.lower() !='p':
                f.write("\ncopy /Y \"" + os.path.join(root, file) + "\" \"" + scandir + backbase + "\\backup_pngs\\" + file + "\"")
            if colorstrip.lower() != 'n': 
                ## Does not strip color information if the user requested to skip this step 
                f.write("\npngcrush.exe -rem cHRM -rem gAMA -rem iCCP -rem sRGB \"" + scandir + backbase + "\\backup_pngs\\" + file + "\" \"" + os.path.join(root, file) + "\"")
            ## Optimizes with OptiPNG
            f.write("\n optipng.exe " + opngoptions + " \"" + os.path.join(root, file) + "\"")
            i += 1
        if cq.lower() == 'y':
            if "css" == ext:
                ## Backup CSS
                f.write("\ncopy /Y \"" + os.path.join(root, file) + "\" \"" + scandir + backbase + "\\backup_css\\" + file + "\"")
                ## CSS tidy.  Safe compression level.
                f.write("\ncsstidy.exe \"" + scandir + backbase + "\\backup_css\\" + file + "\" --compress-colors=true --compress_font-weight=true --preserve_css=true --optimise_shorthands=1 --remove_bslash=true --remove_last_;=true --timestamp=true \"" + os.path.join(root, file) + "\" ")
                i +=1
        if jq.lower() == "y":
            if "jpg" == ext:
                ## Backup JPGs
                f.write("\ncopy /Y \"" + os.path.join(root, file) + "\" \"" + jpgdir + "\\" + file + "\"")
                ## Compress with ImgMagick
                f.write("\nconvert.exe \"" + jpgdir + "\\" + file + "\" -quality " + jqual + " \"" + os.path.join(root, file) + "\" ")
                i +=1
        if i % 100 == 0 and i > 0:
            iecho = str(i)
            print(iecho + " files found.")

## Finished finding files
iecho = str(i)
print(iecho + " files found.")

if quick.lower() != 'p':
    ## Runs peazip portable to compress backups
    f.write("\npeazip.exe -add27z \"" + scandir + backbase + "\"")
    f.write("\necho Please wait till your backup archive has been completed then continue.\npause")

    ## Remove backup directories
    f.write("\nrmdir \"" + scandir + backbase + "\" /s /q")

f.close()
print("\nSearch complete.  Batch file for execution saved to\n" + writedir + ".")
runnow = input("\nWould you like to run the file now? [Y/N]: ")
runnow = runnow.lower()
if runnow == "y": 
    print("\nThe batch file will now compress your PNG, JPG, and CSS files.  This may take a while.")
    os.startfile("pngcrushbatch.bat")
    print("Script completed. You may close this window.")
elif runnow == "n":
    print("\nScript completed. You may close this window.")
    print("\nIf you intended to run the batch file, you may do so manually from \n" + writedir + ".")
else:
    print("\nUnrecognized choice. Script completed.")
    print("\nIf you intended to run the batch file, you may do so manually from \n" + writedir + ".")
    print("\nYou may close this window.")
