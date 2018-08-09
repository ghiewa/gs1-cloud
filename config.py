# Choose output language here (en or nl)
output_language = 'en'

# Choose if you want output to screen per GTIN here (False or True)
output_to_screen = False

# Poolsize is the number of threads used by the program
# There seems to be an optimum of 100. This is tested with 5000 gtins for larger sets of gtins this can set higher eg. 150
poolsize = 100

# If you have to run the same dataset again due to a break or crash
# you can set te batch number you want to start with here.
#
# The batch number is equal to the last digit of the GTINS.
# So the first batch has number 0 (zero) and the last one 9 (nine).
start_with_batch = 0
