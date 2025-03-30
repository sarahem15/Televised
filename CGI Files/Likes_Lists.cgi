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

#listImages = db.query("SELECT imageName FROM list;")

displayName = db.query("SELECT displayName FROM account WHERE username = '" + username.to_s + "';")
bio = db.query("SELECT bio FROM account WHERE username = '" + username.to_s + "';")
pronouns = db.query("SELECT pronouns FROM account WHERE username = '" + username.to_s + "';")
likedLists = db.query("SELECT * FROM likedList WHERE userWhoLiked = '" + username.to_s + "';")
likedLists = likedLists.to_a
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
      puts '<a href="Profile.cgi">Profile</a>'
      puts '<a href="Have_Watched.cgi">Have Watched</a>'
      puts '<a href="Want_to_Watch.cgi">Want to Watch</a>'
      puts '<a href="Profile_Lists.cgi">Lists</a>'
      puts '<a href="Profile_Reviews.cgi">Reviews</a>'
      puts '<a href="#" class="active">Likes</a>'
      puts '<a href="Profile_Ratings.cgi">Ratings</a>'
    puts '</div>'
  puts '<hr>'
  puts '<br>'
  
  puts '<div class="profileListHeader">'
      puts '<a href="#">Reviews</a>'
      puts '<a href="#" class="active">Lists</a>'
    puts '</div>'

puts '<hr style="margin-left: 80px; margin-right: 80px">'
(0...likedLists.size).each do |i|
  seriesImages = db.query("SELECT series.imageName FROM series JOIN curatedListSeries ON curatedListSeries.seriesId = series.showId WHERE curatedListSeries.listId ='" + likedLists[i]['listId'].to_s + "';")
  seriesImages = seriesImages.to_a
  info = db.query("SELECT * FROM curatedListSeries WHERE listId = '" + likedLists[i]['listId'].to_s + "';")
  info = info.to_a
  listDisplayName = db.query("SELECT displayName FROM account WHERE username = '" + info[i]['username'] + "';")
  puts '<div class="listImages">'
    puts '<div class="listWrapper">'
        puts '<section class="carousel-section" id="listsPlease">'
        (0...5).each do |j|
          if i < seriesImages.size
            puts '<div class="itemS">'
                puts '<img src="' + seriesImages[j]['imageName'] + '" alt="' + seriesImages[j]['imageName'] + '" style="height:270px; object-fit: cover;">'
            puts '</div>'
          end
        end
      puts '</section>'
      puts '</div>'
      puts '<div>'
      puts '<section class="titleDate">'
      puts '<a href="listContents.cgi?title=' + info[i]['name'] + '"><h3>' + info[i]['name'] + '</h3></a>'
      puts '<i><h4>' + info[i]['date'].to_s + '</h4></i>'
      puts '</section>'
      puts '<br>'
      puts '<section class="listInfo">'
        puts '<section class="UserDisplay">'
          puts '<img src="./ProfileImages/' + info[i]['username'] + '.jpg" alt="">'
          puts '<a href="othersProfiles.cgi?username=' + info[i]['username'] + '"><h3 id="DisplayName">' + listDisplayName.first['displayName'].to_s + '</h3></a>'
        puts '</section>'
      puts '<h3> series </h3>'
      listId = db.query("SELECT id FROM listOwnership WHERE username = '" + info[i]['username'] + "' AND listName = '" + info[i]['name'] + "';")
      puts '<form action="threebuttons.cgi" method="post">'
      alreadyLiked = db.query("SELECT * FROM likedList WHERE userWhoLiked = '" + username.to_s + "' AND userWhoCreated = '" + info[i]['username'] + "' AND listId = '" + listId.first['id'].to_s + "';")
        puts '<button class="LIKES" style="color: pink;">&#10084</button>'
        currentLikes = db.query("SELECT * FROM likedList WHERE listId = '" + listId.first['id'].to_s + "';")
        (0...currentLikes.size).each do |i|
        likeCount = likeCount + 1
      end
        puts '<a href="whoHasLiked.cgi?listName=' + info[i]['name'] + '&listCreator=' + info[i]['username'] + '&listId=' + listId.first['id'].to_s + '">' + likeCount.to_s + '</a>'
        puts '<input type="hidden" name="likedList" value="TRUE">'
        puts '<input type="hidden" name="profileLikedList" value="TRUE">'
        puts '<input type="hidden" name="listId" value="' + listId.first['id'].to_s + '">'
        puts '<input type="hidden" name="likeUser" value="' + username.to_s + '">'
        puts '<input type="hidden" name="listCreator" value="' + info[i]['username'] + '">'
        
    puts '</form>'
      puts '</section>'
      puts '<h3>' + info[i]['description'] + '</h3>'
      puts '</div>'
    puts '</div>'
     puts '<br>'
puts '<hr style="margin-left: 80px; margin-right: 80px">'
end
 puts '<br>'
  puts '<br>'
    puts '<!-- Scripts -->'
  puts '<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>'
  puts '<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>'
  puts '<script src="Televised.js"></script>'
puts '</body>'
puts '</html>'