# Settings for GS1_Cloud_CHECK_GTINS.py and GS1_Cloud_VIEW_GTINS.py
#
# Choose the name of the inputfile here
input_file = "gtins.txt"

# Choose output language here
# You can find an overview of the available languages in the file messages.py
output_language = 'en'

# Choose if you want output to screen per GTIN here (False or True)
output_to_screen = False

# Poolsize is the number of threads used by the program
# It can be set higher depending on your system and internet connection.
# Please not that GS1 Cloud is still in beta and that the capacity of the API is limited.
# If errors occur and/or the API doesn't give a 100 % return you can lower the pool size in order to get better results.
poolsize = 100

# Batchsize is the number of GTINS send to the API per batch
batchsize = 10000

# If you have to run the same dataset again due to a break or crash
# you can set te batch number you want to start with here.
# You can find the numbers of the processed batches in the log file
# Remember that the first batch is 0 (zero).
start_with_batch = 0
