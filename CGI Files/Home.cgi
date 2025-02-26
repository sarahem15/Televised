#!/usr/bin/ruby
$stdout.sync = true
$stderr.reopen $stdout

puts "Content-type: text/html\n\n"
require 'mysql2'
require 'cgi'

cgi = CGI.new

db = Mysql2::Client.new(
    host: '10.20.3.4', 
    username: 'seniorproject25', 
    password: 'TV_Group123!', 
    database: 'televised_w25'
  )

series = db.query("SELECT imageName FROM series;")
series = series.to_a

sortedSeries = db.query("SELECT * FROM series ORDER BY year DESC;")
sortedSeries = sortedSeries.to_a

puts'<!DOCTYPE html>'
puts'<html lang="en">'

puts'<head>'
  puts'<meta charset="UTF-8">'
  puts'<meta name="viewport" content="width=device-width, initial-scale=1.0">'
  puts'<title>Televised</title>'
  puts'<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">'
  puts'<link rel="stylesheet" href="Televised.css">'
puts'</head>'

puts'<body id="homePage">'
  puts'<nav id="changingNav"></nav> <!-- This is where the navbar will be dynamically loaded -->'
  puts'<br>'
  puts'<h1 id="chaningWelcome"></h1>'
  puts'<h3 id="slogan">Your T.V. Guide, Reimagined</h3>'
  puts'<br>'
  puts'<br>'
  puts'<p>What\'s Popular</p>'
  puts'<hr style="margin-left: 80px; margin-right: 80px">'
  puts'<section id="homePopular">'
    puts'<div class="wrapper">'
      puts'<section class="carousel-section" id="homePopularSection">'
        puts'<a href=#homePopularSection3>‹</a>'
        (0...5).each do |i|
            puts '<div class="item">'
            puts '<form action="series.cgi" method="POST">'
                puts '<input type="image" src="' + series[i]['imageName'] + '" alt="' + series[i]['imageName'] + '">'
                puts '<input type="hidden" name="clicked_image" value="' + series[i]['imageName'] + '">'
                puts '<input type="hidden" name="seasonNumber" value="' + 1.to_s + '">'
            puts '</form>'
            puts '</div>'
        end
        puts'<a href="#homePopularSection2">›</a>'
      puts'</section>'
      puts'<section class="carousel-section" id="homePopularSection2">'
        puts'<a href="#homePopularSection">‹</a>'
        (6...11).each do |i|
            puts '<div class="item">'
            puts '<form action="series.cgi" method="POST">'
                puts '<input type="image" src="' + series[i]['imageName'] + '" alt="' + series[i]['imageName'] + '">'
                puts '<input type="hidden" name="clicked_image" value="' + series[i]['imageName'] + '">'
                puts '<input type="hidden" name="seasonNumber" value="' + 1.to_s + '">'
            puts '</form>'
            puts '</div>'
        end
        puts'<a href="#homePopularSection3">›</a>'
      puts'</section>'
      puts'<section class="carousel-section" id="homePopularSection3">'
        puts'<a href="#homePopularSection2">‹</a>'
        (12...17).each do |i|
            puts '<div class="item">'
            puts '<form action="series.cgi" method="POST">'
                puts '<input type="image" src="' + series[i]['imageName'] + '" alt="' + series[i]['imageName'] + '">'
                puts '<input type="hidden" name="clicked_image" value="' + series[i]['imageName'] + '">'
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
puts '<p> Popular Reviews </p>'
puts '<section class="homeReviews">'

(0...4).each do
puts '<div class="ReviewIndiv">'
  puts '<section class="SeriesImg">'
    puts '<img src="TheUmbrellaAcademy.jpg" alt="The Umbrella Academy">'
  puts '</section>'
  puts '<div class="ReviewContent">'
      puts '<section class="UserDisplay">'
         puts '<img src="./Episodes/adventureTime1.1.jpg" alt="here">'
          puts '<h3> Username </h3>'
      puts '</section>'
      puts '<br>'
      puts '<br>'
      puts '<h4> This show is great! </h4>'
      puts '<section class="Likes">'
        puts '<h5>&#9829</h5>'
        puts '<h4>12</h4>'
      puts '</section>'
  puts '</div>'
puts '</div>'
end

puts '</section>'





 puts '<!-- Scripts -->'
  puts '<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>'
  puts '<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>'
  puts '<script src="Televised.js"></script>'
puts '</body>'

puts '</html>'