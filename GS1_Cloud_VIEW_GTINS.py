#
# Program to VIEW GTINS which are stored in the GS1 Cloud (BETA) via the VIEW API
#
# Author: Sjoerd Schaper (sjoerd.schaper@gs1.nl)
# Source code available at: https://github.com/sjoerdsch/gs1-cloud
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
import config


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
                if config.output_to_screen:
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
    def view(data_in):

        GTIN_in = data_in[:14]
        GTIN_descr = data_in[15:]

        if config.environment == "PROD":
            # URL for the production environment of GS1 Cloud
            url = "https://cloud.gs1.org/api/v1/products/%s/" % GTIN_in
        else:
            # URL for the staging environment of GS1 Cloud
            url = "https://cloud.stg.gs1.org/api/v1/products/%s/" % GTIN_in

        response = requests.request("GET", url, headers=headers)
        api_status_code = response.status_code
        # print(json.dumps(response.text))
        # print(api_status_code)len(view_response)

        if api_status_code == 404:
            if config.output_to_screen:
                print(GTIN_in + ' Not Found')
            log.write('%s Not Found\n' % (GTIN_in))

        if api_status_code in (200, 400):
            view_response = json.loads(response.text)

            for cntr in range(0, len(view_response)):
                ld = ""
                ld_lang = ""
                brand = ""
                brand_lang = ""
                company = ""
                company_lang = ""
                gpc = ""

                if 'exception' in view_response:
                    gtin = GTIN_in
                    messageId = view_response["messageId"]
                    status = 0
                    print(messageId, status)
                else:
                    gtin = view_response[cntr]["gtin"]
                    tm = view_response[cntr]["targetMarket"]
                    gtin = view_response[cntr]["gtin"]
                    tm = view_response[cntr]["targetMarket"]
                    if view_response[cntr]["brand"] != []:
                        brand = view_response[cntr]["brand"][0]['value']
                        brand_lang = view_response[cntr]["brand"][0]['language']
                        if brand_lang == "":
                            brand_lang = '-'
                    if view_response[cntr]["labelDescription"] != []:
                        ld = view_response[cntr]["labelDescription"][0]['value']
                        ld_lang = view_response[cntr]["labelDescription"][0]['language']
                        if ld_lang == "":
                            ld_lang = '-'
                    if view_response[cntr]["gpc"] != []:
                        gpc = view_response[cntr]["gpc"]
                        if gpc is None:
                            gpc = ""
                    if view_response[cntr]["companyName"] != []:
                        company = view_response[cntr]["companyName"][0]['value']
                        company_lang = view_response[cntr]["companyName"][0]['language']
                        if company_lang == "":
                            company_lang = '-'
                    if view_response[cntr]["informationProviderGln"] != []:
                        ip_gln = view_response[cntr]["informationProviderGln"]
                        if ip_gln is None:
                            ip_gln = ""
                    if view_response[cntr]["dataSourceGln"] != []:
                        ds_gln = view_response[cntr]["dataSourceGln"]
                        if ds_gln is None:
                            ds_gln = ""

                    if view_response[cntr]["imageUrlMedium"] != []:
                        image_url = view_response[cntr]["imageUrlMedium"][0]['value']
                        image_url_lang = view_response[cntr]["imageUrlMedium"][0]['language']
                        if image_url_lang == "":
                            image_url_lang = '-'
                    else:
                        image_url = ""
                        image_url_lang = ""

                if config.output_to_screen:
                    print(gtin, tm, brand, brand_lang, ld, ld_lang, gpc, company, company_lang, image_url, image_url_lang, ip_gln, ds_gln, GTIN_descr)

                output.write('%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s \n'
                             % (gtin, tm, brand, brand_lang, ld, ld_lang, gpc, company, company_lang, image_url, image_url_lang, ip_gln, ds_gln, GTIN_descr))
        else:
            if api_status_code == 401:
                print('Full authentication is required to access this resource')
            if api_status_code != 404:
                log.write('%s %s %s \n' % (GTIN_in, api_status_code, json.dumps(response.text)))

        return

    """ Start of the main program """
    gtins = []
    data_in = []
    tested = 0

    userstr = credentials.login['email'] + ':' + credentials.login['api_key']

    usrPass = base64.b64encode(userstr.encode())

    headers = {'Authorization': "Basic %s" % str(usrPass)[2:-1]}

    starttime = time.time()
    timestr = time.strftime("%Y%m%d_%H%M%S")

    # for the sample file no date-time stamp is used
    if config.input_file == "sample_gtins.txt":
        timestr = "yyyymmdd_hhmmss"

    if not os.path.exists('output'):
        os.makedirs('output')

    output_folder = Path("./output/")
    output_file = config.input_file.split(".")

    output_to_open = "%s_view_%s.csv" % (output_file[0], timestr)
    log_to_open = "%s_view_%s.log" % (output_file[0], timestr)

    output = open(output_folder / output_to_open, "w", encoding='utf-8')
    log = open(output_folder / log_to_open, "w", encoding='utf-8')

    # Write CSV Header
    output.write("GTIN|TARGETMARKET|BRANDNAME|LANGUAGE|LABELDESCRIPTION|LANGUAGE|GPC|COMPANY|LANGUAGE|IMAGE|LANGUAGE|INFORMATIONPROVIDER|DATASOURCE|DESCRIPTION_IN_INPUT \n")

    if not os.path.isfile('./input/' + output_file[0] + '_active.txt'):
        print("Please run GS1_Cloud_CHECK_GTINS.py first, in order to identify active GTINS and create the input file (%s_active.txt)." % output_file[0])
        log.write("Please run GS1_Cloud_CHECK_GTINS.py first, in order to identify active GTINS and create the input file (%s_active.txt)\n" % output_file[0])
    else:
        with open(str('./input/' + output_file[0] + '_active.txt'), "r") as myfile:
            for line in myfile:
                gtin = line.replace('\n', '')
                data_in.append(gtin)
                tested = tested + 1
        myfile.close()

    # Instantiate a thread pool with n worker threads
    pool = ThreadPool(config.poolsize)

    # Add the jobs in bulk to the thread pool.
    pool.map(view, data_in)
    pool.wait_completion()

    # The main process is waiting for threads to complete
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
    log.write("Pool size: %s\n" % config.poolsize)
    log.write('\n')
    log.write("GTINS viewed: %s\n" % tested)
    log.write('\n')
    log.write("Time: %s\n" % str(datetime.timedelta(seconds=sec)))
    log.write('\n')
    if tested > 0:
        log.write("Views per second: %s\n" % round(tested / max(sec, 1), 1))

    output.close()
    log.close()
