/mnt/web/www/Televised/Profile_Lists.cgi:161:in `+': no implicit conversion of Date into String (TypeError) from /mnt/web/www/Televised/Profile_Lists.cgi:161:in `block in
' from /mnt/web/www/Televised/Profile_Lists.cgi:132:in `each' from /mnt/web/www/Televised/Profile_Lists.cgi:132:in `
' 

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

# Fetch user information
displayName = db.query("SELECT displayName FROM account WHERE username = '#{username}';")
bio = db.query("SELECT bio FROM account WHERE username = '#{username}';")
pronouns = db.query("SELECT pronouns FROM account WHERE username = '#{username}';")
likeCount = 0
seriesTab = cgi['seriesTab']
if seriesTab == ""
  seriesTab = "SERIES"
end

if cgi['likedList'] == "TRUE"
  db.query("INSERT INTO likedList VALUES('#{username}', '#{cgi['listCreator']}', '#{cgi['listId']}');")
end

# Handle delete request only if form is submitted
if cgi.request_method == 'POST' && cgi['deleteListId']
  delete_list_id = cgi['deleteListId'].to_i

  begin
    # Start a transaction to ensure atomicity
    db.query("START TRANSACTION")

    # Delete from likedList, curatedListSeries, and listOwnership
    db.query("DELETE FROM likedList WHERE listId = #{delete_list_id}")
    db.query("DELETE FROM curatedListSeason WHERE listId = #{delete_list_id}")
    db.query("DELETE FROM curatedListSeries WHERE listId = #{delete_list_id}")
    db.query("DELETE FROM listOwnership WHERE id = #{delete_list_id}")

    # Commit the transaction
    db.query("COMMIT")
    
    # Redirect back to Profile_Lists.cgi after deletion
    puts "<html><body><script>window.location.href='Profile_Lists.cgi';</script></body></html>"
    exit
  rescue Mysql2::Error => e
    # If there's an error, rollback the transaction
    db.query("ROLLBACK")
    puts "<html><body><script>alert('Error deleting list: #{e.message}'); window.location.href='Profile_Lists.cgi';</script></body></html>"
    exit
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
puts '<a href="#!" class="active">Lists</a>'
puts '<a href="Profile_Reviews.cgi">Reviews</a>'
puts '<a href="Likes_Lists.cgi">Likes</a>'
puts '<a href="Profile_Ratings.cgi">Ratings</a>'
puts '</div>'
puts '<hr>'
puts '<br>'

puts '<div class="listProfileButtons">'
puts '<div class="profileListHeader">'

# Handle seriesTab filter
if seriesTab == "SERIES"
  puts '<a href="#"class="active">Series</a>'
  puts '<a href="Profile_Lists.cgi?seriesTab=SEASON">Seasons</a>'
  puts '<a href="Profile_Lists.cgi?seriesTab=EP">Episodes</a>'
  lists = db.query("SELECT DISTINCT name, description, date, username, listId FROM curatedListSeries WHERE username = '#{username}';")
  lists = lists.to_a
elsif seriesTab == "SEASON"
  puts '<a href="Profile_Lists.cgi?seriesTab=SERIES">Series</a>'
  puts '<a href="#" class="active">Seasons</a>'
  puts '<a href="Profile_Lists.cgi?seriesTab=EP">Episodes</a>'
  lists = db.query("SELECT DISTINCT name, description, username, listId FROM curatedListSeason WHERE username = '#{username}';")
  lists = lists.to_a
elsif seriesTab == "EP"
  puts '<a href="Profile_Lists.cgi?seriesTab=SERIES">Series</a>'
  puts '<a href="Profile_Lists.cgi?seriesTab=SEASON">Seasons</a>'
  puts '<a href="#" class="active">Episodes</a>'
  lists = db.query("SELECT DISTINCT name, description, username, listId FROM curatedListEpisode WHERE username = '#{username}';")
  lists = lists.to_a
end
puts '</div>'
puts '<a href="createNewList.cgi"><button id="newListProfile" class="createListButton">Create a New List</button></a>'
puts '</div>'

puts '<hr style="margin-left: 80px; margin-right: 80px">'

(0...lists.size).each do |i|
  puts '<div class="listImages">'
  puts '<div class="listWrapper">'
  puts '<section class="carousel-section" id="listsPlease">'
  if seriesTab == "SERIES"
    listImages = db.query("SELECT imageName FROM series JOIN curatedListSeries ON series.showId = curatedListSeries.seriesId WHERE username = '#{username}' AND name = '#{lists[i]['name']}';")
  elsif seriesTab == "SEASON"
      listImages = db.query("SELECT imageName FROM series JOIN season ON season.seriesId = series.showId JOIN curatedListSeason ON season.seasonId = curatedListSeason.seasonId WHERE username = '#{username}' AND name = '#{lists[i]['name']}';")
  end
  listImages = listImages.to_a
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
  puts '<div class="listNames">'
  puts '<section class="listTitles">'
  puts '<h3>' + lists[i]['name'] + '</h3>'
  puts '</section>'
  puts '<section class="listDescs">'
  puts '<p>' + lists[i]['description'] + '</p>'
  puts '</section>'
  puts '<section class="listDate">'
  puts '<p>' + lists[i]['date'] + '</p>'
  puts '</section>'
  puts '<div class="listOwner">'
  puts '<p>Created by ' + lists[i]['username'] + '</p>'
  puts '</div>'
  puts '</div>'
  puts '<section class="listButtons">'
  # Edit and delete buttons
  puts '<form method="POST" action="createNewList.cgi">'
  puts '<input type="hidden" name="editListId" value="' + lists[i]['listId'].to_s + '">'
  puts '<button type="submit" class="btn btn-warning">Edit List</button>'
  puts '</form>'
  puts '<form method="POST" action="Profile_Lists.cgi">'
  puts '<input type="hidden" name="deleteListId" value="' + lists[i]['listId'].to_s + '">'
  puts '<button type="submit" class="btn btn-danger">Delete List</button>'
  puts '</form>'
  puts '</section>'
  puts '</div>'
end

puts '</body>'
puts '</html>'
