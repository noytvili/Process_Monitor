import psutil, time, base64, datetime, os, platform
from time import strftime, localtime, sleep

global flag
flag = False

def validate(date_text):
    try:
        datetime.datetime.strptime (date_text, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        print ("Incorrect data format, should be YYYY-MM-DD HH:MM:SS")
        main ()

def MonitorMode(x):
    try:
        ClearScreen ()
        PrintScan ()
        while True:
            dict1 = {}
            for p in psutil.process_iter ():
                dict1[p.pid] = p.name (), p.status (), p.create_time ()
                with open ("process_list.csv", "a") as process_list:
                    process_list.write (base64.b64encode (
                        str (p.pid) + "," + p.name () + "," + strftime ("%Y-%m-%d %H:%M:%S",
                                                                        localtime ()) + "," + p.status ()))
                    process_list.write ("\r\n")
            dict2 = {}
            sleep (x)
            for p in psutil.process_iter ():
                dict2[p.pid] = p.name (), p.status (), p.create_time ()
                with open ("process_list.csv", "a") as process_list:
                    process_list.write (base64.b64encode (
                        str (p.pid) + "," + p.name () + "," + strftime ("%Y-%m-%d %H:%M:%S",
                                                                        localtime ()) + "," + p.status ()))
                    process_list.write ("\r\n")
            value = {k: dict2[k] for k in set (dict2) - set (dict1)}
            if value:
                for key, value1 in value.items ():
                    with open ("Status_Log_File.csv", "a") as status_log:
                        name, status, time = value1
                        print (str (key) + "," + name + "," + "opened" + "," + strftime ("%Y-%m-%d %H:%M:%S",
                                                                                         localtime ()))
                        status_log.write (base64.b64encode (
                            str (key) + "," + name + "," + "opened" + "," + strftime ("%Y-%m-%d %H:%M:%S",
                                                                                      localtime ())))
                        status_log.write ("\r\n")
            value = {k: dict1[k] for k in set (dict1) - set (dict2)}
            if value:
                for key, value1 in value.items ():
                    with open ("Status_Log_File.csv", "a") as status_log:
                        name, status, time = value1
                        print (str (key) + "," + name + "," + "closed" + "," + strftime ("%Y-%m-%d %H:%M:%S",
                                                                                         localtime ()))
                        status_log.write (base64.b64encode (
                            str (key) + "," + name + "," + "closed" + "," + strftime ("%Y-%m-%d %H:%M:%S",
                                                                                      localtime ())))
                        status_log.write ("\r\n")
    except KeyboardInterrupt:
        ClearScreen ()
        main ()

def DecodeMode():
    try:
        with open ("process_list.csv") as process_list:
            process_list_Decode = open ("process_list_Decode.csv", "w")  # changed to w from a
            l = process_list.readlines ()
            for i in l:
                process_list_Decode.write (base64.b64decode (i))
                process_list_Decode.write ("\r\n")
    except IOError:
        print ("There is no encode file for processList!\n")
        pass
    try:
        with open ("Status_Log_File.csv") as Status_Log_File:
            Status_Log_File_Decode = open ("Status_Log_File_Decode.csv", "w")  # Changed to w from a
            l = Status_Log_File.readlines ()
            for i in l:
                Status_Log_File_Decode.write (base64.b64decode (i))
                Status_Log_File_Decode.write ("\r\n")
    except IOError:
        print ("There is no encode file for Status_Log!\n")
        pass
    try:
        with open ("Status_Log_File_Manual.csv") as Status_Log_File:
            Status_Log_File_Decode = open ("Status_Log_File_Manual_Decode.csv", "w")
            l = Status_Log_File.readlines ()
            for i in l:
                Status_Log_File_Decode.write (base64.b64decode (i))
                Status_Log_File_Decode.write ("\r\n")
    except IOError:
        print ("There is no encode file for Status_Log_File_Manual!\n")

def user_time_set(time, time_list=[]):
    tmp_time = ""
    # print "user_time_set the time: ", time    # TEST
    time_format = '%Y-%m-%d %H:%M:%S'
    time_dt = datetime.datetime.strptime (time, time_format).time ()
    for i in xrange (0, len (time_list) - 1):
        if datetime.datetime.strptime (time_list[i], time_format).time () == time_dt:
            tmp_time = time_list[i]
            break
        elif datetime.datetime.strptime (time_list[i + 1], time_format).time () > time_dt:
            tmp_time = time_list[i]
            break
    return tmp_time

def ManualMonitor():
    ClearScreen ()
    user_input1 = raw_input("Enter First time in format  YYYY-MM-DD HH:MM:SS\nExample:2018-04-29 21:39:46 \n")
    validate(user_input1)
    user_input2 = raw_input("Enter Second time same format: \n")
    validate(user_input2)
    dict1 = {}
    dict2 = {}
    decoded_list = []
    time_list = []
    try:
        with open ("process_list.csv") as process_list:
            lines = process_list.readlines ()
            for i in lines:
                decoded_list.append (base64.b64decode (i))
            for i in decoded_list:
                line = str (i).split (",")
                time_list.append (line[2])
        # rounding user input 1 & 2 time
        user_input1 = user_time_set (user_input1, time_list)
        user_input2 = user_time_set (user_input2, time_list)

        for i in decoded_list:
            if user_input1 in i:
                s = str (i).split (",")
                dict1[s[0]] = s[1]
            elif user_input2 in i:
                s = str (i).split (",")
                dict2[s[0]] = s[1]

        # try:                                                          # START COMMENT
        #     with open("process_list_Decode.csv") as f:
        #         for line in f:
        #             if user_input1 in line:
        #                 s = line.split(",")
        #                 dict1[s[0]] = s[1]  # dict[pid] = process_name
        #     with open("process_list_Decode.csv") as f:
        #         for line in f:
        #             if user_input2 in line:
        #                 s = line.split(",")
        #                 dict2[s[0]] = s[1]  # dict[pid] = process_name End Comment
        #     print dict1
        #     print dict2
        value = {k: dict2[k] for k in set (dict2) - set (dict1)}
        if value:
            with open ("Status_Log_File_Manual.csv", "w+") as status_log:
                for key, value1 in value.items ():
                    status_log.write ("\r\n")
                    name = value1
                    print (str (key) + "," + name + "," + "opened")
                    status_log.write (base64.b64encode (str (key) + "," + name + "," + "opened"))
        value = {k: dict1[k] for k in set (dict1) - set (dict2)}
        if value:
            with open ("Status_Log_File_Manual.csv", "w+") as status_log:
                for key, value1 in value.items ():
                    status_log.write ("\r\n")
                    name = value1
                    print (str (key) + "," + name + "," + "closed")
                    status_log.write (base64.b64encode (str (key) + "," + name + "," + "closed"))
    except IOError:
        print ("There is no Decode files found!\n")
        pass

#     except KeyboardInterrupt:
#         ClearScreen()
#         main()

def readNumber(x):
    try:
        return int (x)  # raw_input in Python 2.x
    except ValueError:
        pass

def isItExit(x):
    if x == "exit()":
        return True
    else:
        #         raise ValueError('A very specific bad thing happened.')
        pass

def Auth(user, password):
    global flag
    flag = False
    mine = base64.b64encode (password)
    mine2 = base64.b64encode (user)
    if mine2 == "QWRtaW4=" and mine == "UHIwMGNlNTVNMG4hNzBS":
        print ("Success!\n")
        flag = True
    return mine2 == "QWRtaW4=" and mine == "UHIwMGNlNTVNMG4hNzBS"

def DeleteFiles():
    if platform.system () == "Windows":
        os.system ("del *.csv")
    else:
        os.system ("rm *.csv")

def ClearScreen():
    if (platform.system () == "Windows"):
        os.system ("cls")
    else:
        os.system ("clear")

def PrintBye():
    if (platform.system () == "Windows"):
        os.system ("cls")
        os.system ("type goodbye.txt")
    else:
        os.system ("clear")
        os.system ("cat goodbye.txt")

def PrintArt():
    if (platform.system () == "Windows"):
        os.system ("cls")
        os.system ("type art.txt")
    else:
        os.system ("clear")
        os.system ("cat art.txt")

def PrintScan():
    if (platform.system () == "Windows"):
        os.system ("cls")
        os.system ("type scan.txt")
    else:
        os.system ("clear")
        os.system ("cat scan.txt")


def main():
    #     ClearScreen()
    #     PrintArt()
    counter = 0
    try:
        if not flag:
            user = raw_input ("Enter user name:\n")
            password = raw_input ("Enter password:\n")
            if not (Auth (user, password)):
                while counter < 3:
                    print "Wrong username or password, try again. \n\n"
                    counter += 1
                    user = raw_input ("Enter user name:\n")
                    password = raw_input ("Enter password:\n")
                    if counter == 2:
                        print "Too much tries, bye-bye!"
                        PrintBye ()
                        exit ()
                    if Auth (user, password):
                        counter = 4

    except KeyboardInterrupt:
        PrintBye ()
        exit ()
    while True:
        try:
            PrintArt ()
            x = raw_input (
                "(*)For Monitor Mode press 1 \n(*)For Decode Mode press 2 \n(*)For Manual Mode press 3\n(*)Delete all files press 4\n(*)For quit exit() or ctr+c\n")
            if readNumber (x):
                if int (x) == 1:
                    sec = raw_input ("Enter interval in seconds: \n")
                    MonitorMode (int (sec))
                    continue
                elif int (x) == 2:
                    DecodeMode ()
                elif int (x) == 3:
                    ManualMonitor ()
                elif int (x) == 4:
                    DeleteFiles ()
                else:
                    print "Invalid input, try again!"
            elif isItExit (x):
                exit ()
            else:
                print "Invalid input, try again!"
        except KeyboardInterrupt:
            PrintBye ()
            exit ()

def test1():
    try:
        with open ("process_list.csv") as process_list:
            lines = process_list.readlines ()
            decoded = []
            for i in lines:
                decoded.append (base64.b64decode (i))

            print decoded
    except IOError:
        print "there is no such file"

if __name__ == '__main__':
    main ()