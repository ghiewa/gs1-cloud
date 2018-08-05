#
# Program to VIEW GTINS which are stored in the GS1 Cloud (BETA) via the VIEW API
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
    def view(GTIN_in):

        userstr = credentials.login['email'] + ':' + credentials.login['api_key']

        usrPass = base64.b64encode(userstr.encode())

        headers = {'Authorization': "Basic %s" % str(usrPass)[2:-1]}

        url = "https://cloud.gs1.org/api/v1/products/%s/" % GTIN_in

        response = requests.request("GET", url, headers=headers)
        api_status_code = response.status_code
        # print(json.dumps(response.text))
        # print(api_status_code)len(view_response)

        if api_status_code == 404:
            print(GTIN_in + ' Not Found')
            log.write('%s|Not Found\n' % (GTIN_in))

        if api_status_code in (200, 400):
            view_response = json.loads(response.text)

            for cntr in range(0, len(view_response)):

                if 'exception' in view_response:
                    gtin = GTIN_in
                    messageId = view_response["messageId"]
                    status = 0
                else:
                    gtin = view_response[cntr]["gtin"]
                    tm = view_response[cntr]["targetMarket"]
                    brand = view_response[cntr]["brand"][0]['value']
                    brand_lang = view_response[cntr]["brand"][0]['language']
                    ld = view_response[cntr]["labelDescription"][0]['value']
                    ld_lang = view_response[cntr]["labelDescription"][0]['language']
                    gpc = view_response[cntr]["gpc"]
                    company = view_response[cntr]["companyName"][0]['value']
                    company_lang = view_response[cntr]["companyName"][0]['language']
                    ip_gln = view_response[cntr]["informationProviderGln"]
                    ds_gln = view_response[cntr]["dataSourceGln"]

                    if view_response[cntr]["imageUrlMedium"] != []:
                        image_url = view_response[cntr]["imageUrlMedium"][0]['value']
                        image_url_lang = view_response[cntr]["imageUrlMedium"][0]['language']
                        if image_url_lang == "":
                            image_url_lang = 'xx'
                    else:
                        image_url = ""
                        image_url_lang = ""

            # message_out = next(x for x in messages if x[0] == messageId)[1]
                    if ld_lang == "":
                        ld_lang = 'xx'
                    if brand_lang == "":
                        brand_lang = 'xx'
                    if company_lang == "":
                        company_lang = 'xx'

                print(gtin, tm, brand, brand_lang, ld, ld_lang, gpc, company, company_lang, image_url, image_url_lang, ip_gln, ds_gln)

                output.write('%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s \n'
                             % (gtin, tm, brand, brand_lang, ld, ld_lang, gpc, company, company_lang, image_url, image_url_lang, ip_gln, ds_gln))
            else:
                if api_status_code == 401:
                    print('Full authentication is required to access this resource')
                    exit()
                log.write('%s %s %s \n' % (GTIN_in, api_status_code, json.dumps(response.text)))

        return

    gtins = []
    tested = 0
    poolsize = 100  # seems to be an optimum tested with 5000 gtins

    starttime = time.time()
    timestr = time.strftime("%Y%m%d_%H%M%S")

    if not os.path.exists('output'):
        os.makedirs('output')

    output_folder = Path("./output/")

    output_to_open = "view_gtins_%s.csv" % timestr
    log_to_open = "view_gtins_%s.log" % timestr

    output = open(output_folder / output_to_open, "w", encoding='utf-8')
    log = open(output_folder / log_to_open, "w", encoding='utf-8')

    # Write CSV Header
    output.write("GTIN|TARGETMARKET|BRANDNAME|LANGUAGE|LABELDESCRIPTION|LANGUAGE|GPC|COMPANY|LANGUAGE|IMAGE|LANGUAGE|INFORMATIONPROVIDER|DATASOURCE \n")

    if not os.path.isfile("active_gtins.txt"):
        print("Please run GS1_Cloud_CHECK_GTINS.py first. In order to identify active GTINS and create the input file (active_gtins.txt).")
        log.write("Please run GS1_Cloud_CHECK_GTINS.py first. In order to identify active GTINS and create the input file (active_gtins.txt)\n")
    else:
        with open("active_gtins.txt", "r") as myfile:
            for line in myfile:
                gtin = line.replace('\n', '')
                gtins.append(gtin)
                tested = tested + 1
        myfile.close()

    # Instantiate a thread pool with n worker threads
    pool = ThreadPool(poolsize)

    # Add the jobs in bulk to the thread pool. Alternatively you could use
    # `pool.add_task` to add single jobs. The code will block here, which
    # makes it possible to cancel the thread pool with an exception when
    # the currently running batch of workers is finished.
    pool.map(view, gtins)
    pool.wait_completion()

    # Demonstrates that the main process waited for threads to complete
    sec = round((time.time() - starttime))

    print("Done")
    print()
    print("GTINS viewed: ", tested)
    print()
    print("Time:", str(datetime.timedelta(seconds=sec)))
    print()
    if tested > 0:
        print("Views per second: ", round(tested / max(sec, 1), 1))

    log.write('\n')
    log.write("Pool size: %s\n" % poolsize)
    log.write('\n')
    log.write("GTINS viewed: %s\n" % tested)
    log.write('\n')
    log.write("Time: %s\n" % str(datetime.timedelta(seconds=sec)))
    log.write('\n')
    if tested > 0:
        log.write("Views per second: %s\n" % round(tested / max(sec, 1), 1))

    output.close()
    log.close()
