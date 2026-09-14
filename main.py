"""
====================================================================
 PROJECT   : Skincare Tracker
 SUBJECT   : Computer Science
 NAME      : Iffa Intekhab
 CLASS/SEC : 12 - A
====================================================================

 MODULES USED IN THIS PROJECT:
   1. datetime  - used to store the date a product was opened and
                   to calculate expiry dates (date + timedelta math).
   2. pickle    - used for BINARY FILE handling; saves and loads the
                   user's product list (products.dat) so data is not
                   lost when the program closes.
   3. csv       - used for CSV FILE handling; reads two files (skin_concerns.csv and
                   beginner_routine.csv) that the recommendation engine looks up from.
====================================================================
"""

from datetime import date, timedelta
import pickle
import csv


# ====================================================================
# MODULE 1: LOAD SAVED DATA (BINARY FILE - INPUT)
# Loads the product list from products.dat if it exists.
# If this is the first time the program is run, the file won't
# exist yet, so we catch that error and start with an empty list.
# ====================================================================
try:
    with open("products.dat", "rb") as f:
        products = pickle.load(f)
except FileNotFoundError:
    products = []


# ====================================================================
# MODULE 2: CONSTANTS
# Fixed lists used throughout the program - the main menu, product
# categories, and routine timing options.
# ====================================================================
menu_options = ["Add Product", "View All", "Update", "Delete", "Check Expiry",
                "Today's Routine", "Restock Estimator",
                 "Recommendations", "Generate Report", "Export CSV", "Exit"]

categories = ["Cleanser", "Toner/Essence", "Serum", "Moisturizer", "Sunscreen",
              "Exfoliant", "Mask", "Oil", "Others"]

# ====================================================================
# MODULE 3: SORT PRODUCTS BY ROUTINE ORDER
# Rearranges the loaded products so they are always displayed in the
# order they'd actually be used (Cleanser first, then Toner, etc.)
# rather than the order they happened to be added in.
# ====================================================================

def sort_products():
    global products
    sorted_products = []
    for cat in categories:
        for p in products:
            if p["Category"] == cat:
                sorted_products.append(p)
    products = sorted_products
sort_products()

# ====================================================================
# MODULE 4: BEGINNER ONBOARDING (runs once, before the main menu)
# Asks a first-time user for their skin type and shows a simple
# starter routine, read from beginner_routine.csv.
# ====================================================================
Beginner_or_not = input("Are you new to skincare? ").upper()
if Beginner_or_not == "YES":
    beginner_list = []
    with open("beginner_routine.csv", "r", newline="") as g:
        reader_2 = csv.DictReader(g)
        for row in reader_2:
            beginner_list.append(row)

    skin_type = ["Oily", "Dry", "Combination", "Sensitive", "Normal"]

    for i in range(1, len(skin_type) + 1):
        print(i, ".", skin_type[i - 1], ":", beginner_list[i - 1]["Description"])
    skin_type_choice = int(input("Enter the no. corresponding to your skin type: "))

    print("Cleanser recommended for your skin type is:", beginner_list[skin_type_choice - 1]["Cleanser"])
    print("Moisturizer recommended for your skin type is:", beginner_list[skin_type_choice - 1]["Moisturizer"])
    print("Sunscreen recommended for your skin type is:", beginner_list[skin_type_choice - 1]["Sunscreen"])
    print(beginner_list[skin_type_choice - 1]["Notes"])

    add_routine_choice = input("Would you like to save these as starter products? (YES/NO): ").upper()
    if add_routine_choice == "YES":
        starter_cleanser = {"Name": beginner_list[skin_type_choice - 1]["Cleanser"], "Category": "Cleanser",
                            "DateOpened": date.today(), "PAO": 12, "RoutineStep": "BOTH", "AmountLeft": 100}
        starter_moisturizer = {"Name": beginner_list[skin_type_choice - 1]["Moisturizer"], "Category": "Moisturizer",
                               "DateOpened": date.today(), "PAO": 12, "RoutineStep": "BOTH", "AmountLeft": 100}
        starter_sunscreen = {"Name": beginner_list[skin_type_choice - 1]["Sunscreen"], "Category": "Sunscreen",
                             "DateOpened": date.today(), "PAO": 12, "RoutineStep": "BOTH", "AmountLeft": 100}

        products.append(starter_cleanser)
        products.append(starter_moisturizer)
        products.append(starter_sunscreen)
        sort_products()
        print("Your first personalised skincare routine/products added!"
              "\n You can update their real opening date and PAO later from the Update menu."
              "\n You can add more products based on your SKIN CONCERNS through the recommendation menu.")


# ====================================================================
# MODULE 5: MAIN MENU LOOP
# Displays the 11-option menu and routes the user's choice to the
# correct feature below. Runs continuously until the user exits.
# ====================================================================
while True:

    for i in range(1, 12):
        print(i, ".", menu_options[i - 1])

    choice = input("Enter your choice: ")

    # ----------------------------------------------------------------
    # MODULE 5.1: ADD PRODUCT
    # Collects product details from the user and appends a new
    # dictionary to the products list.
    # ----------------------------------------------------------------
    if choice == "1":
        product_name = input("Enter the product name: ")

        for i in range(1, len(categories) + 1):
            print(i, ".", categories[i - 1])
        category_choice = int(input("Enter the No. corresponding to the Category of the product: "))
        category = categories[category_choice - 1]

        year = int(input("enter the year of opening: "))
        month = int(input("enter the month of opening: "))
        day = int(input("enter the day of opening: "))
        date_opened = date(year, month, day)
        period_after_opening = int(input("Enter the PAO in months "
                                         "— check the small jar icon on the packaging, e.g. 6M, 12M:"))


        print("Used in AM, PM, or Both? ")
        routine_times = ["AM", "PM", "BOTH"]
        for i in range(1, len(routine_times) + 1):
            print(i, ".", routine_times[i - 1])
        routine_choice = int(input("Enter the No. corresponding to your choice: "))
        routine_step = routine_times[routine_choice - 1]

        product = {"Name": product_name, "Category": category, "DateOpened": date_opened,
                   "PAO": period_after_opening, "RoutineStep": routine_step, "AmountLeft": 100}
        products.append(product)

    # ----------------------------------------------------------------
    # MODULE 5.2: VIEW ALL PRODUCTS
    # Displays every product currently stored in the list.
    # ----------------------------------------------------------------
    elif choice == "2":
        for i in products:
            print(i)

    # ----------------------------------------------------------------
    # MODULE 5.3: UPDATE A PRODUCT
    # Lets the user pick a product and choose exactly which field
    # (name, category, PAO, or routine step) they want to change.
    # ----------------------------------------------------------------
    elif choice == "3":

        for i in range(1, len(products) + 1):
            print(i, ". ", products[i - 1]["Name"])

        update_choice = int(input("Enter the No. corresponding to the product you wish to update: "))
        for i in range(1, len(products) + 1):
            if i == update_choice:
                print(products[i - 1])

        # what the user wants to update?
        update_fields = ["Product Name", "Product Category", "Date Of Opening ",
                         "PAO(Period After Opening", "Routine Step", "Exit"]
        for i in range(1, len(update_fields) + 1):
            print(i, ".", update_fields[i - 1])

        ask = int(input("What would you like to edit/update? "))

        if ask == 1:
            print("Press 'Enter' to skip ")
            updated_name = input("Enter the product name: ")
            if updated_name == "":
                pass
            else:
                products[update_choice - 1]["Name"] = updated_name

        elif ask == 2:
            for i in range(1, len(categories) + 1):
                print(i, ".", categories[i - 1])
            print("Press 'Enter' to skip ")
            updated_category_choice = int(input("Enter the no. corresponding to the Category of the product: "))
            updated_category = categories[updated_category_choice - 1]

            if updated_category_choice == "":
                pass
            else:
                products[update_choice - 1]["Category"] = updated_category

        elif ask == 4:
            updated_PAO = int(input("Enter the PAO in months — check the small jar icon on the packaging, e.g. 6M, 12M:"))
            products[update_choice - 1]["PAO"] = updated_PAO

        elif ask == 5:
            routine_times = ["AM", "PM", "BOTH"]
            for i in range(1, len(routine_times) + 1):
                print(i, ".", routine_times[i - 1])

            updated_routine_step = int(input("Enter the No. corresponding to the routine Step"))
            products[update_choice - 1]["RoutineStep"] = routine_times[updated_routine_step - 1]

        else:
            pass

    # ----------------------------------------------------------------
    # MODULE 5.4: DELETE A PRODUCT
    # Removes a product from the list by its position number.
    # ----------------------------------------------------------------
    elif choice == "4":
        for i in range(1, len(products) + 1):
            print(i, ". ", products[i - 1]["Name"])

        delete_choice = int(input("Enter the No. corresponding to the product you wish to delete: "))
        products.pop(delete_choice - 1)
        print("Successfully Deleted")

    # ----------------------------------------------------------------
    # MODULE 5.5: CHECK EXPIRY
    # Calculates a product's expiry date (DateOpened + PAO months)
    # and shows how many days remain until it expires.
    # ----------------------------------------------------------------
    elif choice == "5":

        for i in range(1, len(products) + 1):
            print(i, ". ", products[i - 1]["Name"])

        expirydate_choice = int(input("Enter the corresponding no. of the product to check for: "))
        expiry_date = (products[expirydate_choice - 1]["DateOpened"] +
                       (timedelta(days=30) * products[expirydate_choice - 1]["PAO"]))
        print("This product will expire on", expiry_date)
        todays_date = date.today()
        no_of_days = expiry_date - todays_date
        print("in", no_of_days.days, "days")

    # ----------------------------------------------------------------
    # MODULE 5.6: TODAY'S ROUTINE
    # Filters products by AM or PM (including ones marked BOTH) to
    # show only what belongs in the routine the user asks for.
    # ----------------------------------------------------------------
    elif choice == "6":
        print("Today's Routine")

        today_routine_choice = input("AM or PM?").upper()

        for i in (products):
            if today_routine_choice == i["RoutineStep"] or i["RoutineStep"] == "BOTH":
                print(i["Category"], ":", i["Name"])

    # ----------------------------------------------------------------
    # MODULE 5.7: RESTOCK ESTIMATOR (manual check-in)
    # Lets the user log roughly how much product is left and flags
    # ones that are running low.
    # ----------------------------------------------------------------
    elif choice == "7":
        amounts = [100, 75, 50, 25, 0]
        for i in range(1, len(products) + 1):
            print(i, ".", products[i - 1]["Name"])

        amount_check_choice = int(input("Enter the no. corresponding to the product to be checked: "))
        print(products[amount_check_choice - 1]["AmountLeft"])
        if products[amount_check_choice - 1]["AmountLeft"] == 50:
            print("Halfway Done")
        elif products[amount_check_choice - 1]["AmountLeft"] <= 25:
            print("Running low — consider restocking soon!")

        amount_update_choice = input("Do you want to update the amount left?").upper()
        if amount_update_choice == "YES":
            for i in range(1, len(amounts) + 1):
                print(i, ".", amounts[i - 1])

            updated_amount = int(input("Enter the no. corresponding to the amount: "))
            products[amount_check_choice - 1]["AmountLeft"] = amounts[updated_amount - 1]
            print("Updated Successfully")
        else:
            pass

    # ----------------------------------------------------------------
    # MODULE 5.8: RECOMMENDATIONS (CSV FILE - INPUT)
    # Reads skin_concerns.csv and recommends active ingredients,
    # ingredients to avoid combining, and a usage tip for whichever
    # skin concern the user selects.
    # ----------------------------------------------------------------
    elif choice == "8":
        concern_list = []
        concerns_names = []
        with open("skin_concerns.csv", "r", newline="") as f:
            reader = csv.DictReader(f)
            for rows in reader:
                concern_list.append(rows)

            for concern_dict in concern_list:
                concerns_names.append(concern_dict["Concern"])

            for i in range(1, len(concerns_names) + 1):
                print(i, ".", concerns_names[i - 1])

            user_concern_choice = int(input("enter the no. corresponding to your skincare concern: "))
            recommended_active = concern_list[user_concern_choice - 1]["Recommended_Actives"]
            avoid_combining = concern_list[user_concern_choice - 1]["Avoid_Combining"]
            usage_tips = concern_list[user_concern_choice - 1]["Usage_Tip"]

            print("The recommended active for your skin concern is: ", recommended_active,
                  "So look for products with them!")

            print("Avoid combing ", avoid_combining)
            print("Usage tips: ", usage_tips)

        # ----------------------------------------------------------------
        # MODULE 5.9: GENERATE REPORT (TEXT FILE - OUTPUT)
        # Writes a summary of expiry status, AM/PM routine, and low-stock
        # products to a new text file, skincare_report.txt.
        # ----------------------------------------------------------------
    elif choice == "9":
        with open("skincare_report.txt", "w") as f:
            f.write("SKINCARE SHELF-LIFE & ROUTINE TRACKER - REPORT\n")
            f.write("Generated on: " + str(date.today()) + "\n")
            f.write("=" * 50 + "\n\n")

            f.write("EXPIRY STATUS\n")
            f.write("-" * 50 + "\n")
            for p in products:
                expiry_date = p["DateOpened"] + (timedelta(days=30) * p["PAO"])
                days_left = (expiry_date - date.today()).days
                if days_left < 0:
                    status = "EXPIRED"
                elif days_left <= 14:
                    status = "EXPIRING SOON"
                else:
                    status = "OK"
                f.write(p["Name"] + " (" + p["Category"] + ") expires on " + str(expiry_date) +
                        " - " + str(days_left) + " days left - " + status + "\n")

            f.write("\nAM ROUTINE\n")
            f.write("-" * 50 + "\n")
            for p in products:
                if p["RoutineStep"] == "AM" or p["RoutineStep"] == "BOTH":
                    f.write("- " + p["Name"] + " (" + p["Category"] + ")\n")

            f.write("\nPM ROUTINE\n")
            f.write("-" * 50 + "\n")
            for p in products:
                if p["RoutineStep"] == "PM" or p["RoutineStep"] == "BOTH":
                    f.write("- " + p["Name"] + " (" + p["Category"] + ")\n")

            f.write("\nLOW STOCK (25% or less remaining)\n")
            f.write("-" * 50 + "\n")
            for p in products:
                if p["AmountLeft"] <= 25:
                    f.write("- " + p["Name"] + " - " + str(p["AmountLeft"]) + "% left\n")

        print("Report generated and saved to skincare_report.txt")

        # ----------------------------------------------------------------
        # MODULE 5.10: EXPORT CSV (CSV FILE - OUTPUT)
        # Writes the full product list to a CSV file, skincare_products.csv,
        # so it can be opened in Excel or shared as a spreadsheet.
        # ----------------------------------------------------------------
    elif choice == "10":
        with open("skincare_products.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Name", "Category", "Date Opened", "PAO (months)",
                             "Routine Step", "Amount Left"])
            for p in products:
                writer.writerow([p["Name"], p["Category"], str(p["DateOpened"]),
                                 p["PAO"], p["RoutineStep"], p["AmountLeft"]])

        print("Products exported to skincare_products.csv")

        # ----------------------------------------------------------------
        # MODULE 5.11: EXIT (BINARY FILE - OUTPUT)
        # ----------------------------------------------------------------
    elif choice == "11":
        with open("products.dat", "wb") as f:
            pickle.dump(products, f)
        break

    else:
        print("Invalid choice")



