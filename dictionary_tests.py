
import glob, os.path, zipfile, tempfile, shutil, time

def get_files(files_done):
    
    for root, _, files in os.walk("/Users"):
        for f in files:
            fullpath = os.path.join(root, f)
            if ("NDT_P0.ZIP" in fullpath) and not("Google" in fullpath):
                if fullpath not in files_done:
                    os.makedirs(root + " tmp")
                    zip_ref = zipfile.ZipFile(fullpath)
                    zip_ref.extractall(root + " tmp") #extract file to dir
                    zip_ref.close()
                    shutil.rmtree(root + " tmp", ignore_errors=True)
                    
                    return fullpath


if __name__ == '__main__':
    
    files_done = []
    count = 0
    
    while (count < 3):
        if get_files(files_done) == None:
            count += 1
        else:
            files_done.append(get_files(files_done))
            count += 1
            
        #time.sleep(25)
    
