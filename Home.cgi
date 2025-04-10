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
#puts username.to_s
series = db.query("SELECT imageName, showName FROM series;")
series = series.to_a

sortedSeries = db.query("SELECT * FROM series ORDER BY year DESC;")
sortedSeries = sortedSeries.to_a

reviews = db.query("SELECT * FROM seriesReview ORDER BY date DESC;")
reviews = reviews.to_a
likeCount = 0
alreadyLiked = false
reviewId = cgi['reviewId']
reviewCreator = cgi['reviewCreator']
likedReview = cgi['likedReview']

fav1Images = "GossipGirl.jpg,NewGirl.jpg,Community.jpg,ModernFamily.jpg,That70sShow.jpg"
fav1 = "Gossip Girl,New Girl,Community,Modern Family,That '70s Show"
fav2Images = "H2O.jpg,WizardsOfWaverlyPlace.jpg,EveryWitchWay.jpg,Supacell.jpg,PercyJackson.jpg"
fav2 = "H2O: Just Add Water,Wizards Of Waverly Place,Every Witch Way,Supacell,Percy Jackson and the Olympians"
fav3 = "Smiling Friends,Clarksons Farm,Futurama,Bojack Horseman,WandaVision"
fav3Images = "SmilingFriends.jpg,ClarksonsFarm.jpg,Futurama.jpg,BojackHorseman.jpg,WandaVision.jpg"

if likedReview == "TRUE"
    begin
        db.query("INSERT INTO likedSeriesReview VALUES ('" + username.to_s + "', '" + reviewCreator + "', '" + reviewId + "');")
    rescue => e
        db.query("DELETE FROM likedSeriesReview WHERE userWhoLiked = '" + username.to_s + "' AND reviewId = '" + reviewId + "';")
    end
end

puts'<!DOCTYPE html>'
puts'<html lang="en">'

puts'<head>'
  puts'<meta charset="UTF-8">'
  puts'<meta name="viewport" content="width=device-width, initial-scale=1.0">'
  puts'<title>Televised</title>'
  puts'<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">'
  puts'<link rel="stylesheet" href="Televised.css">'
  puts '<script src="fetch-data-loader.js"></script>'
puts'</head>'

puts'<body id="homePage">'
  puts'<nav id="changingNav"></nav> <!-- This is where the navbar will be dynamically loaded -->'
  puts'<br>'
  puts'<h1 id="chaningWelcome"></h1>'
  puts'<h3 id="slogan">Your T.V. Guide, Reimagined</h3>'
  puts'<br>'
  puts'<br>'
  puts'<p>Curator\'s Choice</p>'
  puts'<hr style="margin-left: 80px; margin-right: 80px">'
  puts'<section id="homePopular">'
    puts'<div class="wrapper">'
      puts'<section class="carousel-section" id="homePopularSection">'
        puts'<a href=#homePopularSection3>‹</a>'
        (0...5).each do |i|
            seriesImages = fav1Images.split(",")
            seriesSubtitles = fav1.split(",")
            puts '<div class="item">'
            puts '<form action="series.cgi" method="POST">'
                puts '<input type="image" src="' + seriesImages[i] + '" alt="' + seriesImages[i] + '">'
                puts '<h5 style="text-align: center;">' + seriesSubtitles[i] + '</h5>'
                puts '<input type="hidden" name="clicked_image" value="' + seriesImages[i] + '">'
                puts '<input type="hidden" name="seasonNumber" value="' + 1.to_s + '">'

            puts '</form>'
            
            puts '</div>'
        end
        puts'<a href="#homePopularSection2">›</a>'
      puts'</section>'
      puts'<section class="carousel-section" id="homePopularSection2">'
        puts'<a href="#homePopularSection">‹</a>'
        (0...5).each do |i|
            seriesImages = fav2Images.split(",")
            seriesSubtitles = fav2.split(",")
            puts '<div class="item">'
            puts '<form action="series.cgi" method="POST">'
                puts '<input type="image" src="' + seriesImages[i] + '" alt="' + seriesImages[i] + '">'
                puts '<h5 style="text-align: center;">' + seriesSubtitles[i] + '</h5>'
                puts '<input type="hidden" name="clicked_image" value="' + seriesImages[i] + '">'
                puts '<input type="hidden" name="seasonNumber" value="' + 1.to_s + '">'
            puts '</form>'
            puts '</div>'
        end
        puts'<a href="#homePopularSection3">›</a>'
      puts'</section>'
      puts'<section class="carousel-section" id="homePopularSection3">'
        puts'<a href="#homePopularSection2">‹</a>'
        (0...5).each do |i|
            seriesImages = fav3Images.split(",")
            seriesSubtitles = fav3.split(",")
            puts '<div class="item">'
            puts '<form action="series.cgi" method="POST">'
                puts '<input type="image" src="' + seriesImages[i] + '" alt="' + seriesImages[i] + '">'
                puts '<h5 style="text-align: center;">' + seriesSubtitles[i] + '</h5>'
                puts '<input type="hidden" name="clicked_image" value="' + seriesImages[i] + '">'
                puts '<input type="hidden" name="seasonNumber" value="' + 1.to_s + '">'
            puts '</form>'
            puts '</div>'
        end
        puts '<a href="#homePopularSection">›</a>'
      puts '</section>'
    puts '</div>'
  puts '</section>'

  puts '<p>What\'s New</p>'
  puts '<hr style="margin-left: 80px; margin-right: 80px">'
  puts '<section id="homeNew">'
    puts '<div class="wrapper">'
      puts '<section class="carousel-section" id="homeNewSection1">'
        puts '<a href="#homeNewSection3">‹</a>'
        (0...5).each do |i|
            puts '<div class="item">'
            puts '<form action="series.cgi" method="POST">'
                puts '<input type="image" src="' + sortedSeries[i]['imageName'] + '" alt="' + sortedSeries[i]['imageName'] + '">'
                puts '<input type="hidden" name="clicked_image" value="' + sortedSeries[i]['imageName'] + '">'
                puts '<input type="hidden" name="seasonNumber" value="' + 1.to_s + '">'
                puts '<h5 style="text-align: center;">' + sortedSeries[i]['showName'] + '</h5>'
            puts '</form>'
            puts '</div>'
        end
        puts '<a href="#homeNewSection2">›</a>'
      puts '</section>'
      puts '<section class="carousel-section" id="homeNewSection2">'
        puts '<a href="#homeNewSection1">‹</a>'
        (6...11).each do |i|
            puts '<div class="item">'
            puts '<form action="series.cgi" method="POST">'
                puts '<input type="image" src="' + sortedSeries[i]['imageName'] + '" alt="' + sortedSeries[i]['imageName'] + '">'
                puts '<input type="hidden" name="clicked_image" value="' + sortedSeries[i]['imageName'] + '">'
                puts '<input type="hidden" name="seasonNumber" value="' + 1.to_s + '">'
                puts '<h5 style="text-align: center;">' + sortedSeries[i]['showName'] + '</h5>'
            puts '</form>'
            puts '</div>'
        end
        puts '<a href="#homeNewSection3">›</a>'
      puts '</section>'
      puts '<section class="carousel-section" id="homeNewSection3">'
        puts '<a href="#homeNewSection2">‹</a>'
        (12...17).each do |i|
            puts '<div class="item">'
            puts '<form action="series.cgi" method="POST">'
                puts '<input type="image" src="' + sortedSeries[i]['imageName'] + '" alt="' + sortedSeries[i]['imageName'] + '">'
                puts '<input type="hidden" name="clicked_image" value="' + sortedSeries[i]['imageName'] + '">'
                puts '<input type="hidden" name="seasonNumber" value="' + 1.to_s + '">'
                puts '<h5 style="text-align: center;">' + sortedSeries[i]['showName'].gsub("Fucking", "F***ing") + '</h5>'
            puts '</form>'
            puts '</div>'
        end
        puts '<a href="#homeNewSection1">›</a>'
      puts '</section>'
    puts '</div>'
  puts '</section>'
  puts '<br>'
  puts '<hr>'
  puts '<br>'


puts '<br>'
puts '<!-- reviews -->'
puts '<p> Most Recent Reviews </p>'
puts '<section class="homeReviews">'
    

(0...6).each do |i|
    seriesImage = db.query("SELECT imageName, showName FROM series JOIN seriesReview ON series.showId = seriesReview.seriesId WHERE seriesReview.id = '" + reviews[i]['id'].to_s + "';")
    displayName = db.query("SELECT displayName FROM account where username ='" + reviews[i]['username'] + "';")
puts '<div class="ReviewIndiv">'
  puts '<section class="SeriesImg">'
    puts '<img src="' + seriesImage.first['imageName'] + '" alt="">'
  puts '</section>'
  puts '<div class="ReviewContent">'
      puts '<section class="UserDisplay">'
         puts '<img src="./ProfileImages/' + reviews[i]['username'] + '.jpg" alt="" style="background-color: gray;">'
          puts '<a href="othersProfiles.cgi?username=' + reviews[i]['username'] + '"><h3>' + displayName.first['displayName'] + '</h3></a>'
      puts '</section>'
      puts '<br>'
      puts '<a href="reviewIndiv.cgi?reviewId=' + reviews[i]['id'].to_s + '">'
        puts '<h3>' + seriesImage.first['showName'] + '</h3>'
      puts '</a>'
      puts '<br>'
      puts '<h6>' + reviews[i]['review'] + '</h6>'


      likes = db.query("SELECT * FROM likedSeriesReview WHERE reviewId = '" + reviews[i]['id'].to_s + "';")
      likes = likes.to_a
      (0...likes.size).each do |j|
        #likeCount = likeCount + 1
        if likes[j]['userWhoLiked'] == username.to_s
            alreadyLiked = true
        end
    end

    puts '<form action="Home.cgi" method="post">'
    if alreadyLiked == true
      puts '<button class="LIKES" style="color: pink;">&#10084</button>'
    else
        puts '<button class="LIKES">&#10084</button>'
    end
    puts '<input type="hidden" name="likedReview" value="TRUE">'
    puts '<a href="whoHasLiked.cgi?reviewId=' + reviews[i]['id'].to_s + '&type=EP">' + likes.size.to_s + '</a>'
    puts '<input type="hidden" name="reviewId" value="' + reviews[i]['id'].to_s + '">'
    puts '<input type="hidden" name="reviewCreator" value="' + reviews[i]['username'].to_s + '">'
    puts '</form>'



  puts '</div>'
puts '</div>'
    likeCount = 0
    alreadyLiked = false
end

puts '</section>'
puts '<br>'




 puts '<!-- Scripts -->'
  puts '<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>'
  puts '<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>'
  puts '<script src="Televised.js"></script>'
puts '</body>'

puts '</html>'
session.close