#!/usr/bin/ruby
$stdout.sync = true
$stderr.reopen $stdout

puts "Content-type: text/html\n\n"
require 'mysql2'
require 'cgi'
require 'cgi/session'

cgi = CGI.new
session = CGI::Session.new(cgi)
username = session['username']

seriesId = cgi['seriesID']
epId = cgi['epID']
watchedButton = cgi['watchedButton']
wantToWatch = cgi['wantToWatch']
seasonNumber = cgi['seasonNumber']
seasonId = cgi['seasonId']

seriesRating = cgi['seriesRating']
seasonRating = cgi['seasonRating']
epRating = cgi['epRating']
rated = cgi['rated']

db = Mysql2::Client.new(
    host: '10.20.3.4', 
    username: 'seniorproject25', 
    password: 'TV_Group123!', 
    database: 'televised_w25'
  )


imageName = db.query("SELECT imageName FROM series WHERE showId = '" + seriesId + "';")

# Start HTML output
puts "<!DOCTYPE html>"
puts "<html lang='en'>"
puts "<head>"
puts "<meta charset='UTF-8'>"
puts "<title>Watched</title>"
puts "<link href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css' rel='stylesheet'>"
print "<meta http-equiv='refresh' content='10; url=http://www.cs.transy.edu/Televised/series.cgi?clicked_image=" + imageName.first['imageName'].to_s + "&seasonNumber=" + seasonNumber + "'>\n"
puts "</head>"
puts "<body>"
puts "<div class='container mt-5'>"

# Debugging: Print received parameters
=begin
puts "<h3>Received Parameters:</h3>"
    puts "<p>Series Id: " + cgi['seriesID'] + "</p>"
if (epId != "")
    puts "<p>Episode Id: " + cgi['epID'] + "</p>"
end
puts '<br>'
puts 'add to watched list: ' + watchedButton
=end
if (watchedButton == "TRUE" && epId == "" && seasonId == "")
    db.query('INSERT INTO haveWatchedSeries VALUES ("' + username.to_s + '", "' + seriesId.to_s + '");')
elsif (watchedButton == "TRUE" && seasonId != "")
    db.query('INSERT INTO haveWatchedSeason VALUES ("' + username.to_s + '", "' + seasonId.to_s + '");')
elsif (watchedButton == "TRUE" && epId != "")
    db.query('INSERT INTO haveWatchedEpisode VALUES ("' + username.to_s + '", "' + epId.to_s + '");')
end
#puts '<br>'
#puts 'add to want to watch: ' + wantToWatch 
if (wantToWatch == "TRUE" && epId == "" && seasonId == "")
    db.query('INSERT INTO wantToWatchSeries VALUES ("' + username.to_s + '", "' + seriesId.to_s + '");')
elsif (wantToWatch == "TRUE" && seasonId != "")
    db.query('INSERT INTO wantToWatchSeason VALUES ("' + username.to_s + '", "' + seasonId.to_s + '");')
elsif (wantToWatch == "TRUE" && epId != "")
    db.query('INSERT INTO wantToWatchEpisode VALUES ("' + username.to_s + '", "' + epId.to_s + '");')
    #puts '<br>'
    #puts 'ADDED TO WANT TO WATCH LIST'
end

# CHECK FOR PREV RATING AND DELETE BEFORE INSERT
puts seasonRating.to_s
puts username
puts seriesId.to_s
if rated == "TRUE" && seasonRating == "" && epRating == ""
    db.query("INSERT INTO seriesRating (rating, username, seriesId) VALUES ('" + seriesRating.to_s + "', '" + username.to_s + "', '" + seriesId.to_s + "');")
elsif rated == "TRUE" && seriesRating == "" && epRating == ""
    db.query("INSERT INTO seasonRating (rating, username, seasonId) VALUES ('" + seasonRating.to_s + "', '" + username.to_s + "', '" + seasonId.to_s + "');")
elsif rated == "TRUE" && seriesRating == "" && seasonRating == ""
    db.query("INSERT INTO episodeRating (rating, username, epId) VALUES ('" + epRating.to_s + "', '" + username.to_s + "', '" + epId.to_s + "');")
end

=begin
puts '<br>'
puts 'add to existing list: ' + addToExisting 
puts '<br>'
puts 'add to new list: ' + addToNew 
puts '<br>'
puts 'view on other lists: ' + viewOnOthers 
puts '<br>'
puts 'userName: ' + username.to_s
=end

puts '</body>'
puts '</html>'

session.close