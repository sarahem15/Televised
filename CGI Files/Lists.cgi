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
  puts '<h5 class="text-center text-white mt-5">See some lists created by fellow users.</h5>'
  puts '<br>'


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
      puts '<a href="listContents.cgi?title='+ lists[i]['name'] + '">' + lists[i]['name'] + '</a>'
      puts '<h4>' + lists[i]['date'].to_s + '</h4>'
      puts '</section>'
      puts '<br>'
      puts '<section class="UserDisplay">'
          puts '<img src="./ProfileImages/' + lists[i]['username'].to_s + '.jpg" alt="userProfilePic">'
          puts '<a href="othersProfiles.cgi?username=' + lists[i]['username'].to_s + '"><h3 id="DisplayName">' + displayName.first['displayName'].to_s + '</h3></a>'
        puts '</section>'
        puts '<br>'
      puts '<h3>' + lists[i]['description'] +'</h3>'
    

      if (1 == 1)
        puts '<button class="LIKES" style="color: pink;">&#10084</button>'
      else
        puts '<button class="LIKES">&#10084</button>'
    end
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