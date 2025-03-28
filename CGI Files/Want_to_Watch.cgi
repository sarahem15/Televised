#!/usr/bin/ruby
# Switch images to queries from the database
# Enable debugging
$stdout.sync = true
$stderr.reopen $stdout

require 'mysql2'
require 'cgi'
require 'cgi/session'

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
seriesTab = cgi['seriesTab']
if seriesTab == ""
  seriesTab = "SERIES"
end
size = 0
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
    puts '<img src="ProfileImages/' + username.to_s + '.jpg" alt="">'
    puts '<h3 id=" DisplayName">' + displayName.first['displayName'].to_s + '</h3>'
  puts '</section>'
  puts '<h4>' + pronouns.first['pronouns'].to_s + '</h4>'
  puts '<h4>' + bio.first['bio'].to_s + '</h4>'
  puts '</section>'
  puts '<hr>'
    puts '<div class="profileHeader">'
      puts '<a href="Profile.cgi">Profile</a>'
      puts '<a href="Have_Watched.cgi">Have Watched</a>'
      puts '<a href="#!" class="active">Want to Watch</a>'
      puts '<a href="Profile_Lists.cgi">Lists</a>'
      puts '<a href="Profile_Reviews.cgi">Reviews</a>'
      puts '<a href="Likes_Lists.cgi">Likes</a>'
      puts '<a href="Profile_Ratings.cgi">Ratings</a>'
    puts '</div>'
  puts '<hr>'
  puts '<br>'
  puts '<div class="profileListHeader">'
      if seriesTab == "SERIES"
      puts '<a href="#"class="active">Series</a>'
      puts '<a href="Want_to_Watch.cgi?seriesTab=SEASON">Seasons</a>'
      puts '<a href="Want_to_Watch.cgi?seriesTab=EP">Episodes</a>'

      images = db.query("SELECT series.imageName, series.showName FROM wantToWatchSeries JOIN series ON wantToWatchSeries.seriesId = series.showId WHERE wantToWatchSeries.username = '" + username.to_s + "';")
      images = images.to_a
  elsif seriesTab == "SEASON"
      puts '<a href="Want_to_Watch.cgi?seriesTab=SERIES">Series</a>'
      puts '<a href="#" class="active">Seasons</a>'
      puts '<a href="Want_to_Watch.cgi?seriesTab=EP">Episodes</a>'
      images = db.query("SELECT series.imageName, series.showName, season.seasonNum FROM wantToWatchSeason JOIN season ON wantToWatchSeason.seasonId = season.seasonId JOIN series ON season.seriesId = series.showId WHERE wantToWatchSeason.username = '" + username.to_s + "';")
      images = images.to_a
  elsif seriesTab == "EP"
      puts '<a href="Want_to_Watch.cgi?seriesTab=SERIES">Series</a>'
      puts '<a href="Want_to_Watch.cgi?seriesTab=SEASON">Seasons</a>'
      puts '<a href="#" class="active">Episodes</a>'
      images = db.query("SELECT series.imageName, series.showName, season.seasonNum, episode.epName FROM wantToWatchEpisode JOIN episode ON wantToWatchEpisode.epId = episode.epId JOIN season ON episode.seasonId = season.seasonId JOIN series ON season.seriesId = series.showId WHERE wantToWatchEpisode.username = '" + username.to_s + "';")
      images = images.to_a
  end
    puts '</div>'

  puts '<section class="topFiveFavs">'
    puts '<hr style="margin-left: 80px; margin-right: 80px">'
     (0...images.size).each do |h|
    if (images[size])
    puts '<div class="wrapper">'
      puts '<section class="carousel-section" id="topFiveSeries">'

      # INPUT IMAGES  
      (0...5).each do |i|
        if (images[size])
        puts '<div class="item">'
          puts '<form action="series.cgi" method="POST">'
            puts '<input type="image" src="' + images[size]['imageName'] + '" alt="' + images[size]['imageName'] + '">'
            puts '<input type="hidden" name="clicked_image" value="' + images[size]['imageName'] + '">'
            puts '<input type="hidden" name="seasonNumber" value="' + 1.to_s + '">'
            puts '<h6 style="text-align: center;">' + images[size]['showName'] + '</h6>'
            if seriesTab == "SEASON"
              puts '<h6 style="text-align: center;">Season ' + images[size]['seasonNum'].to_s + '</h6>'
            elsif seriesTab == "EP"
              puts '<h6 style="text-align: center;">S' + images[size]['seasonNum'].to_s + ' ' + images[size]['epName'] + '</h6>'
            end
            size = size + 1
          puts '</form>'
        puts '</div>'
      end
      end
        puts '</section>'
    puts '</div>'
  end
end


    puts '<!-- Scripts -->'
  puts '<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>'
  puts '<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>'
  puts '<script src="Televised.js"></script>'
puts '</body>'
puts '</html>'
session.close