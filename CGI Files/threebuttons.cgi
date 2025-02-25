#!/usr/bin/ruby
$stdout.sync = true
$stderr.reopen $stdout

puts "Content-type: text/html\n\n"
require 'mysql2'
require 'cgi'

cgi = CGI.new

seriesId = cgi['seriesID']
epId = cgi['epID']
watchedButton = cgi['watchedButton']
wantToWatch = cgi['wantToWatch']
addToExisting = cgi['addToExisting']
addToNew = cgi['addToNew']
viewOnOthers = cgi['viewOnOthers']
userName = cgi['displayName']

db = Mysql2::Client.new(
    host: '10.20.3.4', 
    username: 'seniorproject25', 
    password: 'TV_Group123!', 
    database: 'televised_w25'
  )

# Start HTML output
puts "<!DOCTYPE html>"
puts "<html lang='en'>"
puts "<head>"
puts "<meta charset='UTF-8'>"
puts "<title>Watched</title>"
puts "<link href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css' rel='stylesheet'>"
puts "</head>"
puts "<body>"
puts "<div class='container mt-5'>"

# Debugging: Print received parameters
puts "<h3>Received Parameters:</h3>"
    puts "<p>Series Id: " + cgi['seriesID'] + "</p>"
if (epId != "")
    puts "<p>Episode Id: " + cgi['epID'] + "</p>"
end
puts '<br>'
puts 'add to watched list: ' + watchedButton
if (watchedButton == "TRUE" && epId == "" && userName != "")
    #db.query('INSERT INTO haveWatchedSeries VALUES ("' + userName + '", "' + seriesId + '");')
    puts '<br>'
    puts 'ADDED TO WATCHED LIST'
end
puts '<br>'
puts 'add to want to watch: ' + wantToWatch 
puts '<br>'
puts 'add to existing list: ' + addToExisting 
puts '<br>'
puts 'add to new list: ' + addToNew 
puts '<br>'
puts 'view on other lists: ' + viewOnOthers 
puts '<br>'
puts 'userName: ' + userName

puts '</body>'
puts '</html>'