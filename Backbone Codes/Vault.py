import colorama
from password_manager import setPassword, checkPassword
import os, pickle, zipfile, subprocess, getpass # standard libraries
from colorama import Fore, init, Back # pip install colorama
from tkinter import Tk, filedialog # standard libraries
from shutil import copy, rmtree # standard libraries
from datetime import datetime # standard libraries
from stdiomask import getpass

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.getcwd()

init(autoreset=True)

"""
Work Left
    Double Verifications
"""
class Locker:
    def __init__(self):
        __root = Tk()
        __root.withdraw()
        __root.attributes('-topmost', True)

        __root.iconbitmap(os.path.join(BASE_DIR, 'icon.ico'))
        if not os.path.exists('.locker'):
            os.mkdir('.locker')
            with open(".locker/DO NOT CHANGE ANYTHING", "w"):
                pass
        if not os.path.exists('.locker/data'):
            with open('.locker/data', 'wb') as file:
                __object = {
                    "archives": {
                    },
                    "archive_list": [],
                    "archive_counts": 0,
                    "archive_status": "None" # locked unlocked none
                }
                pickle.dump(__object, file)

    def __status(self):
        if not os.path.exists("Locked"):
            if not os.path.exists("Control Panel.{21EC2020-3AEA-1069-A2DD-08002B30309D}"):
                return "non-init"
            else:
                return "locked"
        else:
            return "unlocked"

    def __getFiles(self, multiple=True):
        if multiple:
            return filedialog.askopenfilenames(title='Choose Images or Videos', filetypes=[
                ("All Images", "*.jpg *.jpeg *.png *.bmp *.gif *.tif *.tiff *.eps"),
                ("JPEG", "*.jpg *.jpeg"),
                ("PNG", "*.png"),
                ('ICON', '*.ico'),
                ("Bitmap", "*.bmp"),
                ("GIF", "*.gif"),
                ("TIFF", "*.tif *.tiff"),
                ("EPS", "*.eps"),
                ("Video", "*.mp4 *.avi *.mkv"),
                ("Show all", "*.*")
            ])
        else:
            return filedialog.askopenfilename(title='Choose Thumbnail', filetypes=[
                ("All Images", "*.jpg *.jpeg *.png *.bmp"),
                ("JPEG", "*.jpg *.jpeg"),
                ("PNG", "*.png"),
                ('ICON', '*.ico'),
                ("Bitmap", "*.bmp"),
                ("Show all", "*.*")
            ])

    def lock(self, password):
        print("Checking Password")
        res = checkPassword(password)
        if res == 'no-pass':
            print("You have't created a Password yet!")
        elif res:
            print("Locking the Vault")
            if not os.path.exists("Locked"):
                if not os.path.exists("Control Panel.{21EC2020-3AEA-1069-A2DD-08002B30309D}"):
                    return "InitializationError"
                else:
                    if os.path.exists('.locker/data'):
                        with open('.locker/data', 'rb+') as file:
                            dataobject = pickle.load(file)
                            dataobject['archive_status'] = 'locked'
                            pickle.dump(dataobject, file)
                    return "OverideError"
            else:
                os.system('ren Locked "Control Panel.{21EC2020-3AEA-1069-A2DD-08002B30309D}"')
                os.system('attrib +h +s "Control Panel.{21EC2020-3AEA-1069-A2DD-08002B30309D}"')
                if os.path.exists('.locker/data'):
                    with open('.locker/data', 'rb+') as file:
                        dataobject = pickle.load(file)
                        dataobject['archive_status'] = 'locked'
                        pickle.dump(dataobject, file)
                return "Success"
        else:
            print('Incorrect Password')
            return "PasswordError"

    def unlock(self, password):
        print("Checking Password")
        res = checkPassword(password)
        if res == 'no-pass':
            print("You have't created a Password yet!")
        elif res:
            print("Unlocking The Vault")
            if not os.path.exists("Control Panel.{21EC2020-3AEA-1069-A2DD-08002B30309D}"):
                if not os.path.exists("Locked"):
                    return "InitializationError"
                else:
                    if os.path.exists('.locker/data'):
                        with open('.locker/data', 'rb+') as file:
                            dataobject = pickle.load(file)
                            dataobject['archive_status'] = 'unlocked'
                            pickle.dump(dataobject, file)
                    return "OverideError"
            else:
                os.system('attrib -h -s "Control Panel.{21EC2020-3AEA-1069-A2DD-08002B30309D}"')
                os.system('ren "Control Panel.{21EC2020-3AEA-1069-A2DD-08002B30309D}" Locked')
                if os.path.exists('.locker/data'):
                    with open('.locker/data', 'rb+') as file:
                        dataobject = pickle.load(file)
                        dataobject['archive_status'] = 'unlocked'
                        pickle.dump(dataobject, file)
                return "Success"
        else:
            print("Incorrect Password")
            return "PasswordError"

    def append(self, archive, password):
        print("Checking Password")
        res = checkPassword(password)
        if res == 'no-pass':
            print("You have't created a Password yet!")
        elif res:
            print("Initializing the Vault")
            status = self.__status()
            if status == 'non-init':
                os.mkdir("Locked")
            else:
                self.unlock()
            with open('.locker/data', 'rb+') as file:
                data_object = pickle.load(file)
                if data_object['archive_status'] == 'None':
                    pass
                archive_counts = int(data_object['archive_counts'])
                archive_list = list(data_object['archive_list'])
                archive_extension = '.jpg'
                if archive_counts == 0:
                    data_filelist = []
                    arch = False
                else:
                    ifArchive = data_object['archives'].get(archive, "no_archive")
                    if ifArchive == 'no_archive':
                        data_filelist = []
                        arch = False
                    else:
                        data_filelist = list(data_object['archives'][archive]['filelist'])
                        archive_extension = data_object['archives'][archive]['extension']
                        arch = True

            filelist = self.__getFiles()
            count = 1
            length = len(filelist)
            
            if os.path.exists('Locked/{}.rar'.format(archive)):
                mode = 'a'
            else:
                if os.path.exists('Locked/{}{}'.format(archive, archive_extension)):
                    print(archive, archive_extension)
                    srcname = "Locked/{}{}".format(archive, archive_extension)
                    dstname = "Locked/{}.rar".format(archive)
                    os.rename(srcname, dstname)
                    mode = "a"
                else:
                    mode = 'w'
            print("Compilation of the Vault Data started...")
            with zipfile.ZipFile("Locked/{}.rar".format(archive), mode) as zipper:
                for file in filelist:
                    print("[{} / {}] Compiling {}".format(count, length, file))
                    if not file in data_filelist:
                        zipper.write(file, os.path.join(archive, os.path.basename(file)))
                        data_filelist.append(file)
                        os.remove(file)
                    else:
                        print("""{}File already exist in the archive
                        Filename: {}
                        Directory: {}
                        """.format(Fore.RED, os.path.basename(file), os.path.dirname(file)))
                    count += 1
            if mode == 'w':
                print("Creating Thumbnail")
                thumbnail = self.__getFiles(False)
                copy(thumbnail, os.path.join(BASE_DIR, 'Locked'))
                extension = os.path.splitext(thumbnail)[1]
                os.rename("Locked/{}".format(os.path.basename(thumbnail)), "Locked/{}{}".format(archive, extension))
                thumnname = "{}{}".format(archive, extension)
                subprocess.check_output('copy /b "Locked\\{}" + "Locked\\{}.rar" "Locked\\{}"'.format(thumnname, archive, thumnname), shell=True)
                os.remove("Locked/{}.rar".format(archive))
            else:
                os.rename("Locked/{}.rar".format(archive), "Locked/{}{}".format(archive, archive_extension))
            directory = os.path.dirname(filelist[0])

            print("Updating Archive")

            data_object["archive_counts"] += 1
            data_object['archive_status'] = 'locked'
            if arch == False:
                archive_list.append(archive)
            data_object['archive_list'] = archive_list
            if arch:
                data_object['archives'][archive]["filelist"] = data_filelist
                # data_object['archives'][archive]["date"] = str(datetime.now()).split(".")[0]
                data_object['archives'][archive]["dates"].append(str(datetime.now()).split(".")[0])
                # data_object['archives'][archive]["directory"] = list(data_object['archives'][archive]["directory"]).append(directory)
                data_object['archives'][archive]["directorys"].append(directory)
                data_object['archives'][archive]["counts"] += length
            else:
                newObject = {
                    archive: {
                        "filelist": data_filelist,
                        "dates": [str(datetime.now()).split(".")[0]],
                        "directorys": [directory],
                        "counts": length,
                        "extension": extension
                    }
                }
                data_object['archives'].update(newObject)
            with open('.locker/data', 'wb') as file:
                pickle.dump(data_object, file)
            self.lock(password)
            print("Vault has been secured successfully")
        else:
            print("Incorrect Password")

    def showArchives(self, password):
        res = checkPassword(password)
        if res == 'no-pass':
            print("You have't created a Password yet!")
        elif res:
            if os.path.exists('.locker/data'):
                with open('.locker/data', 'rb') as file:
                    data = list(pickle.load(file)['archive_list'])
                    count = 1
                    length = len(data)
                    for archive in data:
                        print('[{} / {}] {}'.format(count, length, archive))
                        count += 1
            else:
                print("{}No Archive to Show".format(Fore.RED))
        else:
            print("Incorrect Password")

    def delete(self, archive, password):
        res = checkPassword(password)
        if res == 'no-pass':
            print("You have't created a Password yet!")
        elif res:
            if os.path.exists('.locker/data'):
                with open(".locker/data", "rb+") as file:
                    loaded_data = pickle.load(file)
                    if archive in loaded_data['archive_list']:
                        loaded_data['archive_list'].remove(archive)
                        loaded_data['archive_counts'] -= 1
                        extension = loaded_data['archives'][archive]['extension']
                        loaded_data['archives'].pop(archive)
                        file.truncate()
                        file.seek(0)
                        pickle.dump(loaded_data, file)
                        status = self.__status()
                        if status == 'locked':
                            os.chdir("Control Panel.{21EC2020-3AEA-1069-A2DD-08002B30309D}")
                            os.remove("{}{}".format(archive, extension))
                            os.chdir('../')
                        elif status == 'unlocked':
                            os.remove("Locked\\{}{}".format(archive, extension))
                        else:
                            print("You have't started Vault process yet!")
                        self.lock(password)
                        print("Archive {} has been sucessfully deleted".format(archive))
                    else:
                        print("Archive {} doesnot exist!".format(archive))
            else:
                print("Sorry, There are not archives to delete!")
        else:
            print("Incorrect Password")
    def setPass(self):
        if os.path.exists(os.path.join(BASE_DIR, 'secret.pkl')):
            print("Changing Password")
            password = getpass(prompt = "Enter Old Password: ")
            if checkPassword(password):
                while True:
                    password = getpass(prompt="Enter Password: ")
                    cpassword = getpass(prompt="Confirm Password: ")
                    if password == cpassword:
                        setPassword(password)
                        print("Password Has been changed")
                        break
                    else:
                        print("{}Password and Confirm Password didn't matched".format(Fore.RED))
        else:
            print("Creating Password")
            while True:
                password = getpass(prompt="Enter Password: ")
                cpassword = getpass(prompt="Confirm Password: ")
                if password == cpassword:
                    setPassword(password)
                    print("Password Has been created")
                    break
                else:
                    print("{}Password and Confirm Password didn't matched".format(Fore.RED))
    def extract(self, archive, password):
        res = checkPassword(password)
        if res == 'no-pass':
            print("You have't created a Password yet!")
        elif res:
            if not os.path.exists('.locker/data'):
                print("""{}Archive Existence Error
                Archive {} Doesnot exist in this directory.
                Please try to access from the directory where you locked that archive
                """.format(Fore.RED, archive))
            else:
                with open('.locker/data', 'rb') as file:
                    data = pickle.load(file)
                    archive_data = data['archives'].get(archive, "no")
                    if archive_data == 'no':
                        print("""{}Archive Existence Error
                        Archive {} Doesnot exist in this directory.
                        Please try to access from the directory where you locked that archive
                        """.format(Fore.RED, archive))
                    else:
                        status = self.__status()
                        if status == 'locked':
                            pass
                        elif status == 'non-init':
                            exit()
                        extension = archive_data['extension']
                        if os.path.exists("Control Panel.{21EC2020-3AEA-1069-A2DD-08002B30309D}"):
                            os.chdir("Control Panel.{21EC2020-3AEA-1069-A2DD-08002B30309D}")
                            os.rename("{}{}".format(archive, extension), "{}.rar".format(archive))
                            with zipfile.ZipFile("{}.rar".format(archive), "r") as file:
                                file.extractall(ROOT_DIR)
                            os.rename("{}.rar".format(archive), "{}{}".format(archive, extension))
                            os.chdir(ROOT_DIR)

                            os.chdir(archive)
                            os.popen("start .")

                            os.chdir(ROOT_DIR)
                            
                        elif os.path.exists('Locked'):
                            os.chdir("Locked")
                            os.rename("{}{}".format(archive, extension), "{}.rar".format(archive))
                            with zipfile.ZipFile("{}.rar".format(archive), "r") as file:
                                file.extractall(ROOT_DIR)
                            os.rename("{}.rar".format(archive), "{}{}".format(archive, extension))
                            
                            os.chdir(ROOT_DIR)
                            
                            os.chdir(archive)
                            os.popen("start .")
                            
                            os.chdir(ROOT_DIR)
                            self.lock(password)
                        print("Folder Has been Extracted")
        else:
            print("Incorrect Password")

if __name__ == '__main__':
    option = """Choose Options
    (L)ock
    (U)nlock
    (A)dd
    (E)xtract
    (Li)st Archives
    (M)anage Password
    (O)ptions
    (C)lear Screen
    (D)elete
    (Q)uit
    (R)evoke Folder Lock
    """
    print(option)
    locker = Locker()
    while True:
        opt = input("Choose Options: ").lower()
        if opt == 'l':
            locker.lock(getpass())
        elif opt == 'u':
            locker.unlock(getpass())
        elif opt == 'a':
            locker.append(input("Archive Name: "), getpass())
        elif opt == 'e':
            locker.extract(input("Archive Name: "), getpass())
        elif opt == 'li':
            locker.showArchives(getpass())
        elif opt == 'o':
            print(option)
        elif opt == 'd':
            locker.delete(input("Archive Name: "), getpass())
        elif opt == 'c':
            os.system('cls')
        elif opt == 'm':
            locker.setPass()
        elif opt == "r":
            print("All of your unsaved data will be lost and cannot be recovered?")
            op = input("Press [Y/N] to show confirmation: ").lower()
            if op == 'y':
                rmtree('.locker')
                locker.unlock(getpass())
                rmtree('Locked')
                os.remove("secret.pkl")
                print("All the permissions have been revoked!")
                input("Press [ENTER] to Finish")
                exit()
        elif opt == 'q':
            print("Exiting the program")
            input("Press [ENTER] to continue")
            exit()
        else:
            print("{}Invalid Option choosen".format(colorama.Fore.RED))
            pass