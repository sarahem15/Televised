#!/usr/bin/ruby
$stdout.sync = true
$stderr.reopen $stdout

puts "Content-type: text/html\n\n"
require 'mysql2'
require 'cgi'

cgi = CGI.new
seriesImage = cgi['clicked_image']
seasonNum = cgi['seasonNum']

db = Mysql2::Client.new(
    host: '10.20.3.4', 
    username: 'seniorproject25', 
    password: 'TV_Group123!', 
    database: 'televised_w25'
  )

puts seasonNum.to_s
series = db.query("SELECT * FROM series WHERE imageName = '" + seriesImage + "';")
seasons = db.query("SELECT season.* FROM season JOIN series ON season.seriesId = series.showId WHERE series.imageName = '" + seriesImage + "';")

seasonsArray = seasons.to_a
seasonId = seasonsArray[0]['seasonId']
episodes = db.query("SELECT episode.* FROM episode JOIN season ON episode.seasonId = season.seasonId WHERE season.seasonId = '" + seasonId.to_s + "';")

#seasonsArray = seasons.to_a
#episodesArray = episodes.to_a

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

  puts "<h4 style=\"font-family: 'Times New Roman', Times, serif; color: white; text-align: left;\">Main Cast: "
    puts "<span>" + seasonsArray[0]['mainCast'] + "</span>"
  puts "</h4>"

  puts "<h4 style=\"font-family: 'Times New Roman', Times, serif; color: white; text-align: left;\">Streaming: "
    puts "<span>" + series.first['streaming'] + "</span>"
  puts "</h4>"
  puts "<br>"

  puts "<div class=\"seasonNav\">"
  puts "<div class=\"seasonDropdown\">"
    puts "<button class=\"dropbtn\">Season 1"
      puts "<a href=\"shows.html\"></a>"
    puts "</button>"
    puts "<div class=\"dropseason-content\">"
#      puts "<a name=\"clicked_image\" value=" + seriesImage + " href=\"series2.cgi\">Season 2</a>"
      puts "<a href=\"series2.cgi?clicked_image=" + seriesImage + "\">Season 2</a>"
      puts "<a href=\"series3.cgi?clicked_image=" + seriesImage + "\">Season 3</a>"
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
  
  epNum = 1
  episodes.each do |episode|
  # EP INFO FOR EACH
  puts "<div class=\"showInfo\">"
    puts "<img src=\"./Episodes/adventureTime1.1.jpg\" alt=\"Adventure Time\" width=\"300\" height=\"225\">"
    puts "<div class=\"words\">"
      puts "<a href=\"indivEp.cgi?ep_name=" + episode['epName'] + "&show_name=" + series.first['showName'] + "&ep_num=" + epNum.to_s + "\"><h3 style=\"font-family: 'Times New Roman', Times, serif; color: white; text-align: left;\">" + epNum.to_s + ". " + episode['epName'] + "</h3></a>"
      puts "<h4 style=\"font-family: 'Times New Roman', Times, serif; color: #436eb1; text-align: left;\">" + episode['runtime'].to_s + " minutes</h4>"
      puts "<h5 style=\"font-family: 'Times New Roman', Times, serif; color: white; text-align: left;\">" + episode['description'] + "</h5>"
      puts "<div class=\"editButtons\">"
        puts "<button class=\"watchedButton\">EYE</button>"
        puts "<button class=\"reviewButton\">REVIEW</button>"
        puts "<button class=\"rateButton\">STARS</button>"
        puts "<button class=\"menuButton\">MENU</button>"
      puts "</div>"
    puts "</div>"
  puts "</div>"
  epNum = epNum + 1
  end

  puts "<hr>"
  puts "<br>"
puts "</div>"

puts "</body>"
puts "</html>"
