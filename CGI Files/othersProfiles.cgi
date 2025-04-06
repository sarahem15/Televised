#!/usr/bin/ruby
require 'mysql2'
require 'cgi'

# Enable debugging
$stdout.sync = true
$stderr.reopen $stdout

# Initialize CGI
cgi = CGI.new

username = cgi['username']
db = Mysql2::Client.new(
    host: '10.20.3.4', 
    username: 'seniorproject25', 
    password: 'TV_Group123!', 
    database: 'televised_w25'
  )
displayName = db.query("SELECT displayName FROM account WHERE username = '" + username.to_s + "';")
bio = db.query("SELECT bio FROM account WHERE username = '" + username.to_s + "';")
pronouns = db.query("SELECT pronouns FROM account WHERE username = '" + username.to_s + "';")
topFiveSeriesImages = db.query("SELECT imageName, showName, ranking FROM series JOIN topFiveSeries ON topFiveSeries.seriesId = series.showId WHERE username = '" + username.to_s + "' ORDER BY topFiveSeries.ranking ASC;")
topFiveSeriesImages = topFiveSeriesImages.to_a
topFiveSeasonImages = db.query("SELECT imageName, showName, seasonNum, ranking FROM series JOIN season ON season.seriesId = series.showId JOIN topFiveSeason ON topFiveSeason.seasonId = season.seasonId WHERE username = '" + username.to_s + "' ORDER BY topFiveSeason.ranking ASC;")
topFiveSeasonImages = topFiveSeasonImages.to_a
topFiveEpImages = db.query("SELECT imageName, showName, seasonNum, epName, ranking FROM series JOIN season ON season.seriesId = series.showId JOIN episode ON episode.seasonId = season.seasonId JOIN topFiveEpisode ON topFiveEpisode.epId = episode.epId WHERE username = '" + username.to_s + "'  ORDER BY topFiveEpisode.ranking ASC;")
topFiveEpImages = topFiveEpImages.to_a
count = 0


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

puts '<body id="userProfile">'
  puts '<nav id="changingNav"></nav> <!-- This is where the navbar will be dynamically loaded -->'
  puts '<div class="container-fluid">'
  puts '<br>'
  puts '<section class="ProfileInfo">'
  puts '<section class="UserDisplay">'
    puts '<img src="./ProfileImages/' + username.to_s + '.jpg" alt="" style="background-color: gray;">'
    puts '<h3 id="DisplayName">' + displayName.first['displayName'].to_s + '</h3>'
  puts '</section>' 
  puts '<h4>' + pronouns.first['pronouns'].to_s + '</h4>'
  puts '<h4>' + bio.first['bio'].to_s + '</h4>'
  puts '</section>'
  puts '<hr>'
    puts '<div class="profileHeader">'
      puts '<a href="#!" class="active">Profile</a>'
      puts '<a href="userLists.cgi?username=' + username + '">Lists</a>'
      puts '<a href="userReviews.cgi?username=' + username + '">Reviews</a>'
      puts '<a href="userRatings.cgi?username=' + username + '">Ratings</a>'
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
        
        if count < topFiveSeriesImages.size && topFiveSeriesImages[count]['ranking'].to_i == (i+1)
          puts '<form action="series.cgi" method="POST">'
            puts '<input type="image" src="' + topFiveSeriesImages[count]['imageName'] + '" alt="">'
            puts '<input type="hidden" name="clicked_image" value="' + topFiveSeriesImages[count]['imageName'] + '">'
            puts '<input type="hidden" name="seasonNumber" value="1">'
            puts '<h6 style="text-align: center;">' + topFiveSeriesImages[count]['showName'] + '</h6>'
          count = count + 1
        else
          puts '<input type="image" src="" alt="">'
        end
        puts '</form>'
        puts '</div>'
      end
      puts '</section>'
    puts '</div>'

    count = 0
    puts '<p>Top 5 Favorite Seasons</p>'
    puts '<hr style="margin-left: 80px; margin-right: 80px">'
    puts '<div class="wrapper">'
      puts '<section class="carousel-section" id="topFiveSeasons">'
        (0...5).each do |i|
        puts '<div class="item">'
          if count < topFiveSeasonImages.size && topFiveSeasonImages[count]['ranking'].to_i == (i+1)
            puts '<form action="series.cgi" method="POST">'
            puts '<input type="image" src="' + topFiveSeasonImages[count]['imageName'] + '" alt="">'
            puts '<input type="hidden" name="clicked_image" value="' + topFiveSeasonImages[count]['imageName'] + '">'
            puts '<input type="hidden" name="seasonNumber" value="' + topFiveSeasonImages[count]['seasonNum'].to_s + '">'
            puts '<h6 style="text-align: center;">' + topFiveSeasonImages[count]['showName'] + '</h6>'
            puts '<h6 style="text-align: center;">Season ' + topFiveSeasonImages[count]['seasonNum'].to_s + '</h6>'
            count = count + 1
          else
            puts '<input type="image" src="" alt="">'
          end
          puts '</form>'
        puts '</div>'
      end
      puts '</section>'
    puts '</div>'

    count = 0
    puts '<p>Top 5 Favorite Episodes</p>'
    puts '<hr style="margin-left: 80px; margin-right: 80px">'
    puts '<div class="wrapper">'
      puts '<section class="carousel-section" id="topFiveEpisodes">'
        (0...5).each do |i|
        puts '<div class="item">'
        if count < topFiveEpImages.size && topFiveEpImages[count]['ranking'].to_i == (i+1)
          puts '<form action="series.cgi" method="POST">'
            puts '<input type="image" src="' + topFiveEpImages[count]['imageName'] + '" alt="">'
            puts '<input type="hidden" name="clicked_image" value="' + topFiveEpImages[count]['imageName'] + '">'
            puts '<input type="hidden" name="seasonNumber" value="' + topFiveEpImages[count]['seasonNum'].to_s + '">'
            puts '<h6 style="text-align: center;">' + topFiveEpImages[count]['showName'] + '</h6>'
            puts '<h6 style="text-align: center;">S' + topFiveEpImages[count]['seasonNum'].to_s + ' ' + topFiveEpImages[count]['epName'] + '</h6>'
            count = count + 1
          else
            puts '<input type="image" src="" alt="">'
          end
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
#session.close