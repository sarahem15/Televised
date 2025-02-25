#!/usr/bin/ruby
require 'mysql2'
require 'cgi'

# Enable debugging
$stdout.sync = true
$stderr.reopen $stdout

# Initialize CGI
cgi = CGI.new

# Retrieve form parameters
userName = cgi['userNameX']
displayName = cgi['displayName']
bio = cgi['bio']
pronouns = cgi['pronouns']
replies = cgi['replies']

# Print HTTP header
print "Content-type: text/html\r\n\r\n"

# Start HTML output
puts "<!DOCTYPE html>"
puts "<html lang='en'>"
puts "<head>"
puts "<meta charset='UTF-8'>"
puts "<title>Edit Settings</title>"
puts "<link href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css' rel='stylesheet'>"
print "<meta http-equiv='refresh' content='0; url=http://www.cs.transy.edu/Televised/Home.cgi'>\n"
puts "</head>"
puts "<body>"
puts "<div class='container mt-5'>"

# Debugging: Print received parameters
#puts "<h3>Received Parameters:</h3>"
#puts "<p>Username:" + cgi['userNameX'] + "</p>"
#puts "<p>Display name:" + cgi['displayName'] + "</p>"
#puts "<p>Bio:" + cgi['bio'] + "</p>"
#puts "<p>Pronouns:" + cgi['pronouns'] + "</p>"
#puts "<p>Replies:" + cgi['replies'] + "</p>"

# Connect to MySQL and insert data
#begin
  db = Mysql2::Client.new(
    host: '10.20.3.4', 
    username: 'seniorproject25', 
    password: 'TV_Group123!', 
    database: 'televised_w25'
  )


  #db.query("update account set displayName = '" + displayName.to_s + "', bio = '" + bio.to_s + "', pronouns = '" + pronouns.to_s + "' where username = '" + username "';")
puts "</body>"
puts "</html>"

