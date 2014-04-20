## See https://github.com/tigerhawkvok/WebifyDir for component licenses
## and instructions

import os, math, time, yn

def doExit():
    import os,sys
    print("\n")
    os._exit(0)
    sys.exit(0)

# Temporary Stash
rundir = os.environ.get("APPDATA") + "\\WebifyDir\\"
if not os.path.isdir(rundir):
    try:
        os.mkdir(rundir)
    except:
        print("Could not create",rundir)
        print("Please manually create this directory and try again.")
        doExit()
writedir = rundir + "pngcrushbatch.bat"

def simpleVersioning():
    try:
        import simplejson as json
        try:
            # Python 2.7.x
            import urllib
            url = urllib.urlopen("https://api.github.com/repos/tigerhawkvok/WebifyDir")
            obj_raw = url.read()
            url.close()
        except AttributeError:
            # Python 3
            import urllib.request
            with urllib.request.urlopen("https://api.github.com/repos/tigerhawkvok/WebifyDir") as url:
                obj_raw = url.read()
        obj = json.loads(obj_raw)
        time_key = obj['pushed_at']
    except Exception as inst:
        print("Warning: Could not check remote version.",inst)
    try:
        f = open(rundir + ".gitversion")
        read_seconds = f.read()
        f.close()
        if read_seconds == "":
            raise FileNotFoundError
        push_time = time.strptime(time_key,"%Y-%m-%dT%H:%M:%SZ")
        this_time = time.gmtime(float(read_seconds))
        if push_time > this_time:
            if yn.yn("Your version is out of date with GitHub. Do you want visit GitHub and download a new version?"):
                try:
                    os.unlink(rundir + ".gitversion")
                except:
                    print("Could not delete the version file. Be sure to maually delete '.gitversion' before re-running the new version.")
                print("Launching browser. Rerun the script when you've updated.")
                import webbrowser
                webbrowser.open("https://github.com/tigerhawkvok/WebifyDir")
                doExit()
            else:
                print("Skipping update.")
    except FileNotFoundError:
        f = open(rundir + ".gitversion","w")
        read_seconds = time.time()
        f.write(str(read_seconds))
        f.close()
    except Exception as inst:
        print("WARNING: Could not check version.",inst)

print("Webify Directory - Prepare a site for deployment")
print("Get the most current release and report problems to")
print("https://github.com/tigerhawkvok/WebifyDir")

simpleVersioning()

print("\nPlease enter the full directory path. This may be case sensitive. Do not use quotes.")
print("Press [enter] to use the current path.")
try:
    scandir = None
    while scandir is None:
        scandir = input("Path: ")
        if scandir == "":
            scandir = os.getcwd()
        if not os.path.isdir(scandir):
            scandir = None
            print("That path does not exist. Please try again.")
            print("Press Control+C to exit the script.")
except KeyboardInterrupt:
    doExit()

print("Will check",scandir)
    
try:
    quick = input("Press 'Q'[enter] here for a quick webify directory with default options\n    Compress PNGs\n    Strip PNGs of color profile information\n    Compress CSS\n    Compress JPGs to 90% quality\nPress 'P'[enter] to classic PNG-only compression.\nOtherwise, press any key to continue.")
except KeyboardInterrupt:
    doExit()

if quick.lower() != 'q':
    print("\nPlease input a compression level from 1-8, where 8 is highest.")
    print("Be aware high levels of compression may be very slow.")
    print("For details on compression levels, see the OptiPNG documentation.")
    olevel = None
    while olevel is None:
        try:
            olevel = input("Select a level (Default: 7): ")
            olevel = int(olevel)
            if olevel < 0 or olevel > 8:
                raise ValueError
        except KeyboardInterrupt:
            doExit()
        except ValueError:
            olevel = None
            print("Invalid option. Please enter a number from 1-8.")
    if olevel is 1: opngoptions = "-o1"
    elif olevel is 2: opngoptions = "-o2"
    elif olevel is 3: opngoptions = "-o3"
    elif olevel is 4: opngoptions = "-o4"
    elif olevel is 5: opngoptions = "-o5"
    elif olevel is 6: opngoptions = "-o6"
    elif olevel is 7: opngoptions = "-o7"
    elif olevel is 8: opngoptions = "-zc1-9 -zm1-9 -zs0-3 -f0-5"
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
runnow = yn.yn("\nWould you like to run the file now?")
if runnow is True: 
    print("\nThe batch file will now compress your PNG, JPG, and CSS files.  This may take a while.")
    os.startfile("pngcrushbatch.bat")
    print("Script completed. You may close this window.")
else:
    print("\nScript completed. You may close this window.")
    print("\nIf you intended to run the batch file, you may do so manually from \n" + writedir + ".")
