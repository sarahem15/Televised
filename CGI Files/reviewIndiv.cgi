#!/usr/bin/ruby
$stdout.sync = true
$stderr.reopen $stdout

puts "Content-type: text/html\n\n"
require 'mysql2'
require 'cgi'
require 'cgi/session'
#username = "try@try"
cgi = CGI.new
session = CGI::Session.new(cgi)
username = session['username']
time = Time.new

reviewId = cgi['reviewId']
type = cgi['contentType']

db = Mysql2::Client.new(
    host: '10.20.3.4', 
    username: 'seniorproject25', 
    password: 'TV_Group123!', 
    database: 'televised_w25'
  )

epNum = 0
if type == 'SEASON'
  reviewContent = db.query("SELECT * FROM seasonReview WHERE id ='" + reviewId + "';")
  seriesImage = db.query("SELECT showId, imageName, showName, series.year, season.seasonNum FROM series 
    JOIN season ON season.seriesId = series.showID
    JOIN seasonReview ON season.seasonId = seasonReview.seasonId 
    WHERE seasonReview.id= '" + reviewId + "';")
  reviewRating = db.query("SELECT rating FROM seasonRating JOIN seasonReview ON seasonRating.id = seasonReview.ratingId WHERE seasonReview.id = '" + reviewId + "';")
elsif type == 'EP'
  reviewContent = db.query("SELECT * FROM episodeReview WHERE id ='" + reviewId + "';")
  seriesImage = db.query("SELECT showId, imageName, showName, series.year, season.seasonNum, episode.epName FROM series 
    JOIN season ON season.seriesId = series.showID
    JOIN episode ON episode.seasonId = season.seasonId
    JOIN episodeReview ON episode.epId = episodeReview.epId 
    WHERE episodeReview.id= '" + reviewId + "';")
  reviewRating = db.query("SELECT rating FROM episodeRating JOIN episodeReview ON episodeRating.id = episodeReview.ratingId WHERE episodeReview.id = '" + reviewId + "';")
else
  reviewContent = db.query("SELECT * FROM seriesReview WHERE id ='" + reviewId + "';")
  seriesImage = db.query("SELECT showId, imageName, showName, year FROM series JOIN seriesReview ON series.showId = seriesReview.seriesId WHERE seriesReview.id= '" + reviewId + "';")
  reviewRating = db.query("SELECT rating FROM seriesRating JOIN seriesReview ON seriesRating.id = seriesReview.ratingId WHERE seriesReview.id = '" + reviewId + "';")
end
alreadyLiked = false
reviewId = cgi['reviewId']
reviewCreator = cgi['reviewCreator']
likedReview = cgi['likedReview']

if likedReview == "TRUE"
    begin
        db.query("INSERT INTO likedSeriesReview VALUES ('" + username.to_s + "', '" + reviewCreator + "', '" + reviewId + "');")
    rescue => e
        db.query("DELETE FROM likedSeriesReview WHERE userWhoLiked = '" + username.to_s + "' AND reviewId = '" + reviewId + "';")
    end
end

privacy = db.query("SELECT * FROM account WHERE username = '" + reviewContent.first['username'] + "';")
puts'<!DOCTYPE html>'
puts'<html lang="en">'

puts'<head>'
  puts'<meta charset="UTF-8">'
  puts'<meta name="viewport" content="width=device-width, initial-scale=1.0">'
  puts'<title>Televised</title>'
  puts'<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">'
  puts'<link rel="stylesheet" href="Televised.css">'
  puts '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">'
  puts '<script src="fetch-data-loader.js"></script>'
puts'</head>'

puts'<body id="reviewIndiv">'
  puts'<nav id="changingNav"></nav> <!-- This is where the navbar will be dynamically loaded -->'
  puts'<br>'
  puts '<br>'
puts '<div class="originalReview">'
  if type == "SEASON"
    puts '<form action="series.cgi" style="padding: 0; border-width: 0; background-color: transparent; width: 200px;">'
    puts '<input type="hidden" name="clicked_image" value="' + seriesImage.first['imageName'] + '" >'
      puts '<input type="hidden" name="seasonNumber" value="' + seriesImage.first['seasonNum'].to_s + '">'
      likes = db.query("SELECT * FROM likedSeasonReview WHERE reviewId = '" + reviewId + "';")
  elsif type == "EP"
    allEps = db.query("SELECT epName FROM episode JOIN season ON season.seasonId = episode.seasonId JOIN series ON series.showId = season.seriesId WHERE showName = '" + seriesImage.first['showName'] + "';")
          allEps = allEps.to_a
          (0...allEps.size).each do |j|
            if allEps[j]['epName'] == seriesImage.first['epName']
              epNum = j + 1
            end
          end 
    puts '<form action="indivEp.cgi" method="POST">'
      puts '<input type="hidden" name="ep_name" value="' + seriesImage.first['epName'] + '">'
      puts '<input type="hidden" name="show_name" value="' + seriesImage.first['showName'] + '">'
      puts '<input type="hidden" name="seriesId" value="' + seriesImage.first['showId'].to_s + '">'
      puts '<input type="hidden" name="ep_num" value="' + epNum.to_s + '">'
      puts '<input type="hidden" name="seasonNumber" value="' + seriesImage.first['seasonNum'].to_s + '">'
      likes = db.query("SELECT * FROM likedEpisodeReview WHERE reviewId = '" + reviewId + "';")
  else
    puts '<form action="series.cgi">'
    puts '<input type="hidden" name="clicked_image" value="' + seriesImage.first['imageName'] + '">'
      puts '<input type="hidden" name="seasonNumber" value="1">'
      likes = db.query("SELECT * FROM likedSeriesReview WHERE reviewId = '" + reviewId + "';")
  end
  puts "<input type='image' src=\"" + seriesImage.first['imageName'] + "\"alt=\"" + seriesImage.first['imageName'] + "\" style='height: 350px; width: 250px; object-fit: cover;'>" 
  puts '</form>'

	puts '<div class="content-R">'
	puts '<section class="UserDisplay">'
         puts '<img src="./ProfileImages/' + reviewContent.first['username'] + '.jpg" alt="">'
          puts '<a href="othersProfiles.cgi?username=' + reviewContent.first['username'] + '"><h3>' + reviewContent.first['username'] + '</h3></a>'
      puts '</section>'
      puts '<br>'
      puts '<section class="NameAndYear">'
      puts '<h3>' + seriesImage.first['showName'] + '</h3>'
      puts '<h3 style="color: #436eb1;">' + seriesImage.first['year'].to_s + '</h3>'
      puts '</section>'
	puts '<section class="Rating">'
        	(0...5).each do |i|
        		if (i < reviewRating.first['rating'].to_i)
          			puts '<i class="fa fa-star" style="color: white;"></i>'
          		else
          			puts '<i class="fa fa-star"></i>'
          		end
        	end
        puts '</section>'
       puts '<h3>' + reviewContent.first['review'] + '</h3>'

       #######LIKES#########
       likes = likes.to_a
       (0...likes.size).each do |i|
        if likes[i]['userWhoLiked'] == username.to_s
            alreadyLiked = true
          end
        end
       puts '<form class="LikeAndCount" action="reviewIndiv.cgi" method="post">'
       if alreadyLiked
        puts '<button class="LIKES" style="color: pink;">&#10084</button>'
      else
        puts '<button class="LIKES">&#10084</button>'
      end
      puts '<input type="hidden" name="likeSeriesReview" value="TRUE">'
        puts '<a href="whoHasLiked.cgi?reviewId=' + reviewContent.first['id'].to_s + '&type=EP">' + likes.size.to_s + '</a>'
        puts '<input type="hidden" name="clicked_image" value="' + seriesImage.first['imageName'].to_s + '">'
        puts '<input type="hidden" name="seasonNumber" value="' + seriesImage.first['seasonNum'].to_s + '">'
        puts '<input type="hidden" name="reviewId" value="' + reviewContent.first['id'].to_s + '">'
        puts '<input type="hidden" name="reviewCreator" value="' + reviewContent.first['username'].to_s + '">'
        puts '<input type="hidden" name="contentType" value="' + type + '">'
        puts '<input type="hidden" name="likedReview" value="TRUE">'
      puts '</form>'
       puts '<br>'
       puts '<i><h5 style="color: #436eb1">' + reviewContent.first['date'].to_s + '</h5></i>'
       puts '<br>'

	puts '</div>'
  # START DIV FOR TEXT BOX
  if privacy.first['replies'].to_i == 1
       puts '<div class="reply">'
       puts '<form action="threebuttons.cgi" method="POST">'
       puts '<h4>Type your reply here:</h4>'
       puts '<textarea id="reply" name="reply" class="form-control" rows="10"></textarea><br>'
       puts '<input type="hidden" name="seriesID" value="' + seriesImage.first['showId'].to_s + '">'

       if type == 'SEASON'
        puts '<input type="hidden" name="seasonId" value="' + reviewContent.first['seasonId'].to_s + '">'
      elsif type == 'EP'
        puts '<input type="hidden" name="epID" value="' + reviewContent.first['epId'].to_s + '">'
      end

       puts '<input type="hidden" name="reviewId" value="' + reviewId.to_s + '">'
       puts '<input type="hidden" name="username" value="' + username + '">'
       puts "<input type='hidden' name='year' value='" + time.year.to_s + "'>"
       puts "<input type='hidden' name='month' value='" + time.month.to_s + "'>"
       puts "<input type='hidden' name='day' value='" + time.day.to_s + "'>"
       puts "<input type='hidden' name='type' value='" + type + "'>"
       puts "<input type='hidden' name='fromReviewIndiv' value='TRUE'>"
       puts '<button id="saveReply" class="btn" style="background-color: #9daef6;" type="submit">Reply</button>'
      puts '</form>'
      puts '</div>'
end
puts '</div>'

puts '<br>'


puts '<hr style="margin-left: 50px; margin-right: 50px;">'
puts '<h2 style="margin-left: 80px;"> Replies </h2>'
puts '<hr style="margin-left: 80px; margin-right: 1150px;">'
puts '<br>'
if type == 'SEASON'
  replies = db.query("SELECT * FROM seasonReply WHERE reviewId ='" + reviewId + "';")
elsif type == 'EP'
  replies = db.query("SELECT * FROM episodeReply WHERE reviewId ='" + reviewId + "';")
else
  replies = db.query("SELECT * FROM seriesReply WHERE reviewId ='" + reviewId + "';")
end
#replies = db.query("SELECT * FROM seriesReply WHERE reviewId ='" + reviewId + "';")
replies = replies.to_a
(0...replies.size).each do |i|
puts '<div class="content-Reply">'
  puts '<section class="UserDisplay">'
         puts '<img src="./ProfileImages/' + replies[i]['username'] + '.jpg" alt="">'
          puts '<a href="othersProfiles.cgi?username=' + replies[i]['username'] + '">' + '<h3>' + replies[i]['username'] + '</h3></a>'
      puts '</section>'
      puts '<br>'

      if replies[i]['username'] == username
       puts '<div id="text-display">'
    puts '<p>' + replies[i]['reply'] + '</p>'
    puts '<button class="btn" style="background-color: #9daef6;" onclick="showEditForm()">Edit</button>'
  puts '</div>'

      puts ' <div id="edit-form" style="display:none;">'
    puts ' <form action="threebuttons.cgi" method="post" style="width: 50%">'
      puts ' <textarea name="reply" rows="5" cols="0">' + replies[i]['reply'] + '</textarea><br><br>'
      #puts ' <textarea name="text" rows="5" cols="0">' + type + '</textarea><br><br>'
      puts ' <input type="hidden" name="replyId" value="' + replies[i]['id'].to_s + '">'
      puts "<input type='hidden' name='fromReviewIndiv' value='TRUE'>"
      puts "<input type='hidden' name='alreadyReplied' value='TRUE'>"
      puts '<input type="hidden" name="seriesID" value="' + seriesImage.first['showId'].to_s + '">'

       if type == 'SEASON'
        puts '<input type="hidden" name="seasonId" value="' + reviewContent.first['seasonId'].to_s + '">'
      elsif type == 'EP'
        puts '<input type="hidden" name="epID" value="' + reviewContent.first['epId'].to_s + '">'
      end

       puts '<input type="hidden" name="reviewId" value="' + reviewId.to_s + '">'
       puts '<input type="hidden" name="username" value="' + username + '">'
       puts "<input type='hidden' name='year' value='" + time.year.to_s + "'>"
       puts "<input type='hidden' name='month' value='" + time.month.to_s + "'>"
       puts "<input type='hidden' name='day' value='" + time.day.to_s + "'>"
       puts "<input type='hidden' name='type' value='" + type + "'>"

      puts ' <button class="btn" style="background-color: #9daef6;" type="submit">Save</buttom>'
    puts ' </form>'
  puts ' </div>'
      else
        puts '<h3>' + replies[i]['reply'] + '</h3>'
      end

  puts '</div>'
  puts '<br>'
  puts '<hr style="margin-left: 80px; margin-right: 80px;">'
  puts '<br>'
end
  if replies.size == 0 && privacy.first['replies'].to_i == 1
    puts '<h5 style="text-align: center;"> Replies will show up here! </h5>'
  elsif privacy.first['replies'].to_i == 0
    puts '<h5 style="text-align: center;"> This user has disabled replies! </h5>'
  end
  puts '<br>'
puts '<!-- Scripts -->'
  puts '<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>'
  puts '<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>'
  puts '<script src="Televised.js"></script>'

puts "<script>"
puts "    function showEditForm() {"
puts "      document.getElementById('text-display').style.display = 'none';"
puts "      document.getElementById('edit-form').style.display = 'block';"
puts "    }"
puts "  </script>"

puts '</body>'

puts '</html>'