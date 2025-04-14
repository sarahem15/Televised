#!/usr/bin/ruby
# M'Kiyah Baird and Sarah McLoney
# Databases, Winter 2025
# passengerInfo.cgi
# Takes in a passenger's id and gets their information from the database to be displayed. Also uses their last names, ticket numbers, and cabin numbers to find
#   other passengers who may be related
# .infoQuestion -- the question mark (for css purposes), .moreInfo -- tells the user how relationships are calculated on hover
#
# References:
#   Emojis and Symbols (W3Schools) -- https://www.w3schools.com/charsets/ref_emoji_smileys.asp
#


$stdout.sync = true
$stderr.reopen $stdout

puts "Content-type: text/html\n\n"
require 'mysql2'
require 'cgi'


cgi = CGI.new
passengerId = cgi['id']

db = Mysql2::Client.new(
    host: '10.20.3.4', 
    username: 'seniorproject25', 
    password: 'TV_Group123!', 
    database: 'televised_w25'
  )

passengerInfo = db.query("SELECT * FROM passenger WHERE id = '" + passengerId + "';")
unmarriedName = db.query("SELECT * FROM unmarriedName where passenger = '" + passengerId + "';").to_a
lodging = db.query("SELECT * FROM lodging where passenger = '" + passengerId + "';").to_a 

if passengerInfo.first['survive'] == 1
    survived = " survived"
else
    survived = " did not survive &#128128"
end

if passengerInfo.first['gender'] == 1
    gender = " female &#9792 "
    pronouns = "She "
else
    gender = " male &#9794 "
    pronouns = "He "
end

if passengerInfo.first['age'] == 0.0
    age = '<i>unknown</i>'
else 
    age = passengerInfo.first['age'].to_s
end


puts '<HTML>'
puts '<head>'
puts '<link rel="stylesheet" href="titanic.css">'
puts '<TITLE>' + passengerInfo.first['fName'] + ' ' + passengerInfo.first['lName'] + '</TITLE>'
puts '</head>'
puts '<body id="passengerInformation">'
puts '<div class="navbar">'
puts '<br>'
    puts'<ul>'
        puts'<li><a href="titanic.html">Home</a></li>'
        puts'<li><a href="passenger.cgi">Passengers</a></li>'
        puts'<li><a href="attributes.cgi">Attributes</a></li>'
        puts '<li><a href="/Televised/DBTitanic/Admin/titanicUpload.html">Upload</a></li>'
        puts '<li><a href="/Televised/DBTitanic/Admin/modifyAndDelete.html">Modify/Delete</a></li>'
    puts'</ul>'
puts'</div>'

#Passenger Information
puts '<section class="infoBody">'
    #Unmarried Name
    if unmarriedName.size != 0
        puts '<h1>&#128081'
            (0...unmarriedName.size).each do |i|
               puts unmarriedName[i]['name'] + ' '
            end
            puts '&#128081</h1><br>'
    end

    #First and Last name
    puts '<h1>' + passengerInfo.first['honorific'] + ' ' + passengerInfo.first['fName'] + ' ' + passengerInfo.first['lName'] + '</h1><br>'
    puts '<h3>Ticket Number: '
    if lodging.to_s != "[]"
     puts lodging.first['ticketNumber'].to_s 
    else
        puts '<i>unknown</i>' 
    end
    puts '</h3><br>'

    puts '<section class="info">'
        puts passengerInfo.first['honorific'] + ' ' + passengerInfo.first['lName'] + survived + ' the Titanic. <br>'
        puts pronouns + 'was' + gender + 'aged ' + age + '.<br>'
        puts pronouns + 'had ' + passengerInfo.first['siblingSpouse'].to_s + ' sibling(s)/spouse(s) aboard and ' +  passengerInfo.first['parentsKids'].to_s + ' parent(s)/kid(s). <br>'
        puts pronouns + 'embarked from ' + passengerInfo.first['embarkedFrom'] + ' for a fare of $' + passengerInfo.first['fare'].to_s + '.<br>'
        puts pronouns + 'lodged in cabin '
        if lodging.to_s != "[]"
            (0...lodging.size).each do |i|
                if lodging[i]['cabin'] == 'N/A'
                    puts '<i>unknown</i>'
                else
                    puts lodging[i]['cabin'].to_s
                end
            end
        else
            puts '<i>unknown</i>' 
        end
        puts 'in class'
        if lodging.to_s != "[]"
            puts lodging.first['class'].to_s
        else
            puts '<i>unknown</i>' 
        end
        puts '.<br>'
    puts '</section>'
    puts '<br>'
    puts '</section>'
    puts '<hr>'

    # Possible Relationships
    puts '<section class="relationships">'
    puts '<h3>Relationships <div class="infoQuestion">&#10067<span class="moreInfo"><i>Passengers who may be related will appear below. These are determined by last name, ticket# and cabin.</i></span></div></h3>'
        if lodging.first['cabin'] != 'N/A'
            begin
                relationships = db.query("SELECT DISTINCT passenger.id, passenger.honorific, passenger.fName, passenger.lName FROM passenger JOIN lodging ON passenger.id = lodging.passenger WHERE 
                    (passenger.lName = '" + passengerInfo.first['lName'] + "' OR lodging.cabin = '" + lodging.first['cabin'] + "' OR lodging.ticketNumber = '" + lodging.first['ticketNumber'].to_s + "') AND NOT passenger.id = '" + passengerId.to_s + "';").to_a
            rescue => e
            end
        else
            begin
                relationships = db.query("SELECT DISTINCT passenger.id, passenger.honorific, passenger.fName, passenger.lName FROM passenger JOIN lodging ON passenger.id = lodging.passenger WHERE 
                    (passenger.lName = '" + passengerInfo.first['lName'] + "' OR lodging.ticketNumber = '" + lodging.first['ticketNumber'].to_s + "') AND NOT passenger.id = '" + passengerId.to_s + "';").to_a
            rescue => e
            end
        end
        (0...relationships.size).each do |i|
            puts '<a href="passengerInfo.cgi?id=' + relationships[i]['id'].to_s + '">'
            puts relationships[i]['honorific']
            puts relationships[i]['fName']
            puts relationships[i]['lName'] + '</a><br>'
        end
puts '</section>'

puts '<br>'
puts '</body>'
puts '</HTML>'