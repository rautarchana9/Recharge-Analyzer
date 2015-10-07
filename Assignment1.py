from math import sqrt
#
#  Program written in class on 9 July 2014
#
#  There are three main steps:
#      (i) get input
#      (ii) analsye input
#      (iii) print result
#
#  We write one function for each.
#

def get_input_from_user(input_list):
    """ 
This function takes a list of triples of the form (key, example, name),
prompts the user for each such triple and returns a dictionary where
for each key the input value provided by the user is stored.
    """
    my_kosh = {}
    for (key, example, name, default_val) in input_list:
       my_kosh[key] = raw_input("Enter "+ name + example + ": ").strip() or default_val
    return my_kosh

def analyse_input(params):
    """
This function takes a dictionary of parameters, which includes the 
filename, canteen name, etc., and returns the following in a dictionary.
(i)   The total number of recharges
(ii)  The average amount of recharge
(iii) 
    """
    def matches(row, params):
        """
Returns True if the data in the row dictionary and satisfies the conditions in
the params dictionary are compatible, otherwise returns False.
        """

#
# The date_and_time is split here and the day number is computed.
# Then the day_number is translated into week day and stored in row["day"].
# You do not need to do anything to this code. 
#    
        import datetime
        row["date"], row["time"] = row["date_and_time"].split()
        (day, month, year) = (int(x) for x in row["date"].split("-"))
        day_number = datetime.date(year,month,day).weekday()
        row["day"] = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"][day_number]
        row["time"] = [int(x) for x in row["time"].split(":")];

#
# Four things are checked: day, canteen, start_time and end_time.
#  
# Replace the ? by looking at the previous line
#

        day_ok =   params['day'] == "*" or row['day'] == params['day'].lower() 
        canteen_ok =  params["canteen"] == "*" or row["canteen"] == params["canteen"].lower()

        start_time_ok = params["start_time"] == "*" or params["start_time"] <= row["time"]
        end_time_ok =  params["end_time"] == "*" or params["end_time"] >= row["time"]

#         
#       If all four are OK then return True otherwise return False
#
        if day_ok and canteen_ok and start_time_ok and end_time_ok:
            return True
        else:
            return False

#       ---end of def matches---

    import csv
    print "Opening ", params["file_name"], "..."
    with open(params["file_name"], "rb") as my_file:
         inputdata = csv.DictReader(my_file, fieldnames=["date_and_time","amount","canteen"], delimiter=",")

#
#    Initialization: notice minimum is initialized to infinity!
#
         stat_kosh = {"number_of_rows":0, "total":0.0, "mean":0.0,
                      "std_dev":0.0, "maximum":0.0, "minimum":float("inf")    
                     }
         sum_of_squares = 0
         if params["start_time"] != "*":
             params["start_time"] = [int(x) for x in params["start_time"].split(":")];
         if params["end_time"] != "*":    
             params["end_time"] = [int(x) for x in params["end_time"].split(":")];

# We go over all rows in the input data one by one.
# If the row matches the input parameters, then we update stat_kosh 
# appropriately.

         for row in inputdata:
             if matches(row, params):
                 row["amount"] = float(row["amount"])
                 stat_kosh["number_of_rows"] += 1
                 stat_kosh["maximum"] = max(stat_kosh["maximum"], row["amount"])
                 stat_kosh["minimum"] = min(stat_kosh["minimum"], row["amount"])
                 stat_kosh["total"] += row["amount"]
                 sum_of_squares +=  row["amount"]*row["amount"]
     
         if stat_kosh["number_of_rows"] != 0:     
             stat_kosh["mean"] = stat_kosh["total"] / stat_kosh["number_of_rows"]
             stat_kosh["std_dev"] = sqrt(
                                     sum_of_squares/stat_kosh["number_of_rows"]
                                       -  
                                     stat_kosh["mean"] * stat_kosh["mean"]
                                    )

    return stat_kosh

#   ---End of def analyse---


def print_stats(ouput_kosh):

    print "Number of rows = ", output_kosh["number_of_rows"] 

    if output_kosh["number_of_rows"] != 0:
        print "Minimum recharge = Rs.", "%0.2f"%output_kosh["minimum"]
        print "Maximum recharge = Rs.", "%0.2f"%output_kosh["maximum"]
        print "Total recharge = Rs.", "%0.2f"%output_kosh["total"]
        print "Mean recharge = Rs.", "%0.2f"%output_kosh["mean"]
        print "Standard deviation = Rs.", "%0.2f"%output_kosh["std_dev"]
        return True
    else: return False

#
#  Main program
#   
#  The input list is arrange in tuples of the form
#
#  (key, example, name to be used while prompting the user, default)
#
#

print """
Welcome to the recharge analyser program written by Archana Raut!
Leave the entry empty or type '*' if you want to impose no constraints.
"""


print

input_list = [ 
("file_name", "[default recharge_data.csv]", "File Name ", "recharge_data.csv"),
("day", "[e.g., Monday]", "Day ", "*"),
("canteen", "[e.g., basement, east, west_s, west_n]", "Canteen ", "*"),
("start_time", "[e.g., 12:30]", "Start Time for the analysis ", "*"),
("end_time", "[e.g., 14:45]", "End Time for the analysis ", "*"),
]

response = 'y'

while response == 'y' or response == 'yes':
    input_kosh = get_input_from_user(input_list)

    raw_input()

    output_kosh =  analyse_input(input_kosh)

    print_stats(output_kosh)

    print
    response = raw_input("Do you want to continue analysing the records? (y/n) ").lower()
    print

print "Good bye!"
