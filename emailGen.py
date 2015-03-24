from itertools import product
from time import sleep


# Helper generator to flatten the list in possiblilies
def flatten(x):
    result = []
    for el in x:
        if hasattr(el, "__iter__") and not isinstance(el, (str, bytes)):
            result.extend(flatten(el))
        else:
            result.append(el)
    return result
#--------------------------------------------------------



company = input("What is their company domain name?\t")

first_name =  input("What is their first name?\t")
middle_init = input("What is their middle initial? (Enter to skip)\t")
last_name =   input("What is their last name?\t")
birthdate =    input("What is their birthdate? (MM/DD/YYYY)\t")
print("\nGenerating email combinations...")

#--------------


has_middle_init = middle_init and len(middle_init) == 1


# Possibilities for names

first_name_choices = ["", first_name[0], first_name]
# Only use if middle initial entered
if has_middle_init: 
	middle_init_choices = ["", middle_init]
	# Assume middle initial always after first name, and combine them
	first_name_choices = list(product(first_name_choices, middle_init_choices))
last_name_choices = ["", last_name[0], last_name]

name_choices = list(product(first_name_choices, last_name_choices))
name_choices.extend(list(product(last_name_choices, first_name_choices)))


# Possiblilies for birthdates

month, day, year = birthdate.split("/");
# Remove 0 from front of month
month = str(int(month))
# Option for 2 digit year
year2 = year[2:]
birthdate_choices = ["", month, day, year, year2] #, month+day]


# Combining them
possibilities = list(product(name_choices, birthdate_choices))
possibilities.extend(list(product(birthdate_choices, name_choices)))



# Flatten elements, and remove cases where neither name is fully spelled
new_possibilities = []
for elem in possibilities:
	flattened = list(flatten(elem))
	if (first_name in flattened or last_name in flattened):
		new_possibilities.append(flattened)
possibilities = new_possibilities
print(possibilities)

# possibilities is a list of lists, each of which has one element
# from each group, in all possible orders
print("Generated " + str(len(possibilities)) + " possible email name combinations.")
print("Assembling with delimiters...")




# Delimiters
delims = ["",".","_"]
delim_combos = list(product(delims, delims, delims))
delim_combos = [elem for elem in delim_combos if not ("." in elem and "_" in elem)]

#-------------------------------


email_list = []
# All combos are of size 4
for combo in possibilities:
	for delim in delim_combos:
		temp_combo = list(combo)
		print(temp_combo)
		email = ""

		while temp_combo:
			if not temp_combo[0]:
				temp_combo = temp_combo[1:]
				continue
			email += temp_combo[0]
			temp_combo = temp_combo[1:]
			if not temp_combo:
				break
			email += delim[0]
			delim = delim[1:]

		if not email:
			continue
		if email[-1] in delims:
			email = email[:-1]
		email_list.append(email + "@" + company)


# email_list is a massive list of all permutations deemed reasonable
print("Generated " + str(len(email_list)) + " possible email strings.")
sleep(2.5)
print(email_list)

