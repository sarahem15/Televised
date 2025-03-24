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

reviewId = cgi['reviewId']

db = Mysql2::Client.new(
    host: '10.20.3.4', 
    username: 'seniorproject25', 
    password: 'TV_Group123!', 
    database: 'televised_w25'
  )
reviewContent = db.query("SELECT * FROM seriesReview WHERE id ='" + reviewId + "';")
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
	seriesImage = db.query("SELECT imageName, showName, year FROM series JOIN seriesReview ON series.showId = seriesReview.seriesId WHERE seriesReview.id= '" + reviewId + "';")
	reviewRating = db.query("SELECT rating FROM seriesRating JOIN seriesReview ON seriesRating.id = seriesReview.ratingId WHERE seriesReview.id = '" + reviewId + "';")
	puts "<img src=\"" + seriesImage.first['imageName'] + "\"alt=\"" + seriesImage.first['imageName'] + "\">" 
	puts '<div class="content-R">'
	puts '<section class="UserDisplay">'
         puts '<img src="./ProfileImages/' + reviewContent.first['username'] + '.jpg" alt="">'
          puts '<h3>' + reviewContent.first['username'] + '</h3>'
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
       puts '<button class="LIKES" style="color: pink;">&#10084</button>'
	puts '</div>'
puts '</div>'

puts '<br>'


puts '<hr style="margin-left: 50px; margin-right: 50px;">'
puts '<h2 style="margin-left: 80px;"> Replies </h2>'
puts '<hr style="margin-left: 80px; margin-right: 1150px;">'
puts '<br>'
replies = db.query("SELECT * FROM seriesReply WHERE reviewId ='" + reviewId + "';")
replies = replies.to_a
(0...replies.size).each do |i|
puts '<div class="content-Reply">'
  puts '<section class="UserDisplay">'
         puts '<img src="./ProfileImages/' + replies[i]['username'] + '.jpg" alt="">'
          puts '<h3>' + replies[i]['username'] + '</h3>'
      puts '</section>'
      puts '<br>'
       puts '<h3>' + replies[i]['reply'] + '</h3>'
       puts '<button class="LIKES" style="color: pink;">&#10084</button>'
  puts '</div>'
  puts '<br>'
  puts '<hr style="margin-left: 80px; margin-right: 80px;">'
  puts '<br>'
end
  if replies.size == 0 
    puts '<h5 style="text-align: center;"> Replies will show up here! </h5>'
  end
  puts '<br>'
puts '<!-- Scripts -->'
  puts '<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>'
  puts '<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>'
  puts '<script src="Televised.js"></script>'
puts '</body>'

puts '</html>'