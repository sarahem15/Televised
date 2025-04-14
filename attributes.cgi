#!/usr/bin/ruby
# M'Kiyah Baird and Sarah McLoney
# Databases, Winter 2025
# attributes.cgi
# Allows a user to select all of the attributes they want to see from the current state of the Database. Also allows them to order them by first or last name
#   Always shows first and last name, then other attributes
#

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
selectedUnmarriedName = false
selectedCabin = false

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

puts '<div class="body">'
puts '<section class="forms">'
puts '<form action="attributes.cgi" method="POST">'
puts '<input type="checkbox" id="survive" name="attribute" value="survive"><label>Survive</label><br>'
puts '<input type="checkbox" id="gender" name="attribute" value="gender"><label>Gender</label><br>'
puts '<input type="checkbox" name="attribute" value="age"><label>Age</label><br>'
puts '<input type="checkbox" name="attribute" value="embarkedFrom"><label>Embarked From</label><br>'
puts '<input type="checkbox" name="attribute" value="honorific"><label>Honorific</label><br>'
puts '<input type="checkbox" name="attribute" value="cabin"><label>Cabin</label><br>'
puts '<input type="checkbox" name="attribute" value="class"><label>Class</label><br>'
puts '<input type="checkbox" name="attribute" value="siblingSpouse"><label>Siblings and Spouses</label><br>'
puts '<input type="checkbox" name="attribute" value="parentsKids"><label>Parents and Kids</label><br>'
puts '<input type="checkbox" name="attribute" value="fare"><label>Fare</label><br>'
puts '<input type="checkbox" name="attribute" value="unmarriedName"><label>Unmarried Name</label><br>'
puts '<br>'
puts '<input type="submit" name="submit" value="Submit"> <div class="infoQuestion">&#10067<span class="moreInfo"><i>Leave all blank to select all.</i></span></div>'
puts '</form>'
puts '<br>'
puts '<h5>Order By:</h5>'
puts '<form action="attributes.cgi" class="sliding" method="post">'
(0...chosenAttribute.size).each do |i|
    puts '<input type="hidden" name="attribute" value="' + chosenAttribute[i] + '">'
end
if sort == 'az'
    puts '<button name="sort" class="on" value="az">First Name</button>'
    puts '<button name="sort" value="id">Last Name</button>'
    order = 'ORDER by fName ASC'
elsif sort == 'id'
    puts '<button name="sort" value="az">First Name</button>'
    puts '<button name="sort" class="on"value="id">Last Name</button>'
    order = 'ORDER by lName ASC'
else
    puts '<button name="sort" value="az">First Name</button>'
    puts '<button name="sort" value="id">Last Name</button>'
    order = ''
end
puts '</form>'
puts '</section>'
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
        

if (selectQuery != "" && !selectedUnmarriedName) || selectedUnmarriedName || selectedCabin
        puts '</tr>'
        begin
        info = db.query("SELECT DISTINCT passenger.fName, passenger.lName, passenger.id" + selectQuery + " FROM passenger JOIN lodging ON lodging.passenger = passenger.id " + order + ";").to_a
        rescue => e
            #puts e.message
        end
        (0...info.size).each do |i|
            puts '<tr>'
            puts '<td><a href="passengerInfo.cgi?id=' + info[i]['id'].to_s + '">'
            #puts info[i]['id'] 
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
                        elsif nextAttr == 'age' && info[i][nextAttr].to_f == 0.0
                            puts '<td><i>N/A</i></td>'
                        elsif info[i][nextAttr].to_s == "N/A"
                            puts '<td><i>N/A</i></td>'
                        else 
                            puts '<td>' + info[i][nextAttr].to_s + '</td>'
                        end
                    elsif nextAttr == "unmarriedName"
                        unmarriedNames = db.query("SELECT name FROM unmarriedName WHERE passenger ='" + info[i]['id'].to_s + "';").to_a
                        puts '<td>'
                        (0...unmarriedNames.size).each do |h|
                            puts unmarriedNames[h]['name'].to_s
                        end
                        puts '</td>'
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
elsif selectQuery == "" && submit != ""
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
        passenger.honorific, lodging.class, passenger.fare, passenger.siblingSpouse, passenger.parentsKids FROM passenger JOIN lodging ON lodging.passenger = passenger.id " + order + ";").to_a
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
                        end

                        if info[i]['gender'].to_i == 0
                            puts '<td>Male</td>'
                        elsif info[i]['gender'].to_i == 1
                            puts '<td>Female</td>'
                        end
                        if info[i]['age'].to_f == 0.0
                            puts '<td><i>N/A</i></td>'
                        else      
                            puts '<td>' + info[i]['age'].to_s + '</td>'
                        end
                        puts '<td>' + info[i]['embarkedFrom'].to_s + '</td>'
                        puts '<td>' + info[i]['honorific'].to_s + '</td>'
                        puts '<td>' + info[i]['class'].to_s + '</td>'
                        puts '<td>' + info[i]['fare'].to_s + '</td>'
                        puts '<td>' + info[i]['siblingSpouse'].to_s + '</td>'
                        puts '<td>' + info[i]['parentsKids'].to_s + '</td>'

                        cabins = db.query("SELECT cabin FROM lodging WHERE passenger = '" + info[i]['id'].to_s + "';").to_a
                        puts '<td>'

                        (0...cabins.size).each do |h|
                            puts cabins[h]['cabin']
                        end
                        puts '</td>'

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