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

reviewText = cgi['reviewText']
year = cgi['year']
month = cgi['month']
day = cgi['day']
#rateId = cgi['ratingId']
review = cgi['review']



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
print "<meta http-equiv='refresh' content='0; url=http://www.cs.transy.edu/Televised/series.cgi?clicked_image=" + imageName.first['imageName'].to_s + "&seasonNumber=" + seasonNumber + "'>\n"
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
    alreadyWatched = db.query("SELECT * FROM haveWatchedSeries WHERE seriesId = '" + seriesId.to_s + "' AND username = '" + username.to_s + "';")
    episodes = db.query("SELECT episode.epId FROM episode JOIN season ON episode.seasonId = season.seasonId JOIN series ON season.seriesId = series.showId WHERE series.showId = '" + seriesId.to_s + "';")
    episodes = episodes.to_a
    seasons = db.query("SELECT season.seasonId FROM season JOIN series ON season.seriesId = series.showId WHERE series.showId = '" + seriesId.to_s + "';")
    seasons = seasons.to_a
    if (alreadyWatched.to_a.to_s != "[]")
        db.query("DELETE FROM haveWatchedSeries WHERE username = '" + username.to_s + "' AND seriesId = '" + seriesId.to_s + "';")
        (0...episodes.size).each do |i|
            begin
                db.query('DELETE FROM haveWatchedEpisode WHERE username = "' + username.to_s + '" AND epId = "' + episodes[i]['epId'].to_s + '";')
            rescue => e
                puts e.message
            end
        end
        (0...seasons.size).each do |i|
            begin
                db.query('DELETE FROM haveWatchedSeason WHERE username = "' + username.to_s + '" AND seasonId = "' + seasons[i]['seasonId'].to_s + '";')
            rescue => e
                puts e.message
            end
        end
    else
        db.query('INSERT INTO haveWatchedSeries VALUES ("' + username.to_s + '", "' + seriesId.to_s + '");') 
        (0...episodes.size).each do |i|
            alreadyWatchedEp = db.query("SELECT * FROM haveWatchedEpisode WHERE epId = '" + episodes[i]['epId'].to_s + "' AND username = '" + username.to_s + "';")
            if (alreadyWatchedEp.to_a.to_s == "[]")
                db.query('INSERT INTO haveWatchedEpisode VALUES ("' + username.to_s + '", "' + episodes[i]['epId'].to_s + '");')
            end
        end
        (0...seasons.size).each do |i|
            alreadyWatchedSeason = db.query("SELECT * FROM haveWatchedSeason WHERE seasonId = '" + seasons[i]['seasonId'].to_s + "' AND username = '" + username.to_s + "';")
            if (alreadyWatchedSeason.to_a.to_s == "[]")
                db.query('INSERT INTO haveWatchedSeason VALUES ("' + username.to_s + '", "' + seasons[i]['seasonId'].to_s + '");')
            end
        end
    end
elsif (watchedButton == "TRUE" && seasonId != "")
    alreadyWatched = db.query("SELECT * FROM haveWatchedSeason WHERE seasonId = '" + seasonId.to_s + "' AND username = '" + username.to_s + "';")
    if (alreadyWatched.to_a.to_s != "[]")
        db.query("DELETE FROM haveWatchedSeason WHERE username = '" + username.to_s + "' AND seasonId = '" + seasonId.to_s + "';")
    else    
        db.query('INSERT INTO haveWatchedSeason VALUES ("' + username.to_s + '", "' + seasonId.to_s + '");')
    end
elsif (watchedButton == "TRUE" && epId != "")
    alreadyWatched = db.query("SELECT * FROM haveWatchedEpisode WHERE epId = '" + epId.to_s + "' AND username = '" + username.to_s + "';")
    if (alreadyWatched.to_a.to_s != "[]")
        db.query("DELETE FROM haveWatchedEpisode WHERE username = '" + username.to_s + "' AND epId = '" + epId.to_s + "';")
    else
        db.query('INSERT INTO haveWatchedEpisode VALUES ("' + username.to_s + '", "' + epId.to_s + '");')
        #db.query('INSERT INTO haveWatchedEpisode VALUES ("' + username.to_s + '", "' + episodes)
    end
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
#puts seasonRating.to_s
#puts username
#puts seriesId.to_s
if rated == "TRUE" && seasonRating == "" && epRating == "" && review != "true"
   alreadyRatedSeries = db.query("SELECT * FROM seriesRating WHERE seriesId = '" + seriesId.to_s + "' AND username = '" + username.to_s + "';")
    if (alreadyRatedSeries.to_a.to_s != "[]")
        db.query("UPDATE seriesRating SET rating = " + seriesRating.to_s + " WHERE seriesId = '" + seriesId.to_s + "' AND username = '" + username.to_s + "';")
    else
        db.query("INSERT INTO seriesRating (rating, username, seriesId) VALUES ('" + seriesRating.to_s + "', '" + username.to_s + "', '" + seriesId.to_s + "');")
    end
    alreadyWatched = db.query("SELECT * FROM haveWatchedSeries WHERE seriesId = '" + seriesId.to_s + "' AND username = '" + username.to_s + "';")
    if (alreadyWatched.to_a.to_s == "[]")
        db.query('INSERT INTO haveWatchedSeries VALUES ("' + username.to_s + '", "' + seriesId.to_s + '");')
    end
elsif rated == "TRUE" && seriesRating == "" && epRating == "" && review != "true"
    alreadyRatedSeason = db.query("SELECT * FROM seasonRating WHERE seasonId = '" + seasonId.to_s + "' AND username = '" + username.to_s + "';")
    if (alreadyRatedSeason.to_a.to_s != "[]")
        db.query("UPDATE seasonRating SET rating = " + seasonRating.to_s + " WHERE seasonId = '" + seasonId.to_s + "' AND username = '" + username.to_s + "';")
    else
        db.query("INSERT INTO seasonRating (rating, username, seasonId) VALUES ('" + seasonRating.to_s + "', '" + username.to_s + "', '" + seasonId.to_s + "');")
    end
    alreadyWatched = db.query("SELECT * FROM haveWatchedSeason WHERE seasonId = '" + seasonId.to_s + "' AND username = '" + username.to_s + "';")
    if (alreadyWatched.to_a.to_s == "[]")   
        db.query('INSERT INTO haveWatchedSeason VALUES ("' + username.to_s + '", "' + seasonId.to_s + '");')
    end
elsif rated == "TRUE" && seriesRating == "" && seasonRating == "" && review != "true"
    alreadyRatedEp = db.query("SELECT * FROM episodeRating WHERE epId = '" + epId.to_s + "' AND username = '" + username.to_s + "';")
    if (alreadyRatedEp.to_a.to_s != "[]")
        db.query("UPDATE episodeRating SET rating = " + epRating.to_s + " WHERE epId = '" + epId.to_s + "' AND username = '" + username.to_s + "';")
    else
        db.query("INSERT INTO episodeRating (rating, username, epId) VALUES ('" + epRating.to_s + "', '" + username.to_s + "', '" + epId.to_s + "');")
    end
    alreadyWatched = db.query("SELECT * FROM haveWatchedEpisode WHERE epId = '" + epId.to_s + "' AND username = '" + username.to_s + "';")
    if (alreadyWatched.to_a.to_s == "[]")
        db.query('INSERT INTO haveWatchedEpisode VALUES ("' + username.to_s + '", "' + epId.to_s + '");')
    end
end
 if review != ""
    date = year + "-" + month + "-" + day
    #db.query("INSERT INTO seriesReview VALUES (NULL, '" + review + "', '" + username.to_s + "', '" + seriesId.to_s + "', '" + ratingId.to_s + "', '" +  date + "');")
    puts seriesId.to_s
    puts 'rating is' + seriesRating
    puts reviewText
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