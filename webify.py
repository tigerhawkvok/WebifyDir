## See https://github.com/tigerhawkvok/WebifyDir for component licenses
## and instructions

import os, math, time, yn

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
        colorstrip = yn.yn("Do you wish to do this?")
        jq = yn.yn("Would you like to compress the JPGs in this folder?")
        if jq is True:
            jqual = input("Please enter the JPG compression quality you desire. Lower is more highly compressed. \n(90% default): ")
            try:
                int(jqual) + 1
            except TypeError:
                print("Invalid number. Defaulting to 90%")
                jqual = 90

        cq = yn.yn("Would you like to compress the CSS files in this directory?")
    else:
        jq=False
        colorstrip=False
        cq=False
        jqual='100'

else:
    opngoptions = '-o7'
    jq = True
    jqual = str(90)
    cq = True
    colorstrip = True
    olevel='7, and JPG compression at ' + jqual + ' percent quality.'

if cq and jq is True:
    extend = ", CSS files, and JPG files"
elif cq is True:
    extend = " and CSS files"
elif jq is True:
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
    if jq is True: f.write("\nmkdir \"" + jpgdir + "\"")
    if cq is True: f.write("\nmkdir \"" + scandir + backbase + "\\backup_css\"")
for root, dirs, files in os.walk(scandir): 
    for file in files:
        # make search case insensitive
        fname=file.lower()
        ext=fname[-3:]
        if "png" == ext:
            ## backup PNGs for all but classic mode
            if quick.lower() !='p':
                f.write("\ncopy /Y \"" + os.path.join(root, file) + "\" \"" + scandir + backbase + "\\backup_pngs\\" + file + "\"")
            if colorstrip is True: 
                f.write("\npngcrush.exe -rem cHRM -rem gAMA -rem iCCP -rem sRGB \"" + scandir + backbase + "\\backup_pngs\\" + file + "\" \"" + os.path.join(root, file) + "\"")
            ## Optimizes with OptiPNG
            f.write("\n optipng.exe " + opngoptions + " \"" + os.path.join(root, file) + "\"")
            i += 1
        if cq is True:
            if "css" == ext:
                ## Backup CSS
                f.write("\ncopy /Y \"" + os.path.join(root, file) + "\" \"" + scandir + backbase + "\\backup_css\\" + file + "\"")
                ## CSS tidy.  Safe compression level.
                f.write("\ncsstidy.exe \"" + scandir + backbase + "\\backup_css\\" + file + "\" --compress-colors=true --compress_font-weight=true --preserve_css=true --optimise_shorthands=1 --remove_bslash=true --remove_last_;=true --timestamp=true \"" + os.path.join(root, file) + "\" ")
                i +=1
        if jq is True:
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
