#!/usr/bin/ruby
# M'Kiyah Baird and Sarah McLoney
# Databases, Winter 2025
# attributes.cgi
# Allows a user to select all of the attributes they want to see from the current state of the Database. Also allows them to order them by first or last name
#   Always shows first and last name to sort by them (shows the other attributes in relation to first and last name), then other attributes
#   Because unmarried name and cabin are multivalued, they don't go in the select query but are selected separately

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

selectQuery = ""
chosenAttribute = cgi.params['attribute']
sort = cgi['sort']
submit = cgi['submit']
clear = cgi['Clear']
selectedUnmarriedName = false
selectedCabin = false

#### HTML PAGE ####
puts '<HTML>'
puts '<head>'
puts '<link rel="stylesheet" href="titanic.css">'
puts '<TITLE>Attributes</TITLE>'
puts '</head>'
puts '<body id="attributes">'

## Navigation Bar
puts '<div class="navbar">'
puts '<br>'
    puts'<ul>'
        puts'<li><a href="titanic.html">Home</a></li>'
        puts'<li><a href="passenger.cgi">Passengers</a></li>'
        puts'<li><a class="active" href="#!">Attributes</a></li>'
        puts '<li><a href="/Televised/DBTitanic/Admin/titanicUpload.html">Upload</a></li>'
        puts '<li><a href="/Televised/DBTitanic/Admin/modifyAndDelete.html">Modify/Delete</a></li>'
    puts'</ul>'
puts'</div>'

puts '<h1>Current State</h1>'
## .body -- separates the content body from the navigation bar (also allows for a split into two sections in css)
puts '<div class="body">'
# Form
puts '<section class="forms">'
puts '<h3>Select any of the attributes to see them in the current state of the database.</h3>'
puts '<form action="attributes.cgi" method="POST">'
puts '<input type="checkbox" id="survive" name="attribute" value="survive"><label>Survive</label><br>'
puts '<input type="checkbox" id="gender" name="attribute" value="gender"><label>Gender</label><br>'
puts '<input type="checkbox" name="attribute" value="age"><label>Age</label><br>'
puts '<input type="checkbox" name="attribute" value="embarkedFrom"><label>Embarked From</label><br>'
puts '<input type="checkbox" name="attribute" value="honorific"><label>Honorific</label><br>'
puts '<input type="checkbox" name="attribute" value="cabin"><label>Cabin</label><br>'
puts '<input type="checkbox" name="attribute" value="class"><label>Class</label><br>'
puts '<input type="checkbox" name="attribute" value="siblingSpouse"><label>Siblings and Spouses</label><br>'
puts '<input type="checkbox" name="attribute" value="parentKid"><label>Parents and Kids</label><br>'
puts '<input type="checkbox" name="attribute" value="fare"><label>Fare</label><br>'
puts '<input type="checkbox" name="attribute" value="unmarriedName"><label>Unmarried Name</label><br>'
puts '<br>'
puts '<input type="submit" name="submit" value="Submit"> <input type="submit" name="clear" value="Clear"> <div class="infoQuestion">&#10067<span class="moreInfo"><i>Leave all blank to select all.</i></span></div>'
puts '</form>'
puts '<br>'

# Order the information by first or last name
puts '<h5>Order By:</h5>'
puts '<form action="attributes.cgi" class="sort" method="post">'
(0...chosenAttribute.size).each do |i|
    puts '<input type="hidden" name="attribute" value="' + chosenAttribute[i] + '">'
end
if sort == 'fName'
    puts '<button name="sort" class="on" value="fName">First Name</button>'
    puts '<button name="sort" value="lName">Last Name</button>'
    order = 'ORDER by fName ASC'
elsif sort == 'lName'
    puts '<button name="sort" value="fName">First Name</button>'
    puts '<button name="sort" class="on" value="lName">Last Name</button>'
    order = 'ORDER by lName ASC'
else
    puts '<button name="sort" value="fName">First Name</button>'
    puts '<button name="sort" value="lName">Last Name</button>'
    order = ''
end
puts '</form>'
puts '</section>'


## Creating the Table 
puts '<section class="attrInfo">'
    puts '<table class="passInfo">'
    puts '<tr>'
        puts '<th>First Name</th>'
        puts '<th>Last Name</th>'

        (0...chosenAttribute.size).each do |i|
            puts '<th>' + chosenAttribute[i].to_s + '</th>'
            if chosenAttribute[i] != "unmarriedName" && chosenAttribute[i] != "cabin"
                selectQuery = selectQuery + ", " + chosenAttribute[i].to_s
            elsif chosenAttribute[i] == "cabin"
                selectedCabin = true
            else
                selectedUnmarriedName = true
            end
        end
        
# If the query isn't empty and they haven't selected unmarried name, or they have selected unmarried name or cabin, and they haven't cleared the table
if (selectQuery != "" && !selectedUnmarriedName) || selectedUnmarriedName || selectedCabin && clear != "Clear"
        puts '</tr>'
        begin
            info = db.query("SELECT DISTINCT passenger.fName, passenger.lName, passenger.id" + selectQuery + " FROM passenger JOIN lodging ON lodging.passenger = passenger.id " + order + ";").to_a
        rescue => e
        end
        (0...info.size).each do |i|
            puts '<tr>'
            puts '<td><a href="passengerInfo.cgi?id=' + info[i]['id'].to_s + '">'
            puts info[i]['fName'] + '</a></td>'
            puts '<td><a href="passengerInfo.cgi?id=' + info[i]['id'].to_s + '">' + info[i]['lName'] + '</a></td>'
                (0...chosenAttribute.size).each do |j|
                    nextAttr = chosenAttribute[j]
                    if nextAttr != "" && nextAttr != "unmarriedName" && nextAttr != "cabin"
                        if nextAttr == 'gender' && info[i][nextAttr].to_i == 1
                            puts '<td>Female</td>'
                        elsif nextAttr == 'gender' && info[i][nextAttr].to_i == 0
                            puts '<td>Male</td>'
                        elsif nextAttr == 'survive' && info[i][nextAttr].to_i == 0
                            puts '<td>False</td>'
                        elsif nextAttr == 'survive' && info[i][nextAttr].to_i == 1
                            puts '<td>True</td>'
                        elsif (nextAttr == 'age' || nextAttr == 'survive' || nextAttr == 'gender' || nextAttr == 'fare'|| nextAttr == 'ticketNumber' || nextAttr == 'siblingSpouse' || nextAttr == 'parentKid' || nextAttr == 'class') && info[i][nextAttr].to_i == -1
                            puts '<td><i>N/A</i></td>'
                        elsif info[i][nextAttr].to_s == "N/A"
                            puts '<td><i>N/A</i></td>'
                        else 
                            puts '<td>' + info[i][nextAttr].to_s + '</td>'
                        end

                    # Output the unmarried names in one column
                    elsif nextAttr == "unmarriedName"
                        unmarriedNames = db.query("SELECT name FROM unmarriedName WHERE passenger ='" + info[i]['id'].to_s + "';").to_a
                        puts '<td>'
                        (0...unmarriedNames.size).each do |h|
                            puts unmarriedNames[h]['name'].to_s
                        end
                        puts '</td>'

                    # Output the cabins in one column
                    elsif nextAttr == "cabin"
                        cabins = db.query("SELECT cabin FROM lodging WHERE passenger = '" + info[i]['id'].to_s + "';").to_a
                        puts '<td>'
                        (0...cabins.size).each do |h|
                            puts cabins[h]['cabin'].to_s
                        end
                        puts '</td>'
                    end
                end
           puts '</tr>'
        end  

# For everything in the table
elsif selectQuery == "" && submit != "" && clear != "Clear"
    puts '<th>Survive</th>'
    puts '<th>Gender</th>'
    puts '<th>Age</th>'
    puts '<th>Embarked From</th>'
    puts '<th>Honorific</th>'
    puts '<th>Class</th>'
    puts '<th>Fare</th>'
    puts '<th>Siblings/Spouses</th>'
    puts '<th>Parents/Kids</th>'
    puts '<th>Cabin</th>'
    puts '<th>Unmarried Name</th>'
    puts '</tr>'
    begin
        info = db.query("SELECT DISTINCT passenger.fName, passenger.lName, passenger.id, passenger.survive, passenger.gender, passenger.age, passenger.embarkedFrom,
        passenger.honorific, lodging.class, passenger.fare, passenger.siblingSpouse, passenger.parentKid FROM passenger JOIN lodging ON lodging.passenger = passenger.id " + order + ";").to_a
        rescue => e
            #puts e.message
        end
        (0...info.size).each do |i|
            puts '<tr>'
            puts '<td><a href="passengerInfo.cgi?id=' + info[i]['id'].to_s + '">'
            #puts info[i]['id'] 
            puts info[i]['fName'] + '</a></td>'
            puts '<td><a href="passengerInfo.cgi?id=' + info[i]['id'].to_s + '">' + info[i]['lName'] + '</a></td>'
                        if info[i]['survive'].to_i == 0
                            puts '<td>False</td>'
                        elsif info[i]['survive'].to_i == 1
                            puts '<td>True</td>'
                        else
                            puts '<td><i>N/A</i></td>'
                        end

                        if info[i]['gender'].to_i == 0
                            puts '<td>Male</td>'
                        elsif info[i]['gender'].to_i == 1
                            puts '<td>Female</td>'
                        else
                            puts '<td><i>N/A</i></td>'
                        end
                        if info[i]['age'].to_i == -1
                            puts '<td><i>N/A</i></td>'
                        else      
                            puts '<td>' + info[i]['age'].to_s + '</td>'
                        end
                        puts '<td>' + info[i]['embarkedFrom'].to_s + '</td>'
                        puts '<td>' + info[i]['honorific'].to_s + '</td>'
                        if info[i]['class'].to_i == -1
                            puts '<td><i>N/A</i></td>'
                        else
                            puts '<td>' + info[i]['class'].to_s + '</td>'
                        end
                        if info[i]['fare'].to_i == -1
                            puts '<td><i>N/A</i></td>'
                        else
                            puts '<td>' + info[i]['fare'].to_s + '</td>'
                        end
                        if info[i]['siblingSpouse'].to_i == -1
                            puts '<td><i>N/A</i></td>'
                        else
                            puts '<td>' + info[i]['siblingSpouse'].to_s + '</td>'
                        end
                        if info[i]['parentKid'].to_i == -1
                            puts '<td><i>N/A</i></td>'
                        else
                            puts '<td>' + info[i]['parentKid'].to_s + '</td>'
                        end

                        # Output the cabins in one column
                        cabins = db.query("SELECT cabin FROM lodging WHERE passenger = '" + info[i]['id'].to_s + "';").to_a
                        puts '<td>'
                        (0...cabins.size).each do |h|
                            puts cabins[h]['cabin']
                        end
                        puts '</td>'

                        # Output the unmarried names in one column
                        unmarriedNames = db.query("SELECT name FROM unmarriedName WHERE passenger = '" + info[i]['id'].to_s + "';").to_a
                        puts '<td>'
                        (0...unmarriedNames.size).each do |h|
                            puts unmarriedNames[h]['name'].to_s
                        end
                        puts '</td>'
                end
           puts '</tr>'
        end  
    puts '</table>'
puts '</section>'
puts '</div>'
puts '<br>'
puts '</body>'
puts '</HTML>'