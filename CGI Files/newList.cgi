#!/usr/bin/ruby
require 'mysql2'
require 'cgi'

# Enable debugging
$stdout.sync = true
$stderr.reopen $stdout

# Initialize CGI
cgi = CGI.new

# Retrieve form parameters
listName = cgi['listName']
type = cgi['type']
views = cgi['views']
description = cgi['description']

# Print HTTP header
print "Content-type: text/html\r\n\r\n"

# Start HTML output
puts "<!DOCTYPE html>"
puts "<html lang='en'>"
puts "<head>"
puts "<meta charset='UTF-8'>"
puts "<title>Create New List</title>"
puts "<link href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css' rel='stylesheet'>"
print "<meta http-equiv='refresh' content='0; url=http://www.cs.transy.edu/Televised/Profile_Lists.cgi'>\n"
puts "</head>"
puts "<body>"
puts "<div class='container mt-5'>"

# Debugging: Print received parameters
=begin
puts "<h3>Received Parameters:</h3>"
puts "<p>List name:" + cgi['listName'] + "</p>"
puts "<p>Description:" + cgi['description'] + "</p>"
puts "<p>Type:" + cgi['type'] + "</p>"
puts "<p>Views:" + cgi['views'] + "</p>"
=end
# Connect to MySQL and insert data
#begin
  db = Mysql2::Client.new(
    host: '10.20.3.4', 
    username: 'seniorproject25', 
    password: 'TV_Group123!', 
    database: 'televised_w25'
  )


  #db.query("update lists set listName = '" + listName.to_s + "', description = '" + description.to_s + "', listType = '" + type.to_s + "' where username = '" + username "';")