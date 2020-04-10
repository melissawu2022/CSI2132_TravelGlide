import psycopg2
import datetime
from prettytable import PrettyTable

# ASSUMPTION NO USER MAKES ANY MISTAKE PUTTING IN DATA
# ASSUMPTION USERS DONT PUT LOWERCASE AND UPPERCASE LETTERS WRONG
# ASSUMPTION A USER WOULD LIKE TO CONTINUE TO THE END OF EACH FUNCTION BEFORE CHANGING THEIR MIND AND DOING SOMETHING ELSE
# ASSUMPTION IF A USER MAKES A MISTAKES IT HAPPENS ONLY ONCE (TRY EXCEPT BUILT IN FUNCTION DOES NOT SEEM TO WORK FOR MULTIPLE MISTAKES)
# ASSUMPTION A USER CAN READ THE RESULTS BY THE FORMAT PRINTED
# ASSUMPTION

# Username and password for the database
user = input("Database username: ")
password = input("Database password: ")


# Function for signup or signin
def main():
    try:
        condition = True
        while condition:
            option = int(input("Please enter 1 for SignUp, or 2 for SignIn: "))
            if option == 1:
                signUp( )
                condition = False
            elif option == 2:
                option2 = int(input("Are you an employee or a user? enter 1 for employee or 2 for user: "))
                if option2 == 1:  # option 1 is employee, option 2 is user
                    signInE( )
                else:
                    signInU( )
                condition = False
    except:
        print("An error has occured please try again.")
        main( )


#  Function for users signIn
def signInU():
    try:
        condition = True
        while condition:
            firstName = input("Please enter your first name: ")
            email = input("Please enter your email: ")
            # starting connection to the database
            conn = psycopg2.connect(
                "host= web0.eecs.uottawa.ca port=15432 dbname=group_154 user=" + "'" + user + "'" + "password=" + "'" + password + "'")
            cur = conn.cursor( )
            cur.execute(' SELECT email FROM Users WHERE firstName =' + "'" + firstName + "'")
            emailCheck = cur.fetchall( )
            # closing connection
            cur.close( )
            conn.close( )

            emailCheckS = (''.join(map(str, emailCheck[0])))

            if email == emailCheckS:
                condition = False
                optionHorG = int(input("Would you like to continue as a guest or a host? "
                                       "Enter 1 for guest"
                                       " or Enter 2 for host: "))
                if optionHorG == 1:  # option 1 is guest, option 2 is host
                    signInG( )
                else:
                    signInH( )
    except:
        print("An error has occured please try again.")
        signInU( )


def signInG():
    try:
        optionRorB = int(input("Would you like to leave a review"
                               " or book a room?"
                               " Enter 1 for booking a room,"
                               " Enter 2 for leaving a review: "))
        if optionRorB == 1:  # option 1 is booking a room, option 2 is leaving a review
            # starting a connection to the database
            conn = psycopg2.connect(
                "host= web0.eecs.uottawa.ca port=15432 dbname=group_154 user=" + "'" + user + "'" + "password=" + "'" + password + "'")
            cur = conn.cursor( )
            cur.execute(' SELECT * FROM Property')
            allProperty = cur.fetchall( )
            # closing connection
            cur.close( )
            conn.close( )
            headers = ["property id", "host id", "street name", "propertype", "roomtype", "accommodates", "bathroom",
                       "bedroom", "available date", "house number", "city", "max amount of guests", "amenities",
                       "price per hour"]
            table = PrettyTable(headers)
            for row in allProperty:
                table.add_row(list(row))
            print(table)
            emailG = input("Please enter your email to continue: ")
            idProperty = input("Please enter the property-id number you would like to book,"
                               "it is the first digits on the items in the list as the format shows : ")
            # Starting a connection with the database
            conn = psycopg2.connect(
                "host= web0.eecs.uottawa.ca port=15432 dbname=group_154 user=" + "'" + user + "'" + "password=" + "'" + password + "'")
            cur = conn.cursor( )
            cur.execute('SELECT user_id FROM users WHERE email =' + "'" + emailG + "'")
            iduser1 = cur.fetchone( )
            idUserG = str(iduser1[0])
            # closing connection
            cur.close( )
            conn.close( )
            # Starting a connection with the database
            conn = psycopg2.connect(
                "host= web0.eecs.uottawa.ca port=15432 dbname=group_154 user=" + "'" + user + "'" + "password=" + "'" + password + "'")
            cur = conn.cursor( )
            cur.execute('SELECT guest_id FROM guest WHERE user_id=' + "'" + idUserG + "'")
            idGuest1 = cur.fetchone( )
            idGuest = str(idGuest1[0])
            # closing connection
            cur.close( )
            conn.close( )

            # Starting a connection with the database
            conn = psycopg2.connect(
                "host= web0.eecs.uottawa.ca port=15432 dbname=group_154 user=" + "'" + user + "'" + "password=" + "'" + password + "'")
            cur = conn.cursor( )
            cur.execute('SELECT host_id FROM property WHERE property_id=' + "'" + idProperty + "'")
            idHost1 = cur.fetchone( )
            idHost = str(idHost1[0])
            # closing connection
            cur.close( )
            conn.close( )
            signingDate = input("Please enter the signing date in the format of mm/dd/yy: ")

            startDate = input("Please enter the date you want to start the booking in the format of  mm/dd/yy: ")

            endDate = input("Please enter the date you want to end the booking in the format of mm/dd/yy: ")

            # staring a connection to the database
            conn = psycopg2.connect(
                "host= web0.eecs.uottawa.ca port=15432 dbname=group_154 user=" + "'" + user + "'" + "password=" + "'" + password + "'")
            cur = conn.cursor( )
            cur.execute(
                'INSERT INTO RentalAgreement(property_id,guest_id,host_id,signingDate,startDate,endDate) VALUES (' + "'" + idProperty + "'" + ',' + "'" + idGuest + "'" + ',' + "'" + idHost + "'" + ',' + "'" + signingDate + "'" + ',' + "'" + startDate + "'" + ',' + "'" + endDate + "'" + ')')
            conn.commit( )
            # closing connection
            cur.close( )
            conn.close( )

            # starting a connection to the database
            conn = psycopg2.connect(
                "host= web0.eecs.uottawa.ca port=15432 dbname=group_154 user=" + "'" + user + "'" + "password=" + "'" + password + "'")
            cur = conn.cursor( )
            cur.execute(
                'UPDATE property SET availabledate =' + "'" + endDate + "'" + ' Where property_id =' + "'" + idProperty + "'")
            conn.commit( )
            # closing connection
            cur.close( )
            conn.close( )

            # Starting a connection to the database
            conn = psycopg2.connect(
                "host= web0.eecs.uottawa.ca port=15432 dbname=group_154 user=" + "'" + user + "'" + "password=" + "'" + password + "'")
            cur = conn.cursor( )
            cur.execute('SELECT rentalagreement_id FROM rentalagreement WHERE property_id=' + "'" + idProperty + "'"+" AND signingdate="+"'"+signingDate+"'"+" AND startdate="+"'"+startDate+"'"+" AND enddate="+"'"+endDate+"'")
            idRentalAgreement = cur.fetchone( )
            # closing connection
            cur.close( )
            conn.close( )
            idRentalAgreement1 = str(idRentalAgreement[0])
            paymentType = input("Please enter your payment type: enter Debit or Credit: ")
            amount = input("Please enter the amount of your payment: ")
            status = None
            # Starting a connection to the database
            conn = psycopg2.connect(
                "host= web0.eecs.uottawa.ca port=15432 dbname=group_154 user=" + "'" + user + "'" + "password=" + "'" + password + "'")
            cur = conn.cursor( )
            cur.execute(
                'INSERT INTO payment(rentalagreement_id, paymenttype, amount) VALUES(' + "'" + idRentalAgreement1 + "'" + ',' + "'" + paymentType + "'" + "," + "'" + amount + "'"+ ')')
            conn.commit( )
            # Closing the connection
            cur.close( )
            conn.close( )
            print("The booking was successful!")
            conditionToContinure = int(input(
                "Would you like to continue to booking and revewing menue or the main menu? enter 1 for booking and revewing, enter 2 for the main menu, or 3 for exiting: "))
            if conditionToContinure == 1:
                signInG( )
            elif conditionToContinure == 2:
                signInU( )
            else:
                print("Thank you for using this app, stay safe and wash your hands!")
        else:
            # Connection to the database
            emailR = input("Please enter your user email to continue: ")
            conn = psycopg2.connect(
                "host= web0.eecs.uottawa.ca port=15432 dbname=group_154 user=" + "'" + user + "'" + "password=" + "'" + password + "'")
            cur = conn.cursor( )
            cur.execute('SELECT user_id FROM users WHERE email= ' + "'" + emailR + "'")
            idUserR1 = cur.fetchone( )
            idUserR = str(idUserR1[0])
            # closing the connection
            cur.close( )
            conn.close( )

            # connection to the database
            conn = psycopg2.connect(
                "host= web0.eecs.uottawa.ca port=15432 dbname=group_154 user=" + "'" + user + "'" + "password=" + "'" + password + "'")
            cur = conn.cursor( )
            cur.execute('SELECT guest_id FROM guest WHERE user_id= ' + "'" + idUserR + "'")
            idGuestR1 = cur.fetchone( )
            idGuestR = str(idGuestR1[0])
            # closing the connection
            cur.close( )
            conn.close( )

            # connection to the database
            conn = psycopg2.connect(
                "host= web0.eecs.uottawa.ca port=15432 dbname=group_154 user=" + "'" + user + "'" + "password=" + "'" + password + "'")
            cur = conn.cursor( )
            cur.execute('SELECT * FROM rentalagreement WHERE guest_id= ' + "'" + idGuestR + "'")
            rProperty = cur.fetchall( )
            # closing the connection
            cur.close( )
            conn.close( )
            headers = ["rentalagreement id", "property id", "host id", "signing date", "end date"]
            table = PrettyTable(headers)
            for row in rProperty:
                table.add_row(list(row))
            print(table)
            idProperty = input("Please enter the property id you want to do a review on: ")

            rating = input("Please enter the rating from 1-5: ")

            communication = input("Please enter the rating for the communication with the host from 1-5: ")

            cleanliness = input("Please enter the tidiness rating from 1-5: ")
            # starting a connection to the database
            conn = psycopg2.connect(
                "host= web0.eecs.uottawa.ca port=15432 dbname=group_154 user=" + "'" + user + "'" + "password=" + "'" + password + "'")
            cur = conn.cursor( )
            cur.execute(
                'INSERT INTO Review(property_id,rating,guest_id,communication,cleanliness) VALUES (' + "'" + idProperty + "'" + ',' + "'" + rating + "'" + ',' + "'" + idGuestR + "'" + ',' + "'" + communication + "'" + ',' + "'" + cleanliness + "'" + ')')
            conn.commit( )
            # closing connection
            cur.close( )
            conn.close( )
            print("Review has been successfully submitted!")
            conditionToContinure = int(input(
                "Would you like to continue to booking and revewing menue or the main menu? enter 1 for booking and revewing, enter 2 for the main menu, or 3 for exiting: "))
            if conditionToContinure == 1:
                signInG( )
            elif conditionToContinure == 2:
                signInU( )
            else:
                print("Thank you for using this app, stay safe and wash your hands!")
    except:
        print("An error has occured please try again.")
        signInG( )


def signInH():
    try:
        choice = int(input("Would you like to add a property? Type 1 for yes, 2 for no"))
        if choice == 1:  # add property
            streetname = input("What is the street name? ")
            houseNumber = input("Enter house number: ")
            city = input("Enter city: ")
            propertyType = input("Enter property type(apartment, b&b, vacation homes): ")
            price = input("Enter property rate/price for one night: ")
            maxGuest = input("Enter max number of guests: ")
            roomType = input("Enter room type:(private or shared room) ")
            accommodations = input("What accommodations does this property have: ")
            amenities = input("Specify the amenities this property has: ")
            bedroom = input("Give a brief description of the bedroom (100 characters and under): ")
            inputDate = input("Enter the date of availability in format 'mm/dd/yy': ")
            day, month, year = inputDate.split('/')
            isValidDate = True
            try:
                datetime.datetime(int(year), int(month), int(day))
            except ValueError:
                isValidDate = False
            if (isValidDate):
                print("Input date is valid ..")
            else:
                print("Input date is not valid..")
                inputDate = input("Enter the date of availability in format 'mm/dd/yy': ")
            numBathroom = input("How many bathrooms does this property have?")
            flag = False
            while not (flag):
                try:
                    intNum = int(numBathroom)
                    if intNum < 0:
                        numBathroom = input("How many bathrooms does this property have? ")
                        flag = False
                    else:
                        flag = True
                except:
                    flag = False
            emailH = input("Please confirm your email to make this listing: ")

            # starting a connection with the database
            conn = psycopg2.connect(
                "host= web0.eecs.uottawa.ca port=15432 dbname=group_154 user=" + "'" + user + "'" + "password=" + "'" + password + "'")
            cur = conn.cursor( )
            cur.execute('SELECT user_id FROM users WHERE email=' + "'" + emailH + "'")
            iduserH = cur.fetchone( )
            # Might need to change this to just iduserH[0] instead of int(''.join(map(str,idhost[0])))
            iduserH1 = str(iduserH[0])
            # closing connection
            cur.close( )
            conn.close( )

            # starting a connection with the database to get the host id from the user id
            conn = psycopg2.connect(
                "host= web0.eecs.uottawa.ca port=15432 dbname=group_154 user=" + "'" + user + "'" + "password=" + "'" + password + "'")
            cur = conn.cursor( )
            cur.execute('SELECT host_id FROM host WHERE user_id=' + iduserH1)
            idhost = cur.fetchone( )
            # Might need to change this to just idhost[0] instead of int(''.join(map(str,idhost[0])))
            idhost1 = str(idhost[0])
            print(idhost1)
            print(iduserH1)

            cur.execute(
                "INSERT INTO property(host_id,streetname,propertytype,roomtype,accommodates,bathroom,bedroom,"
                "availabledate,housenumber,city,maxguest,amenities,price) VALUES(" + "'" + idhost1 + "'" + ',' + "'" + streetname + "'" + ',' + "'" + propertyType + "'" + ',' + "'" + roomType + "'" + ',' + "'" + accommodations + "'" + ',' + "'" + numBathroom + "'" + ',' + "'" + bedroom + "'" + ',' + "'" + inputDate + "'" + ',' + "'" + houseNumber + "'" + ',' + "'" + city + "'" + ',' + "'" + maxGuest + "'" + ',' + "'" + amenities + "'" + "," + "'" + price + "')")
            conn.commit( )
            # closing connection
            cur.close( )
            conn.close( )
            print("The property has been added!")
            conditionToContinure = int(input(
                "Would you like to continue to add another property or the main menu? enter 1 for adding another property, enter 2 for the main menu, or 3 for exiting: "))
            if conditionToContinure == 1:
                signInH( )
            elif conditionToContinure == 2:
                signInU( )
            else:
                print("Thank you for using this app, stay safe and wash your hands!")
        else:
            pass
    except:
        print("An error has occured please start again.")
        signInH( )


def signUp():
    try:
        # starting a connection to the database
        conn = psycopg2.connect(
            "host= web0.eecs.uottawa.ca port=15432 dbname=group_154 user=" + "'" + user + "'" + "password=" + "'" + password + "'")
        cur = conn.cursor( )

        firstNameInput = input("Please enter your first name : ")
        lastNameInput = input("Please enter your last name :  ")
        emailInput = input("Please enter your email :  ")
        phoneNumInput = input("Please enter your Phone Number :  ")
        houseNumInput = int(input("Please enter your House Number :  "))
        streetNameInput = input("Please enter your street :  ")
        cityInput = input("Please enter your city :  ")
        provinceOrStateInput = input("Please enter your Province/State:  ")
        addressInput = str(houseNumInput) + " " + streetNameInput + ", " + cityInput
        countryInput = input("Please enter your Country :  ")
        # make assumption that they did not mess up the above
        # TODO make it more robust make sure they enter a proper number

        # create a user account
        cur.execute(
            'INSERT INTO Users(firstName,lastName,email,phoneNumber,address,provinceOrState,country) VALUES ( ' + "'" + firstNameInput + "'" + ',' + "'" + lastNameInput + "'" + ',' + "'" + emailInput + "'" + ',' + "'" + phoneNumInput + "'" + ',' + "'" + addressInput + "'" + ',' + "'" + provinceOrStateInput + "'" + ',' + "'" + countryInput + "'" + ' )')
        conn.commit( )
        # closing connection
        cur.close( )
        conn.close( )
        # assume user_id is auto incremented

        # starting a connection to the database
        conn = psycopg2.connect(
            "host= web0.eecs.uottawa.ca port=15432 dbname=group_154 user=" + "'" + user + "'" + "password=" + "'" + password + "'")
        cur = conn.cursor( )

        # this is only selecting from user
        cur.execute(
            'SELECT user_id FROM users WHERE firstName=' + "'" + firstNameInput + "'" + "AND lastName = " + "'" + lastNameInput + "'")
        userIdentification = cur.fetchone( )
        userIdentification1 = str(userIdentification[0])
        # closing connection
        cur.close( )
        conn.close( )

        # create a host account
        # starting a connection to the database
        conn = psycopg2.connect(
            "host= web0.eecs.uottawa.ca port=15432 dbname=group_154 user=" + "'" + user + "'" + "password=" + "'" + password + "'")
        cur = conn.cursor( )
        cur.execute('INSERT INTO Host(user_id) VALUES ( ' + userIdentification1 + ")")
        conn.commit( )
        # closing connection
        cur.close( )
        conn.close( )

        # starting a connection to the database
        conn = psycopg2.connect(
            "host= web0.eecs.uottawa.ca port=15432 dbname=group_154 user=" + "'" + user + "'" + "password=" + "'" + password + "'")
        cur = conn.cursor( )
        cur.execute('INSERT INTO Guest(user_id,branch_id) VALUES ( ' + userIdentification1 + ",4)")
        conn.commit( )
        # closing connection
        cur.close( )
        conn.close( )

        # for now bring them to sign in page
        print("now that you have signed up, sign in!")
        signInU( )
    except:
        print("An error has occured please try again")
        signUp( )


def signInE():
    try:
        # starting a connection to the database
        conn = psycopg2.connect(
            "host= web0.eecs.uottawa.ca port=15432 dbname=group_154 user=" + "'" + user + "'" + "password=" + "'" + password + "'")
        cur = conn.cursor( )

        position = input("Enter position (employee or manager): ")

        empID = input("Please enter your employee ID: ")
        cur.execute("SELECT position FROM employee WHERE employee_id = " + "'" + empID + "'")
        positionE1 = cur.fetchone( )
        cur.close( )
        conn.close( )
        positionE = str(positionE1[0])
        if positionE == position:
            conn = psycopg2.connect(
                "host= web0.eecs.uottawa.ca port=15432 dbname=group_154 user=" + "'" + user + "'" + "password=" + "'" + password + "'")
            cur = conn.cursor( )
            choice = input("Enter 1 to view occupied properties and 2 to view properties that are still available :")
            if int(choice) == 1:
                query = "SELECT * FROM rentalagreement"
                cur.execute(query)
                headers = ["rentalagreement", "property_id", "guest_id", "host_id", "signingdate", "startdate",
                           "enddate"]
            else:
                query = "SELECT * FROM property"
                cur.execute(query)
                headers = ["property_id", "host_id", "Street name", "Property type", "Room type", "Accommodations",
                           "Number of bathrooms", "Number of bedrooms", "Available date", "House Number", "City",
                           "Max Number of Guests", "Amenities", "Price"]
            table = PrettyTable(headers)
            data = cur.fetchall( )
            for row in data:
                table.add_row(list(row))
            print(table)
            # closing connection
            cur.close( )
            conn.close( )
        else:
            signInE( )
    except:
        print("An error has occured please start again.")
        signInE( )


# Do not touch this
if __name__ == "__main__":
    main( )
