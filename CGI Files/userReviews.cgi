#!/usr/bin/ruby
$stdout.sync = true
$stderr.reopen $stdout

puts "Content-type: text/html\n\n"
require 'mysql2'
require 'cgi'
require 'cgi/session'

cgi = CGI.new
session = CGI::Session.new(cgi)
sessionUser = session['username'].to_s


db = Mysql2::Client.new(
    host: '10.20.3.4', 
    username: 'seniorproject25', 
    password: 'TV_Group123!', 
    database: 'televised_w25'
  )

username = cgi['username']
displayName = db.query("SELECT displayName FROM account WHERE username = '" + username.to_s + "';")
bio = db.query("SELECT bio FROM account WHERE username = '" + username.to_s + "';")
pronouns = db.query("SELECT pronouns FROM account WHERE username = '" + username.to_s + "';")

seriesTab = cgi['seriesTab']
if seriesTab == ""
  seriesTab = "SERIES"
end
contentType = ""
alreadyLiked = false
if cgi['likedReview'] == "TRUE"
  if seriesTab == "SERIES"
    begin
      db.query("INSERT INTO likedSeriesReview VALUES ('" + sessionUser + "', '" + username.to_s + "', '" +  cgi['reviewId'] + "');")
    rescue
      db.query("DELETE FROM likedSeriesReview WHERE userWhoLiked = '" + sessionUser + "' AND reviewId = '" +  cgi['reviewId'] + "';")
    end
  elsif seriesTab == "SEASON"
    begin
      db.query("INSERT INTO likedSeasonReview VALUES ('" + sessionUser + "', '" + username.to_s + "', '" +  cgi['reviewId'] + "');")
    rescue
      db.query("DELETE FROM likedSeasonReview WHERE userWhoLiked = '" + sessionUser + "' AND reviewId = '" +  cgi['reviewId'] + "';")
    end
  else
    begin
      db.query("INSERT INTO likedEpisodeReview VALUES ('" + sessionUser + "', '" + username.to_s + "', '" +  cgi['reviewId'] + "');")
    rescue
      db.query("DELETE FROM likedEpisodeReview WHERE userWhoLiked = '" + sessionUser + "' AND reviewId = '" +  cgi['reviewId'] + "';")
    end
  end
end

puts'<head>'
  puts'<meta charset="UTF-8">'
  puts'<meta name="viewport" content="width=device-width, initial-scale=1.0">'
  puts'<title>Televised</title>'
  puts'<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">'
  puts'<link rel="stylesheet" href="Televised.css">'
  puts '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">'
  puts '<script src="fetch-data-loader.js"></script>'
puts'</head>'
puts'<body id="userProfile">'
  puts'<nav id="changingNav"></nav> <!-- This is where the navbar will be dynamically loaded -->'
  puts'<br>'
  puts '<section class="ProfileInfo">'
  puts '<section class="UserDisplay">'
    puts '<img src="ProfileImages/' + username.to_s + '.jpg" alt="">'
    puts '<h3 id="DisplayName">' + displayName.first['displayName'].to_s + '</h3>'
  puts '</section>'
  puts '<h4>' + pronouns.first['pronouns'].to_s + '</h4>'
  puts '<h4>' + bio.first['bio'].to_s + '</h4>'
  puts '</section>'
  puts '<hr>'
     puts '<div class="profileHeader">'
      puts '<a href="othersProfiles.cgi?username=' + username + '">Profile</a>'
      puts '<a href="userLists.cgi?username=' + username + '">Lists</a>'
      puts '<a href="#!" class="active">Reviews</a>'
      puts '<a href="userRatings.cgi?username=' + username + '">Ratings</a>'
    puts '</div>'
  puts '<hr>'
  puts '<br>'

  puts '<div class="listProfileButtons">'
  puts '<div class="profileListHeader">'
      if seriesTab == "SERIES"
      puts '<a href="#"class="active">Series</a>'
      puts '<a href="userReviews.cgi?username=' + username + '&seriesTab=SEASON">Seasons</a>'
      puts '<a href="userReviews.cgi?username=' + username + '&seriesTab=EP">Episodes</a>'
      seriesReviews = db.query("SELECT * FROM seriesReview WHERE username = '" + username.to_s + "';")
  elsif seriesTab == "SEASON"
      puts '<a href="userReviews.cgi?username=' + username + '&seriesTab=SERIES">Series</a>'
      puts '<a href="#" class="active">Seasons</a>'
      puts '<a href="userReviews.cgi?username=' + username + '&seriesTab=EP">Episodes</a>'
      seriesReviews = db.query("SELECT * FROM seasonReview WHERE username = '" + username.to_s + "';")
  elsif seriesTab == "EP"
      puts '<a href="userReviews.cgi?username=' + username + '&seriesTab=SERIES">Series</a>'
      puts '<a href="userReviews.cgi?username=' + username + '&seriesTab=SEASON">Seasons</a>'
      puts '<a href="#" class="active">Episodes</a>'
      seriesReviews = db.query("SELECT * FROM episodeReview WHERE username = '" + username.to_s + "';")
  end

  seriesReviews = seriesReviews.to_a
    puts '</div>'
puts '</div>'
puts '<hr>'
puts '<br>'
(0...seriesReviews.size).each do |i|
  if seriesTab == "SERIES"
    seriesImage = db.query("SELECT imageName, showName, showId, year FROM series JOIN seriesReview ON series.showId = seriesReview.seriesId WHERE seriesReview.id= '" + seriesReviews[i]['id'].to_s + "';")
    reviewRating = db.query("SELECT rating FROM seriesRating JOIN seriesReview ON seriesRating.id = seriesReview.ratingId WHERE seriesReview.id = '" + seriesReviews[i]['id'].to_s + "';")
    likes = db.query("SELECT * FROM likedSeriesReview WHERE reviewId = '" + seriesReviews[i]['id'].to_s + "';")
  elsif seriesTab == "SEASON"
    seriesImage = db.query("SELECT imageName, showName, showId, series.year, season.seasonNum FROM series JOIN season ON season.seriesId = series.showId JOIN seasonReview ON seasonReview.seasonId = season.seasonId WHERE seasonReview.id = '" + seriesReviews[i]['id'].to_s + "';")
    reviewRating = db.query("SELECT rating FROM seasonRating JOIN seasonReview ON seasonRating.id = seasonReview.ratingId WHERE seasonReview.id = '" + seriesReviews[i]['id'].to_s + "';")
    contentType = "SEASON"
    likes = db.query("SELECT * FROM likedSeasonReview WHERE reviewId = '" + seriesReviews[i]['id'].to_s + "';")
  else
     seriesImage = db.query("SELECT imageName, showName, showId, series.year, season.seasonNum, episode.epName FROM series JOIN season ON season.seriesId = series.showId JOIN episode ON episode.seasonId = season.seasonId JOIN episodeReview ON episodeReview.epId = episode.epId WHERE episodeReview.id = '" + seriesReviews[i]['id'].to_s + "';")
     reviewRating = db.query("SELECT rating FROM episodeRating JOIN episodeReview ON episodeRating.id = episodeReview.ratingId WHERE episodeReview.id = '" + seriesReviews[i]['id'].to_s + "';") 
    contentType = "EP"
    likes = db.query("SELECT * FROM likedEpisodeReview WHERE reviewId = '" + seriesReviews[i]['id'].to_s + "';")
  end

epNum = 0
puts '<div class="originalReview">'
  if seriesTab != "EP"
    puts '<form action="series.cgi" method="POST">'
      puts '<input type="hidden" name="clicked_image" value="' + seriesImage.first['imageName'] + '">'
      puts '<input type="hidden" name="seasonNumber" value="1">'
  else
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
  end  
	puts "<input type='image' src=\"" + seriesImage.first['imageName'] + "\"alt=\"" + seriesImage.first['imageName'] + "\" style='width: 200px; height: 270px; object-fit: cover;'>" 
  puts '</form>'
	puts '<div class="content-R">'
      puts '<section class="NameAndYear">'
      puts '<a href="reviewIndiv.cgi?reviewId=' + seriesReviews[i]['id'].to_s + '&contentType=' + contentType + '">'
      puts '<h3>' + seriesImage.first['showName'] + '</h3>'
      if seriesTab == "SEASON"
        puts '<h3>Season ' + seriesImage.first['seasonNum'].to_s + '</h3>'
      elsif seriesTab != "SERIES"
        puts '<h3>S' + seriesImage.first['seasonNum'].to_s + ' ' + seriesImage.first['epName'] + '</h3>'
      end
      puts '</a>'
      puts '<h3 style="color: #436eb1;">' + seriesImage.first['year'].to_s + '</h3>'
      puts '</section>'
	puts '<section class="Rating">'
        	(0...5).each do |i|
        		if (i < reviewRating.first['rating'].to_i)
          			puts '<i class="fa fa-star" style="color: yellow;"></i>'
          		else
          			puts '<i class="fa fa-star"></i>'
          		end
        	end
        puts '</section>'
       puts '<h3>' + seriesReviews[i]['review'] + '</h3>'
       likes = likes.to_a
      (0...likes.size).each do |j|
        #likeCount = likeCount + 1
        if likes[j]['userWhoLiked'] == sessionUser.to_s
            alreadyLiked = true
        end
    end

    puts '<form action="userReviews.cgi" method="post">'
    if alreadyLiked == true
      puts '<button class="LIKES" style="color: pink;">&#10084</button>'
    else
        puts '<button class="LIKES">&#10084</button>'
    end
    puts '<input type="hidden" name="likedReview" value="TRUE">'
    puts '<a href="whoHasLiked.cgi?reviewId=' + seriesReviews[i]['id'].to_s + '&type=EP">' + likes.size.to_s + '</a>'
    puts '<input type="hidden" name="reviewId" value="' + seriesReviews[i]['id'].to_s + '">'    
    puts '<input type="hidden" name="username" value="' + username.to_s + '">'
    puts '<input type="hidden" name="seriesTab" value="' + seriesTab + '">'
    puts '</form>'
    alreadyLiked = false

	puts '</div>'
puts '</div>'
puts '<br>'
puts '<hr style="margin-left: 80px; margin-right: 80px;">'
end
puts '<br>'
puts '<!-- Scripts -->'
  puts '<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>'
  puts '<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>'
  puts '<script src="Televised.js"></script>'
puts '</body>'

puts '</html>'
session.close