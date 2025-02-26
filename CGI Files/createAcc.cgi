#!/usr/bin/ruby
require 'mysql2'
require 'cgi'
require 'cgi/session'

# Enable debugging
$stdout.sync = true
$stderr.reopen $stdout

# Initialize CGI
cgi = CGI.new
session = CGI::Session.new(cgi)

# Retrieve form parameters
unameCreateInput = cgi['unameCreateInput']
passCreateInput = cgi['passCreateInput']

session['username'] = unameCreateInput
session.close
print cgi.header(
  'cookie' => CGI::Cookie.new('name' => 'CGISESSID', 'value' => session.session_id, 'httponly' => true, 'secure' => true)
)

# Print HTTP header
print "Content-type: text/html\r\n\r\n"

# Start HTML output
puts "<!DOCTYPE html>"
puts "<html lang='en'>"
puts "<head>"
puts "<meta charset='UTF-8'>"
puts "<title>Account Creation</title>"
puts "<link href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css' rel='stylesheet'>"
print "<meta http-equiv='refresh' content='0; url=http://www.cs.transy.edu/Televised/Home.cgi'>\n"
puts "</head>"
puts "<body>"
puts "<div class='container mt-5'>"

# Debugging: Print received parameters
=begin
puts "<h3>Received Parameters:</h3>"
puts "<p>Username:" + cgi['unameCreateInput'] + "</p>"
puts "<p>Password:" + cgi['passCreateInput'] + "</p>"
=end
# Connect to MySQL and insert data
#begin
  db = Mysql2::Client.new(
    host: '10.20.3.4', 
    username: 'seniorproject25', 
    password: 'TV_Group123!', 
    database: 'televised_w25'
  )

db.query("INSERT INTO account (username, password, replies) VALUES ('" + cgi['unameCreateInput'] + "','" + cgi['passCreateInput'] + "', '1');")

# automatically public = 1
# top 5 by media
# have watched by media
# wtow by media

puts "</body>"
puts "</html>"

session.close