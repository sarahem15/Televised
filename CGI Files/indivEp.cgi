#!/usr/bin/ruby
$stdout.sync = true
$stderr.reopen $stdout

puts "Content-type: text/html\n\n"
require 'mysql2'
require 'cgi'

cgi = CGI.new
episodeName = cgi['ep_name']
showName = cgi['show_name']
epNum = cgi['ep_num']
db = Mysql2::Client.new(
    host: '10.20.3.4', 
    username: 'seniorproject25', 
    password: 'TV_Group123!', 
    database: 'televised_w25'
  )

episode = db.query("SELECT * FROM episode WHERE epName = '" + episodeName + "';")

puts "<!DOCTYPE html>"
puts "<html lang=\"en\">"
puts "<head>"
    puts "<meta charset=\"UTF-8\">"
    puts "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">"
    puts "<title>Televised</title>"
    puts "<link href=\"https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css\" rel=\"stylesheet\">"
    puts "<link rel=\"stylesheet\" href=\"Televised.css\">"
puts "</head>"
puts "<body id=\"episodePage\">"
    puts "<nav id=\"changingNav\"></nav>"

    puts "<script src=\"https://code.jquery.com/jquery-3.6.0.min.js\"></script>"
    puts "<script src=\"https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js\"></script>"
    puts "<script src=\"Televised.js\"></script>"

  puts "<br>"
  puts "<div class=\"episodesPage\">"


  #HERE
  
    puts "<img src=\"H2O.jpg\"alt=\"placeholder\">\n" 
    puts "<br>"

      puts "<h1 style=\"font-family: 'Times New Roman', Times, serif; color: white; text-align: left;\">" + showName + "</h1>"
      puts "<div class=\"epWords\">"
      puts "<h3 style=\"font-family: 'Times New Roman', Times, serif; color: #436eb1; text-align: left;\"> Season 1 </h2>"
      puts "<br>"
      puts "<h3 style=\"font-family: 'Times New Roman', Times, serif; color: white; text-align: left;\"> Episode " + epNum.to_s + "</h4>"
      puts "<br>"
      puts "<h3 style=\"font-family: 'Times New Roman', Times, serif; color: #436eb1; text-align: left;\"> RATING </h4>"
      puts "<br>"
    puts "</div>"
    puts "<div class=\"epWords\">"
      puts "<h3 style=\"font-family: 'Times New Roman', Times, serif; color: #436eb1; text-align: left;\">" + episode.first['epName'] + "</h2>"
      puts "<br>"
      puts "<h3 style=\"font-family: 'Times New Roman', Times, serif; color: white; text-align: left;\">" + episode.first['releaseDate'] + "</h4>"
      puts "<br>"
      puts "<h3 style=\"font-family: 'Times New Roman', Times, serif; color: #436eb1; text-align: left;\"" + episode.first['runTime'].to_s + "</h4>"
      puts "<br>"
    puts "</div>"
   puts "<br>"
  puts "<h4 style=\"font-family: 'Times New Roman', Times, serif; color: white; text-align: left;\">Description: "
  puts "<span>" + episode.first['description'] + "</span></h4>"

#Buttons!

  puts "<h4 style=\"font-family: 'Times New Roman', Times, serif; color: white; text-align: left;\">Cast: "
    puts "<span>" + episode.first['topCast'] + "</span>"
  puts "</h4>"

  puts "<br>"
  puts "<hr>"

  puts '<section class="epReviews">'
  puts '<div class="ReviewIndiv">'
  puts '<div class="ReviewContent">'
      puts '<section class="UserDisplay">'
          puts '<img src="./Episodes/adventureTime1.1.jpg" alt="here">'
          puts '<h3> Username </h3>'
          #RATING!
      puts '</section>'
      puts '<br>'
      puts '<br>'
      puts '<h4> This show is great! </h4>'
      puts '<section class="Likes">'
        puts '<h5>&#9829</h5>'
        puts '<h4>12</h4>' #db query to get likes
      puts '</section>'
  puts '</div>'
puts '</div>'
puts '<div class="ReviewIndiv">'
  puts '<div class="ReviewContent">'
      puts '<section class="UserDisplay">'
          puts '<img src="./Episodes/adventureTime1.1.jpg" alt="here">'
          puts '<h3> Username </h3>'
          #RATING!
      puts '</section>'
      puts '<br>'
      puts '<br>'
      puts '<h4> This show is great! </h4>'
      puts '<section class="Likes">'
        puts '<h5>&#9829</h5>'
        puts '<h4>12</h4>' #db query to get likes
      puts '</section>'
  puts '</div>'
puts '</div>'
puts '<div class="ReviewIndiv">'
  puts '<div class="ReviewContent">'
      puts '<section class="UserDisplay">'
          puts '<img src="./Episodes/adventureTime1.1.jpg" alt="here">'
          puts '<h3> Username </h3>'
          #RATING!
      puts '</section>'
      puts '<br>'
      puts '<br>'
      puts '<h4> This show is great! </h4>'
      puts '<section class="Likes">'
        puts '<h5>&#9829</h5>'
        puts '<h4>12</h4>' #db query to get likes
      puts '</section>'
  puts '</div>'
puts '</div>'
puts '<div class="ReviewIndiv">'
  puts '<div class="ReviewContent">'
      puts '<section class="UserDisplay">'
          puts '<img src="./Episodes/adventureTime1.1.jpg" alt="here">'
          puts '<h3> Username </h3>'
          #RATING!
      puts '</section>'
      puts '<br>'
      puts '<br>'
      puts '<h4> This show is great! </h4>'
      puts '<section class="Likes">'
        puts '<h5>&#9829</h5>'
        puts '<h4>12</h4>' #db query to get likes
      puts '</section>'
  puts '</div>'
puts '</div>'
puts '<div class="ReviewIndiv">'
  puts '<div class="ReviewContent">'
      puts '<section class="UserDisplay">'
          puts '<img src="./Episodes/adventureTime1.1.jpg" alt="here">'
          puts '<h3> Username </h3>'
          #RATING!
      puts '</section>'
      puts '<br>'
      puts '<br>'
      puts '<h4> This show is great! </h4>'
      puts '<section class="Likes">'
        puts '<h5>&#9829</h5>'
        puts '<h4>12</h4>' #db query to get likes
      puts '</section>'
  puts '</div>'
puts '</div>'
puts '<div class="ReviewIndiv">'
  puts '<div class="ReviewContent">'
      puts '<section class="UserDisplay">'
          puts '<img src="./Episodes/adventureTime1.1.jpg" alt="here">'
          puts '<h3> Username </h3>'
          #RATING!
      puts '</section>'
      puts '<br>'
      puts '<br>'
      puts '<h4> This show is great! </h4>'
      puts '<section class="Likes">'
        puts '<h5>&#9829</h5>'
        puts '<h4>12</h4>' #db query to get likes
      puts '</section>'
  puts '</div>'
puts '</div>'


puts '</section>'

puts "</div>"

puts "</body>"
puts "</html>"