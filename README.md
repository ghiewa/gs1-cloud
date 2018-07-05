# GS1 Cloud GTIN CHECK (BETA)

Program to CHECK the validity of GTINS/EAN codes against the GS1 Cloud (BETA) CHECK API

The GS1 Cloud will be the largest source of trusted product information in the world, making it possible for businesses to meet the expectations of today’s digital world.
For more information  <a href="https://www.gs1.org/services/gs1-cloud" target="_blank">GS1.org</a>.

**Install and usage notes**
1. Install Python3 on your computer. 
2. Download the zip with the programfiles on your local machine and unpack and store it in a local map.
3. Put your credentials (email and api-key) in the file credentials.py. 
   The API key can be found in the <a href="https://cloud.gs1.org/gs1-portal/" target="_blank">GS1 Cloud user interface</a> 
   under 'Account'.
4. Add your set of GTINS in the file gtins.txt. The program has been tested with up to 500.000 GTINS in one file.
   The GTINS have to be 14 digits long, including leading zero's. The attached file gtins.txt will generate most of the current messages.
5. Run the program in the shell program of your OS (..>python "GS1 Cloud Check GTINS.py") or a Python IDE. 
   It will test about 35 GTINS per second.
6. Find the output in .\output\Tested_gtins_yyyymmdd_hhmmss.csv.
   Also a log file is created as .\output\Tested_gtins_yyyymmdd_hhmmss.log
7. View and analyze your results in a spreadsheet or database.

