#!/usr/bin/ruby
# Switch images to queries from the database
# Enable debugging
$stdout.sync = true
$stderr.reopen $stdout

puts "Content-type: text/html\n\n"
require 'mysql2'
require 'cgi'
#require 'cgi/session'

# Initialize CGI
cgi = CGI.new
#session = CGI::Session.new(cgi)
#username = session['username']
username = cgi['username']

db = Mysql2::Client.new(
    host: '10.20.3.4', 
    username: 'seniorproject25', 
    password: 'TV_Group123!', 
    database: 'televised_w25'
  )

#seriesImages = db.query("SELECT imageName FROM series;")
#seriesImages = seriesImages.to_a()
displayName = db.query("SELECT displayName FROM account WHERE username = '" + username.to_s + "';")

bio = db.query("SELECT bio FROM account WHERE username = '" + username.to_s + "';")
pronouns = db.query("SELECT pronouns FROM account WHERE username = '" + username.to_s + "';")
seriesTab = cgi['seriesTab']
if seriesTab == ""
  seriesTab = "SERIES"
end


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
    puts '<img src="ProfileImages/' + username.to_s + '.jpg" alt="">'
    puts '<h3 id="DisplayName">' + displayName.first['displayName'].to_s + '</h3>'
  puts '</section>'
  puts '<h4>' + pronouns.first['pronouns'].to_s + '</h4>'
  puts '<h4>' + bio.first['bio'].to_s + '</h4>'
  puts '</section>'
  puts '<hr>'
     puts '<div class="profileHeader">'
      puts '<a href="othersProfiles.cgi?username=' + username + '">Profile</a>'
      puts '<a href="#!" class="active">Lists</a>'
      puts '<a href="userReviews.cgi?username=' + username + '">Reviews</a>'
      puts '<a href="userRatings.cgi?username=' + username + '">Ratings</a>'
    puts '</div>'
  puts '<hr>'
  puts '<br>'

  puts '<div class="listProfileButtons">'
  puts '<div class="profileListHeader">'
      if seriesTab == "SERIES"
      puts '<a href="#"class="active">Series</a>'
      puts '<a href="userLists.cgi?username=' + username + '&seriesTab=SEASON">Seasons</a>'
      puts '<a href="userLists.cgi?username=' + username + '&seriesTab=EP">Episodes</a>'
      lists = db.query("SELECT DISTINCT name, description, date FROM curatedListSeries WHERE username = '" + username.to_s + "';")
      lists = lists.to_a
  elsif seriesTab == "SEASON"
      puts '<a href="userLists.cgi?username=' + username + '&seriesTab=SERIES">Series</a>'
      puts '<a href="#" class="active">Seasons</a>'
      puts '<a href="userLists.cgi?username=' + username + '&seriesTab=EP">Episodes</a>'
      lists = db.query("SELECT DISTINCT name, description, date FROM curatedListSeason WHERE username = '" + username.to_s + "';")
      lists = lists.to_a
  elsif seriesTab == "EP"
      puts '<a href="userLists.cgi?username=' + username + '&seriesTab=SERIES">Series</a>'
      puts '<a href="userLists.cgi?username=' + username + '&seriesTab=SEASON">Seasons</a>'
      puts '<a href="#" class="active">Episodes</a>'
      lists = db.query("SELECT DISTINCT name, description, date FROM curatedListEpisode WHERE username = '" + username.to_s + "';")
      lists = lists.to_a
  end
    puts '</div>'
puts '</div>'

(0...lists.size).each do |i|
puts '<hr style="margin-left: 80px; margin-right: 80px">'
  puts '<div class="listImages">'
    puts '<div class="listWrapper">'
        puts '<section class="carousel-section" id="listsPlease">'
        listImages = db.query("SELECT imageName FROM series JOIN curatedListSeries ON series.showId = curatedListSeries.seriesId WHERE username = '" + username.to_s + "' AND name = '" + lists[i]['name'] + "';")
        listImages = listImages.to_a
        if seriesTab == "SEASON"
          listImages = db.query("SELECT imageName FROM series JOIN season ON season.seriesId = series.showId JOIN curatedListSeason ON season.seasonId = curatedListSeason.seasonId WHERE username = '" + username.to_s + "' AND name = '" + lists[i]['name'] + "';")
          listImages = listImages.to_a
        elsif seriesTab == "EP"
          listImages = db.query("SELECT imageName FROM series JOIN season ON season.seriesId = series.showId JOIN episode ON episode.seasonId = season.seasonId JOIN curatedListEpisode ON episode.epId = curatedListEpisode.epId WHERE username = '" + username.to_s + "' AND name = '" + lists[i]['name'] + "';")
          listImages = listImages.to_a
        end

        (0...5).each do |j|
          puts '<div class="itemS">'
          if (j < listImages.size)
              puts '<img src="' + listImages[j]['imageName'] + '" alt="' + listImages[j]['imageName'] + '">'
          else
            puts '<img src="" alt="">'
          end
          puts '</div>'
        end
      puts '</section>'
      puts '</div>'
      puts '<div>'
      puts '<section class="titleDate">'
      puts '<a href="listContents.cgi?title='+ lists[i]['name'] + '&contentType=' + seriesTab + '">' + lists[i]['name'] + '</a>'
      puts '<h4>' + lists[i]['date'].to_s + '</h4>'
      puts '</section>'

      puts '<h3>' + lists[i]['description'] +'</h3>'
      puts '</div>'
    puts '</div>'
    puts '<br>'
end
    puts '<!-- Scripts -->'
  puts '<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>'
  puts '<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>'
  puts '<script src="Televised.js"></script>'
puts '</body>'
puts '</html>'
#session.close