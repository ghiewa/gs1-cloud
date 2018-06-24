#
# Program to CHECK the validity of GTINS against the GS1 Cloud (BETA) CHECK API
#
# Author: Sjoerd Schaper (sjoerd.schaper@gs1.nl)
#
# Put your credentials (email and api-key) in the file credentials.py
#

import datetime
import json
import time
from io import open
import requests
from queue import Queue
from threading import Thread
import base64
from pathlib import Path
import os
import credentials


class Worker(Thread):
    """ Thread executing tasks from a given tasks queue """
    def __init__(self, tasks):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.start()

    def run(self):
        while True:
            func, args, kargs = self.tasks.get()
            try:
                func(*args, **kargs)
            except Exception as e:
                # An exception happened in this thread
                print(e)
            finally:
                # Mark this task as done, whether an exception happened or not
                self.tasks.task_done()


class ThreadPool:
    """ Pool of threads consuming tasks from a queue """
    def __init__(self, num_threads):
        self.tasks = Queue(num_threads)
        for _ in range(num_threads):
            Worker(self.tasks)

    def add_task(self, func, *args, **kargs):
        """ Add a task to the queue """
        self.tasks.put((func, args, kargs))

    def map(self, func, args_list):
        """ Add a list of tasks to the queue """
        for args in args_list:
            self.add_task(func, args)

    def wait_completion(self):
        """ Wait for completion of all the tasks in the queue """
        self.tasks.join()


if __name__ == "__main__":

    # Function to be executed in a thread
    def check(GTIN_in):

        # Choose output language here
        output_language = 'en'

        if output_language == 'en':
            # Standard set of messages in English
            messages = [("E001", "Integrity failed: The length of this GTIN is invalid."),
                        ("E002", "Integrity failed: Incorrect check digit."),
                        ("E003", "Integrity failed: String contains alphanumerical characters."),
                        ("E004", "Incorrect number.That GS1 prefix(3 - digit country code) does not exist."),
                        ("E005", "Incorrect number based on GS1 Prefix reserved for special use."),
                        ("S001", "Unknown number, no information can be returned."),
                        ("S002", "Unknown GTIN from a license issued to: "),
                        ("S003", "Active GTIN from a license issued to: "),
                        ("S004", "Inactive GTIN from a license issued to: "),
                        ("S005", "Active GTIN from a license issued to:")]
        else:
            # Messages in local language
            messages = [("E001", "Onjuiste structuur: De lengte van de GTIN is niet correct (moet 14 cijfers zijn)."),
                        ("E002", "Onjuiste structuur: Niet correct controle getal."),
                        ("E003", "Onjuiste structuur: De GTIN bevat alfanumerieke karakters."),
                        ("E004", "Onjuist nummer. De GS1 prefix(3-cijferige landcode) bestaat niet."),
                        ("E005", "Onjuist nummer: de GS1 Prefix is gereserveerd voor speciale toepassingen."),
                        ("S001", "Onbekend nummer, er kan geen informatie gegeven worden."),
                        ("S002", "Onbekende GTIN van een licentie verleend aan: "),
                        ("S003", "Actieve GTIN van een licentie verleend aan: "),
                        ("S004", "Inactieve GTIN van een licentie verleend aan: "),
                        ("S005", "Actieve GTIN van een licentie verleend aan:")]



        userstr= credentials.login['email'] + ':' + credentials.login['api_key']

        usrPass = base64.b64encode(userstr.encode())

        headers = {'Authorization': "Basic %s" % str(usrPass)[2:-1]}

        url = "https://cloud.gs1.org/api/v1/products/%s/check" % GTIN_in

        response = requests.request("GET", url, headers=headers)
        api_status_code = response.status_code
        # print(json.dumps(response.text))

        if api_status_code in (200, 400):
            x = json.loads(response.text)

            company = ""

            if 'exception' in x:
                gtin = GTIN_in
                messageId = x["messageId"]
                status = 0
            else:
                gtin = x["gtin"]
                messageId = x["reason"][0]['messageId']
                status = x["status"]
                if 'gcpCompanyName' in x:
                    company = x["gcpCompanyName"]

            message_out = next(x for x in messages if x[0] == messageId)[1]

            print(api_status_code, status, gtin, messageId, message_out, company)

            output.write('%s|%s|%s|%s|%s \n' % (gtin, status, messageId, message_out, company))
        else:
            log.write('%s %s %s \n' % (GTIN_in, api_status_code, json.dumps(response.text)))
        return


    gtins = []
    tested = 0
    poolsize = 100  # seems to be an optimum tested with 5000 gtins

    starttime = time.time()
    timestr = time.strftime("%Y%m%d_%H%M%S")

    output_folder = Path("./output/")

    output_to_open = "Tested_gtins_%s.csv" % timestr
    log_to_open = "Tested_gtins_%s.log" % timestr
    
    #f = open(file_to_open)

    output = open(output_folder / output_to_open, "w", encoding='utf-8')
    log = open(output_folder / log_to_open, "w", encoding='utf-8')

    # Write CSV Header
    output.write("GTIN|STATUS|MESSAGEID|REASON|COMPANY \n")

    # Generate list of GTINS
    with open("gtins.txt", "r") as myfile:
        for line in myfile:
            gtin = line.replace('\n', '')
            gtins.append(gtin)
            tested = tested + 1


    # Instantiate a thread pool with n worker threads
    pool = ThreadPool(poolsize)

    # Add the jobs in bulk to the thread pool. Alternatively you could use
    # `pool.add_task` to add single jobs. The code will block here, which
    # makes it possible to cancel the thread pool with an exception when
    # the currently running batch of workers is finished.
    pool.map(check, gtins)
    pool.wait_completion()

    # Demonstrates that the main process waited for threads to complete
    sec = round((time.time() - starttime))

    print("Done")
    print()
    print("Pool size: ", poolsize)
    print()
    print("GTINS checked: ", tested)
    print()
    print("Time:", str(datetime.timedelta(seconds=sec)))
    print()
    if tested > 0:
        print("Checks per second: ",round(tested/sec,1))

    log.write('\n')
    log.write("Pool size: %s\n" % poolsize)
    log.write('\n')
    log.write("GTINS checked: %s\n" % tested)
    log.write('\n')
    log.write("Time: %s\n" % str(datetime.timedelta(seconds=sec)))
    log.write('\n')
    if tested >0:
        log.write("Checks per second: %s\n" % round(tested / sec, 1))

    output.close()
    myfile.close()
    log.close()
