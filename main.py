from datetime import date,timedelta
import pickle
import csv

try:
    with open("products.dat", "rb") as f:
        products = pickle.load(f)

except FileNotFoundError:
    products = []



menu_options = ["Add Product", "View All", "Update", "Delete", "Check Expiry", "Today's Routine", "Restock Estimator",
           "Recommendations", "Generate Report", "Export CSV", "Exit"]
categories=["Cleanser","Toner/Essence","Serum","Moisturizer","Sunscreen","Exfoliant","Mask","Oil","Others"]
sorted_products = []

for cat in categories:
    for p in products:
        if p["Category"] == cat:
            sorted_products.append(p)

products = sorted_products



Beginner_or_not=input("Are you new to skincare? ").upper()
if Beginner_or_not =="YES":
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

        print("The recommended active for your skin concern is: ", recommended_active)
        print("Avoid combing", avoid_combining)
        print("Usage tips:", usage_tips)





#MENU PANEL
while True:

    for i in range(1,12):
        print(i,".",menu_options[i-1])


    choice=input("Enter your choice: ")
















#ADDING A PRODUCT
    if choice == "1":
        product_name=input("Enter the product name: ")




        for i in range(1,len(categories)+1):
            print(i,".",categories[i-1])
        category_choice=int(input("Enter the No. corresponding to the Category of the product: "))
        category=categories[category_choice-1]



        year = int(input("enter the year of opening: "))
        month = int(input("enter the month of opening: "))
        day = int(input("enter the day of opening: "))
        date_opened = date(year, month, day)
        period_after_opening = int(input("Enter the PAO in months — check the small jar icon on the packaging, e.g. 6M, 12M:"))


        print("Used in AM, PM, or Both? ")
        routine_times=["AM","PM","BOTH"]
        for i in range(1,len(routine_times)+1):
            print(i,".",routine_times[i-1])
        routine_choice = int(input("Enter the No. corresponding to your choice: "))
        routine_step=routine_times[routine_choice-1]


        product={"Name":product_name,"Category":category,"DateOpened" : date_opened,"PAO": period_after_opening,"RoutineStep":routine_step,"AmountLeft":100}
        products.append(product)













#DISPLAYING THE PRODUCTS SAVED
    elif choice == "2":
        for i in products:
            print(i)











#UPDATING THE INFORMATION SAVED
    elif choice == "3":

        for i in range(1,len(products)+1):
            print(i, ". ", products[i - 1]["Name"])


        update_choice=int(input("Enter the No. corresponding to the product you wish to update: "))
        for i in range(1,len(products)+1):
            if i==update_choice:
                print(products[i-1])

        # what the user wants to update?
        update_fields = ["Product Name", "Product Category", "Date Of Opening ", "PAO(Period After Opening", "Routine Step","Exit"]
        for i in range(1,len(update_fields)+1):
            print(i,".",update_fields[i-1])

        ask = int(input("What would you like to edit/update? "))


        if ask==1:
            print("Press 'Enter' to skip ")
            updated_name = input("Enter the product name: ")
            if updated_name == (""
                                ""):
                pass
            else:
                products[update_choice - 1]["Name"] = updated_name


        elif ask==2:
            for i in range(1, len(categories) + 1):
                print(i, ".", categories[i - 1])
            print("Press 'Enter' to skip ")
            updated_category_choice = int(input("Enter the no. corresponding to the Category of the product: "))
            updated_category = categories[updated_category_choice - 1]

            if updated_category_choice == (""
                                           ""):
                pass
            else:
                products[update_choice - 1]["Category"] = updated_category


        # elif ask == 3:
        #     options_2=["Year of Opening","Month of Opening","Day of Opening"]
        #     for i in range(1,len(options_2)+1):
        #         print(1,".",options_2[i-1])
        #
        #     ask_2 = int(input("What would you like to change?"))
        #
        #
        #     if ask_2==1:
        #          updated_year=int(input("Enter the updated Year: "))
        #
        #
        #       products[update_choice]["DateOpened"]=


        elif ask == 4:

            updated_PAO=int(input("Enter the PAO in months — check the small jar icon on the packaging, e.g. 6M, 12M:"))
            products[update_choice-1]["PAO"]=updated_PAO


        elif ask==5:
            routine_times = ["AM", "PM", "BOTH"]
            for i in range(1, len(routine_times) + 1):
                print(i, ".", routine_times[i - 1])

            updated_routine_step = int(input("Enter the No. corresponding to the routine Step"))

            products[update_choice-1]["RoutineStep"]=routine_times[updated_routine_step-1]

        else:
            pass














#DELETING A Product
    elif choice == "4":
        for i in range(1,len(products)+1):
            print(i,". ",products[i-1]["Name"])

        delete_choice=int(input("Enter the No. corresponding to the product you wish to delete: "))
        products.pop(delete_choice-1)
        print("Successfully Deleted")











#PERIOD OF TIME LEFT BEFORE EXPIRY
    elif choice == "5":

        for i in range(1, len(products) + 1):
            print(i, ". ", products[i - 1]["Name"])

        expirydate_choice = int(input("Enter the corresponding no. of the product to check for: "))
        expiry_date=products[expirydate_choice-1]["DateOpened"]+(timedelta(days=30)*products[expirydate_choice-1]["PAO"])
        print("This product will expire on",expiry_date)
        todays_date=date.today()
        no_of_days=expiry_date-todays_date
        print("in",no_of_days.days,"days")











#PERSONAL ROUTINE
    elif choice == "6":
        print("Today's Routine")

        today_routine_choice=input("AM or PM?").upper()

        for i in (products):
            if today_routine_choice== i["RoutineStep"] or i["RoutineStep"]=="BOTH":
                print(i["Category"],":",i["Name"])


















    elif choice == "7":
        amounts=[100,75,50,25,0]
        for i in range(1,len(products)+1):
            print(i,".",products[i-1]["Name"])

        amount_check_choice=int(input("Enter the no. corresponding to the product to be checked: "))
        print(products[amount_check_choice-1]["AmountLeft"])
        if products[amount_check_choice-1]["AmountLeft"]==50:
            print("Halfway Done")
        elif products[amount_check_choice-1]["AmountLeft"]<=25:
            print("Running low — consider restocking soon!")


        amount_update_choice=input("Do you want to update the amount left?").upper()
        if amount_update_choice=="YES":
            for i in range(1,len(amounts)+1):
                print(i,".",amounts[i-1])

            updated_amount = int(input("Enter the no. corresponding to the amount: "))

            products[amount_check_choice-1]["AmountLeft"]=amounts[updated_amount-1]
            print("Updated Successfully")

        else:
            pass













    elif choice == "8" :
        concern_list = []
        concerns_names = []
        with open("skin_concerns.csv","r",newline="") as f:
            reader=csv.DictReader(f)
            for rows in reader:
                concern_list.append(rows)

            for concern_dict in concern_list:
                concerns_names.append(concern_dict["Concern"])

            for i in range(1,len(concerns_names)+1):
                print(i,".",concerns_names[i-1])

            user_concern_choice=int(input("enter the no. corresponding to your skincare concern: "))
            recommended_active=concern_list[user_concern_choice-1]["Recommended_Actives"]
            avoid_combining=concern_list[user_concern_choice-1]["Avoid_Combining"]
            usage_tips=concern_list[user_concern_choice-1]["Usage_Tip"]


            print("The recommended active for your skin concern is: ", recommended_active, "So look for products with them!")
            print("Avoid combing ",avoid_combining)
            print("Usage tips: ",usage_tips)











    elif choice == "9":
        print("Generate Report")

    elif choice == "10":
        print("Export CSV")

    elif choice == "11":
        with open("products.dat", "wb") as f:
            pickle.dump(products, f)
        break
    else:
        print("Invalid choice")





