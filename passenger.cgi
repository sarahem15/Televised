#!/usr/bin/ruby
# M'Kiyah Baird and Sarah McLoney
# Databases, Winter 2025
# passenger.cgi
# Allows a user to search for a passenger by any attribute. Each field is searched together (and), separately (or), or removed from the search (not). 
# Uses LIKE to search through first, last, unmarried name, and fare by first characters. Replaces -1s with N/A to indicate missing information. 
#       Allows users to search by -12 for integer values to see missing.
# First and Last name are hrefs to passengerInfo.cgi --
#       Sends the selected passenger id to passengerInfo, allows user to see specific information for any passenger
# References:  
#    Hover text, learned in Senior Project (W3Schools) -- https://www.w3schools.com/css/css_tooltip.asp (used in multiple files)

$stdout.sync = true
$stderr.reopen $stdout

puts "Content-type: text/html\n\n"
require 'mysql2'
require 'cgi'

cgi = CGI.new

db = Mysql2::Client.new(
    host: '10.20.3.4', 
    username: 'seniorproject25', 
    password: 'TV_Group123!', 
    database: 'televised_w25'
  )

firstName = cgi['firstName'].gsub("'", "\\\\'")
lastName = cgi['lastName'].gsub("'", "\\\\'")
unmarriedName = cgi['unmarriedName'].gsub("'", "\\\\'")
age = cgi['age']
range1 = cgi['range1']
range2 = cgi['range2']
gender = cgi['gender']
survive = cgi['survive']
honorific = cgi['honorific']
embarkedFrom = cgi.params['embarkedFrom']
cabin = cgi['cabin']
passClass = cgi.params['class']
andOr = cgi['submit']
fare = cgi['fare']
parentKid = cgi['parentKid']
siblingSpouse = cgi['siblingSpouse']
attrToSearch = ""
attrToList = ""
uQuery = ""
embarked = ""
classes = ""

# Clear the table
if cgi['clear'] == "Clear"
    firstName = ""
    lastName = ""
    unmarriedName = ""
    age = ""
    range1 = ""
    range2 = ""
    gender = ""
    survive = ""
    honorific = ""
    embarkedFrom = ""
    cabin = ""
    passClass = ""
end

# Set the conditional
firstChar = ""
if andOr == 'Any'
    searchBy =  ' OR '
elsif andOr == 'None'
    searchBy =  ' AND NOT '
    firstChar = 'NOT '
else
    searchBy = ' AND '
end


#### HTML PAGE ####
puts '<HTML>'
puts '<head>'
puts '<link rel="stylesheet" href="titanic.css">'
puts '<TITLE>Attributes</TITLE>'
puts '</head>'
puts '<body id="passengerSearch">'

## Navigation Bar
puts '<div class="navbar">'
puts '<br>'
    puts'<ul>'
        puts'<li><a href="titanic.html">Home</a></li>'
        puts'<li><a class="active" href="#!">Passengers</a></li>'
        puts'<li><a href="attributes.cgi">Attributes</a></li>'
        puts '<li><a href="/Televised/DBTitanic/Admin/titanicUpload.html">Upload</a></li>'
        puts '<li><a href="/Televised/DBTitanic/Admin/modifyAndDelete.html">Modify/Delete</a></li>'
    puts'</ul>'
puts'</div>'

puts '<h1>Search</h1>'
## .body -- separates the content body from the navigation bar (also allows for a split into two sections in css)
puts '<div class="body">'

# form
puts '<section class="forms">'
puts '<h3>To search for a specific passenger, use any of the attributes below.</h3>'
puts '<h4>Name</h4>'
puts '<form action="passenger.cgi" method="POST">'
puts '<label for="firstName">First Name</label> <input type="text" id="firstName" name="firstName" value="' + firstName + '"><br>'
puts '<label for="lastName">Last Name</label> <input type="text" id="lastName" name="lastName" value="' + lastName + '"><br>'
puts '<label for="unmarriedName">Unmarried Name</label> <input type="text" id="unmarriedName" name="unmarriedName" value="' + unmarriedName + '"><br>'
puts '<br>'
puts '<hr>'
puts '<h4>Age <div class="infoQuestion">&#10067<span class="moreInfo">To see missing number values, enter \'-1\'</span></div></h4>'
puts '<input type="number" id="age" name="age" value="' + age + '" min="-1"><br>'
puts '- or -'
puts '<br>'
puts 'from <input type="number" id="age" name="range1" value="' + range1 + '" min="-1"> to <input type="number" id="age" name="range2" value="' + range2 + '" min="-1"><br>'
puts '<br>'
puts '<hr>'
puts '<h4>Gender</h4>'
puts '<label for="female">Female</label> <input type="radio" id="female" name="gender" value="1"><br>'
puts '<label for="male">Male</label> <input type="radio" id="male" name="gender" value="0"><br>'
puts '<br>'
puts '<hr>'
puts '<h4>Survive</h4>'
puts '<label for="yes">Yes</label> <input type="radio" id="yes" name="survive" value="1"><br>'
puts '<label for="no">No</label> <input type="radio" id="no" name="survive" value="0"><br>'
puts '<br>'
puts '<hr>'
puts '<h4>Honorific</h4>'
puts '<input type="text" id="Honorific" name="honorific" value="' + honorific + '"><br>'
puts '<br>'
puts '<hr>'
embarkedLocations = db.query("SELECT DISTINCT embarkedFrom FROM passenger WHERE embarkedFrom != '';").to_a
puts '<h4>Embarked From Locations</h4>'
(0...embarkedLocations.size).each do |i|
    puts '<input type="checkbox" name="embarkedFrom" value="' + embarkedLocations[i]['embarkedFrom'] + '"><label>' + embarkedLocations[i]['embarkedFrom'] + '</label><br>'
end
puts '<br>'
puts '<hr>'
puts '<h4>Cabin</h4>'
puts '<input type="text" name="cabin" value="' + cabin + '"><br>'
puts '<br>'
puts '<hr>'
puts '<h4>Class</h4>'
puts '<input type="checkbox" id="1" name="class" value="1"><label for="1">1</label><br>'
puts '<input type="checkbox" id="2" name="class" value="2"><label for="2">2</label><br>'
puts '<input type="checkbox" id="3" name="class" value="3"><label for="3">3</label><br>'
puts '<input type="checkbox" id="n/a" name="class" value="-1"><label for="n/a">N/A</label><br>'
puts '<br>'
puts '<hr>'
puts '<h4>Fare <div class="infoQuestion">&#10067<span class="moreInfo"><i>(Represented by a float. If you would like $12, put \'12.\')</i></span></div></h4>'
puts '<input type="text" id="fare" name="fare" value="' + fare + '"><br>'
puts '<br>'
puts '<hr>'

puts '<h4>Siblings/Spouse</h4>'
puts '<input type="number" name="siblingSpouse" value="' + siblingSpouse + '" min="-1"><br>'
puts '<br>'
puts '<hr>'
puts '<h4>Parents/Kids</h4>'
puts '<input type="number" name="parentKid" value="' + parentKid + '"  min="-1"><br>'
puts '<br>'
puts '<hr>'
puts '<br>'
puts '<div class="infoQuestion">&#10067<span class="moreInfo"><i>Select \'All\' to search by all qualifications entered, \'Any\' for any of the qualifications, or \'None\' for none to appear.</i></span></div>'
puts '<br>'
puts '<br>'
puts '<input type="submit" name="submit" value="All">'
puts '<input type="submit" name="submit" value="Any">'
puts '<input type="submit" name="submit" value="None">'
puts '<input type="submit" name="clear" value="Clear">'
puts '<br>'
puts '<br>'
puts '</form>'
puts '</section>'


## Creating the queries to search and list (attrToSearch -- what they want to search by, attrToList -- what appears on the screen)
if firstName != ""
    attrToSearch = attrToSearch + "|fName like '" + firstName + "%'|"
end
if lastName != ""
    attrToSearch = attrToSearch + "|lName like '" + lastName + "%'|"
end
if unmarriedName != ""
    attrToList = attrToList + ", unmarriedName.passenger"
    attrToSearch = attrToSearch + "|name like '" + unmarriedName + "%'|"
    uQuery = "JOIN unmarriedName ON unmarriedName.passenger = passenger.id"
end
if age != ""
    attrToSearch = attrToSearch + "|age = '" + age + "'|"
    attrToList = attrToList + ", passenger.age"
elsif range1 != "" && range2 != ""
    attrToSearch = attrToSearch + "|age BETWEEN '" + range1 + "' AND '" + range2 + "'|"
    attrToList = attrToList + ", passenger.age"
end
if gender != ""
    attrToSearch = attrToSearch + "|gender = '" + gender + "'|"
    attrToList = attrToList + ", passenger.gender"
end
if survive != ""
    attrToSearch = attrToSearch + "|survive = '" + survive + "'|"
    attrToList = attrToList + ", passenger.survive"
end
if honorific != ""
    attrToSearch = attrToSearch + "|honorific = '" + honorific + "'|"
    attrToList = attrToList + ", passenger.honorific"
end
if embarkedFrom[0].to_s != ""
    if embarkedFrom.size > 1
        (0...embarkedFrom.size).each do |i|
            if i == 0
                embarked = embarkedFrom[i].strip + "'"
            else 
                embarked = embarked + " OR embarkedFrom = '" + embarkedFrom[i].strip + "'"
            end
        end
        attrToList = attrToList + ", passenger.embarkedFrom"
    else
        embarked = embarkedFrom[0].to_s.strip + "'"
    end
    attrToSearch = attrToSearch + "|embarkedFrom = '" + embarked + "|"
end
if passClass[0].to_s != ""
    if passClass.size > 1
        (0...passClass.size).each do |i|
            if i == 0
                classes = passClass[i].to_s.strip + "'"
            else 
                classes = classes + " OR class = '" + passClass[i].to_s.strip + "'"
            end
        end
        attrToList = attrToList + ", lodging.class"
    else
        classes = passClass[0].to_s.strip + "'"
    end
    attrToSearch = attrToSearch + "|class = '" + classes + "|"
    attrToList = attrToList + ", lodging.class"
end
if cabin != ""
    attrToSearch = attrToSearch + "|cabin = '" + cabin + "'|"
    attrToList = attrToList + ", lodging.class"
end
if fare != ""
    attrToSearch = attrToSearch + "|fare like '" + fare + "%'|"
    attrToList = attrToList + ", passenger.fare"
end
if siblingSpouse != ""
    attrToSearch = attrToSearch + "|siblingSpouse = '" + siblingSpouse + "'|"
    attrToList = attrToList + ", passenger.siblingSpouse"
end
if parentKid != ""
    attrToSearch = attrToSearch + "|parentKid = '" + parentKid + "'|"
    attrToList = attrToList + ", passenger.parentKid"
end

## Creating the table
# Replaces the '|' with the chosen search conditional (and, or, not)
attrToSearch = attrToSearch.gsub("||", searchBy).gsub("|", "")
#removes the table name to get the attributes
attributes = attrToList.gsub("passenger.", "").gsub("lodging.", "").gsub("unmarriedName.", "").split(", ")
puts '<section class="attrInfo">'
puts '<table class="passInfo">'
    puts '<tr>'
        puts '<th>First Name</th>'
        puts '<th>Last Name</th>'
        (0...attributes.size).each do |j|
            if attributes[j] != ""
                if attributes[j] == "passenger"
                    puts '<th>Unmarried Name</th>'
                else
                    puts '<th>' + attributes[j].to_s + '</th>'
                end
            end
        end
    puts '</tr>'

# if the search isn't empty 
### DEBUG -- puts attrToSearch
if attrToSearch != ""
    begin
        passengers = db.query("SELECT DISTINCT passenger.id, passenger.fName, passenger.lName" + attrToList + " FROM passenger JOIN lodging ON lodging.passenger = passenger.id " + uQuery + " WHERE " + firstChar + attrToSearch + ";").to_a
    rescue => e
        #puts e.message
    end
    if passengers.size != 0
        (0...passengers.size).each do |i|
            puts '<tr>'
            puts '<td><a href="passengerInfo.cgi?id=' + passengers[i]['id'].to_s + '">'
            puts passengers[i]['fName'] + '</a></td>'
            puts '<td><a href="passengerInfo.cgi?id=' + passengers[i]['id'].to_s + '">' + passengers[i]['lName'] + '</a></td>'
                (0...attributes.size).each do |j|
                    nextAttr = attributes[j]
                    if nextAttr != ""
                        # Output the unmarried names in one column
                        if unmarriedName != "" && nextAttr == 'passenger'
                            begin
                                uMNames = db.query("SELECT * FROM unmarriedName WHERE passenger = '" + passengers[i]['id'].to_s + "';").to_a
                            rescue => e
                            end
                            puts '<td>'
                            (0...uMNames.size).each do |h|
                                puts uMNames[h]['name'].to_s
                            end
                            puts '</td>'
                        elsif nextAttr == 'gender'
                            if passengers[i][nextAttr].to_i == 1
                                puts '<td>Female</td>'
                            elsif passengers[i][nextAttr].to_i == 0
                                puts '<td>Male</td>'
                            else
                                puts '<td><i>N/A</i></td>'
                            end
                        elsif nextAttr == 'survive'
                            if passengers[i][nextAttr].to_i == 1
                                puts '<td>YES</td>'
                            elsif passengers[i][nextAttr].to_i == 0
                                puts '<td>NO</td>'
                            else
                                puts '<td><i>N/A</i></td>'
                            end
                        elsif (nextAttr == 'age' || nextAttr == 'survive' || nextAttr == 'gender' || nextAttr == 'fare'|| nextAttr == 'ticketNumber' || nextAttr == 'siblingSpouse' || nextAttr == 'parentKid' || nextAttr == 'class') && passengers[i][nextAttr].to_i == -1
                                puts '<td><i>N/A</i></td>'
                        else
                            puts '<td>' + passengers[i][nextAttr].to_s + '</td>'
                        end
                    end
                end
           puts '</tr>'
        end 
        puts '</table>'
    else 
        # Puts error message if nothing in the table from the query
       puts '</table>'
        puts '<h2 style="text-align:center; background-color:black; height: 80px;">We can\'t seem to find that passenger!</h2>' 
    end
end
puts '</section>'
puts '</div>'
puts '<br>'
puts '</body>'
puts '</HTML>'