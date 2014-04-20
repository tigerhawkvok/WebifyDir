## See https://github.com/tigerhawkvok/WebifyDir for component licenses
## and instructions

import os, math

userdir = os.environ.get("USERPROFILE")
drive = os.environ.get("HOMEDRIVE")

if userdir == None or drive == None:
    print("WARNING: Your environment variables may be corrupt.")
    if drive == None:
        print("%HOMEDRIVE% variable error.  Assuming C:\\")
        drive="C:"
    if userdir == None:
        print("%USERPROFILE% variable error. Falling back ...")
        if os.path.exists(drive + "\\Users"):
            userdir = drive + "\\Users"
        elif os.path.exists(drive + "\\Documents and Settings"):
            userdir = drive + "\\Documents and Settings"
        else:
            print("Fallback faliure. Option 1 set as " + drive)
            userfallbackerror = True

## Edit the batch file output directory here. 
## Each "\" in the path must be escaped to "\\".
writedir = os.getcwd() + "\\pngcrushbatch.bat"

## Checks for presence of "Pictures" directory.
## If it isn't there, program assumes XP style directories and checks those.
## If that fails too, program falls back to the main user directory.
scandir_pix = userdir + "\\Pictures"
if os.path.exists(scandir_pix) == False:
    if userfallbackerror != True:
        ## Check XP paths
        scandir_pix = userdir + "\\My Documents\\My Pictures"
        if os.path.exists(scandir_pix) == False:
            print("WARNING: Pictures directory not found in either XP or Vista/7 style paths.\nFalling back to user directory.")
            scandir_pix = userdir
            pictureswarning = True
    else:
        scandir_pix = drive

scandir_root = drive  + "\\" 

## Scan choices
print("\nWhere would you like to scan?")
print("[1] " + scandir_pix)
print("[2] " + scandir_root + " (VERY SLOW)")
print("[3] A custom directory?")
scanval = input("Please enter the appropriate number and press ENTER: ")

## Scan option parsing
if scanval == "1":
    warningmessage = ""
    scandir = scandir_pix
elif scanval == "2": 
    warningmessage = "This may take a few minutes. Compression may fail if you have inappropriate write permissions."
    scandir = scandir_root
elif scanval == "3":
    print("\nWARNING: You have selected a custom directory.  Please enter the full path. This may be case sensitive. Do not use quotes.")
    scandir = input("Path: ")
    warningmessage = ""
else:
    print("\nNo option or invalid option selection.\nDefaulting to " + scandir_pix + ".")
    scandir = scandir_pix
    warningmessage=""

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


print("\n" + scandir + " being searched for PNG files. Compression will take place at compression level " + olevel + ". Please wait. " + warningmessage + "\n")

i = 0
f = open(writedir,'w') 
for root, dirs, files in os.walk(scandir): 
    for file in files:
        # make search case insensitive
        fname=file.lower()
        ext=fname[-3:]
        if "png" == ext:
            f.write("\n optipng.exe " + opngoptions + " \"" + os.path.join(root, file) + "\"")
            i += 1
            if i % 100 == 0:
                iecho = str(i)
                print(iecho + " files found.")
iecho = str(i)
print(iecho + " files found.")
f.close()
print("\nSearch complete.  Batch file for execution saved to\n" + writedir + ".")
runnow = input("\nWould you like to run the file now? [Y/N]: ")
runnow = runnow.lower()
if runnow == "y": 
    print("\nThe batch file will now compress your PNG files.  This may take a while.")
    os.startfile("pngcrushbatch.bat")
    print("Script completed. You may close this window.")
elif runnow == "n":
    print("\nScript completed. You may close this window.")
else:
    print("\nUnrecognized choice. Script completed.")
    print("If you intended to run the batch file, you may do so manually from \n" + writedir + ".")
    print("You may close this window.")
