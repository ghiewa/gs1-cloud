# Settings for GS1_Cloud_CHECK_GTINS.py and GS1_Cloud_VIEW_GTINS.py
#
# Choose the name of the inputfile here
# Standard value = "sample_gtins.txt"
input_file = "sample_gtins.txt"

# Choose output language here
# You can find an overview of the available languages in the file messages.py
# Standard value = 'en'
output_language = 'en'

# Choose if you want output to screen per GTIN here (False or True)
# Standard value = False
output_to_screen = False

# Choose the maximum length of the description read from the input_file
# If a large data file takes to much memory you can lower this value
# Standard value = 100
max_length_description = 100

# Header for the output files
# It's possible to change it to your own langugage here
# You can also add extra colums to the in- and output bij using "|" as delimiter in the GTIN description
# Add the column titles to this header also using "|" as delimiter
# Standard value = "GTIN|STATUS|MESSAGEID|REASON|GCP_COMPANY|COMPANY|LANGUAGE|GS1_MO|DESCRIPTION_IN_INPUT \n"
csv_header = "GTIN|STATUS|MESSAGEID|REASON|GCP_COMPANY|COMPANY|LANGUAGE|GS1_MO|DESCRIPTION_IN_INPUT\n"

# Poolsize is the number of threads used by the program
# It can be set higher depending on your system and internet connection.
# Please note that GS1 Cloud is still in beta and that the capacity of the API is limited.
# If errors occur and/or the API doesn't give a 100 % return you can lower the pool size in order to get better results.
# Standard value = 100
poolsize = 100

# Batchsize is the number of GTINS send to the API per batch
# Standard value = 10000
batchsize = 10000

# If you have to run the same dataset again due to a break or crash
# you can set te batch number you want to start with here.
# You can find the numbers of the processed batches in the log file
# Remember that the first batch is 0 (zero).
# Standard value = 0
start_with_batch = 0
