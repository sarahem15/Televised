#!/usr/bin/ruby
$stdout.sync = true
$stderr.reopen $stdout

puts "Content-type: text/html\n\n"
require 'mysql2'
require 'cgi'

cgi = CGI.new
seriesImage = cgi['clicked_image']

db = Mysql2::Client.new(
    host: '10.20.3.4', 
    username: 'seniorproject25', 
    password: 'TV_Group123!', 
    database: 'televised_w25'
  )


series = db.query("SELECT * FROM series WHERE imageName = '" + seriesImage + "';")
mainCast = db.query("SELECT season.mainCast FROM season JOIN series ON season.seriesId = series.showId WHERE series.imageName = '" + seriesImage + "';")

#  genre = db.query("SELECT showName FROM series WHERE genre = 'Comedy';")
#  puts "<p>am:" + mainCast.first['mainCast'].to_s + "</p>"

puts "<!DOCTYPE html>"
puts "<html lang=\"en\">"
puts "<head>"
    puts "<meta charset=\"UTF-8\">"
    puts "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">"
    puts "<title>Televised</title>"
    puts "<link href=\"https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css\" rel=\"stylesheet\">"
    puts "<link rel=\"stylesheet\" href=\"Televised.css\">"
puts "</head>"
puts "<body id=\"showsPage\">"
    puts "<nav id=\"changingNav\"></nav>"

    puts "<script src=\"https://code.jquery.com/jquery-3.6.0.min.js\"></script>"
    puts "<script src=\"https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js\"></script>"
    puts "<script src=\"Televised.js\"></script>"

  puts "<br>"
  puts "<div class=\"seriesPage\">"


  #HERE
  puts "<div class=\"showInfo\">" 
    puts "<img src=\"" + seriesImage + "\"alt=\"" + seriesImage + "\">" 
    puts "<br>"
    puts "<div class=\"showWords\">"

      puts "<h1 style=\"font-family: 'Times New Roman', Times, serif; color: white; text-align: left;\">" + series.first['showName'] + "</h1>"

      puts "<h2 style=\"font-family: 'Times New Roman', Times, serif; color: #436eb1; text-align: left;\">" + series.first['genre'] + "</h2>"
      puts "<br>"
      puts "<h3 style=\"font-family: 'Times New Roman', Times, serif; color: white; text-align: left;\">" + series.first['description']+ "</h4>"
      puts "<br>"
      puts "<h3 style=\"font-family: 'Times New Roman', Times, serif; color: #436eb1; text-align: left;\">" + series.first['year'].to_s + "</h4>"
      puts "<br>"
    puts "</div>"
   puts "</div>" 
   puts "<br>"
  puts "<h4 style=\"font-family: 'Times New Roman', Times, serif; color: white; text-align: left;\">Creator: "
  puts "<span>" + series.first['creator'] + "</span></h4>"

  #NEED FROM SEASON
  puts "<h4 style=\"font-family: 'Times New Roman', Times, serif; color: white; text-align: left;\">Main Cast: "
    puts "<span>" + mainCast.first['mainCast'] + "</span>"
  puts "</h4>"

  puts "<h4 style=\"font-family: 'Times New Roman', Times, serif; color: white; text-align: left;\">Streaming: "
    puts "<span>" + series.first['streaming'] + "</span>"
  puts "</h4>"
  puts "<br>"

  puts "<div class=\"seasonNav\">"
  puts "<div class=\"seasonDropdown\">"
    puts "<button class=\"dropbtn\">Season1"
      puts "<a href=\"shows.html\"></a>"
    puts "</button>"
    puts "<div class=\"dropseason-content\">"
      puts "<a href=\"showsseason2.html\">Season 2</a>"
      puts "<a href=\"showsseason3.html\">Season 3</a>"
    puts "</div>"
  puts "</div>"
  puts "<div class=\"editButtons\">"
    puts "<button class=\"watchedButton\">EYE</button>"
    puts "<button class=\"reviewButton\">REVIEW</button>"
    puts "<button class=\"rateButton\">STARS</button>"
    puts "<button class=\"menuButton\">MENU</button>"
  puts "</div>"
  puts "</div>"

  puts "<hr>"
  
  puts "<div class=\"showInfo\">"
    puts "<img src=\"./Episodes/adventureTime1.1.jpg\" alt=\"Adventure Time\" width=\"300\" height=\"225\">"
    puts "<div class=\"words\">"
      puts "<h3 style=\"font-family: 'Times New Roman', Times, serif; color: white; text-align: left;\">1. Title</h3>"
      puts "<h4 style=\"font-family: 'Times New Roman', Times, serif; color: #436eb1; text-align: left;\">runTime</h4>"
      puts "<h5 style=\"font-family: 'Times New Roman', Times, serif; color: white; text-align: left;\">Description</h5>"
      puts "<div class=\"editButtons\">"
        puts "<button class=\"watchedButton\">EYE</button>"
        puts "<button class=\"reviewButton\">REVIEW</button>"
        puts "<button class=\"rateButton\">STARS</button>"
        puts "<button class=\"menuButton\">MENU</button>"
      puts "</div>"
    puts "</div>"
  puts "</div>"

  puts "<hr>"
  puts "<br>"
puts "</div>"

puts "</body>"
puts "</html>"