#!/usr/bin/ruby
# Switch images to queries from the database
# Enable debugging
$stdout.sync = true
$stderr.reopen $stdout

puts "Content-type: text/html\n\n"
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
  puts '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">'
  puts '<script src="fetch-data-loader.js"></script>'
puts '</head>'

puts '<body id="userRatings">'
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
      puts '<a href="Profile.cgi">Profile</a>'
      puts '<a href="Have_Watched.cgi">Have Watched</a>'
      puts '<a href="Want_to_Watch.cgi">Want to Watch</a>'
      puts '<a href="Profile_Lists.cgi">Lists</a>'
      puts '<a href="Profile_Reviews.cgi">Reviews</a>'
      puts '<a href="Likes_Lists.cgi">Likes</a>'
      puts '<a href="#!" class="active">Ratings</a>'
    puts '</div>'
  puts '<hr>'
  puts '<br>'

  puts '<div class="listProfileButtons">'
  puts '<div class="profileListHeader">'
      if seriesTab == "SERIES"
      puts '<a href="#"class="active">Series</a>'
      puts '<a href="Profile_Ratings.cgi?seriesTab=SEASON">Seasons</a>'
      puts '<a href="Profile_Ratings.cgi?seriesTab=EP">Episodes</a>'
      ratings = db.query("SELECT DISTINCT seriesId, rating FROM seriesRating WHERE username = '" + username.to_s + "';")
      ratings = ratings.to_a
  elsif seriesTab == "SEASON"
      puts '<a href="Profile_Ratings.cgi?seriesTab=SERIES">Series</a>'
      puts '<a href="#" class="active">Seasons</a>'
      puts '<a href="Profile_Ratings.cgi?seriesTab=EP">Episodes</a>'
      ratings = db.query("SELECT DISTINCT seasonId, rating FROM seasonRating WHERE username = '" + username.to_s + "';")
      ratings = ratings.to_a
  elsif seriesTab == "EP"
      puts '<a href="Profile_Ratings.cgi?seriesTab=SERIES">Series</a>'
      puts '<a href="Profile_Ratings.cgi?seriesTab=SEASON">Seasons</a>'
      puts '<a href="#" class="active">Episodes</a>'
      ratings = db.query("SELECT DISTINCT epId, rating FROM episodeRating WHERE username = '" + username.to_s + "';")
      ratings = ratings.to_a
  end
    puts '</div>'
puts '</div>'

(0...ratings.size).each do |i|
puts '<hr style="margin-left: 80px; margin-right: 80px">'
    puts '<div class="listWrapper">'
    if seriesTab == "SERIES"
        rateImages = db.query("SELECT imageName, showName, year FROM series JOIN seriesRating ON series.showId = seriesRating.seriesId WHERE username = '" + username.to_s + "';")
    elsif seriesTab == "SEASON"
      rateImages = db.query("SELECT imageName, showName, year FROM series JOIN seasonRating ON series.showId = seriesRating.seriesId WHERE username = '" + username.to_s + "';")
    elsif seriesTab == "EP"
      rateImages = db.query("SELECT imageName, showName, year FROM series JOIN seriesRating ON series.showId = seriesRating.seriesId WHERE username = '" + username.to_s + "';")
    end
        rateImages = rateImages.to_a
        puts "<img src=\"" + rateImages[i]['imageName'] + "\"alt=\"" + rateImages[i]['imageName'] + "\" style='width: 100px; height: 150px;'>" 
  puts '<div class="content-R">'
      puts '<br>'
      puts '<section class="NameAndYear">'
      puts '<h3>' + rateImages[i]['showName'] + '</h3>'
      puts '<h3 style="color: #436eb1;">' + rateImages[i]['year'].to_s + '</h3>'
      puts '</section>'
  puts '<section class="Rating">'
          (0...5).each do |j|
            if (j < ratings[i]['rating'].to_i)
                puts '<i class="fa fa-star" style="color: white;"></i>'
            else
              puts '<i class="fa fa-star"></i>'
            end
          end
        puts '</section>'
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
session.close