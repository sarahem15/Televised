#!/usr/bin/ruby
require 'mysql2'
require 'cgi'
require 'cgi/session'

# Enable debugging
$stdout.sync = true
$stderr.reopen $stdout

# Initialize CGI
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


puts "Content-type: text/html\n\n"
puts '<!DOCTYPE html>'
puts '<html lang="en">'

puts '<head>'
  puts '<meta charset="UTF-8">'
  puts '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
  puts '<title>Televised</title>'
  puts '<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">'
  puts '<link rel="stylesheet" href="Televised.css">'
puts '</head>'

puts '<body id="profile">'
  puts '<nav id="changingNav"></nav> <!-- This is where the navbar will be dynamically loaded -->'
  puts '<div class="container-fluid">'
  puts '<br>'
  puts '<section class="ProfileInfo">'
  puts '<section class="UserDisplay">'
    puts '<img src="./Episodes/adventureTime1.1.jpg" alt="testing123">'
    puts '<h3 id="DisplayName">' + displayName.first['displayName'].to_s + '</h3>'
  puts '</section>' 
  puts '<h4>' + pronouns.first['pronouns'].to_s + '</h4>'
  puts '<h4>' + bio.first['bio'].to_s + '</h4>'
  puts '</section>'
  puts '<hr>'
    puts '<div class="profileHeader">'
      puts '<a href="#!" class="active">Profile</a>'
      puts '<a href="Have_Watched.cgi">Have Watched</a>'
      puts '<a href="Want_to_Watch.cgi">Want to Watch</a>'
      puts '<a href="Profile_Lists.cgi">Lists</a>'
      puts '<a href="#">Reviews</a>'
      puts '<a href="Likes_Lists.cgi">Likes</a>'
      puts '<a href="#">Ratings</a>'
    puts '</div>'
  puts '<hr>'
  puts '<br>'

  puts '<section class="topFiveFavs">'
    puts '<p>Top 5 Favorite Series</p>'
    puts '<hr style="margin-left: 80px; margin-right: 80px">'
    puts '<div class="wrapper">'
      puts '<section class="carousel-section" id="topFiveSeries">'
      (0...5).each do |i|
        puts '<div class="item">'
          puts '<form action="series.cgi" method="POST">'
            puts '<input type="image" src="" alt="">'
            puts '<input type="hidden" name="clicked_image" value="">'
          puts '</form>'
        puts '</div>'
      end
      puts '</section>'
    puts '</div>'

    puts '<p>Top 5 Favorite Seasons</p>'
    puts '<hr style="margin-left: 80px; margin-right: 80px">'
    puts '<div class="wrapper">'
      puts '<section class="carousel-section" id="topFiveSeasons">'
        (0...5).each do |i|
        puts '<div class="item">'
          puts '<form action="series.cgi" method="POST">'
            puts '<input type="image" src="" alt="">'
            puts '<input type="hidden" name="clicked_image" value="">'
          puts '</form>'
        puts '</div>'
      end
      puts '</section>'
    puts '</div>'


    puts '<p>Top 5 Favorite Episodes</p>'
    puts '<hr style="margin-left: 80px; margin-right: 80px">'
    puts '<div class="wrapper">'
      puts '<section class="carousel-section" id="topFiveEpisodes">'
        (0...5).each do |i|
        puts '<div class="item">'
          puts '<form action="series.cgi" method="POST">'
            puts '<input type="image" src="" alt="">'
            puts '<input type="hidden" name="clicked_image" value="">'
          puts '</form>'
        puts '</div>'
      end
      puts '</section>'
    puts '</div>'

    puts '<!-- Scripts -->'
  puts '<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>'
  puts '<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>'
  puts '<script src="Televised.js"></script>'
puts '</body>'
puts '</html>'
session.close