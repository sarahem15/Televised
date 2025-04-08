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

#username = "try@try"
db = Mysql2::Client.new(
    host: '10.20.3.4', 
    username: 'seniorproject25', 
    password: 'TV_Group123!', 
    database: 'televised_w25'
  )
displayName = db.query("SELECT displayName FROM account WHERE username = '" + username.to_s + "';")
bio = db.query("SELECT bio FROM account WHERE username = '" + username.to_s + "';")
pronouns = db.query("SELECT pronouns FROM account WHERE username = '" + username.to_s + "';")
topFiveSeries = db.query("SELECT imageName, showName, ranking FROM series JOIN topFiveSeries ON topFiveSeries.seriesId = series.showId WHERE username = '" + username.to_s + "' ORDER BY topFiveSeries.ranking ASC;")
topFiveSeries = topFiveSeries.to_a
topFiveSeason = db.query("SELECT imageName, showName, seasonNum, ranking FROM series JOIN season ON season.seriesId = series.showId JOIN topFiveSeason ON topFiveSeason.seasonId = season.seasonId WHERE username = '" + username.to_s + "' ORDER BY topFiveSeason.ranking ASC;")
topFiveSeason = topFiveSeason.to_a
topFiveEpisode = db.query("SELECT imageName, showName, series.showId, season.seasonNum, episode.epName, ranking FROM series JOIN season ON season.seriesId = series.showId JOIN episode ON episode.seasonId = season.seasonId JOIN topFiveEpisode ON topFiveEpisode.epId = episode.epId WHERE username = '" + username.to_s + "'  ORDER BY topFiveEpisode.ranking ASC;")
topFiveEpisode = topFiveEpisode.to_a
count = 0
epNum = 0

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
      puts '<a href="Profile_Reviews.cgi">Reviews</a>'
      puts '<a href="Likes_Lists.cgi">Likes</a>'
      puts '<a href="Profile_Ratings.cgi">Ratings</a>'
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
          if count < topFiveSeries.size && topFiveSeries[count]['ranking'] == (i+1) 
            puts '<form action="series.cgi" method="POST">'
            puts '<input type="image" src="' + topFiveSeries[count]['imageName'] + '" alt="">'
            puts '<input type="hidden" name="clicked_image" value="' + topFiveSeries[count]['imageName'] + '">'
            puts '<input type="hidden" name="seasonNumber" value="1">'
            puts '</form>'
            puts '<h6 style="text-align: center;">' + topFiveSeries[count]['showName'].to_s + '</h6>'
            count = count + 1
          else 
            puts '<input type="image" src="" alt="">'
            puts '<input type="hidden" name="clicked_image" value="">'
            puts '</form>'
          end
        puts '</div>'
      end
      count = 0
      puts '</section>'
    puts '</div>'

    puts '<p>Top 5 Favorite Seasons</p>'
    puts '<hr style="margin-left: 80px; margin-right: 80px">'
    puts '<div class="wrapper">'
      puts '<section class="carousel-section" id="topFiveSeasons">'
        (0...5).each do |i|
        puts '<div class="item">'
          if count < topFiveSeason.size && topFiveSeason[count]['ranking'] == (i+1) 
            puts '<form action="series.cgi" method="POST">'
            puts '<input type="image" src="' + topFiveSeason[count]['imageName'] + '" alt="">'
            puts '<input type="hidden" name="clicked_image" value="' + topFiveSeason[count]['imageName'] + '">'
            puts '<input type="hidden" name="seasonNumber" value="' + topFiveSeason[count]['seasonNum'].to_s + '">'
          puts '</form>'
          puts '<h6 style="text-align: center;">' + topFiveSeason[count]['showName'].to_s + '</h6>'
            puts '<h6 style="text-align: center;">Season ' + topFiveSeason[count]['seasonNum'].to_s + '</h6>'
            count = count + 1
          else
            puts '<input type="image" src="" alt="">'
            puts '<input type="hidden" name="clicked_image" value="">'
          puts '</form>'
          end
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
          if count < topFiveEpisode.size && topFiveEpisode[count]['ranking'] == (i+1)
          allEps = db.query("SELECT epName FROM episode JOIN season ON season.seasonId = episode.seasonId JOIN series ON series.showId = season.seriesId WHERE showName = '" + topFiveEpisode[count]['showName'].gsub("'", "\\\\'") + "';")
          allEps = allEps.to_a
          (0...allEps.size).each do |j|
            if allEps[j]['epName'] == topFiveEpisode[count]['epName']
              epNum = j + 1
            end
          end 
            puts '<form action="indivEp.cgi" method="POST">'
            puts '<input type="image" src="' + topFiveEpisode[count]['imageName'] + '" alt="">'
            puts '<input type="hidden" name="ep_name" value="' + topFiveEpisode[count]['epName'] + '">'
            puts '<input type="hidden" name="show_name" value="' + topFiveEpisode[count]['showName'] + '">'
            puts '<input type="hidden" name="seriesId" value="' + topFiveEpisode[count]['showId'].to_s + '">'
            puts '<input type="hidden" name="ep_num" value="' + epNum.to_s + '">'
            puts '<input type="hidden" name="seasonNumber" value="' + topFiveEpisode[count]['seasonNum'].to_s + '">'
          puts '</form>'
          puts '<h6 style="text-align: center;">' + topFiveEpisode[count]['showName'].to_s + '</h6>'
            puts '<h6 style="text-align: center;">S' + topFiveEpisode[count]['seasonNum'].to_s + ' ' + topFiveEpisode[count]['epName'].to_s + '</h6>'
            count = count + 1
          else
            puts '<input type="image" src="" alt="">'
            puts '<input type="hidden" name="clicked_image" value="">'
          puts '</form>'
          end
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