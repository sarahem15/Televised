#!/usr/bin/ruby
$stdout.sync = true
$stderr.reopen $stdout

puts "Content-type: text/html\n\n"
require 'mysql2'
require 'cgi'

cgi = CGI.new
seriesImage = cgi['clicked_image']
seasonNumber = cgi['seasonNumber'].to_i

db = Mysql2::Client.new(
    host: '10.20.3.4', 
    username: 'seniorproject25', 
    password: 'TV_Group123!', 
    database: 'televised_w25'
  )

series = db.query("SELECT * FROM series WHERE imageName = '" + seriesImage + "';")
seasons = db.query("SELECT season.* FROM season JOIN series ON season.seriesId = series.showId WHERE series.imageName = '" + seriesImage + "';")
seasonsArray = seasons.to_a
seasonId = seasonsArray[seasonNumber-1]['seasonId']
episodes = db.query("SELECT episode.* FROM episode JOIN season ON episode.seasonId = season.seasonId WHERE season.seasonId = '" + seasonId.to_s + "';")
seriesId = series.first['showId']
numOfSeasons = series.first['numOfSeasons']

seriesId = series.first['showId']
streaming = db.query("SELECT * FROM streaming WHERE seriesId = '" + seriesId.to_s + "';")
streaming = streaming.to_a

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
      puts "<br>"

      puts "<div class=\"editButtons\">"
      puts '<form action="threebuttons.cgi" method="POST">'
        puts '<button class="watchedButton"><i class="eye-icon fa fa-eye"></i></button>'
        #puts "<button class=\"watchedButton\">EYE</button>"
        puts '<input type="hidden" name="seriesID" value="' + seriesId.to_s + '">'
        puts '<input type="hidden" name="watchedButton" value="TRUE">'
        puts '<input type="hidden" name="seasonNumber" value="' + seasonNumber.to_s + '">'
        puts '</form>'
        puts "<button class=\"reviewButton\" data-bs-toggle=\"toggle\" data-bs-target=\"#CreateReview\">REVIEW</button>"
        #puts "<button class=\"rateButton\">STARS</button>"

=begin
        puts "<button class=\"submit\" id=\"stars\">"
        puts "<span id=\"star1\"><class=\"fa fa-star\"></span>"
        puts "</button>"
=end
        puts '<form action="threebuttons.cgi" method="POST">'
        puts '<button class="star">'
        puts '<span id="star2" class="fa fa-star"></span>'
        puts '<input type="hidden" name="seriesRating" value="2">'
        puts '<input type="hidden" name="seriesID" value="' + seriesId.to_s + '">'
        puts '<input type="hidden" name="seasonNumber" value="' + seasonNumber.to_s + '">'

        puts '<span id="star3" class="fa fa-star"></span>'
        puts '<input type="hidden" name="seriesRating" value="3">'
        puts '<input type="hidden" name="seriesID" value="' + seriesId.to_s + '">'
        puts '<input type="hidden" name="seasonNumber" value="' + seasonNumber.to_s + '">'
        puts '</button>'
        puts '</form>'

=begin
        puts "<button class=\"submit\" id=\"stars\">"
        puts '<span id="star2" class="fa fa-star"></span>'
        puts '<span id="star3" class="fa fa-star"></span>'
        puts '<span id="star4" class="fa fa-star"></span>'
        puts '<span id="star5" class="fa fa-star"></span>'
        puts "</button>"
=end

        puts "<div class=\"seasonDropdown\">"
        puts "<button class=\"menuButton\">MENU</button>"
        puts "<div class=\"dropseason-content\">"
        puts '<form action="threebuttons.cgi" method="POST">'
        puts "<button>Add to Want to Watch</button>"
        puts '<input type="hidden" name="seriesID" value="' + seriesId.to_s + '">'
        puts '<input type="hidden" name="wantToWatch" value="TRUE">'
        puts '<input type="hidden" name="seasonNumber" value="' + seasonNumber.to_s + '">'
        puts '</form>'
        puts '<form action="threebuttons.cgi" method="POST">'
        puts "<button>Add to Existing List</button>"
        puts '<input type="hidden" name="seriesID" value="' + seriesId.to_s + '">'
        puts '<input type="hidden" name="seasonNumber" value="' + seasonNumber.to_s + '">'
        puts '</form>'
        puts '<form action="createNewList.cgi" method="POST">'
        puts "<button>Add to New List</button>"
        puts '<input type="hidden" name="seriesID" value="' + seriesId.to_s + '">'
        puts '</form>'
        puts '<form action="otherLists.cgi" method="POST">'
        puts "<button>View on Other's Lists</button>"
        puts '<input type="hidden" name="seriesID" value="' + seriesId.to_s + '">'
        puts '<input type="hidden" name="seasonNumber" value="' + seasonNumber.to_s + '">'
        puts '</form>'
        puts "</div>"
        puts "</div>"
      puts "</div>"

    puts "</div>"
   puts "</div>" 

   puts "<br>"
  puts "<h4 style=\"font-family: 'Times New Roman', Times, serif; color: white; text-align: left;\">Creator: "
  puts "<span>" + series.first['creator'] + "</span></h4>"
  puts "<h4 style=\"font-family: 'Times New Roman', Times, serif; color: white; text-align: left;\">Main Cast: "
    puts "<span>" + seasonsArray[0]['mainCast'] + "</span>"
  puts "</h4>"
  puts "<h4 style=\"font-family: 'Times New Roman', Times, serif; color: white; text-align: left;\">Streaming: "
    (0...streaming.size).each do |i|
      print "<span>" + streaming[i]['service'].strip
      if streaming.size == 1
        puts "</span>"
      elsif i == (streaming.size - 1)
        puts "</span>"
      else
        puts ",</span>"
      end
    end
  puts "</h4>"
  puts "<br>"

  puts "<div class=\"seasonNav\">"
  puts "<div class=\"seasonDropdown\">"
    if numOfSeasons > 1
      puts "<button class=\"dropbtn\">Season " + seasonNumber.to_s + " &#9660"
    elsif numOfSeasons = 1
    puts "<button class=\"dropbtn\">Season " + seasonNumber.to_s 
    end
      puts "<a href=\"series.cgi\"></a>"
    puts "</button>"
    puts "<div class=\"dropseason-content\">"
      if seasonNumber == 1 and numOfSeasons >= 3
        puts "<a href=\"series.cgi?clicked_image=" + seriesImage + "&seasonNumber=2\">Season 2</a>"
        puts "<a href=\"series.cgi?clicked_image=" + seriesImage + "&seasonNumber=3\">Season 3</a>"
      elsif seasonNumber == 1 and numOfSeasons == 2
        puts "<a href=\"series.cgi?clicked_image=" + seriesImage + "&seasonNumber=2\">Season 2</a>"
      elsif seasonNumber == 2 and numOfSeasons >= 3
        puts "<a href=\"series.cgi?clicked_image=" + seriesImage + "&seasonNumber=1\">Season 1</a>"
        puts "<a href=\"series.cgi?clicked_image=" + seriesImage + "&seasonNumber=3\">Season 3</a>"
      elsif seasonNumber == 2 and numOfSeasons == 2
        puts "<a href=\"series.cgi?clicked_image=" + seriesImage + "&seasonNumber=1\">Season 1</a>"
      elsif seasonNumber == 3 and numOfSeasons >= 3
        puts "<a href=\"series.cgi?clicked_image=" + seriesImage + "&seasonNumber=1\">Season 1</a>"
        puts "<a href=\"series.cgi?clicked_image=" + seriesImage + "&seasonNumber=2\">Season 2</a>"
      end
    puts "</div>"
  puts "</div>"
  puts "<div class=\"editButtons\">"
      puts '<form action="threebuttons.cgi" method="POST">'
        #puts "<button class=\"watchedButton\">EYE</button>"
        puts '<button class="watchedButton"><i class="eye-icon fa fa-eye"></i></button>'
        puts '<input type="hidden" name="seriesID" value="' + seriesId.to_s + '">'
        puts '<input type="hidden" name="watchedButton" value="TRUE">'
        puts '<input type="hidden" name="seasonNumber" value="' + seasonNumber.to_s + '">'
        puts '<input type="hidden" name="seasonId" value="' + seasonId.to_s + '">'
        puts '</form>'
        puts "<button class=\"reviewButton\" data-bs-toggle=\"toggle\" data-bs-target=\"#CreateReview\">REVIEW</button>"
        puts "<button class=\"rateButton\">STARS</button>"
        puts "<div class=\"seasonDropdown\">"
        puts "<button class=\"menuButton\">MENU</button>"
        puts "<div class=\"dropseason-content\">"
        puts '<form action="threebuttons.cgi" method="POST">'
        puts "<button>Add to Want to Watch</button>"
        puts '<input type="hidden" name="seriesID" value="' + seriesId.to_s + '">'
        puts '<input type="hidden" name="wantToWatch" value="TRUE">'
        puts '<input type="hidden" name="seasonNumber" value="' + seasonNumber.to_s + '">'
        puts '<input type="hidden" name="seasonId" value="' + seasonId.to_s + '">'
        puts '</form>'
        puts '<form action="threebuttons.cgi" method="POST">'
        puts "<button>Add to Existing List</button>"
        puts '<input type="hidden" name="seriesID" value="' + seriesId.to_s + '">'
        puts '<input type="hidden" name="seasonNumber" value="' + seasonNumber.to_s + '">'
        puts '<input type="hidden" name="seasonId" value="' + seasonId.to_s + '">'
        puts '</form>'
        puts '<form action="createNewList.cgi" method="POST">'
        puts "<button>Add to New List</button>"
        puts '<input type="hidden" name="seriesID" value="' + seriesId.to_s + '">'
        puts '<input type="hidden" name="seasonNumber" value="' + seasonNumber.to_s + '">'
        puts '<input type="hidden" name="seasonId" value="' + seasonId.to_s + '">'
        puts '</form>'
        puts '<form action="threebuttons.cgi" method="POST">'
        puts "<button>View on Other's Lists</button>"
        puts '<input type="hidden" name="seriesID" value="' + seriesId.to_s + '">'
        puts '<input type="hidden" name="seasonNumber" value="' + seasonNumber.to_s + '">'
        puts '<input type="hidden" name="seasonId" value="' + seasonId.to_s + '">'
        puts '</form>'
        puts "</div>"
        puts "</div>"
      puts "</div>"
  puts "</div>"

  puts "<hr>"
  
  epNum = 1
  episodes.each do |episode|
  # EP INFO FOR EACH
  puts "<div class=\"epInfo\">"
    puts "<img src=\"./Episodes/" + seriesImage.split('.')[0] + seasonNumber.to_s + "." + epNum.to_s + ".1.jpg\" alt=\"" + seriesImage + "\" width=\"300\" height=\"225\">"
    puts "<div class=\"words\">"
      puts "<a href=\"indivEp.cgi?ep_name=" + episode['epName'] + "&show_name=" + series.first['showName'] + "&ep_num=" + epNum.to_s + "&seasonNumber=" + seasonNumber.to_s + "\"><h3 style=\"font-family: 'Times New Roman', Times, serif; text-align: left;\">" + epNum.to_s + ". " + episode['epName'] + "</h3></a>"
      puts "<h4 style=\"font-family: 'Times New Roman', Times, serif; color: #436eb1; text-align: left;\">" + episode['runtime'].to_s + " minutes</h4>"
      puts "<h5 style=\"font-family: 'Times New Roman', Times, serif; color: white; text-align: left;\">" + episode['description'] + "</h5>"
      puts "<div class=\"editButtons\">"
      puts '<form action="threebuttons.cgi" method="POST">'
        puts '<button class="watchedButton"><i class="eye-icon fa fa-eye"></i></button>'
        #puts "<button class=\"watchedButton\">EYE</button>"
        puts '<input type="hidden" name="seriesID" value="' + seriesId.to_s + '">'
        puts '<input type="hidden" name="epID" value="' + episode['epId'].to_s + '">'
        puts '<input type="hidden" name="watchedButton" value="TRUE">'
        puts '<input type="hidden" name="seasonNumber" value="' + seasonNumber.to_s + '">'
        puts '</form>'
        puts "<button class=\"reviewButton\" data-bs-toggle=\"toggle\" data-bs-target=\"#CreateReview\">REVIEW</button>"
        puts "<button class=\"rateButton\">STARS</button>"
        puts "<div class=\"seasonDropdown\">"
        puts "<button class=\"menuButton\">MENU</button>"
        puts "<div class=\"dropseason-content\">"
        puts '<form action="threebuttons.cgi" method="POST">'
        puts "<button>Add to Want to Watch</button>"
        puts '<input type="hidden" name="seriesID" value="' + seriesId.to_s + '">'
        puts '<input type="hidden" name="epID" value="' + episode['epId'].to_s + '">'
        puts '<input type="hidden" name="wantToWatch" value="TRUE">'
        puts '<input type="hidden" name="seasonNumber" value="' + seasonNumber.to_s + '">'
        puts '</form>'
        puts '<form action="threebuttons.cgi" method="POST">'
        puts "<button>Add to Existing List</button>"
        puts '<input type="hidden" name="seriesID" value="' + seriesId.to_s + '">'
        puts '<input type="hidden" name="epID" value="' + episode['epId'].to_s + '">'
        puts '<input type="hidden" name="addToExisting" value="TRUE">'
        puts '<input type="hidden" name="seasonNumber" value="' + seasonNumber.to_s + '">'
        puts '</form>'
        puts '<form action="createNewList.cgi" method="POST">'
        puts "<button>Add to New List</button>"
        puts '<input type="hidden" name="seriesID" value="' + seriesId.to_s + '">'
        puts '<input type="hidden" name="epID" value="' + episode['epId'].to_s + '">'
        puts '</form>'
        puts '<form action="threebuttons.cgi" method="POST">'
        puts "<button>View on Other's Lists</button>"
        puts '<input type="hidden" name="seriesID" value="' + seriesId.to_s + '">'
        puts '<input type="hidden" name="epID" value="' + episode['epId'].to_s + '">'
        puts '<input type="hidden" name="viewOnOthers" value="TRUE">'
        puts '<input type="hidden" name="seasonNumber" value="' + seasonNumber.to_s + '">'
        puts '</form>'
        puts "</div>"
        puts "</div>"
        
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
