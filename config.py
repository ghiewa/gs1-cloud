# Choose output language here
# you can find an overview of the available languages in the file messages.py
output_language = 'en'

# Choose if you want output to screen per GTIN here (False or True)
output_to_screen = False

# Poolsize is the number of threads used by the program
# It can be set upto 500. Depending on your system and internet connection you might be able to increase it.
poolsize = 500

# If you have to run the same dataset again due to a break or crash
# you can set te batch number you want to start with here.
#
# The batch number is equal to the last digit of the GTINS.
# So the first batch has number 0 (zero) and the last one 9 (nine).
start_with_batch = 0
