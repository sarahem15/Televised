#!/usr/bin/ruby
# Switch images to queries from the database
# Enable debugging
$stdout.sync = true
$stderr.reopen $stdout

puts "Content-type: text/html\n\n"
require 'mysql2'
require 'cgi'

# Initialize CGI
cgi = CGI.new
username = cgi['username']

db = Mysql2::Client.new(
    host: '10.20.3.4', 
    username: 'seniorproject25', 
    password: 'TV_Group123!', 
    database: 'televised_w25'
  )
ratings = db.query("SELECT DISTINCT seriesId, rating FROM seriesRating WHERE username = '" + username.to_s + "';")
ratings = ratings.to_a
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
      puts '<a href="userLists.cgi?username=' + username + '" >Lists</a>'
      puts '<a href="userReviews.cgi?username=' + username + '">Reviews</a>'
      puts '<a href="#!" class="active">Ratings</a>'
    puts '</div>'
  puts '<hr>'
  puts '<br>'

  puts '<div class="listProfileButtons">'
  puts '<div class="profileListHeader">'
      if seriesTab == "SERIES"
      puts '<a href="#"class="active">Series</a>'
      puts '<a href="userRatings.cgi?username=' + username + '&seriesTab=SEASON">Seasons</a>'
      puts '<a href="userRatings.cgi?username=' + username + '&seriesTab=EP">Episodes</a>'
      ratings = db.query("SELECT DISTINCT seriesId, rating FROM seriesRating WHERE username = '" + username.to_s + "';")
      rateImages = db.query("SELECT imageName, showName, year FROM series JOIN seriesRating ON series.showId = seriesRating.seriesId WHERE username = '" + username.to_s + "';")
  elsif seriesTab == "SEASON"
      puts '<a href="userRatings.cgi?username=' + username + '&seriesTab=SERIES">Series</a>'
      puts '<a href="#" class="active">Seasons</a>'
      puts '<a href="userRatings.cgi?username=' + username + '&seriesTab=EP">Episodes</a>'
      ratings = db.query("SELECT DISTINCT seasonId, rating FROM seasonRating WHERE username = '" + username.to_s + "';")
      rateImages = db.query("SELECT series.imageName, series.showName, series.year, season.seasonNum FROM series JOIN season ON series.showId = season.seriesId JOIN seasonRating ON seasonRating.seasonId = season.seasonId WHERE username = '" + username.to_s + "';")
  elsif seriesTab == "EP"
      puts '<a href="userRatings.cgi?username=' + username + '&seriesTab=SERIES">Series</a>'
      puts '<a href="userRatings.cgi?username=' + username + '&seriesTab=SEASON">Seasons</a>'
      puts '<a href="#" class="active">Episodes</a>'
      ratings = db.query("SELECT DISTINCT epId, rating FROM episodeRating WHERE username = '" + username.to_s + "';")
      rateImages = db.query("SELECT series.imageName, series.showName, series.year, season.seasonNum, episode.epName FROM series JOIN season ON series.showId = season.seriesId JOIN episode ON episode.seasonId = season.seasonId JOIN episodeRating ON episodeRating.epId = episode.epId WHERE username = '" + username.to_s + "';")
  end

      ratings = ratings.to_a
      rateImages = rateImages.to_a
    puts '</div>'
puts '</div>'
puts '<hr style="margin-left: 80px; margin-right: 80px">'
epNum = 0
(0...ratings.size).each do |i|
  puts '<br>'

    puts '<div class="listWrapper" style="width: 30%;">'
        if seriesTab != "EP"
          puts '<form action="series.cgi">'
            puts '<input type="hidden" name="clicked_image" value="' + rateImages[i]['imageName'] + '">'
            puts '<input type="hidden" name="seasonNumber" value="' + rateImages[i]['seasonNum'].to_s + '">'
        else
          allEps = db.query("SELECT epName FROM episode JOIN season ON season.seasonId = episode.seasonId JOIN series ON series.showId = season.seriesId WHERE showName = '" + rateImages[i]['showName'] + "';")
          allEps = allEps.to_a
          (0...allEps.size).each do |j|
            if allEps[j]['epName'] == rateImages[i]['epName']
              epNum = j + 1
            end
          end 
          puts '<form action="indivEp.cgi" method="POST">'
            puts '<input type="hidden" name="ep_name" value="' + rateImages[i]['epName'] + '">'
            puts '<input type="hidden" name="show_name" value="' + rateImages[i]['showName'] + '">'
            puts '<input type="hidden" name="seriesId" value="' + rateImages[i]['showId'].to_s + '">'
            puts '<input type="hidden" name="ep_num" value="' + epNum.to_s + '">'
            puts '<input type="hidden" name="seasonNumber" value="' + rateImages[i]['seasonNum'].to_s + '">'
        end  
        puts "<input type='image' src=\"" + rateImages[i]['imageName'] + "\"alt=\"" + rateImages[i]['imageName'] + "\" style='width: 150px; height: 220px; object-fit:cover;'>" 
        puts '</form>'
  puts '<div class="content-R">'
      puts '<br>'
      puts '<section class="NameAndYear">'
      puts '<h3>' + rateImages[i]['showName'] + '</h3>'
      puts '<h3 style="color: #436eb1;">' + rateImages[i]['year'].to_s + '</h3>'
      puts '</section>'
      if seriesTab == "SEASON"
        puts '<h4>Season ' + rateImages[i]['seasonNum'].to_s + '</h4>'
      elsif seriesTab == "EP"
        puts '<h4>Season ' + rateImages[i]['seasonNum'].to_s + ' ' + rateImages[i]['epName'] + '</h4>'
      end
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
  puts '<hr style="margin-left: 80px; margin-right: 80px">'
end

  puts '<br>'
    puts '<!-- Scripts -->'
  puts '<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>'
  puts '<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>'
  puts '<script src="Televised.js"></script>'
puts '</body>'
puts '</html>'
