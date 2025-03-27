#!/usr/bin/ruby
# Switch images to queries from the database
# Enable debugging
#Display in ascending order when date field is added
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
#username = "try@try"
seriesId = cgi['seriesID']
seasonNum = cgi['seasonNum']
epId = cgi['epId']
if epId != ""
    epSearch = true
else
    epSearch = false
end

if epId == "" && seasonNum != ""
    seasonSearch = true
else
    seasonSearch = false
end
db = Mysql2::Client.new(
    host: '10.20.3.4', 
    username: 'seniorproject25', 
    password: 'TV_Group123!', 
    database: 'televised_w25'
  )

seriesImages = db.query("SELECT imageName FROM series;")
seriesImages = seriesImages.to_a()
lists = db.query("SELECT name, description, username, date FROM curatedListSeries WHERE seriesId ='" + seriesId + "' AND privacy = 1;")
lists = lists.to_a
showName = db.query("SELECT showName FROM series WHERE showId = '" + seriesId + "';")
likeCount = 0


puts '<!DOCTYPE html>'
puts '<html lang="en">'

puts '<head>'
puts '<meta charset="UTF-8">'
  puts '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
  puts '<title>Televised</title>'
  puts '<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">'
  puts '<link rel="stylesheet" href="Televised.css">'
puts '</head>'

puts '<body id="viewOnOtherLists">'
  puts '<nav id="changingNav"></nav> <!-- This is where the navbar will be dynamically loaded -->'
  puts '<div class="container-fluid">'
  puts '<br>'
  puts '<h1>Lists containing ' + showName.first['showName'] + '!</h1>'
  puts '<br>'

if (lists.size == 0)
    puts '<hr style="margin-left: 80px; margin-right: 80px">'
    puts '<h5 style="text-align: center;">Looks like there are no lists containing this title!</h5>'
else
(0...lists.size).each do |i|
puts '<hr style="margin-left: 80px; margin-right: 80px">'
  puts '<div class="listImages">'
    puts '<div class="listWrapper">'
        puts '<section class="carousel-section" id="listsPlease">'
        listImages = db.query("SELECT imageName FROM series JOIN curatedListSeries ON series.showId = curatedListSeries.seriesId WHERE name = '" + lists[i]['name'] + "';")
        listImages = listImages.to_a
        displayName = db.query("SELECT displayName FROM account WHERE username = '" + lists[i]['username'] + "';")
        (0...5).each do |j|
        puts '<div class="itemS">'
        if (j < listImages.size)
            puts '<img src="' + listImages[j]['imageName'] + '" alt="' + listImages[j]['imageName'] + '" style="height:270px; object-fit: cover;">'
        else
            puts '<img src="" alt="">'
        end
        puts '</div>'
        end
      puts '</section>'
      puts '</div>'
      puts '<div>'
      puts '<section class="titleDate">'
      puts '<a href="listContents.cgi?title='+ lists[i]['name'] + '">' + lists[i]['name'] + '</a>'
      puts '<i><h4>' + lists[i]['date'].to_s + '</h4></i>'
      puts '</section>'
      puts '<br>'
      puts '<section class="UserDisplay">'
          puts '<img src="./ProfileImages/' + lists[i]['username'].to_s + '.jpg" alt="userProfilePic">'
          puts '<h3 id=" DisplayName">' + displayName.first['displayName'] + '</h3>'
        puts '</section>'
        puts '<br>'
      puts '<h3>' + lists[i]['description'] +'</h3>'

      listId = db.query("SELECT id FROM listOwnership WHERE username = '" + lists[i]['username'] + "' AND listName = '" + lists[i]['name'] + "';")
      puts '<form action="threebuttons.cgi" method="post">'
      alreadyLiked = db.query("SELECT * FROM likedList WHERE userWhoLiked = '" + username.to_s + "' AND userWhoCreated = '" + lists[i]['username'] + "' AND listId = '" + listId.first['id'].to_s + "';")
      (0...alreadyLiked.size).each do |i|
        likeCount = likeCount + 1
      end
      if (alreadyLiked.to_a != [])
        puts '<button class="LIKES" style="color: pink;">&#10084</button>'
        puts '<a href="whoHasLiked.cgi?listName=' + lists[i]['name'] + '&listCreator=' + lists[i]['username'] + '&listId=' + listId.first['id'].to_s + '">' + likeCount.to_s + '</a>'
        puts '<input type="hidden" name="likedList" value="TRUE">'
        puts '<input type="hidden" name="listId" value="' + listId.first['id'].to_s + '">'
        puts '<input type="hidden" name="likeUser" value="' + username.to_s + '">'
        puts '<input type="hidden" name="listCreator" value="' + lists[i]['username'] + '">'
        end
    puts '</form>'

      puts '</div>'
    puts '</div>'
    puts '<br>'
end
end
    puts '<!-- Scripts -->'
  puts '<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>'
  puts '<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>'
  puts '<script src="Televised.js"></script>'
puts '</body>'
puts '</html>'
session.close