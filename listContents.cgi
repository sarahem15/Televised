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
likedList = cgi['likedList']
#likeUser = cgi['likeUser']
type = cgi['contentType']
db = Mysql2::Client.new(
    host: '10.20.3.4', 
    username: 'seniorproject25', 
    password: 'TV_Group123!', 
    database: 'televised_w25'
  )

alreadyLiked = false
if type == 'SERIES'
  listContent = db.query("SELECT series.imageName, series.showId, series.showName, curatedListSeries.username FROM series JOIN curatedListSeries ON series.showId = curatedListSeries.seriesId WHERE name = '" + listTitle + "';")
  haveWatched = db.query("SELECT seriesId FROM haveWatchedSeries WHERE username = '" + username.to_s + "';")
elsif type == 'SEASON'
  listContent = db.query("SELECT series.imageName, series.showId, series.showName, season.seasonNum, curatedListSeason.username FROM series JOIN season ON series.showId = season.seriesId JOIN curatedListSeason ON season.seasonId = curatedListSeason.seasonId WHERE name = '" + listTitle + "';")
  haveWatched = db.query("SELECT seasonId FROM haveWatchedSeason WHERE username = '" + username.to_s + "';")
else
  listContent = db.query("SELECT series.imageName, series.showId, series.showName, episode.epName, season.seasonNum, curatedListEpisode.username FROM series JOIN season ON series.showId = season.seriesId JOIN episode ON episode.seasonId = season.seasonId JOIN curatedListEpisode ON episode.epId = curatedListEpisode.epId WHERE name = '" + listTitle + "';")
  haveWatched = db.query("SELECT epId FROM haveWatchedEpisode WHERE username = '" + username.to_s + "';") 
end
listContent = listContent.to_a
haveWatched = haveWatched.to_a
listId = db.query("SELECT id FROM listOwnership WHERE listName = '" + listTitle + "';")
likes = db.query("SELECT * FROM likedList WHERE listId = '" + listId.first['id'].to_s + "';")
likes = likes.to_a

displayName = db.query("SELECT displayName FROM account WHERE username = '" + listContent.first['username'] + "';")
if likedList == "TRUE"
  begin
    db.query("INSERT INTO likedList VALUES ('" + username.to_s + "', '" + listContent.first['username'] + "', '" + listId.first['id'].to_s + "');")
  rescue 
    db.query("DELETE FROM likedList WHERE userWhoLiked = '" + username.to_s + "' AND listId = '" + listId.first['id'].to_s + "';")
  end
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
puts '<body id="listContent">'
  puts '<nav id="changingNav"></nav> <!-- This is where the navbar will be dynamically loaded -->'
  
  puts '<section class="contentList">'
  puts '<section class="UserDisplay" style="max-width: 390px">'
    puts '<img src="./ProfileImages/' + listContent.first['username'] + '.jpg" alt="">'
    puts '<h3>List by <a href="othersProfiles.cgi?username=' + listContent.first['username'] + '">' + displayName.first['displayName'] + '</a></h3>'
  puts '</section>'
  puts '<br>'
  puts '<section class="titleLike">'
  puts '<h1>' + listTitle.to_s + '</h1>'
  (0...likes.size).each do |j|
  if likes[j]['userWhoLiked'] == username.to_s
    alreadyLiked = true
  end
end

puts '<form  class="LikeAndCount" action="listContents.cgi" method="post">'
      #alreadyLiked = db.query("SELECT * FROM likedList WHERE userWhoLiked = '" + username.to_s + "' AND userWhoCreated = '" + lists[i]['username'] + "' AND listId = '" + listId.first['id'].to_s + "';")
      
      if (alreadyLiked)
        puts '<button class="LIKES" style="color: pink;">&#10084</button>'
      else
        puts '<button class="LIKES">&#10084</button>'
        end
        puts '<a href="whoHasLiked.cgi?listName=' + listTitle + '&listCreator=' + listContent.first['username'] + '&listId=' + listId.first['id'].to_s + '">' + likes.size.to_s + '</a>'
        puts '<input type="hidden" name="likedList" value="TRUE">'
        puts '<input type="hidden" name="listId" value="' + listId.first['id'].to_s + '">'
        #puts '<input type="hidden" name="likeUser" value="' + username.to_s + '">'
        puts '<input type="hidden" name="listCreator" value="' + listContent.first['username'] + '">'
        puts '<input type="hidden" name="title" value="' + listTitle + '">'
        puts '<input type="hidden" name="contentType" value="' + type + '">'
        
    puts '</form>'
    puts '</section>'
  puts '<hr>'
  puts '<section class="contents">'
  puts '<div class="listContents">'
  (0...listContent.size).each do |i|
    puts '<div class="listItem">'
        puts '<form action="series.cgi" method="POST" style="height: 350px; width: 175px;">'
          puts '<input type="image" src="' + listContent[i]['imageName'] + '" alt="' + listContent[i]['imageName'] + '" style="height: 80%; width: 170px; object-fit: cover;">'
          puts '<input type="hidden" name="clicked_image" value="' + listContent[i]['imageName'] + '">'
          puts '<input type="hidden" name="seasonNumber" value="1">'
          puts '<h6 style="text-align: center;">' + listContent[i]['showName'] + '</h6>'
          if type != "SERIES" && type != "SEASON"
            puts '<h6 style="text-align: center">S' + listContent[i]['seasonNum'].to_s + ' ' + listContent[i]['epName'] + '</h6>'
          elsif type == "SEASON"
            puts '<h6 style="text-align: center">Season ' + listContent[i]['seasonNum'].to_s + '</h6>'
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