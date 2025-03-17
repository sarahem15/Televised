#!/usr/bin/ruby
require 'mysql2'
require 'cgi'
require 'cgi/session'

# Enable debugging
$stdout.sync = true
$stderr.reopen $stdout
# Print HTTP header
print "Content-type: text/html\r\n\r\n"

# Initialize CGI
cgi = CGI.new
session = CGI::Session.new(cgi)

# Retrieve form parameters
unameCreateInput = cgi['unameCreateInput']
passCreateInput = cgi['passCreateInput']

unameSignInInput = cgi['unameSignInInput']
passSignInInput = cgi['passSignInInput']

attempting = cgi['attempting']
fromCreate = cgi['fromCreate']

good = true

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

# Are we trying to create a new user, if so, need to check user name in use
if fromCreate == "true" 
  puts '<script>console.log("Checking for good username")</script>'
  puts "<script>"
  puts 'goodName = localStorage.getItem("FalseFlag");'
  puts 'console.log(goodName)'
  puts '</script>'

  db = Mysql2::Client.new(
        host: '10.20.3.4', 
        username: 'seniorproject25', 
        password: 'TV_Group123!', 
        database: 'televised_w25'
        )
  
  users = db.query("SELECT username from account;")
  
  good = true
  users.each do |user|
    puts '<script>console.log("' + user['username'] + '");</script>'
    if user['username'] == unameCreateInput 
      good = false
    end
  end

  if good 
    puts '<script>console.log("User made a good name, inserting")</script>'
    puts "<script>"
    puts 'localStorage.setItem("FalseFlag", "false");'
    puts 'localStorage.setItem("userSignedIn", "true");'
    puts 'localStorage.setItem("username", "' + unameCreateInput + '");'
    puts '</script>'
    
    db.query("INSERT INTO account (username, password, displayName) VALUES ('" + cgi['unameCreateInput'] + "','" + cgi['passCreateInput'] + "','" + cgi['unameCreateInput'] + "');")
    session['username'] = unameCreateInput
    session.close
    print cgi.header(
    'cookie' => CGI::Cookie.new('name' => 'CGISESSID', 'value' => session.session_id, 'httponly' => true, 'secure' => true)
    )
  else
    puts '<script>console.log("User made bad name, let them know and retry")</script>'
    puts "<script>"
    puts 'alert("Username already in use.   Bad monkey, Bobo!");'
    puts 'localStorage.setItem("FalseFlag", "true");'
    puts 'localStorage.setItem("userSignedIn", "false");'
#    puts 'location.reload(true)'
    puts '</script>'
  end 
else 
  # not coming from creation
  puts '<script>console.log("Its life but not as we know it")</script>'
  puts 'localStorage.setItem("FalseFlag", "false");'
end


if attempting == "true" 
  puts '<script>console.log("Attempting a login....");</script>'
       
  db = Mysql2::Client.new(
        host: '10.20.3.4', 
        username: 'seniorproject25', 
        password: 'TV_Group123!', 
        database: 'televised_w25'
        )
  
  users = db.query("SELECT username,password from account;")
       
  good = false
  users.each do |user|
    if user['username'] == unameSignInInput and user['password'] == passSignInInput 
      good = true
      break
    end
  end
  
  if good
    puts "<script>"
    puts 'console.log("Login matched!")' 
    puts 'localStorage.setItem("FalseFlag", "false");'
    puts 'localStorage.setItem("userSignedIn", "true");'
    puts 'localStorage.setItem("username", "' + unameSignInInput + '");'
    #puts 'window.attachLoggedInEvents();'
    puts '</script>'
    session['username'] = unameSignInInput
    session.close
    print cgi.header(
    'cookie' => CGI::Cookie.new('name' => 'CGISESSID', 'value' => session.session_id, 'httponly' => true, 'secure' => true)
    )
  else
    puts "<script>"
    puts 'console.log("Login failed!")' 
    puts 'alert("Either the username or password is invalid.");'
    puts 'localStorage.setItem("FalseFlag", "false");'
    puts 'localStorage.setItem("userSignedIn", "false");'
    puts 'localStorage.setItem("username", "' + unameSignInInput + '");'
    puts '</script>'
  end
end


puts '  <script>console.log("OK")</script>'
puts '  <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>'
puts '  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>'
puts '  <script src="Televised.js"></script>'

=begin

# Debugging: Print received parameters

puts "<h3>Received Parameters:</h3>"
puts "<p>Username:" + cgi['unameCreateInput'] + "</p>"
puts "<p>Password:"f + cgi['passCreateInput'] + "</p>"

# Connect to MySQL and insert data
#begin
  db = Mysql2::Client.new(
    host: '10.20.3.4', 
    username: 'seniorproject25', 
    password: 'TV_Group123!', 
    database: 'televised_w25'
  )

db.query("INSERT INTO account (username, password, replies) VALUES ('" + cgi['unameCreateInput'] + "','" + cgi['passCreateInput'] + "', '1');")
=end
# automatically public = 1
# top 5 by media
# have watched by media
# wtow by media

puts "</body>"
puts "</html>"