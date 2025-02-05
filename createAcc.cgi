#!/usr/bin/ruby
require 'mysql2'
require 'cgi'

# Enable debugging
$stdout.sync = true
$stderr.reopen $stdout

# Initialize CGI
cgi = CGI.new

# Retrieve form parameters
unameCreateInput = cgi['unameCreateInput']
passCreateInput = cgi['passCreateInput']

=begin
# Print HTTP header
print "Content-type: text/html\r\n\r\n"

# Start HTML output
puts "<!DOCTYPE html>"
puts "<html lang='en'>"
puts "<head>"
puts "<meta charset='UTF-8'>"
puts "<title>Account Creation</title>"
puts "<link href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css' rel='stylesheet'>"
puts "</head>"
puts "<body>"
puts "<div class='container mt-5'>"

# Debugging: Print received parameters
puts "<h3>Received Parameters:</h3>"
puts "<p>Username:" + cgi['unameCreateInput'] + "</p>"
puts "<p>Password:" + cgi['passCreateInput'] + "</p>"

=end

# Connect to MySQL and insert data
begin
  db = Mysql2::Client.new(
    host: 'localhost', 
    username: 'root', 
    password: 'TV_Group123!', 
    database: 'media'
  )


  db.query("INSERT INTO accounts (username, password) VALUES ('" + cgi['unameCreateInput'] + "','" + cgi['passCreateInput'] + "');")
end

