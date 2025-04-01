#!/usr/bin/ruby
puts "Content-type: text/html\n\n"
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
listTitle = cgi['title']
type = cgi['contentType']
db = Mysql2::Client.new(
    host: '10.20.3.4', 
    username: 'seniorproject25', 
    password: 'TV_Group123!', 
    database: 'televised_w25'
  )


if type == 'SERIES'
  listContent = db.query("SELECT series.imageName, series.showId, series.showName, curatedListSeries.username FROM series JOIN curatedListSeries ON series.showId = curatedListSeries.seriesId WHERE name = '" + listTitle + "';")
  haveWatched = db.query("SELECT seriesId FROM haveWatchedSeries WHERE username = '" + username.to_s + "';")
  haveWatched = haveWatched.to_a
elsif type == 'SEASON'
  listContent = db.query("SELECT series.imageName, series.showId, series.showName, curatedListSeason.username FROM series JOIN season ON series.showId = season.seriesId JOIN curatedListSeason ON season.seasonId = curatedListSeason.seasonId WHERE name = '" + listTitle + "';")
  haveWatched = db.query("SELECT seasonId FROM haveWatchedSeason WHERE username = '" + username.to_s + "';")
  haveWatched = haveWatched.to_a
else
  listContent = db.query("SELECT series.imageName, series.showId, series.showName, episode.epName, season.seasonNum, curatedListEpisode.username FROM series JOIN season ON series.showId = season.seriesId JOIN episode ON episode.seasonId = season.seasonId JOIN curatedListEpisode ON episode.epId = curatedListEpisode.epId WHERE name = '" + listTitle + "';")
  haveWatched = db.query("SELECT epId FROM haveWatchedEpisode WHERE username = '" + username.to_s + "';")
  haveWatched = haveWatched.to_a
end
listContent = listContent.to_a

displayName = db.query("SELECT displayName FROM account WHERE username = '" + listContent.first['username'] + "';")

puts '<!DOCTYPE html>'
puts '<html lang="en">'

puts '<head>'
  puts '<meta charset="UTF-8">'
  puts '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
  puts '<title>Televised</title>'
  puts '<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">'
  puts '<link rel="stylesheet" href="Televised.css">'
puts '</head>'
puts '<body id="listContent">'
  puts '<nav id="changingNav"></nav> <!-- This is where the navbar will be dynamically loaded -->'
  
  puts '<section class="contentList">'
  puts '<section class="UserDisplay" style="max-width: 390px">'
    puts '<img src="./ProfileImages/' + listContent.first['username'] + '.jpg" alt="">'
    puts '<h3>List by ' + displayName.first['displayName'] + '</h3>'
  puts '</section>'
  puts '<br>'
  puts '<h1>' + listTitle.to_s + '</h1>'
  puts '<hr>'
  puts '<section class="contents">'
  puts '<div class="listContents">'
  (0...listContent.size).each do |i|
    puts '<div class="listItem">'
        puts '<form action="series.cgi" method="POST" style="height: 300px;">'
          puts '<input type="image" src="' + listContent[i]['imageName'] + '" alt="' + listContent[i]['imageName'] + '" style="height: 80%; width: 170px; object-fit: cover;">'
          puts '<input type="hidden" name="clicked_image" value="' + listContent[i]['imageName'] + '">'
          puts '<input type="hidden" name="seasonNumber" value="1">'
          puts '<h6 style="text-align: center">' + listContent[i]['showName'] + '</h6>'
          if type != "SERIES" && type != "SEASON"
            puts '<h6 style="text-align: center">S' + listContent[i]['seasonNum'].to_s + ' ' + listContent[i]['epName'] + '</h6>'
          end
       puts ' </form>'
   puts '</div>'
 end
       puts '<br>'
  puts '</div>'

  tempCount = 0
  if (haveWatched.size > 0)
  (0...listContent.size).each do |i|
    (0...haveWatched.size).each do |h|

      if type == "SERIES"
        if (haveWatched[h]['seriesId'] == listContent[i]['showId'])
            tempCount = tempCount + 1
        end
      elsif type == "SEASON"
        if (haveWatched[h]['seasonId'] == listContent[i]['showId'])
            tempCount = tempCount + 1
        end
      else
        if (haveWatched[h]['epId'] == listContent[i]['showId'])
            tempCount = tempCount + 1
        end
      end
    end
  end
end

  puts "<h6> You've watched " + tempCount.to_s + " of " + listContent.size.to_s + " </h6>"
puts '</section>'
puts '</section>'

   puts '<!-- Scripts -->'
  puts '<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>'
 puts ' <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>'
  puts '<script src="Televised.js"></script>'
puts '</body>'
puts '</html>'
session.close