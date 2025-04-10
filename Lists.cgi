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

db = Mysql2::Client.new(
    host: '10.20.3.4', 
    username: 'seniorproject25', 
    password: 'TV_Group123!', 
    database: 'televised_w25'
  )

seriesImages = db.query("SELECT imageName FROM series;")
seriesImages = seriesImages.to_a()
lists = db.query("SELECT DISTINCT name, description, username, date FROM curatedListSeries WHERE privacy = 1;")
lists = lists.to_a
likeCount = 0
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

puts '<body id="ListsPage">'
  puts '<nav id="changingNav"></nav> <!-- This is where the navbar will be dynamically loaded -->'
  puts '<div class="container-fluid">'
  puts '<br>'
  puts '<h1 class="text-center text-white mt-5">Find a List!</h1>'
  puts '<br>'
  puts '<button id="newListProfile" class="createListButton" style="margin: auto;"> <a href="createNewList.cgi"> Create a New List </a> </button>'
  puts '<h5 class="text-center text-white mt-5">See some lists created by fellow users.</h5>'
  #puts '<br>'
  #puts '<hr style="margin-left: 80px; margin-right: 80px">'
if (seriesTab == "SERIES")
    puts '<div class="center mt-5">'
    puts '<div class="pagination">'
            puts '<a class="active" href="Lists.cgi?seriesTab=SERIES">Series</a>'
            puts '<a href="Lists.cgi?seriesTab=SEASON">Season</a>'
            puts '<a href="Lists.cgi?seriesTab=EP">Episode</a>'
          puts '</div>'
        puts '</div>'
elsif (seriesTab == "SEASON")
    puts '<div class="center mt-5">'
    puts '<div class="pagination">'
            puts '<a href="Lists.cgi?seriesTab=SERIES">Series</a>'
            puts '<a class="active" href="Lists.cgi?seriesTab=SEASON">Season</a>'
            puts '<a href="Lists.cgi?seriesTab=EP">Episode</a>'
          puts '</div>'
        puts '</div>'
elsif (seriesTab == "EP")
    puts '<div class="center mt-5">'
    puts '<div class="pagination">'
            puts '<a href="Lists.cgi?seriesTab=SERIES">Series</a>'
            puts '<a href="Lists.cgi?seriesTab=SEASON">Season</a>'
            puts '<a class="active" href="Lists.cgi?seriesTab=EP">Episode</a>'
          puts '</div>'
        puts '</div>'
    end
puts '<hr style="margin-left: 80px; margin-right: 80px">'
puts '<br>'
if seriesTab == "SERIES"
(0...lists.size).each do |i|

  puts '<div class="listImages">'
    puts '<div class="listWrapper">'
        puts '<section class="carousel-section" id="listsPlease">'
        listImages = db.query("SELECT imageName FROM series JOIN curatedListSeries ON series.showId = curatedListSeries.seriesId WHERE name = '" + lists[i]['name'].gsub("'", "\\\\'") + "';")
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
      puts '<a href="listContents.cgi?title='+ lists[i]['name'].gsub("'", "\\\\'") + '&contentType=SERIES">' + lists[i]['name'] + '</a>'
      puts '<i><h4>' + lists[i]['date'].to_s + '</h4></i>'
      puts '</section>'
      puts '<br>'
      puts '<section class="UserDisplay">'
          puts '<img src="./ProfileImages/' + lists[i]['username'].to_s + '.jpg" alt="" style="background-color: gray;">'
          puts '<a href="othersProfiles.cgi?username=' + lists[i]['username'].to_s + '"><h3 id="DisplayName">' + displayName.first['displayName'].to_s + '</h3></a>'
        puts '</section>'
        puts '<br>'
      puts '<h3>' + lists[i]['description'] +'</h3>'
        
        listId = db.query("SELECT id FROM listOwnership WHERE username = '" + lists[i]['username'] + "' AND listName = '" + lists[i]['name'].gsub("'", "\\\\'") + "';")
      puts '<form action="threebuttons.cgi" method="post">'
      alreadyLiked = db.query("SELECT * FROM likedList WHERE userWhoLiked = '" + username.to_s + "' AND userWhoCreated = '" + lists[i]['username'] + "' AND listId = '" + listId.first['id'].to_s + "';")
      
      if (alreadyLiked.to_a != [])
        puts '<button class="LIKES" style="color: pink;">&#10084</button>'
      else
        puts '<button class="LIKES">&#10084</button>'
        end
        currentLikes = db.query("SELECT * FROM likedList WHERE listId = '" + listId.first['id'].to_s + "';")
      (0...currentLikes.size).each do |i|
        likeCount = likeCount + 1
      end
        puts '<a href="whoHasLiked.cgi?listName=' + lists[i]['name'].gsub("'", "\\\\'") + '&listCreator=' + lists[i]['username'] + '&listId=' + listId.first['id'].to_s + '">' + likeCount.to_s + '</a>'

        puts '<input type="hidden" name="likedList" value="TRUE">'
        puts '<input type="hidden" name="listId" value="' + listId.first['id'].to_s + '">'
        puts '<input type="hidden" name="likeUser" value="' + username.to_s + '">'
        puts '<input type="hidden" name="listCreator" value="' + lists[i]['username'] + '">'
        
    puts '</form>'
      puts '</div>'
    puts '</div>'
    puts '<br>'
    puts '<hr style="margin-left: 80px; margin-right: 80px">'
    likeCount = 0
end

elsif seriesTab == "EP"

lists = db.query("SELECT DISTINCT name, description, username, date FROM curatedListEpisode WHERE privacy = 1;")
lists = lists.to_a
(0...lists.size).each do |i|

  puts '<div class="listImages">'
    puts '<div class="listWrapper">'
        puts '<section class="carousel-section" id="listsPlease">'
        listImages = db.query("SELECT imageName FROM series JOIN season ON season.seriesId = series.showId JOIN episode ON episode.seasonId = season.seasonId JOIN curatedListEpisode ON episode.epId = curatedListEpisode.epId WHERE name = '" + lists[i]['name'] + "';")
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
      puts '<a href="listContents.cgi?title='+ lists[i]['name'] + '&contentType=EPISODE">' + lists[i]['name'] + '</a>'
      puts '<i><h4>' + lists[i]['date'].to_s + '</h4></i>'
      puts '</section>'
      puts '<br>'
      puts '<section class="UserDisplay">'
          puts '<img src="./ProfileImages/' + lists[i]['username'].to_s + '.jpg" alt="" style="background-color: gray;">'
          puts '<a href="othersProfiles.cgi?username=' + lists[i]['username'].to_s + '"><h3 id="DisplayName">' + displayName.first['displayName'].to_s + '</h3></a>'
        puts '</section>'
        puts '<br>'
      puts '<h3>' + lists[i]['description'] +'</h3>'
        
        listId = db.query("SELECT id FROM listOwnership WHERE username = '" + lists[i]['username'] + "' AND listName = '" + lists[i]['name'].gsub("'", "\\\\'") + "';")
      puts '<form action="threebuttons.cgi" method="post">'
      alreadyLiked = db.query("SELECT * FROM likedList WHERE userWhoLiked = '" + username.to_s + "' AND userWhoCreated = '" + lists[i]['username'] + "' AND listId = '" + listId.first['id'].to_s + "';")
      
      if (alreadyLiked.to_a != [])
        puts '<button class="LIKES" style="color: pink;">&#10084</button>'
      else
        puts '<button class="LIKES">&#10084</button>'
        end
        currentLikes = db.query("SELECT * FROM likedList WHERE listId = '" + listId.first['id'].to_s + "';")
      (0...currentLikes.size).each do |i|
        likeCount = likeCount + 1
      end
        puts '<a href="whoHasLiked.cgi?listName=' + lists[i]['name'].gsub("'", "\\\\'") + '&listCreator=' + lists[i]['username'] + '&listId=' + listId.first['id'].to_s + '">' + likeCount.to_s + '</a>'

        puts '<input type="hidden" name="likedList" value="TRUE">'
        puts '<input type="hidden" name="listId" value="' + listId.first['id'].to_s + '">'
        puts '<input type="hidden" name="likeUser" value="' + username.to_s + '">'
        puts '<input type="hidden" name="listCreator" value="' + lists[i]['username'] + '">'
        
    puts '</form>'
      puts '</div>'
    puts '</div>'
    puts '<br>'
    puts '<hr style="margin-left: 80px; margin-right: 80px">'
    likeCount = 0
end


else
lists = db.query("SELECT DISTINCT name, description, username, date FROM curatedListSeason WHERE privacy = 1;")
lists = lists.to_a
(0...lists.size).each do |i|
  puts '<div class="listImages">'
    puts '<div class="listWrapper">'
        puts '<section class="carousel-section" id="listsPlease">'
        listImages = db.query("SELECT imageName FROM series JOIN season ON season.seriesId = series.showId JOIN curatedListSeason ON season.seasonId = curatedListSeason.seasonId WHERE name = '" + lists[i]['name'].gsub("'", "\\\\'") + "';")
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
      puts '<a href="listContents.cgi?title='+ lists[i]['name'] + '&contentType=SEASON">' + lists[i]['name'] + '</a>'
      puts '<i><h4>' + lists[i]['date'].to_s + '</h4></i>'
      puts '</section>'
      puts '<br>'
      puts '<section class="UserDisplay">'
          puts '<img src="./ProfileImages/' + lists[i]['username'].to_s + '.jpg" alt="" style="background-color: gray;">'
          puts '<a href="othersProfiles.cgi?username=' + lists[i]['username'].to_s + '"><h3 id="DisplayName">' + displayName.first['displayName'].to_s + '</h3></a>'
        puts '</section>'
        puts '<br>'
      puts '<h3>' + lists[i]['description'] +'</h3>'
        
        listId = db.query("SELECT id FROM listOwnership WHERE username = '" + lists[i]['username'] + "' AND listName = '" + lists[i]['name'].gsub("'", "\\\\'") + "';")
      puts '<form action="threebuttons.cgi" method="post">'
      alreadyLiked = db.query("SELECT * FROM likedList WHERE userWhoLiked = '" + username.to_s + "' AND userWhoCreated = '" + lists[i]['username'] + "' AND listId = '" + listId.first['id'].to_s + "';")
      
      if (alreadyLiked.to_a != [])
        puts '<button class="LIKES" style="color: pink;">&#10084</button>'
      else
        puts '<button class="LIKES">&#10084</button>'
        end
        currentLikes = db.query("SELECT * FROM likedList WHERE listId = '" + listId.first['id'].to_s + "';")
      (0...currentLikes.size).each do |i|
        likeCount = likeCount + 1
      end
        puts '<a href="whoHasLiked.cgi?listName=' + lists[i]['name'] + '&listCreator=' + lists[i]['username'] + '&listId=' + listId.first['id'].to_s + '">' + likeCount.to_s + '</a>'

        puts '<input type="hidden" name="likedList" value="TRUE">'
        puts '<input type="hidden" name="listId" value="' + listId.first['id'].to_s + '">'
        puts '<input type="hidden" name="likeUser" value="' + username.to_s + '">'
        puts '<input type="hidden" name="listCreator" value="' + lists[i]['username'] + '">'
        
    puts '</form>'
      puts '</div>'
    puts '</div>'
    puts '<br>'
    puts '<hr style="margin-left: 80px; margin-right: 80px">'
    likeCount = 0
end
end
puts '<br>'
if (seriesTab == "SERIES")
    puts '<div class="center mt-5">'
    puts '<div class="pagination">'
            puts '<a class="active" href="Lists.cgi?seriesTab=SERIES">Series</a>'
            puts '<a href="Lists.cgi?seriesTab=SEASON">Season</a>'
            puts '<a href="Lists.cgi?seriesTab=EP">Episode</a>'
          puts '</div>'
        puts '</div>'
elsif (seriesTab == "SEASON")
    puts '<div class="center mt-5">'
    puts '<div class="pagination">'
            puts '<a href="Lists.cgi?seriesTab=SERIES">Series</a>'
            puts '<a class="active" href="Lists.cgi?seriesTab=SEASON">Season</a>'
            puts '<a href="Lists.cgi?seriesTab=EP">Episode</a>'
          puts '</div>'
        puts '</div>'
elsif (seriesTab == "EP")
    puts '<div class="center mt-5">'
    puts '<div class="pagination">'
            puts '<a href="Lists.cgi?seriesTab=SERIES">Series</a>'
            puts '<a href="Lists.cgi?seriesTab=SEASON">Season</a>'
            puts '<a class="active" href="Lists.cgi?seriesTab=EP">Episode</a>'
          puts '</div>'
        puts '</div>'
    end
puts '<br>'
    puts '<!-- Scripts -->'
  puts '<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>'
  puts '<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>'
  puts '<script src="Televised.js"></script>'
puts '</body>'
puts '</html>'
session.close


=begin
.LIKES {
    background-color: transparent;
    color: white;
    font-size: 30px;
    padding: 0;
}

.LIKES:hover {color: pink; background-color: transparent;}

.LIKES active {
    color: red;
}
=end