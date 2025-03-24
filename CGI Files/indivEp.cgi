#!/usr/bin/ruby
$stdout.sync = true
$stderr.reopen $stdout

puts "Content-type: text/html\n\n"
require 'mysql2'
require 'cgi'

require 'cgi/session'

cgi = CGI.new
session = CGI::Session.new(cgi)
username = session['username']

episodeName = cgi['ep_name']
showName = cgi['show_name']
epNum = cgi['ep_num']
seasonNumber = cgi['seasonNumber']
seriesId = cgi['seriesId']
db = Mysql2::Client.new(
    host: '10.20.3.4', 
    username: 'seniorproject25', 
    password: 'TV_Group123!', 
    database: 'televised_w25'
  )

#seriesImage = db.query("SELECT imageName FROM series WHERE showName = '" + showName + "';")
episode = db.query("SELECT episode.* FROM episode JOIN season ON episode.seasonId = season.seasonId
  JOIN series ON season.seriesId = series.showId WHERE episode.epName = '" + episodeName.gsub("'", "\\\\'") + "' AND series.showName = '" + showName.gsub("'", "\\\\'") + "';")

#puts "<img src=\"./Episodes/" + seriesImage.split('.')[0] + seasonNumber.to_s + "." + epNum.to_s + ".1.jpg\" alt=\"" + seriesImage[0] + "\" width=\"300\" height=\"225\">"



puts "<!DOCTYPE html>"
puts "<html lang=\"en\">"
puts "<head>"
    puts "<meta charset=\"UTF-8\">"
    puts "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">"
    puts "<title>Televised</title>"
    puts "<link href=\"https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css\" rel=\"stylesheet\">"
    puts "<link rel=\"stylesheet\" href=\"Televised.css\">"
    puts '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">'
puts "</head>"
puts "<body id=\"episodePage\">"
    puts "<nav id=\"changingNav\"></nav>"

    puts "<script src=\"https://code.jquery.com/jquery-3.6.0.min.js\"></script>"
    puts "<script src=\"https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js\"></script>"
    puts "<script src=\"Televised.js\"></script>"

  puts "<br>"
  puts "<div class=\"episodesPage\">"


  #HERE
    (1...4).each do |i|
      puts "<img src=\"Episodes/" + showName.gsub(" ", "").gsub("'", "") + seasonNumber.to_s + "." + epNum.to_s + "." + i.to_s + ".jpg\" alt=\"\">" 
    end
    puts "<br>"
    puts "<br>"
      puts "<h1 style=\"font-family: 'Times New Roman', Times, serif; color: white; text-align: left;\">" + showName + "</h1>"
      puts "<div class=\"epWords\">"
      puts "<h3> Season 1 </h2>"
      puts "<h3> Episode " + epNum.to_s + "</h4>"
      puts "<h3> RATING </h4>"
      puts "<h3>" + episode.first['epName'] + "</h2>"
      puts "<h3>" + episode.first['releaseDate'] + "</h4>"
      puts "<h3>" + episode.first['runtime'].to_s + "m</h4>"
    puts "</div>"
   puts "<br>"
  puts "<h4 class=\"epDes\">"
  puts "<span>" + episode.first['description'] + "</span></h4>"
  puts "<br>"
  puts "<br>"
  puts "<div class=\"editButtons\">"
      puts '<form action="threebuttons.cgi" method="POST">'
        puts '<button class="watchedButton"><i class="eye-icon fa fa-eye"></i></button>'
        #puts '<input type="hidden" name="seriesID" value="' + seriesId.to_s + '">'
        puts '<input type="hidden" name="watchedButton" value="TRUE">'
        #puts '<input type="hidden" name="epID" value="' + episode['epId'].to_s + '">'
        puts '</form>'
        puts "<button class=\"reviewButton\">REVIEW</button>"
        #puts "<button class=\"rateButton\">STARS</button>"

        (0...5).each do |i|
          puts '<form action="threebuttons.cgi" method="POST">'
          puts '<button class="fa fa-star"></button>'
          puts '<input type="hidden" name="epRating" value="' + (i+1).to_s + '">'
          puts '<input type="hidden" name="seriesID" value="' + seriesId.to_s + '">'
          puts '<input type="hidden" name="epID" value="' + episode.first['epId'].to_s + '">'
          puts '<input type="hidden" name="seasonNumber" value="' + seasonNumber.to_s + '">'
          puts '<input type="hidden" name="rated" value="TRUE">'
          puts '</form>'
        end

        puts "<div class=\"seasonDropdown\">"
        puts '<button class="menuButton"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-three-dots" viewBox="0 0 16 16">
  <path d="M3 9.5a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3m5 0a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3m5 0a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3"/>
</svg></button>'
        puts "<div class=\"dropseason-content\">"
        puts '<form action="threebuttons.cgi" method="POST">'
        puts "<button>Add to Want to Watch</button>"
        #puts '<input type="hidden" name="seriesID" value="' + seriesId.to_s + '">'
        puts '</form>'
        puts '<form action="threebuttons.cgi" method="POST">'
        puts "<button>Add to Existing List</button>"
        #puts '<input type="hidden" name="seriesID" value="' + seriesId.to_s + '">'
        puts '</form>'
        puts '<form action="threebuttons.cgi" method="POST">'
        puts "<button>Add to New List</button>"
        #puts '<input type="hidden" name="seriesID" value="' + seriesId.to_s + '">'
        puts '</form>'
        puts '<form action="threebuttons.cgi" method="POST">'
        puts "<button>View on Other's Lists</button>"
        #puts '<input type="hidden" name="seriesID" value="' + seriesId.to_s + '">'
        puts '</form>'
        puts "</div>"
        puts "</div>"
      puts "</div>"
        puts "<br>"
  puts "<h3 style=\"font-family: 'Times New Roman', Times, serif; color: white; text-align: left;\"> Writers: " + episode.first['writers'] + "</h4>"
  puts "<br>"
#Buttons!


  puts "<h4 style=\"font-family: 'Times New Roman', Times, serif; color: white; text-align: left;\">Cast: "
    puts "<span>" + episode.first['topCast'] + "</span>"
  puts "</h4>"

  puts "<br>"
  puts "<hr>"

  puts '<section class="epReviews">'
  (0...6).each do |i|
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
          puts '<h5 id="Heart">&#9829</h5>'
          puts '<h4>12</h4>' #db query to get likes
        puts '</section>'
    puts '</div>'
  puts '</div>'
end
puts '</section>'
puts "</div>"
puts "</body>"
puts "</html>"