#!/usr/bin/ruby
require 'mysql2'
require 'cgi'
require 'cgi/session'
require 'stringio'

# Enable debugging
$stdout.sync = true
$stderr.reopen $stdout

print "Content-type: text/html\r\n\r\n"

# Initialize CGI

uploadLocation = "/NFSHome/Televised/public_html/ProfileImages/"
cgi = CGI.new("html5")
session = CGI::Session.new(cgi)
username = session['username']

fromfile = cgi.params['fileName'].first
originalName = cgi.params['fileName'].first.instance_variable_get("@original_filename")
fileType = originalName.split(".")
lastDot = fileType.size - 1
if (originalName != "" && (fileType[lastDot] == "jpg" || fileType[lastDot] == "png"))
  tofile = uploadLocation + username + ".jpg" 
  File.open(tofile.untaint, 'w') { |file| file << fromfile.read}
end


# Retrieve form parameters
displayName = cgi['displayName']
bio = cgi['bio']
pronouns = cgi['pronouns']
if cgi['replies'] == "Public"
  replies = 1
else
  replies = 0
end


# Print HTTP header

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
#puts "<div class='container mt-5'>"
#puts "Uploaded: " + originalName
# Debugging: Print received parameters
=begin
puts "<h3>Received Parameters:</h3>"
puts "<p>Username:" + username + "</p>"
puts "<p>Display name:" + cgi['displayName'] + "</p>"
puts "<p>Bio:" + cgi['bio'] + "</p>"
puts "<p>Pronouns:" + cgi['pronouns'] + "</p>"
puts "<p>Replies:" + cgi['replies'] + "</p>"
=end

# Connect to MySQL and insert data
#begin
  db = Mysql2::Client.new(
    host: '10.20.3.4', 
    username: 'seniorproject25', 
    password: 'TV_Group123!', 
    database: 'televised_w25'
  )

#puts "update account set displayName = '" + displayName.to_s + "', bio = '" + bio.to_s + "', pronouns = '" + pronouns.to_s + "', replies = '" +  replies.to_s + "' where username = '" + username.to_s + "';"
db.query("update account set displayName = '" + displayName.to_s + "', bio = '" + bio.to_s + "', pronouns = '" + pronouns.to_s + "', replies = '" +  replies.to_s + "' where username = '" + username.to_s + "';")
puts "</body>"
puts "</html>"

session.close