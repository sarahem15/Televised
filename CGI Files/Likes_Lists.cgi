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

db = Mysql2::Client.new(
    host: '10.20.3.4', 
    username: 'seniorproject25', 
    password: 'TV_Group123!', 
    database: 'televised_w25'
  )

#listImages = db.query("SELECT imageName FROM list;")
seriesImages = db.query("SELECT imageName FROM series;")
seriesImages = seriesImages.to_a()

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
  puts '<section class="UserDisplay">'
    puts '<img src="./Episodes/adventureTime1.1.jpg" alt="testing123">'
    puts '<h3 id=" DisplayName"> DisplayName </h3>'
  puts '</section>'

  puts '<hr>'
     puts '<div class="profileHeader">'
      puts '<a href="Profile.html">Profile</a>'
      puts '<a href="Have_Watched.html">Have Watched</a>'
      puts '<a href="Want_to_Watch.html">Want to Watch</a>'
      puts '<a href="Profile_Lists.cgi">Lists</a>'
      puts '<a href="#">Reviews</a>'
      puts '<a href="#" class="active">Likes</a>'
      puts '<a href="#">Ratings</a>'
    puts '</div>'
  puts '<hr>'
  puts '<br>'
  
  puts '<div class="profileListHeader">'
      puts '<a href="#">Reviews</a>'
      puts '<a href="#" class="active">Lists</a>'
    puts '</div>'

(0...5).each do |i|
puts '<hr style="margin-left: 80px; margin-right: 80px">'
  puts '<div class="listImages">'
    puts '<div class="listWrapper">'
        puts '<section class="carousel-section" id="listsPlease">'
        (0...5).each do |j|
        puts '<div class="itemS">'
            puts '<img src="' + seriesImages[j]['imageName'] + '" alt="' + seriesImages[j]['imageName'] + '">'
        puts '</div>'
        end
      puts '</section>'
      puts '</div>'
      puts '<div>'
      puts '<section class="titleDate">'
      puts '<h1>LIST TITLE</h1>'
      puts '<h4>DATE</h4>'
      puts '</section>'

      puts '<h3>DESCRIPTION of the list goes here!!</h3>'
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