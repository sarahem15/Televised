#!/usr/bin/ruby
# M'Kiyah Baird and Sarah McLoney
# Databases, Winter 2025
# titanicUpload.cgi

### ADMIN LOGIN ###
# 	Username: smcloney
# 	Password: csJintonG#1

# Titanic Upload
# Takes in a .csv file containing information about the Titanic's passengers with a "|" delimiter and 14 columns.
# 	The data is then inserted into a user-specified table. More than one table can be chosen.
# 	If the the following attributes do not have found data, then a -1 is inserted:
# 		survive, class, gender, age, siblingSpouse, parentKid, ticketNumber, and fare
# 	If the following attributes do not have found data, then "N/A" is inserted:
# 		honorific, fName, lName, cabin, and embarkedFrom
# 	As an encrypted file, the Admin, who is assumed to know MySQL, will be told to try again if:
# 		they did not select a table name from the corresponding titanicUpload.html file,
# 		the primary 'passenger' table is empty, as the other tables, 'lodging' and 'unmarriedName,' both reference 'passenger,'
# 		the uploaded file is empty,
# 		the uploaded file does not contain the right amount of columns,
# 		or an unexpected and unknown error has occurred.
# 	If the upload and populate is successful, the Admin then sees all three tables and their data displayed.
# 		If an error did occur, it is printed to the screen.

# Reference:
# 	Used to calculate the number of entries in an existing table -- https://stackoverflow.com/questions/1893424/count-table-rows

$stdout.sync = true
$stderr.reopen $stdout

puts "Content-type: text/html\n\n"
require 'mysql2'
require 'cgi'
require 'stringio'

db = Mysql2::Client.new(:host=>'10.20.3.4', :username=>'seniorproject25', :password=>'TV_Group123!', :database=>'televised_w25')
cgi = CGI.new
tableName = cgi.params['tableName']
uploadLocation = "/NFSHome/Televised/public_html/DBTitanic/Admin/Uploads/"
fromfile = cgi.params['fileName'].first
originalName = cgi.params['fileName'].first.instance_variable_get("@original_filename")

passengerEmpty = false
emptyFile = false
incorrectColumnCount = false
passengerCount = db.query("SELECT COUNT(*) FROM passenger;")
if passengerCount.first['COUNT(*)'] == 0
	passengerEmpty = true
end

if passengerCount.first['COUNT(*)'] == 0
	passengerNum = 1
else
	passengerNum = passengerCount.first['COUNT(*)']
end

toFile = uploadLocation + originalName 
File.open(toFile.untaint, 'w') { |file| file << fromfile.read}
titanicFile = IO.readlines(toFile)
if (titanicFile.size == 0)
	emptyFile = true
else
	numOfColumns = titanicFile[0].split("|")
	if numOfColumns.size != 14
		incorrectColumnCount = true
	end
end

if (tableName.size != 0) && (!passengerEmpty || tableName[0] == "passenger") && (!emptyFile) && (!incorrectColumnCount)
	titanicFile.drop(1).each do |fileRead|
		currentLine = fileRead.split("|")
		if currentLine[0].strip == "False"
			survive = 0
		elsif currentLine[0].strip == "True"
			survive = 1
		else
			survive = -1
		end
	
		if currentLine[1] == ""
			passClass = -1
		else
			passClass = currentLine[1]
		end

		if currentLine[2] == ""
			honorific = "N/A"
		else
			honorific = currentLine[2]
		end

		if currentLine[3] == ""
			firstName = "N/A"
		else
			firstName = currentLine[3]
		end

		if currentLine[4] == ""
			lastName = "N/A"
		else
			lastName = currentLine[4]
		end

		unmarriedName = currentLine[5].split(" ")
		if currentLine[6].strip == "male"
			gender = 0
		elsif currentLine[6].strip == "female"
			gender = 1
		else
			gender = -1
		end
	
		if currentLine[7] == ""
			age = -1
		else
			age = currentLine[7]
		end

		if currentLine[8] == ""
			siblingsSpouse = -1
		else
			siblingsSpouse = currentLine[8]
		end

		if currentLine[9] == ""
			parentsKids = -1
		else
			parentsKids = currentLine[9]
		end

		if currentLine[10] == ""
			ticketNumber = -1
		else
			ticketNumber = currentLine[10]
		end
	
		if currentLine[11] == ""
			fare = -1
		else
			fare = currentLine[11]
		end

		if currentLine[12] == ""
			cabins = "N/A"
		else
			cabins = currentLine[12].split(" ")
		end
	
		if currentLine[13] == ""
			embarkedFrom = "N/A"
		else
			embarkedFrom = currentLine[13]
		end

		(0...tableName.size).each do |i|
			if tableName[i] == "passenger"
				begin
					db.query("INSERT INTO passenger Values(NULL, '" + survive.to_s.strip + "','" + firstName.gsub("'", "\\\\'").strip + "','" + 
						lastName.gsub("'", "\\\\'").strip + "','" + gender.to_s.strip + "','" + age.to_s.strip + "','" + siblingsSpouse.to_s.strip + "','" + parentsKids.to_s.strip + 
						"', '" + embarkedFrom.strip + "', '" + honorific.strip + "', '" + fare.to_s + "');")
				rescue => e
					puts "With id " + passengerNum.to_s + " in table 'passenger': " + e.message + "<br>"
				end

			elsif tableName[i] == "unmarriedName"
				(0...unmarriedName.size).each do |i|
					begin
						db.query("INSERT INTO unmarriedName Values(NULL,'" + unmarriedName[i].gsub("'", "\\\\'").strip + "','" + passengerNum.to_s.strip + "');")
					rescue => e
						puts "With id " + passengerNum.to_s + " in table 'unmarriedName': " + e.message + "<br>"
					end
				end

			elsif tableName[i] == "lodging"
				if cabins == "N/A"
					begin
						db.query("INSERT INTO lodging Values(NULL, '" + ticketNumber.to_s + "','" + cabins + "','" + 
							passClass.to_s + "','" + passengerNum.to_s + "');")
					rescue => e
						puts "With id " + passengerNum.to_s + " in table 'lodging': " + e.message + "<br>"
					end
				else
					(0...cabins.size).each do |i|
						begin
							db.query("INSERT INTO lodging Values(NULL, '" + ticketNumber.to_s + "','" + cabins[i] + "','" + 
								passClass.to_s + "','" + passengerNum.to_s + "');")
						rescue => e
							puts "With id " + passengerNum.to_s + " in table 'lodging': " + e.message + "<br>"
						end
					end
				end
			end
		end
		passengerNum = passengerNum + 1
	end

	puts "<html>"
	puts "<head>"
	puts "<link rel=\"stylesheet\" href=\"/Televised/DBTitanic/User/titanic.css\">"
	puts "<title>Mass Insert</title></head>"
	puts "<body id='modAndDelete'>"
	puts "<H1 style=\"text-align: center;\"> Success! </H1>\n"
	puts '<section class="currentState">'
		puts '<section class="adminInfo">'
		puts '<table class="passInfo">'
		puts '<h3 style="color: white; text-align: center;"> Passenger </h3>'
	    puts '<tr>'
	    	puts '<th>ID</th>'
	    	puts '<th>Survive</th>'
	        puts '<th>First Name</th>'
	        puts '<th>Last Name</th>'
	        puts '<th>Gender</th>'
	        puts '<th>Age</th>'
	        puts '<th>Sibling/Spouse</th>'
	        puts '<th>Parent/Kid</th>'
	        puts '<th>Embarked From</th>'
	        puts '<th>Honorific</th>'
	        puts '<th>Fare</th>'
	    puts '</tr>'
	    passenger = db.query("SELECT * FROM passenger;").to_a
	    (0...passenger.size).each do |i|
	    	puts '<tr>'
	    	puts '<td>' + passenger[i]['id'].to_s + '</td>'
	    	puts '<td>' + passenger[i]['survive'].to_s + '</td>'
	    	puts '<td>' + passenger[i]['fName'].to_s + '</td>'
	    	puts '<td>' + passenger[i]['lName'].to_s + '</td>'
	    	puts '<td>' + passenger[i]['gender'].to_s + '</td>'
	    	puts '<td>' + passenger[i]['age'].to_s + '</td>'
	    	puts '<td>' + passenger[i]['siblingSpouse'].to_s + '</td>'
	    	puts '<td>' + passenger[i]['parentKid'].to_s + '</td>'
	    	puts '<td>' + passenger[i]['embarkedFrom'].to_s + '</td>'
	    	puts '<td>' + passenger[i]['honorific'].to_s + '</td>'
	    	puts '<td>' + passenger[i]['fare'].to_s + '</td>'
	    	puts '</tr>'
	    end

	    puts '</table>'
	    puts '</section>'
	    puts '<section class="adminInfo">'
		puts '<table class="passInfo">'
		puts '<h3 style="color: white; text-align: center;"> Lodging </h3>'
	    puts '<tr>'
	    	puts '<th>ID</th>'
	    	puts '<th>Ticket Number</th>'
	        puts '<th>Cabin</th>'
	        puts '<th>Class</th>'
	        puts '<th>Passenger</th>'
	    puts '</tr>'
	    lodging = db.query("SELECT * FROM lodging;").to_a
	    (0...lodging.size).each do |i|
	    	puts '<tr>'
	    	puts '<td>' + lodging[i]['id'].to_s + '</td>'
	    	puts '<td>' + lodging[i]['ticketNumber'].to_s + '</td>'
	    	puts '<td>' + lodging[i]['cabin'].to_s + '</td>'
	    	puts '<td>' + lodging[i]['class'].to_s + '</td>'
	    	puts '<td>' + lodging[i]['passenger'].to_s + '</td>'
	    	puts '</tr>'
	    end

	    puts '</table>'
	    puts '</section>'
	    puts '<section class="adminInfo">'
		puts '<table class="passInfo">'
		puts '<h3 style="color: white; text-align: center;"> Unmarried Name </h3>'
	    puts '<tr>'
	    	puts '<th>ID</th>'
	    	puts '<th>Name</th>'
	        puts '<th>Passenger</th>'
	    puts '</tr>'
	    unmarriedName = db.query("SELECT * FROM unmarriedName;").to_a
	    (0...unmarriedName.size).each do |i|
	    	puts '<tr>'
	    	puts '<td>' + unmarriedName[i]['id'].to_s + '</td>'
	    	puts '<td>' + unmarriedName[i]['name'].to_s + '</td>'
	    	puts '<td>' + unmarriedName[i]['passenger'].to_s + '</td>'
	    	puts '</tr>'
	    end

	    puts '</table>'
	    puts '</section>'
	    puts '</section>'
	puts "</body>"
	puts "</html>"
elsif tableName.size == 0
	puts "<html>"
	puts "<head>"
	puts "<meta http-equiv='refresh' content='45; url=titanicUpload.html'>"
	puts "<title>Mass Insert</title></head>"
	puts "<H1 style=\"text-align: center;\"> ERROR: You did not select a table name. Please try again! </H1>\n"
	puts "</body>"
	puts "</html>"
elsif passengerEmpty
	puts "<html>"
	puts "<head>"
	puts "<meta http-equiv='refresh' content='45; url=titanicUpload.html'>"
	puts "<title>Mass Insert</title></head>"
	puts "<H1 style=\"text-align: center;\"> ERROR: You must populate the 'passenger' table first. Please try again! </H1>\n"
	puts "</body>"
	puts "</html>"
elsif emptyFile
	puts "<html>"
	puts "<head>"
	puts "<meta http-equiv='refresh' content='45; url=titanicUpload.html'>"
	puts "<title>Mass Insert</title></head>"
	puts "<H1 style=\"text-align: center;\"> ERROR: The uploaded file was empty. Please try again! </H1>\n"
	puts "</body>"
	puts "</html>"
elsif incorrectColumnCount
	puts "<html>"
	puts "<head>"
	puts "<meta http-equiv='refresh' content='45; url=titanicUpload.html'>"
	puts "<title>Mass Insert</title></head>"
	puts "<H1 style=\"text-align: center;\"> ERROR: The uploaded file does not have the correct amount of columns. Please try again! </H1>\n"
	puts "</body>"
	puts "</html>"
else
	puts "<html>"
	puts "<head>"
	puts "<meta http-equiv='refresh' content='45; url=titanicUpload.html'>"
	puts "<title>Mass Insert</title></head>"
	puts "<H1 style=\"text-align: center;\"> ERROR: Something unexpected happened! Th error message is printed above. </H1>\n"
	puts "</body>"
	puts "</html>"
end