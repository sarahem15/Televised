#!/usr/bin/ruby
# Titanic Upload
# Uploading the information from the titanic csv into the database

# https://stackoverflow.com/questions/1893424/count-table-rows

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

passengerNum = 1
passengerEmpty = false
emptyFile = false
incorrectColumnCount = false
passengerCount = db.query("SELECT COUNT(*) FROM passenger;")
if passengerCount.first['COUNT(*)'] == 0
	passengerEmpty = true
end

toFile = uploadLocation + originalName 
File.open(toFile.untaint, 'w') { |file| file << fromfile.read}
titanicFile = IO.readlines(toFile)
if (titanicFile.size == 0)
	emptyFile = true
end

numOfColumns = titanicFile[0].split("|")
if numOfColumns.size != 14
	incorrectColumnCount = true
end

if (tableName.size != 0) && (!passengerEmpty || tableName[0] == "passenger") && (!emptyFile) && (!incorrectColumnCount)
	titanicFile.drop(1).each do |fileRead|
		currentLine = fileRead.split("|")
		#puts passengerNum.to_s
		if currentLine[0].strip == "False"
			survive = 0
		else
			survive = 1
		end
	
		passClass = currentLine[1]
		honorific = currentLine[2]
		firstName = currentLine[3]
		lastName = currentLine[4]
		unmarriedName = currentLine[5].split(" ")
		if currentLine[6].strip == "male"
			gender = 0
		else
			gender = 1
		end
	
		if currentLine[7] == ""
			age = 0
		else
			age = currentLine[7]
		end

		siblingsSpouse = currentLine[8]
		parentsKids = currentLine[9]
		if currentLine[10] == ""
			ticketNumber = 0
		else
			ticketNumber = currentLine[10]
		end
	
		fare = currentLine[11]
		if currentLine[12] == ""
			cabins = "N/A"
		else
			cabins = currentLine[12].split(" ")
		end
	
		embarkedFrom = currentLine[13]
		(0...tableName.size).each do |i|
			if tableName[i] == "passenger"
				begin
				db.query("INSERT INTO passenger Values(NULL, '" + survive.to_s.strip + "','" + firstName.gsub("'", "\\\\'").strip + "','" + 
					lastName.gsub("'", "\\\\'").strip + "','" + gender.to_s.strip + "','" + age.to_s.strip + "','" + siblingsSpouse.to_s.strip + "','" + parentsKids.to_s.strip + 
					"', '" + embarkedFrom.strip + "', '" + honorific.strip + "', '" + fare.to_s + "');")
				rescue => e
					puts e.message
				end


			elsif tableName[i] == "unmarriedName"
				(0...unmarriedName.size).each do |i|
					db.query("INSERT INTO unmarriedName Values(NULL,'" + unmarriedName[i].gsub("'", "\\\\'").strip + "','" + passengerNum.to_s.strip + "');")
				end

			elsif tableName[i] == "lodging"
				if cabins == "N/A"
					db.query("INSERT INTO lodging Values(NULL, '" + ticketNumber.to_s + "','" + cabins + "','" + 
						passClass.to_s + "','" + passengerNum.to_s + "');")
				else
					(0...cabins.size).each do |i|
						db.query("INSERT INTO lodging Values(NULL, '" + ticketNumber.to_s + "','" + cabins[i] + "','" + 
							passClass.to_s + "','" + passengerNum.to_s + "');")
					end
				end
			end
		end
		passengerNum = passengerNum + 1
	end
	puts "<html>"
	puts "<head>"
	#puts "<meta http-equiv='refresh' content='45; url=titanicUpload.html'>"
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
	    	puts '<td>' + passenger[i]['parentsKids'].to_s + '</td>'
	    	puts '<td>' + passenger[i]['embarkedFrom'].to_s + '</td>'
	    	puts '<td>' + passenger[i]['honorific'].to_s + '</td>'
	    	puts '<td>' + passenger[i]['fare'].to_s + '</td>'
	    	puts '</tr>'
	    end
	    puts '</table>'
	    puts '</section>'
		#puts '<br>'
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
	    #puts '<br>'
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
	puts "<meta http-equiv='refresh' content='45; url=upload.html'>"
	puts "<title>Mass Insert</title></head>"
	puts "<H1 style=\"text-align: center;\"> ERROR: You did not select a table name. Please try again! </H1>\n"
	puts "</body>"
	puts "</html>"
elsif passengerEmpty
	puts "<html>"
	puts "<head>"
	puts "<meta http-equiv='refresh' content='45; url=upload.html'>"
	puts "<title>Mass Insert</title></head>"
	puts "<H1 style=\"text-align: center;\"> ERROR: You must populate the 'passenger' table first. Please try again! </H1>\n"
	puts "</body>"
	puts "</html>"
elsif emptyFile
	puts "<html>"
	puts "<head>"
	puts "<meta http-equiv='refresh' content='45; url=upload.html'>"
	puts "<title>Mass Insert</title></head>"
	puts "<H1 style=\"text-align: center;\"> ERROR: The uploaded file was empty. Please try again! </H1>\n"
	puts "</body>"
	puts "</html>"
elsif incorrectColumnCount
	puts "<html>"
	puts "<head>"
	puts "<meta http-equiv='refresh' content='45; url=upload.html'>"
	puts "<title>Mass Insert</title></head>"
	puts "<H1 style=\"text-align: center;\"> ERROR: The uploaded file does not have the correct amount of columns. Please try again! </H1>\n"
	puts "</body>"
	puts "</html>"
else
	puts "<html>"
	puts "<head>"
	puts "<meta http-equiv='refresh' content='45; url=upload.html'>"
	puts "<title>Mass Insert</title></head>"
	puts "<H1 style=\"text-align: center;\"> ERROR: Something unknown happened! </H1>\n"
	puts "</body>"
	puts "</html>"
end