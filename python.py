#######################################################
#
# Function for executing an SQL command
#
#######################################################

def executeSQLCommand (sql_command):

   ##########################
   # Connect to the MySQL DB
   ##########################

   password = "Abc123456!" # this is your MySQL database password, NOT the password you use when you log into PythonAnywhere! I told you to write it down somewhere... >:->
   results = ()

   # you'll find the info you need to enter in your Databases Tab on PythonAnywhere
   db = MySQLdb.connect("JakobK2022.mysql.eu.pythonanywhere-services.com","JakobK2022",password, "JakobK2022$MarsDB")

   cursor = db.cursor()

   try:
       cursor.execute(sql_command)  # Execute the SQL command
       results = cursor.fetchall()  # Fetch all the rows in a list of lists.
       db.commit() # only necessary if the command changes the DB, but hey...
   except:
       db.rollback() # if stuff went wrong, no change to the DB should be made
       print ("+++++++++ Error: unable to fetch data from database")
   db.close()
   return results


def application(environ, start_response):
   if environ.get('PATH_INFO') == '/':
       status = '200 OK'


       LANDING_PAGE = LANDING_PAGE_START + LANDING_PAGE_END
       content = LANDING_PAGE

   elif environ.get('PATH_INFO') == '/Newsroom':
       status = '200 OK'


       content = NEWS_PAGE

   elif environ.get('PATH_INFO') == '/Register':
       status = '200 OK'

       sql_cmd = "SELECT Fname, Lname, PhoneNumber, UserPassword, Email, Ethnicity, Plot  FROM UserInfo"
       User_Info_from_db = executeSQLCommand (sql_cmd)

       USERINFO_DATA_HTML = ""

       for userinfo_record in User_Info_from_db:


           Lname = userinfo_record[0]
           Fname = userinfo_record[1]
           PhoneNumber = userinfo_record[2]
           UserPassword = userinfo_record[3]
           Email = userinfo_record[4]
           Ethnicity = userinfo_record[5]
           Plot = userinfo_record[6]

           USERINFO_DATA_HTML += "<tr> <td>" + Fname + "</td> <td>" + Lname + "</td> <td>" + PhoneNumber + "</td> <td>" + UserPassword + "</td> <td>" + Email + "</td> <td>" + Ethnicity + "</td> <td>" + str(Plot) + "</td> <td>" + REGISTER_PAGE_DELETE



       REGISTER_PAGE_HTML = REGISTER_PAGE_START + USERINFO_DATA_HTML + REGISTER_PAGE_END

       content = REGISTER_PAGE_HTML


   elif environ.get('PATH_INFO') == '/Registernow':
       status = '200 OK'

     # get the user input from the HTTP query string for LastName=



       HttpQuery = parse_qs(environ['QUERY_STRING'])

       userinput_LastName = HttpQuery.get('fname', ['DummyLastName'])[0]



       # get the user input from the HTTP query string for FirstName=

       userinput_FirstName = HttpQuery.get('lname', ['DummyFirstName'])[0]



       # get the user input from the HTTP query string for Email=

       userinput_Email = HttpQuery.get('phone', ['dummy@student.university-reutlingen.de'])[0]



       # get the user input from the HTTP query string for Country=

       userinput_Country = HttpQuery.get('email', ['NoCountry'])[0]



       # get the user input from the HTTP query string for University=

       userinput_University = HttpQuery.get('password', ['NoUniversity'])[0]

       #get the user input from the HTTP query string for Experience=



       userinput_Experience = HttpQuery.get('ethnicity', ['NoExperience'])[0]



       # get the user input from the HTTP query string for Password=

       userinput_Password = HttpQuery.get('plot', ['%'])[0]


       #construct the SQL command (this time it's an INSERT statement)



       sql_cmd = "INSERT INTO UserInfo (Fname, Lname, PhoneNumber, UserPassword, Email, Ethnicity, Plot) VALUES ('"

       sql_cmd += userinput_LastName

       sql_cmd += "', '"

       sql_cmd += userinput_FirstName

       sql_cmd += "','"

       sql_cmd += userinput_Email

       sql_cmd += "','"

       sql_cmd += userinput_Country

       sql_cmd += "','"

       sql_cmd += userinput_University

       sql_cmd += "','"

       sql_cmd += userinput_Experience

       sql_cmd += "','"

       sql_cmd += userinput_Password

       sql_cmd += "')"

       print ("+++++++++++SQL command++++++++++++", sql_cmd)

       executeSQLCommand (sql_cmd)



       content = LANDING_PAGE_START

   elif environ.get('PATH_INFO') == '/Buy':
       status = '200 OK'

       sql_cmd = "SELECT Location, Lname, Fname, RentP, BuyP  FROM RealEstate"
       Real_Estate_from_db = executeSQLCommand (sql_cmd)

       REALESTATE_DATA_HTML = ""

       # STEP 2: For each employee record in the DB
       i = 1
       c = 1
       for realestate_record in Real_Estate_from_db:

           # a record is a LIST of values (one value per column), so we need to access each value separately.
           # This follows the sequence in the SELECT statement above, starting with 0!
           if (i%2) != 0:
               location = realestate_record[0] # employee_record[0] includes the FirstName value
               Lname = realestate_record[1] # employee_record[1] includes the LastName value
               Fname = realestate_record[2]
               RentP = realestate_record[3]
               BuyP = realestate_record[4]

               pNbr = " plot #" + str(c)

               # Print fetched employee_record, just so we see it
               print (location, Lname, Fname, RentP, BuyP )

               REALESTATE_DATA_HTML += PLOT_LIST_I + str(pNbr) + PLOT_LIST_II + str(location) + PLOT_LIST_III + str(Fname) + " "+ str(Lname) + PLOT_LIST_IV + str(BuyP) + PLOT_LIST_V + str(RentP) + PLOT_LIST_VI

               i += 1
               c += 1
           else:

               location = realestate_record[0] # employee_record[0] includes the FirstName value
               Lname = realestate_record[1] # employee_record[1] includes the LastName value
               Fname = realestate_record[2]
               RentP = realestate_record[3]
               BuyP = realestate_record[4]

               pNbr = " plot #" + str(c)

               #Print fetched employee_record, just so we see it
               print (location, Lname, Fname, RentP, BuyP )

               REALESTATE_DATA_HTML += PLOT_LIST_VII + str(pNbr) + PLOT_LIST_VIII + str(location) + PLOT_LIST_IX + str(Fname) + " "+ str(Lname) + PLOT_LIST_X + str(BuyP) + PLOT_LIST_XI + str(RentP) + PLOT_LIST_XII
               i += 1
               c += 1


           BUY_PAGE = PLOT_LISTING_START + REALESTATE_DATA_HTML + PLOT_LISTING_END
           content = BUY_PAGE

   elif environ.get('PATH_INFO') == '/deleteinput':

       status = '200 OK'

       print ("######### Your Experience page - DELETE ##########")



       # get the user input from the HTTP query string for LastName=



       # get the user input from the HTTP query string for Email=

       HttpQuery = parse_qs(environ['QUERY_STRING'])

       userinput_Email = HttpQuery.get('Email', ['$'])[0]

       userinput_Password = HttpQuery.get('Password', ['$'])[0]



       # construct the SQL command (this time it's an INSERT statement)



       sql_cmd = "DELETE FROM UserInfo WHERE Email = '" + userinput_Email + "' AND UserPassword = '" + userinput_Password + "'"



       ###################################

       #

       #print insert statement in the Log

       #

       ###################################



       print ("+++++++++++SQL command++++++++++++", sql_cmd)



       #########################

       #

       #execute the SQL command

       #

       #########################

       #if userinput_LastName != 'DummyLastName' and userinput_FirstName != 'DummyFirstName' and userinput_Email != 'dummy@student.university-reutlingen.de' and userinput_Country != 'NoCountry' and userinput_University != 'NoUniversity' and userinput_Experience != 'NoExperience' and userinput_Password != '%':



       executeSQLCommand (sql_cmd)



       ##############

       #

       #show content

       #

       ##############



       sql_cmd = "SELECT Fname, Lname, PhoneNumber, UserPassword, Email, Ethnicity, Plot  FROM UserInfo"
       User_Info_from_db = executeSQLCommand (sql_cmd)

       USERINFO_DATA_HTML = ""

       for userinfo_record in User_Info_from_db:


           Lname = userinfo_record[0]
           Fname = userinfo_record[1]
           PhoneNumber = userinfo_record[2]
           UserPassword = userinfo_record[3]
           Email = userinfo_record[4]
           Ethnicity = userinfo_record[5]
           Plot = userinfo_record[6]

           USERINFO_DATA_HTML += "<tr> <td>" + Fname + "</td> <td>" + Lname + "</td> <td>" + PhoneNumber + "</td> <td>" + UserPassword + "</td> <td>" + Email + "</td> <td>" + Ethnicity + "</td> <td>" + str(Plot) + "</td> <td>" + REGISTER_PAGE_DELETE



       REGISTER_PAGE_HTML = REGISTER_PAGE_START + "Delete Successful" + USERINFO_DATA_HTML + REGISTER_PAGE_END

       content = REGISTER_PAGE_HTML


   elif environ.get('PATH_INFO') == '/Search':
       status = '200 OK'


       HttpQuery = parse_qs(environ['QUERY_STRING'])

       userinput = HttpQuery.get('search', ['%'])[0]

       sql_cmd = "SELECT UserInfo.Lname, UserInfo.Fname, UserInfo.PhoneNumber, UserInfo.UserPassword, UserInfo.Email, UserInfo.Ethnicity, UserInfo.Plot FROM UserInfo WHERE UserInfo.Lname like '" + userinput + "'"

       print ("####### SQL command ####### ", sql_cmd)

       User_Info_from_db = executeSQLCommand(sql_cmd)

       USERINFO_DATA_HTML = ""



       for userinfo_record in User_Info_from_db:


           Lname = userinfo_record[0]
           Fname = userinfo_record[1]
           PhoneNumber = userinfo_record[2]
           UserPassword = userinfo_record[3]
           Email = userinfo_record[4]
           Ethnicity = userinfo_record[5]
           Plot = userinfo_record[6]

           USERINFO_DATA_HTML += "<tr> <td>" + Lname + "</td> <td>" + Fname + "</td> <td>" + PhoneNumber + "</td> <td>" + UserPassword + "</td> <td>" + Email + "</td> <td>" + Ethnicity + "</td> <td>" + str(Plot) + "</td> <td>"

       print ("######## HTML string #######",USERINFO_DATA_HTML)

       REGISTER_PAGE_HTML = REGISTER_PAGE_START + USERINFO_DATA_HTML + REGISTER_PAGE_END

       content = REGISTER_PAGE_HTML

   elif environ.get('PATH_INFO') == '/':
       status = '200 OK'


       LANDING_PAGE = LANDING_PAGE_START + LANDING_PAGE_END
       content = LANDING_PAGE

   else:
       status = '404 NOT FOUND'
       content = '<h1>Page not found. Idiot! </h1>'

   ########### Don't touch this, just leave it as is ################
   response_headers = [('Content-Type', 'text/html'), ('Content-Length', str(len(content)))]
   start_response(status, response_headers)
   yield content.encode('utf8')