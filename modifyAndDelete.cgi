#!/usr/bin/ruby
# M'Kiyah Baird and Sarah McLoney
# Databases, Winter 2025
# modifyAndDelete.cgi

### ADMIN LOGIN ###
#   Username: smcloney
#   Password: csJintonG#1

# Attempts to perform an Admin-entered MySQL query.
#   On the corresponding modifyAndDelete.html file, the Admin, who is assumed to know MySQL, is asked to drop the semicolon and substitue the following:
#       Instead of using 'WHERE', substitue it with 'W', and
#       instead of using '=', substitue it with 'equals'.
#       This was done to avoid the 403 Forbidden message when inputting proper MySQL queries into the textbox. After trial and error submissions, these
#           two substitutions were found to fix the issue. This file then uses .gsub to correct the substitutons and have the proper MySQL syntax.
#   The query is parsed to determine if the Admin attempted any of the following commands:
#       DROP, CREATE, or ALTER a table by dropping a column.
#       Since our three tables are already normalized, there is no need for the Admin to have the ability to permanently change their structure.
#       If any of these commands were attempted, then the Admin is told that they are not allowed to do so.
#   If the query fails for any other reason, then it is printed to the screen.
#   If the query is successful, then the Admin sees all three tables displayed.

# References:
#   Used to incorporate the arrow emoji on the corresponding .html file -- https://emojiguide.org/right-arrow
#   Used to compare strings in the inputted MySQL query -- https://stackoverflow.com/questions/2844507/how-to-compare-strings-ignoring-the-case

$stdout.sync = true
$stderr.reopen $stdout

puts "Content-type: text/html\n\n"
require 'mysql2'
require 'cgi'
require 'stringio'

db = Mysql2::Client.new(:host=>'10.20.3.4', :username=>'seniorproject25', :password=>'TV_Group123!', :database=>'televised_w25')
cgi = CGI.new
query = cgi['query']
attemptedDrop = false
attemptedCreate = false
attemptedAlter = false

querySplit = query.split(" ")
if (querySplit[0].casecmp("DROP") == 0) && (querySplit[1].casecmp("TABLE") == 0)
	attemptedDrop = true
end

if (querySplit[0].casecmp("CREATE") == 0) && (querySplit[1].casecmp("TABLE") == 0)
	attemptedCreate = true
end

if (querySplit[0].casecmp("ALTER") == 0) && (querySplit[1].casecmp("TABLE") == 0) && (querySplit[3].casecmp("DROP") == 0) && (querySplit[4].casecmp("COLUMN") == 0)
    attemptedAlter = true
end

finalQuery = query.gsub(" W ", " WHERE ").gsub("equals", "=")

puts "<html>"
puts "<head>"
puts "<link rel=\"stylesheet\" href=\"/Televised/DBTitanic/User/titanic.css\">"
puts "<title> Modfiy and Delete Result </title></head>"
puts "<body id='modAndDelete'>"

if (!attemptedDrop) && (!attemptedCreate) && (!attemptedAlter)
	begin
		db.query(finalQuery + ";")
	rescue => e
		errorMessage = e.message
	end
end

if attemptedDrop
	puts "<H1 style=\"text-align: center;\"> ERROR: You cannot drop a table! </H1>\n"
elsif attemptedCreate
	puts "<H1 style=\"text-align: center;\"> ERROR: You cannot create a table! </H1>\n"
elsif attemptedAlter
    puts "<H1 style=\"text-align: center;\"> ERROR: You cannot alter a table! </H1>\n"
elsif errorMessage.class != NilClass
	puts "<H1 style=\"text-align: center;\"> ERROR: Something was wrong with your query! </H1>\n"
	puts "<H2 style=\"text-align: center;\">" + errorMessage + "</H2>\n"
	puts "<H3 style=\"text-align: center;\"> Original query: " + finalQuery + ";</H3>\n"
else
	puts "<H1 style=\"text-align: center;\"> Success! </H1>\n"
    puts "<H3 style=\"text-align: center;\"> Original query: " + finalQuery + ";</H3>\n"
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
end

puts "</body>"
puts "</html>"