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
rateId = cgi['ratingId']
review = cgi['review']

alreadyReviewedSeries = cgi['alreadyReviewedSeries']
alreadyReviewedSeason = cgi['alreadyReviewedSeason']
alreadyReviewedEp = cgi['alreadyReviewedEp']
alreadyReplied = cgi['alreadyReplied']
puts alreadyReplied

reply = cgi['reply']
replyId = cgi['replyId']
reviewId = cgi['reviewId']
fromReviewIndiv = cgi['fromReviewIndiv']
type = cgi['type']

fromIndivEp = cgi['fromIndivEp']
epNum = cgi['epNum']
likedList = cgi['likedList']
otherList = cgi['otherList']
userWhoLiked = cgi['likeUser']
listId = cgi['listId']
listCreator = cgi['listCreator']
profileLikedList = cgi['profileLikedList']


db = Mysql2::Client.new(
    host: '10.20.3.4', 
    username: 'seniorproject25', 
    password: 'TV_Group123!', 
    database: 'televised_w25'
  )


imageName = db.query("SELECT imageName, showName FROM series WHERE showId = '" + seriesId + "';")
epName = db.query("SELECT epName from episode WHERE epId = '" + epId + "';")
=begin
puts "0: " + epId.to_s
puts "1: " + epName.first['epName']
puts "2: " + imageName.first['showName']
puts "3: " + seriesId
puts "4: " + epNum.to_s
puts "5: " + seasonNumber
=end
# Start HTML output
puts "<!DOCTYPE html>"
puts "<html lang='en'>"
puts "<head>"
puts "<meta charset='UTF-8'>"
puts "<title>Watched</title>"
puts "<link href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css' rel='stylesheet'>"
if fromIndivEp == 'TRUE'
    print "<meta http-equiv='refresh' content='0; url=http://www.cs.transy.edu/Televised/indivEp.cgi?ep_name=" + epName.first['epName'].to_s + "&show_name=" + imageName.first['showName'] + "&seriesID=" + seriesId + "&ep_num=" + epNum + "&seasonNumber=" + seasonNumber + "'>\n"
elsif likedList == "TRUE" && profileLikedList == ""
    print "<meta http-equiv='refresh' content='0; url=http://www.cs.transy.edu/Televised/Lists.cgi'>\n"
elsif otherList == "TRUE"
    print "<meta http-equiv='refresh' content='0; url=http://www.cs.transy.edu/Televised/otherLists.cgi?seriesID=" + seriesId + "seasonNumber=" + seasonNumber + "&seasonId=" + seasonId + "&epId=" + epId + "'>\n"
elsif profileLikedList != ""
    print "<meta http-equiv='refresh' content='0; url=http://www.cs.transy.edu/Televised/Likes_Lists.cgi'>\n"
elsif fromReviewIndiv == 'TRUE'
    if type == 'SEASON'
        print "<meta http-equiv='refresh' content='0; url=http://www.cs.transy.edu/Televised/reviewIndiv.cgi?reviewId=" + reviewId.to_s + "&contentType=SEASON'>\n"
    elsif type == 'EP'
        print "<meta http-equiv='refresh' content='0; url=http://www.cs.transy.edu/Televised/reviewIndiv.cgi?reviewId=" + reviewId.to_s + "&contentType=EP'>\n"
    else
        print "<meta http-equiv='refresh' content='0; url=http://www.cs.transy.edu/Televised/reviewIndiv.cgi?reviewId=" + reviewId.to_s + "'>\n"
    end
else
    print "<meta http-equiv='refresh' content='0; url=http://www.cs.transy.edu/Televised/series.cgi?clicked_image=" + imageName.first['imageName'].to_s + "&seasonNumber=" + seasonNumber + "'>\n"
end
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
        db.query('DELETE FROM seriesRating WHERE username = "' + username.to_s + '" AND seriesId = "' + seriesId.to_s + '";')
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
        begin 
            db.query("DELETE FROM wantToWatchSeries WHERE username = '" + username.to_s + "' AND seriesId = '" + seriesId.to_s + "';")
        rescue => e
        end
        (0...episodes.size).each do |i|
            alreadyWatchedEp = db.query("SELECT * FROM haveWatchedEpisode WHERE epId = '" + episodes[i]['epId'].to_s + "' AND username = '" + username.to_s + "';")
            if (alreadyWatchedEp.to_a.to_s == "[]")
                db.query('INSERT INTO haveWatchedEpisode VALUES ("' + username.to_s + '", "' + episodes[i]['epId'].to_s + '");')
            end
            begin 
                db.query("DELETE FROM wantToWatchEpisode WHERE username = '" + username.to_s + "' AND epId = '" + episodes[i]['epId'].to_s + "';")
            rescue => e
            end
        end
        (0...seasons.size).each do |i|
            alreadyWatchedSeason = db.query("SELECT * FROM haveWatchedSeason WHERE seasonId = '" + seasons[i]['seasonId'].to_s + "' AND username = '" + username.to_s + "';")
            if (alreadyWatchedSeason.to_a.to_s == "[]")
                db.query('INSERT INTO haveWatchedSeason VALUES ("' + username.to_s + '", "' + seasons[i]['seasonId'].to_s + '");')
            end
            begin 
                db.query("DELETE FROM wantToWatchSeason WHERE username = '" + username.to_s + "' AND seasonId = '" + seasons[i]['seasonId'].to_s + "';")
            rescue => e
            end
        end
    end
elsif (watchedButton == "TRUE" && seasonId != "")
    alreadyWatched = db.query("SELECT * FROM haveWatchedSeason WHERE seasonId = '" + seasonId.to_s + "' AND username = '" + username.to_s + "';")
    episodes = db.query("SELECT episode.epId FROM episode JOIN season ON episode.seasonId = season.seasonId WHERE season.seasonId = '" + seasonId.to_s + "';")
    episodes = episodes.to_a
    if (alreadyWatched.to_a.to_s != "[]")
        db.query("DELETE FROM haveWatchedSeason WHERE username = '" + username.to_s + "' AND seasonId = '" + seasonId.to_s + "';")
        (0...episodes.size).each do |i|
            begin
                db.query('DELETE FROM haveWatchedEpisode WHERE username = "' + username.to_s + '" AND epId = "' + episodes[i]['epId'].to_s + '";')
            rescue => e
                puts e.message
            end
        end
    else    
        db.query('INSERT INTO haveWatchedSeason VALUES ("' + username.to_s + '", "' + seasonId.to_s + '");')
        begin 
            db.query("DELETE FROM wantToWatchSeason WHERE username = '" + username.to_s + "' AND seasonId = '" + seasonId.to_s + "';")
        rescue => e
        end
        (0...episodes.size).each do |i|
            alreadyWatchedEp = db.query("SELECT * FROM haveWatchedEpisode WHERE epId = '" + episodes[i]['epId'].to_s + "' AND username = '" + username.to_s + "';")
            if (alreadyWatchedEp.to_a.to_s == "[]")
                db.query('INSERT INTO haveWatchedEpisode VALUES ("' + username.to_s + '", "' + episodes[i]['epId'].to_s + '");')
            end
            begin 
                db.query("DELETE FROM wantToWatchEpisode WHERE username = '" + username.to_s + "' AND epId = '" + episodes[i]['epId'].to_s + "';")
            rescue => e
            end
        end
    end
elsif (watchedButton == "TRUE" && epId != "")
    alreadyWatched = db.query("SELECT * FROM haveWatchedEpisode WHERE epId = '" + epId.to_s + "' AND username = '" + username.to_s + "';")
    if (alreadyWatched.to_a.to_s != "[]")
        db.query("DELETE FROM haveWatchedEpisode WHERE username = '" + username.to_s + "' AND epId = '" + epId.to_s + "';")
    else
        db.query('INSERT INTO haveWatchedEpisode VALUES ("' + username.to_s + '", "' + epId.to_s + '");')
        begin 
            db.query("DELETE FROM wantToWatchEpisode WHERE username = '" + username.to_s + "' AND epId = '" + epId.to_s + "';")
        rescue => e
        end
        #db.query('INSERT INTO haveWatchedEpisode VALUES ("' + username.to_s + '", "' + episodes)
    end
end
#puts '<br>'
#puts 'add to want to watch: ' + wantToWatch 
if (wantToWatch == "TRUE" && epId == "" && seasonId == "")
    begin
        db.query('INSERT INTO wantToWatchSeries VALUES ("' + username.to_s + '", "' + seriesId.to_s + '");')
    rescue => e
        db.query('DELETE FROM wantToWatchSeries WHERE username = "' + username.to_s + '" AND seriesId = "' + seriesId.to_s + '";')
    end
    begin 
        db.query("DELETE FROM haveWatchedSeries WHERE username = '" + username.to_s + "' AND seriesId = '" + seriesId.to_s + "';")
    rescue => e
    end
elsif (wantToWatch == "TRUE" && seasonId != "")
    begin
        db.query('INSERT INTO wantToWatchSeason VALUES ("' + username.to_s + '", "' + seasonId.to_s + '");')
    rescue => e
        db.query('DELETE FROM wantToWatchSeason WHERE username = "' + username.to_s + '" AND seasonId = "' + seasonId.to_s + '";')
    end
    begin 
        db.query("DELETE FROM haveWatchedSeason WHERE username = '" + username.to_s + "' AND seasonId = '" + seasonId.to_s + "';")
    rescue => e
    end
elsif (wantToWatch == "TRUE" && epId != "")
    begin
        db.query('INSERT INTO wantToWatchEpisode VALUES ("' + username.to_s + '", "' + epId.to_s + '");')
    rescue => e
        db.query('DELETE FROM wantToWatchEpisode WHERE username = "' + username.to_s + '" AND epId = "' + epId.to_s + '";')
    end
    begin 
        db.query("DELETE FROM haveWatchedEpisode WHERE username = '" + username.to_s + "' AND epId = '" + epId.to_s + "';")
    rescue => e
    end
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

# ADD EDITS AND DELETES
if review != ""
    if seriesRating != ""
        if rateId != ""
            date = year + "-" + month + "-" + day
            #db.query("INSERT INTO seriesReview VALUES (NULL, '" + reviewText.gsub("'", "\\\\'") + "', '" + username.to_s + "', '" + seriesId.to_s + "', '" + rateId.to_s + "', '" +  date + "');")
            if alreadyReviewedSeries == 'TRUE'
                db.query("UPDATE seriesReview SET review = '" + reviewText.gsub("'", "\\\\'") + "', date = '" + date + "' WHERE ratingId = '" + rateId.to_s + "' AND username = '" + username.to_s + "';")
            else
               db.query("INSERT INTO seriesReview VALUES (NULL, '" + reviewText.gsub("'", "\\\\'") + "', '" + username.to_s + "', '" + seriesId.to_s + "', '" + rateId.to_s + "', '" +  date + "');")
            end 
        else
            date = year + "-" + month + "-" + day
            db.query("INSERT INTO seriesRating (rating, username, seriesId) VALUES ('" + seriesRating.to_s + "', '" + username.to_s + "', '" + seriesId.to_s + "');")
            rateId = db.query("SELECT id from seriesRating WHERE username = '" + username.to_s + "' AND seriesId = '" + seriesId.to_s + "';")
            rateId = rateId.first['id'].to_s
            db.query("INSERT INTO seriesReview VALUES (NULL, '" + reviewText.gsub("'", "\\\\'") + "', '" + username.to_s + "', '" + seriesId.to_s + "', '" + rateId.to_s + "', '" +  date + "');")
        end
        begin
            db.query("INSERT INTO haveWatchedSeries VALUES ('" + username.to_s + "', '" + seriesId.to_s + "');")
        rescue => e
        end
    end
    if seasonRating != ""
        if rateId != ""
            date = year + "-" + month + "-" + day
            #db.query("INSERT INTO seasonReview VALUES (NULL, '" + reviewText.gsub("'", "\\\\'") + "', '" + username.to_s + "', '" + seasonId.to_s + "', '" + rateId.to_s + "', '" +  date + "');")
            if alreadyReviewedSeason == 'TRUE'
                db.query("UPDATE seasonReview SET review = '" + reviewText.gsub("'", "\\\\'") + "', date = '" + date + "' WHERE ratingId = '" + rateId.to_s + "' AND username = '" + username.to_s + "';")
                #puts "updated"
            else
               db.query("INSERT INTO seasonReview VALUES (NULL, '" + reviewText.gsub("'", "\\\\'") + "', '" + username.to_s + "', '" + seasonId.to_s + "', '" + rateId.to_s + "', '" +  date + "');")
            end
        else
            date = year + "-" + month + "-" + day
            db.query("INSERT INTO seasonRating (rating, username, seasonId) VALUES ('" + seasonRating.to_s + "', '" + username.to_s + "', '" + seasonId.to_s + "');")
            rateId = db.query("SELECT id from seasonRating WHERE username = '" + username.to_s + "' AND seasonId = '" + seasonId.to_s + "';")
            rateId = rateId.first['id'].to_s
            db.query("INSERT INTO seasonReview VALUES (NULL, '" + reviewText.gsub("'", "\\\\'") + "', '" + username.to_s + "', '" + seasonId.to_s + "', '" + rateId.to_s + "', '" +  date + "');")
        end
         begin
            db.query("INSERT INTO haveWatchedSeason VALUES ('" + username.to_s + "', '" + seasonId.to_s + "');")
        rescue => e
        end
    end

    if epRating != ""
        if rateId != ""
            date = year + "-" + month + "-" + day
            #db.query("INSERT INTO episodeReview VALUES (NULL, '" + reviewText.gsub("'", "\\\\'") + "', '" + username.to_s + "', '" + epId.to_s + "', '" + rateId.to_s + "', '" +  date + "');")
            if alreadyReviewedEp == 'TRUE'
                db.query("UPDATE episodeReview SET review = '" + reviewText.gsub("'", "\\\\'") + "', date = '" + date + "' WHERE ratingId = '" + rateId.to_s + "' AND username = '" + username.to_s + "';")
                #puts "updated"
            else
               db.query("INSERT INTO episodeReview VALUES (NULL, '" + reviewText.gsub("'", "\\\\'") + "', '" + username.to_s + "', '" + epId.to_s + "', '" + rateId.to_s + "', '" +  date + "');")
            end
        else
            date = year + "-" + month + "-" + day
            db.query("INSERT INTO episodeRating (rating, username, epId) VALUES ('" + epRating.to_s + "', '" + username.to_s + "', '" + epId.to_s + "');")
            rateId = db.query("SELECT id from episodeRating WHERE username = '" + username.to_s + "' AND epId = '" + epId.to_s + "';")
            rateId = rateId.first['id'].to_s
            db.query("INSERT INTO episodeReview VALUES (NULL, '" + reviewText.gsub("'", "\\\\'") + "', '" + username.to_s + "', '" + epId.to_s + "', '" + rateId.to_s + "', '" +  date + "');")
        end
         begin
            db.query("INSERT INTO haveWatchedEpisode VALUES ('" + username.to_s + "', '" + epId.to_s + "');")
        rescue => e
        end
    end

end

# REPLY STUFF STARTS HERE
if reply != ""
    date = year + "-" + month + "-" + day
    puts type
    if type == "SEASON"
        if alreadyReplied == 'TRUE'
            db.query("UPDATE seasonReply SET reply = '" + reply.gsub("'", "\\\\'") + "', date = '" + date + "' WHERE id = '" + replyId.to_s + "' AND username = '" + username.to_s + "';")
        else
            db.query("INSERT INTO seasonReply VALUES (NULL, '" + reply.gsub("'", "\\\\'") + "', '" + username + "', '" + seasonId.to_s + "', '" + reviewId.to_s + "', '" + date + "');")
        end
    elsif type == "EP"
        if alreadyReplied == 'TRUE'
            db.query("UPDATE episodeReply SET reply = '" + reply.gsub("'", "\\\\'") + "', date = '" + date + "' WHERE id = '" + replyId.to_s + "' AND username = '" + username.to_s + "';")
        else
            db.query("INSERT INTO episodeReply VALUES (NULL, '" + reply.gsub("'", "\\\\'") + "', '" + username + "', '" + epId.to_s + "', '" + reviewId.to_s + "', '" + date + "');")
        end
    else
        if alreadyReplied == 'TRUE'
            db.query("UPDATE seriesReply SET reply = '" + reply.gsub("'", "\\\\'") + "', date = '" + date + "' WHERE id = '" + replyId.to_s + "' AND username = '" + username.to_s + "';")
        else
            db.query("INSERT INTO seriesReply VALUES (NULL, '" + reply.gsub("'", "\\\\'") + "', '" + username + "', '" + seriesId.to_s + "', '" + reviewId.to_s + "', '" + date + "');")
        end
    end
end

if (likedList == "TRUE") || (otherList == "TRUE")
    alreadyLiked = db.query("SELECT * FROM likedList WHERE userWhoLiked = '" + username.to_s + "' AND listId = '" + listId + "';")
    if alreadyLiked.to_a == []
        db.query("INSERT INTO likedList VALUES ('" + userWhoLiked + "', '" + listCreator + "', '" + listId + "');")
    else
        db.query("DELETE FROM likedList WHERE userWhoLiked = '" + userWhoLiked + "' AND userWhoCreated = '" + listCreator + "' AND listId = '" + listId + "';")
    end
end

puts '</body>'
puts '</html>'

session.close