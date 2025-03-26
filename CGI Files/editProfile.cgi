#!/usr/bin/ruby
require 'mysql2'
require 'cgi'
require 'cgi/session'
require 'stringio'
require 'open-uri'

# Enable debugging
$stdout.sync = true
$stderr.reopen $stdout

print "Content-type: text/html\r\n\r\n"

# Initialize CGI

def url_exists?(url)
      begin
        URI.open(url)
        true
      rescue OpenURI::HTTPError, SocketError
        false
      end
    end

uploadLocation = "/NFSHome/Televised/public_html/ProfileImages/"
cgi = CGI.new("html5")
session = CGI::Session.new(cgi)
username = session['username']
fromfile = cgi.params['fileName'].first
originalName = cgi.params['fileName'].first.instance_variable_get("@original_filename")
if (fromfile != "")
  fileType = originalName.split(".")
  lastDot = fileType.size - 1
    if (originalName != "" && (fileType[lastDot] == "jpg" || fileType[lastDot] == "png" || fileType[lastDot] == "jpeg"))
      tofile = uploadLocation + username + ".jpg" 
  
    begin 
      File.open(tofile.untaint, 'w') { |file| file << fromfile.read}
    rescue => e
    end
  end
end
=begin
else
  uploadedProfile = "https://cs.transy.edu/Televised/ProfileImages/" + username + ".jpg"
  valid = url_exists?(uploadedProfile)
  if !valid
    fromfile = "/NFSHome/Televised/public_html/ProfileImages/default.jpg"
    tofile = uploadLocation + username + ".jpg"
    begin 
      File.open(tofile.untaint, 'w') { |file| file << fromfile.read}
    rescue => e
      puts e.message
    end
  end
end
=end

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
print "<meta http-equiv='refresh' content='10; url=http://www.cs.transy.edu/Televised/Profile.cgi'>\n"
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