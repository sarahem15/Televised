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

db = Mysql2::Client.new(
    host: '10.20.3.4', 
    username: 'seniorproject25', 
    password: 'TV_Group123!', 
    database: 'televised_w25'
  )


displayName = db.query("SELECT displayName FROM account WHERE username = '" + username.to_s + "';")
bio = db.query("SELECT bio FROM account WHERE username = '" + username.to_s + "';")
pronouns = db.query("SELECT pronouns FROM account WHERE username = '" + username.to_s + "';")
seriesReviews = db.query("SELECT * FROM seriesReview WHERE username = '" + username.to_s + "';")
seriesReviews = seriesReviews.to_a
seriesTab = cgi['seriesTab']
if seriesTab == ""
  seriesTab = "SERIES"
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
puts'<body id="profileReviews">'
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
      puts '<a href="Profile.cgi">Profile</a>'
      puts '<a href="Have_Watched.cgi">Have Watched</a>'
      puts '<a href="Want_to_Watch.cgi">Want to Watch</a>'
      puts '<a href="Profile_Lists.cgi">Lists</a>'
      puts '<a href="#!" class="active">Reviews</a>'
      puts '<a href="Likes_Lists.cgi">Likes</a>'
      puts '<a href="Profile_Ratings.cgi">Ratings</a>'
    puts '</div>'
  puts '<hr>'
  puts '<br>'

  puts '<div class="listProfileButtons">'
  puts '<div class="profileListHeader">'
      if seriesTab == "SERIES"
      puts '<a href="#"class="active">Series</a>'
      puts '<a href="Profile_Reviews.cgi?seriesTab=SEASON">Seasons</a>'
      puts '<a href="Profile_Reviews.cgi?seriesTab=EP">Episodes</a>'
      seriesReviews = db.query("SELECT * FROM seriesReview WHERE username = '" + username.to_s + "';")
  elsif seriesTab == "SEASON"
      puts '<a href="Profile_Reviews.cgi?seriesTab=SERIES">Series</a>'
      puts '<a href="#" class="active">Seasons</a>'
      puts '<a href="Profile_Reviews.cgi?seriesTab=EP">Episodes</a>'
      seriesReviews = db.query("SELECT * FROM seasonReview WHERE username = '" + username.to_s + "';")
  elsif seriesTab == "EP"
      puts '<a href="Profile_Reviews.cgi?seriesTab=SERIES">Series</a>'
      puts '<a href="Profile_Reviews.cgi?seriesTab=SEASON">Seasons</a>'
      puts '<a href="#" class="active">Episodes</a>'
      seriesReviews = db.query("SELECT * FROM episodeReview WHERE username = '" + username.to_s + "';")
  end
  seriesReviews = seriesReviews.to_a
    puts '</div>'
puts '</div>'
puts '<hr>'
puts '<br>'
(0...seriesReviews.size).each do |i|
puts '<div class="originalReview">'
	if seriesTab == "SERIES"
    seriesImage = db.query("SELECT imageName, showName, year FROM series JOIN seriesReview ON series.showId = seriesReview.seriesId WHERE seriesReview.id= '" + seriesReviews[i]['id'].to_s + "';")
    reviewRating = db.query("SELECT rating FROM seriesRating JOIN seriesReview ON seriesRating.id = seriesReview.ratingId WHERE seriesReview.id = '" + seriesReviews[i]['id'].to_s + "';")
  elsif seriesTab == "SEASON"
    seriesImage = db.query("SELECT imageName, showName, year FROM series JOIN season ON season.seriesId = series.showId JOIN seasonReview ON seasonReview.seasonId = season.seasonId WHERE seasonReview.id = '" + seriesReviews[i]['id'].to_s + "';")
    reviewRating = db.query("SELECT rating FROM seasonRating JOIN seasonReview ON seasonRating.id = seasonReview.ratingId WHERE seasonReview.id = '" + seriesReviews[i]['id'].to_s + "';")
  else
     seriesImage = db.query("SELECT imageName, showName, year FROM series JOIN season ON season.seriesId = series.showId JOIN episode ON episode.seasonId = season.seasonId JOIN episodeReview ON episodeReview.epId = episode.epId WHERE episodeReview.id = '" + seriesReviews[i]['id'].to_s + "';")
     reviewRating = db.query("SELECT rating FROM episodeRating JOIN episodeReview ON episodeRating.id = episodeReview.ratingId WHERE episodeReview.id = '" + seriesReviews[i]['id'].to_s + "';") 
  end
	puts "<img src=\"" + seriesImage.first['imageName'] + "\"alt=\"" + seriesImage.first['imageName'] + "\">" 
	puts '<div class="content-R">'
      puts '<section class="NameAndYear">'
      puts '<a href="reviewIndiv.cgi?reviewId=' + seriesReviews[i]['id'].to_s + '">'
      puts '<h3>' + seriesImage.first['showName'] + '</h3>'
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
       puts '<button class="LIKES" style="color: pink;">&#10084</button>'
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