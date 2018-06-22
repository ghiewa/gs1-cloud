# GS1 Cloud GTIN CHECK (BETA)

Program to CHECK the validity of GTINS/EAN codes against the GS1 Cloud (BETA) CHECK API

Install the program on your local machine. It's written in Python 3.

Put your credentials (email and api-key) in the file credentials.py. 
The API key can be found in the GS1 Cloud user interface under 'Account'.

Add your set of GTINS in the file gtins.txt. The program has been tested with up to 500.000 GTINS in one file.
The GTINS have to be 14 digits long, including leading zero's. The attached file gtins.txt will generate most of the current messages.

Run the program. It will test about 35 GTINS per second.

Find the output in .\output\Tested_gtins_yyyymmdd_hhmmss.csv

Also a log file is created as .\output\Tested_gtins_yyyymmdd_hhmmss.log

For more information  <a href="https://www.gs1.org/services/gs1-cloud" target="_blank">GS1.org</a>.
