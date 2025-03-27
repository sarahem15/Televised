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
username = session['username'].to_s

db = Mysql2::Client.new(
    host: '10.20.3.4', 
    username: 'seniorproject25', 
    password: 'TV_Group123!', 
    database: 'televised_w25'
  )

listName = cgi['listName']
listId = cgi['listId']
listCreator = cgi['listCreator']
displayName = db.query("SELECT displayName FROM account WHERE username = '" + username + "';")
likes = db.query("SELECT * FROM likedList WHERE listId = '" + listId + "';")
likes = likes.to_a

listImages = db.query ("SELECT imageName FROM series JOIN curatedListSeries ON curatedListSeries.seriesId = series.showId WHERE curatedListSeries.name ='" + listName + "';")
listImages = listImages.to_a

puts '<!DOCTYPE html>'
puts '<html lang="en">'

puts '<head>'
puts "<meta charset=\"UTF-8\">"
    puts "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">"
    puts "<title>Televised</title>"
    puts "<link href=\"https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css\" rel=\"stylesheet\">"
    puts "<link rel=\"stylesheet\" href=\"Televised.css\">"
puts "</head>"
puts "<body id=\"whoLiked\">"
    puts "<nav id=\"changingNav\"></nav>"
    puts '<br>'
    puts '<br>'
    puts '<section class="LikesContent" style="margin-left: 5%; margin-right: 5%;">'
  puts '<section class="UserDisplay" style="max-width: 390px">'
    puts '<img src="./ProfileImages/' + username + '.jpg" alt="here">'
    puts '<h3 style="color: #a3afe1;">Likes for ' + displayName.first['displayName'].to_s + '\'s List</h3>'
  puts '</section>'
  puts '<br>'
  puts '<h1>' + listName + '</h1>'
  puts '<hr style="border-width: 5px; color: #a3afe1;">'
  puts '<div class="Content-type">'
  puts '<section>'
  puts '<h5 id="nameHeader"> Name </h5>'
  puts '<br>'
    (0...likes.size).each do |i|
        likeDisplayName = db.query("SELECT displayName FROM account JOIN likedList ON likedList.userWhoLiked = account.username WHERE likedList.userWhoLiked = '" + likes[i]['userWhoLiked'] + "';")
        puts '<section class="UserDisplay" style="max-width: 390px">'
            puts '<img src="./ProfileImages/' + likes[i]['userWhoLiked'] + '.jpg" alt="">'
            puts '<h3>' + likeDisplayName.first['displayName'].to_s + '</h3>'
        puts '</section>'
    end

  puts '</section>'
  puts '<section>'
  puts '<section class="images">'
  (0...listImages.size).each do |i|
    puts '<img src="' + listImages[i]['imageName'] + '" alt="">'
   end
  puts '</section>'
  puts '<br>'
  puts '<h6 style="text-align: center;">' + listImages.size.to_s + ' shows</h6>'
  puts '</section>'
  puts '</div>'
puts '</section>'
puts '<!-- Scripts -->'
  puts '<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>'
  puts '<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>'
  puts '<script src="Televised.js"></script>'
puts '</body>'
puts '</html>'
session.close