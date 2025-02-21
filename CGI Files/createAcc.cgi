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

# Connect to MySQL and insert data
#begin
  db = Mysql2::Client.new(
    host: '10.20.3.4', 
    username: 'seniorproject25', 
    password: 'TV_Group123!', 
    database: 'televised_w25'
  )


db.query("INSERT INTO account (username, password) VALUES ('" + cgi['unameCreateInput'] + "','" + cgi['passCreateInput'] + "');")
# accountId = db.query("SELECT accountId FROM account WHERE username = '" + unameCreateInput + "';")
user = unameCreateInput.split('@')[0].strip 
tableName = user.to_s + "ListInfo"
# ADD DATE CREATED AND UPDATED AND PRIVACY
db.query("create table " + tableName + " (listInfoId int NOT NULL AUTO_INCREMENT, name char(50), 
  mediaType char(7), description char(200), primary key (listInfoId));")
puts "INSERT INTO " + tableName.to_s + " VALUES ('Want to Watch', 'series', 'N/A');"
#db.query("insert into " + tableName.to_s + " values ('Want to Watch', 'series', 'N/A');")

# automatically public
# top 5 by media
# have watched by media
# wtow by media