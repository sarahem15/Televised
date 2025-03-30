#!/usr/bin/ruby
$stdout.sync = true
$stderr.reopen $stdout

puts "Content-type: text/html\n\n"
require 'mysql2'
require 'cgi'
require 'cgi/session'
require 'open-uri'
cgi = CGI.new
time = Time.new
session = CGI::Session.new(cgi)
username = session['username']

seriesImage = cgi['clicked_image']
seasonNumber = cgi['seasonNumber'].to_i
trueWatched = cgi['trueWatched']

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
seriesRating = 0
seasonRating = 0
episodeRating = 0

sumRating = 0
avgSeasonRating = 0
seasonRatings = db.query("SELECT rating FROM seasonRating where seasonId = '" + seasonId.to_s + "';")
seasonRatings = seasonRatings.to_a
(0...seasonRatings.size).each do |i|
  sumRating = sumRating + seasonRatings[i]['rating'].to_i
end
if seasonRatings.size != 0
  avgSeasonRating = sumRating/seasonRatings.size
end

sumRating = 0
avgSeriesRating = 0
seriesRatings = db.query("SELECT rating FROM seriesRating where seriesId = '" + seriesId.to_s + "';")
seriesRatings = seriesRatings.to_a
(0...seriesRatings.size).each do |i|
  sumRating = sumRating + seriesRatings[i]['rating'].to_i
end
if seriesRatings.size != 0
  avgSeriesRating = sumRating/seriesRatings.size
end


#puts username.to_s
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
      puts '<div class="titleRating">'
      puts "<h1 style=\"font-family: 'Times New Roman', Times, serif; color: white; text-align: left;\">" + series.first['showName'] + "</h1>"
      puts '<section class="avgRating" style="height: 10px;">'
        if avgSeriesRating != 0
          (0...5).each do |j|
            if (j < avgSeriesRating)
                puts '<i class="fa fa-star" style="color: white;"></i>'
            else
              puts '<i class="fa fa-star"></i>'
            end
          end
        else
            puts '<h3 style="width: 300px;">NO AVG RATING</h3>'
        end
        puts '</section>'      
        puts '</div>'
        puts '<br>'
      puts "<h2 style=\"font-family: 'Times New Roman', Times, serif; color: #436eb1; text-align: left;\">" + series.first['genre'] + "</h2>"
      puts "<br>"
      puts "<h3 style=\"font-family: 'Times New Roman', Times, serif; color: white; text-align: left;\">" + series.first['description']+ "</h4>"
      puts "<br>"
      puts "<h3 style=\"font-family: 'Times New Roman', Times, serif; color: #436eb1; text-align: left;\">" + series.first['year'].to_s + "</h4>"
      puts "<br>"
      puts "<br>"

      puts "<div class=\"editButtons\" >"
      puts '<form action="threebuttons.cgi" method="POST">'
      alreadyWatchedSeries = db.query("SELECT * FROM haveWatchedSeries WHERE username = '" + username + "'AND seriesId = '" + seriesId.to_s + "';")
        if (alreadyWatchedSeries.to_a.to_s != "[]")
          puts '<button class="watchedButton"><i class="eye-icon fa fa-eye" style="color: #6bdf10;" ></i></button>'
        else
          puts '<button class="watchedButton"><i class="eye-icon fa fa-eye"></i></button>'
        end
        #puts "<button class=\"watchedButton\">EYE</button>"
        puts '<input type="hidden" name="seriesID" value="' + seriesId.to_s + '">'
        puts '<input type="hidden" name="watchedButton" value="TRUE">'
        puts '<input type="hidden" name="seasonNumber" value="' + seasonNumber.to_s + '">'
        puts '</form>'
        puts "<button class=\"reviewButton\" data-bs-toggle=\"modal\" data-bs-target=\"#CreateSeriesReview\">&#128488</button>"
        #puts "<button class=\"rateButton\">STARS</button>"

          alreadyRatedSeries = db.query("SELECT * FROM seriesRating WHERE seriesId = '" + seriesId.to_s + "' AND username = '" + username + "';")
          if (alreadyRatedSeries.to_a.to_s != "[]")
            seriesRating = alreadyRatedSeries.first['rating'].to_i
          end
          #alreadyRated = alreadyRated.to_a


      puts '<section class="Rating">'
        (0...5).each do |i|
          puts '<form action="threebuttons.cgi" method="POST">'
          if (i < seriesRating)
            puts '<button class="fa fa-star" style="color: yellow;"></button>'
          else
            puts '<button class="fa fa-star"></button>'
          end
          puts '<input type="hidden" name="seriesRating" value="' + (i+1).to_s + '">'
          puts '<input type="hidden" name="seriesID" value="' + seriesId.to_s + '">'
          puts '<input type="hidden" name="seasonNumber" value="' + seasonNumber.to_s + '">'
          puts '<input type="hidden" name="rated" value="TRUE">'
          puts '</form>'
        end
        puts '</section>'

        puts "<div class=\"seasonDropdown\">"
        puts '<button class="menuButton"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-three-dots" viewBox="0 0 16 16">
  <path d="M3 9.5a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3m5 0a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3m5 0a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3"/>
</svg></button>'

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
    elsif numOfSeasons == 1
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

  puts '<section class="avgRating" style="height: 10px;">'
        if avgSeasonRating != 0
          puts 
          (0...5).each do |j|
            if (j < avgSeasonRating)
                puts '<i class="fa fa-star" style="color: white;"></i>'
            else
              puts '<i class="fa fa-star"></i>'
            end
          end
        else
            puts '<h3 style="width: 300px;">NO AVG RATING</h3>'
        end
        puts '</section>'


  puts "<div class=\"editButtons\">"
      puts '<form action="threebuttons.cgi" method="POST">'
        #puts "<button class=\"watchedButton\">EYE</button>"
        alreadyWatchedSeason = db.query("SELECT * FROM haveWatchedSeason WHERE username = '" + username + "'AND seasonId = '" + seasonId.to_s + "';")
        if (alreadyWatchedSeason.to_a.to_s != "[]")
          puts '<button class="watchedButton"><i class="eye-icon fa fa-eye" style="color: #6bdf10;"></i></button>'
        else
          puts '<button class="watchedButton"><i class="eye-icon fa fa-eye"></i></button>'
        end
        puts '<input type="hidden" name="seriesID" value="' + seriesId.to_s + '">'
        puts '<input type="hidden" name="watchedButton" value="TRUE">'
        puts '<input type="hidden" name="seasonNumber" value="' + seasonNumber.to_s + '">'
        puts '<input type="hidden" name="seasonId" value="' + seasonId.to_s + '">'
        puts '</form>'
        puts "<button class=\"reviewButton\" data-bs-toggle=\"modal\" data-bs-target=\"#CreateSeasonReview\">&#128488</button>"
        # puts "<button class=\"rateButton\">STARS</button>"
        alreadyRatedSeason = db.query("SELECT * FROM seasonRating WHERE username = '" + username + "' AND seasonId = '" + seasonId.to_s + "';")
          if (alreadyRatedSeason.to_a.to_s != "[]")
            seasonRating = alreadyRatedSeason.first['rating'].to_i
          end

        puts '<section class="Rating">'
        (0...5).each do |i|
          puts '<form action="threebuttons.cgi" method="POST">'
          if (i < seasonRating)
            puts '<button class="fa fa-star" style="color: yellow;"></button>'
          else
            puts '<button class="fa fa-star"></button>'
          end
          puts '<input type="hidden" name="seasonRating" value="' + (i+1).to_s + '">'
          puts '<input type="hidden" name="seriesID" value="' + seriesId.to_s + '">'
          puts '<input type="hidden" name="seasonId" value="' + seasonId.to_s + '">'
          puts '<input type="hidden" name="seasonNumber" value="' + seasonNumber.to_s + '">'
          puts '<input type="hidden" name="rated" value="TRUE">'
          puts '</form>'
        end
        puts '</section>'

        puts "<div class=\"seasonDropdown\">"
        puts '<button class="menuButton"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-three-dots" viewBox="0 0 16 16">
  <path d="M3 9.5a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3m5 0a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3m5 0a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3"/>
</svg></button>'
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
        puts '<form action="otherLists.cgi" method="POST">'
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
  
  ############################
  epNum = 1
  episodes.each do |episode|
  # EP INFO FOR EACH
  puts "<div class=\"epInfo\">"

    def url_exists?(url)
      begin
        URI.open(url)
        true
      rescue OpenURI::HTTPError, SocketError
        false
      end
    end


    imageSource = "https://cs.transy.edu/Televised/Episodes/" + seriesImage.split('.')[0] + seasonNumber.to_s + "." + epNum.to_s + ".1.jpg"
    valid = url_exists?(imageSource)
    if valid
      puts "<img src=\"./Episodes/" + seriesImage.split('.')[0] + seasonNumber.to_s + "." + epNum.to_s + ".1.jpg\" alt=\"" + seriesImage + "\" width=\"300\" height=\"225\">"
    else
      puts "<img src=\"./Episodes/Televised.jpg\" alt=\"" + seriesImage + "\" width=\"300\" height=\"225\">"
    end

    puts "<div class=\"words\">"
    puts '<section class="titleTime">'
      puts "<a href=\"indivEp.cgi?ep_name=" + episode['epName'].gsub("'", "\\\\'").gsub("#", "\\\#").gsub(".", "\\\.") + "&show_name=" + series.first['showName'] + "&seriesID=" + series.first['showId'].to_s + "&ep_num=" + epNum.to_s + "&seasonNumber=" + seasonNumber.to_s + "\"><h3 style=\"font-family: 'Times New Roman', Times, serif; text-align: left;\">" + epNum.to_s + ". " + episode['epName'] + "</h3></a>"
      puts "<h4 style=\"font-family: 'Times New Roman', Times, serif; color: #436eb1; text-align: left;\">" + episode['runtime'].to_s + "m</h4>"
      puts '</section>'
      puts "<h5 style=\"font-family: 'Times New Roman', Times, serif; color: white; text-align: left;\">" + episode['description'] + "</h5>"
      puts "<div class=\"editButtons\">"
      puts '<form action="threebuttons.cgi" method="POST">'
        alreadyWatchedEpisode = db.query("SELECT * FROM haveWatchedEpisode WHERE username = '" + username + "'AND epId = '" + episode['epId'].to_s + "';")
        if (alreadyWatchedEpisode.to_a.to_s != "[]")
          puts '<button class="watchedButton"><i class="eye-icon fa fa-eye" style="color: #6bdf10;"></i></button>'
        else
          puts '<button class="watchedButton"><i class="eye-icon fa fa-eye"></i></button>'
        end
        #puts "<button class=\"watchedButton\">EYE</button>"
        puts '<input type="hidden" name="seriesID" value="' + seriesId.to_s + '">'
        puts '<input type="hidden" name="epID" value="' + episode['epId'].to_s + '">'
        puts '<input type="hidden" name="watchedButton" value="TRUE">'
        puts '<input type="hidden" name="seasonNumber" value="' + seasonNumber.to_s + '">'
        puts '</form>'


        puts "<button class=\"reviewButton\" data-bs-toggle=\"modal\" 
        data-epName=\"" + episode['epName'] + "\"
        data-bs-target=\"#CreateEpisodeReview\">&#128488</button>"

        alreadyRatedEpisode = db.query("SELECT * FROM episodeRating WHERE username = '" + username + "' AND epId = '" + episode['epId'].to_s + "';")
          if (alreadyRatedEpisode.to_a.to_s != "[]")
            episodeRating = alreadyRatedEpisode.first['rating'].to_i
          end
        puts '<section class="Rating">'
        (0...5).each do |i|
          puts '<form action="threebuttons.cgi" method="POST">'
          if (i < episodeRating)
            puts '<button class="fa fa-star" style="color: yellow;"></button>'
          else
            puts '<button class="fa fa-star"></button>'
          end
          puts '<input type="hidden" name="epRating" value="' + (i+1).to_s + '">'
          puts '<input type="hidden" name="seriesID" value="' + seriesId.to_s + '">'
          puts '<input type="hidden" name="epID" value="' + episode['epId'].to_s + '">'
          puts '<input type="hidden" name="seasonNumber" value="' + seasonNumber.to_s + '">'
          puts '<input type="hidden" name="rated" value="TRUE">'
          puts '</form>'
        end
        puts '</section>'

        puts "<div class=\"seasonDropdown\">"
        puts '<button class="menuButton"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-three-dots" viewBox="0 0 16 16">
  <path d="M3 9.5a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3m5 0a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3m5 0a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3"/>
</svg></button>'
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
        puts '<form action="otherLists.cgi" method="POST">'
        puts "<button>View on Other's Lists</button>"
        puts '<input type="hidden" name="epId" value="' + episode['epId'].to_s + '">'
        puts '<input type="hidden" name="seriesID" value="' + seriesId.to_s + '">'
        puts '</form>'
        puts "</div>"
        puts "</div>"
        
      puts "</div>"
    puts "</div>"
  puts "</div>"

  puts "<hr>"
  episodeRating = 0
  epNum = epNum + 1
  end

  puts "<br>"
puts "</div>"


# Series Review Modal
puts "<div id='reviewSeriesModal'>"
puts "  <div class='modal fade' id='CreateSeriesReview' tabindex='-1' aria-labelledby='createReviewLabel' aria-hidden='true'>"
puts "    <div class='modal-dialog'>"
puts "      <div class='modal-content'>"
puts "        <div class='modal-header'>"
puts "          <h5 class='modal-title' id='createReviewLabel'>Leave a Review</h5>"
puts "          <button type='button' class='btn-close' data-bs-dismiss='modal' aria-label='Close'></button>"
puts "        </div>"
puts "        <div class='modal-body'>"
puts "          <form id='createSeriesReviewForm' name='createSeriesReviewForm' method='POST' action='threebuttons.cgi'>"
puts "            <div class='row'>"
puts "              <div class='col'>"
puts "                <img src='" + seriesImage + "' alt='' id='mediaReviewImage'>"
puts "              </div>"
  puts "<br>"
puts "              <div class='col' id='showInfo'>"
puts "                <p id='reviewHeader'>I WATCHED…</p>"
puts "                <p id='reviewShowTitle'>" + series.first['showName'] + "</p>"
puts "              </div>"
  puts "<br>"
puts "            </div>"
puts "            <div class='mb-3'>"
puts "              <textarea name='reviewText' class='form-control' id='userReview' placeholder='Add a review…' required></textarea>"
puts "            </div>"
puts "            <div class='row'>"
puts "              <div class='col'>"
#puts "            <section class='Rating'>"

if seriesRating == 0
   puts '<label for="Rating">You must provide a rating: </label><br>'
   #puts '<select name"Rating" id="Rating">'
                    puts '<select id="rating" name="ratingId" class="form-control">'

                    puts '<option value="1">1</option>'
                    puts '<option value="2">2</option>'
                    puts '<option value="3">3</option>'
                    puts '<option value="4">4</option>'
                    puts '<option value="4">5</option>'
  puts '</select>'

else 
ratingId = db.query("SELECT id from seriesRating WHERE username = '" + username.to_s + "' AND seriesId = '" + seriesId.to_s + "';")
ratingId = ratingId.first['id'].to_s
(0...5).each do |i|
 # puts "              <form action='threebuttons.cgi' method='POST'>"
  if (i < seriesRating)
            #puts '<button class="fa fa-star" style="color: yellow;"></button>'
            puts '<i class="fa fa-star" style="font-size:24px;color:yellow"></i>'
          else
            #puts '<button class="fa fa-star"></button>'
            puts '<i class="fa fa-star" style="font-size:24px;color:white"></i>'
          end
=begin
  puts "                <input type='hidden' name='seriesRating' value='#{i}'>"
  puts "                <input type='hidden' name='seriesID' value='#{seriesId}'>"
  puts "                <input type='hidden' name='seasonNumber' value='#{seasonNumber}'>"
  puts "                <input type='hidden' name='rated' value='TRUE'>"
  puts "                <input type='hidden' name='review' value='true'>"
=end
  #puts "              </form>"
end
end
#puts "            </section>"
puts "              </div>"


puts "                <input type='hidden' name='year' value='#{time.year}'>"
puts "                <input type='hidden' name='month' value='#{time.month}'>"
puts "                <input type='hidden' name='day' value='#{time.day}'>"

  puts "                <input type='hidden' name='seriesRating' value='#{seriesRating}'>"
  puts "                <input type='hidden' name='seriesID' value='#{seriesId}'>"
  puts "                <input type='hidden' name='seasonNumber' value='#{seasonNumber}'>"
  puts "                <input type='hidden' name='ratingId' value='#{ratingId}'>"
  puts "                <input type='hidden' name='review' value='true'>"

=begin
puts "              <div class='col'>"
puts "            <button class='LIKES' style='color: pink;'' id='likeBtn'>&#10084</button>"
puts "              </div>"
puts "            </div>"
=end
puts '<br>'
puts "            <div class='modal-footer'>"
puts "              <button type='button' class='btn btn-secondary' data-bs-dismiss='modal'>Close</button>"
puts "              <button type='submit' class='btn btn-primary'>Submit Review</button>"
puts "            </div>"
puts "          </form>"
puts "        </div>"
puts "      </div>"
puts "    </div>"
puts "  </div>"
puts "</div>"

# Season Review Modal
puts "<div id='reviewSeasonModal'>"
puts "  <div class='modal fade' id='CreateSeasonReview' tabindex='-1' aria-labelledby='createReviewLabel' aria-hidden='true'>"
puts "    <div class='modal-dialog'>"
puts "      <div class='modal-content'>"
puts "        <div class='modal-header'>"
puts "          <h5 class='modal-title' id='createReviewLabel'>Leave a Review</h5>"
puts "          <button type='button' class='btn-close' data-bs-dismiss='modal' aria-label='Close'></button>"
puts "        </div>"
puts "        <div class='modal-body'>"
puts "          <form id='createSeasonReviewForm' name='createSeasonReviewForm' method='POST' action='threebuttons.cgi'>"
puts "            <div class='row'>"
puts "              <div class='col'>"
puts "                <img src='" + seriesImage + "' alt='' id='mediaReviewImage'>"
puts "              </div>"
  puts "<br>"
puts "              <div class='col' id='showInfo'>"
puts "                <p id='reviewHeader'>I WATCHED…</p>"
puts "                <p id='reviewShowTitle'>" + series.first['showName'] + "</p>"
puts "                <p id='reviewSENum'>Season " + seasonNumber.to_s + "</p>"
#puts "                <p id='reviewEpName'>Episode Name</p>"
puts "              </div>"
  puts "<br>"
puts "            </div>"
puts "            <div class='mb-3'>"
puts "              <textarea name='reviewText' class='form-control' id='userReview' placeholder='Add a review…' required></textarea>"
puts "            </div>"
puts "            <div class='row'>"
puts "              <div class='col'>"
puts "            <section class='Rating'>"

(0...5).each do |i|
 # puts "              <form action='threebuttons.cgi' method='POST'>"
  if (i < seasonRating)
            puts '<button class="fa fa-star" style="color: yellow;"></button>'
          else
            puts '<button class="fa fa-star"></button>'
          end
  puts "                <input type='hidden' name='seriesRating' value='#{i}'>"
  puts "                <input type='hidden' name='seriesID' value='#{seriesId}'>"
  puts "                <input type='hidden' name='seasonNumber' value='#{seasonNumber}'>"
  puts "                <input type='hidden' name='rated' value='TRUE'>"
  puts "                <input type='hidden' name='review' value='true'>"

  #puts "              </form>"
end
puts "            </section>"
puts "              </div>"


puts "                <input type='hidden' name='year' value='#{time.year}'>"
puts "                <input type='hidden' name='month' value='#{time.month}'>"
puts "                <input type='hidden' name='day' value='#{time.day}'>"

puts "              <div class='col'>"
puts "            <button class='LIKES' style='color: pink;'' id='likeBtn'>&#10084</button>"
puts "              </div>"
puts "            </div>"
puts '<br>'
puts "            <div class='modal-footer'>"
puts "              <button type='button' class='btn btn-secondary' data-bs-dismiss='modal'>Close</button>"
puts "              <button type='submit' class='btn btn-primary'>Submit Review</button>"
puts "            </div>"
puts "          </form>"
puts "        </div>"
puts "      </div>"
puts "    </div>"
puts "  </div>"
puts "</div>"

# Episode Review Modal
puts "<div id='reviewEpisodeModal'>"
puts "  <div class='modal fade' id='CreateEpisodeReview' tabindex='-1' aria-labelledby='createReviewLabel' aria-hidden='true'>"
puts "    <div class='modal-dialog'>"
puts "      <div class='modal-content'>"
puts "        <div class='modal-header'>"
puts "          <h5 class='modal-title' id='createReviewLabel'>Leave a Review</h5>"
puts "          <button type='button' class='btn-close' data-bs-dismiss='modal' aria-label='Close'></button>"
puts "        </div>"
puts "        <div class='modal-body'>"
puts "          <form id='createEpisodeReviewForm' name='createEpisodeReviewForm' method='POST' action='threebuttons.cgi'>"
puts "            <div class='row'>"
puts "              <div class='col'>"
puts "                <img src='" + seriesImage + "' alt='' id='mediaReviewImage'>"
puts "              </div>"
  puts "<br>"
puts "              <div class='col' id='showInfo'>"
puts "                <p id='reviewHeader'>I WATCHED…</p>"
puts "                <p id='reviewShowTitle'>" + series.first['showName'] + "</p>"
puts "                <p id='reviewSENum'>Season " + seasonNumber.to_s + "</p>"
puts "                <p id='reviewEpName'</p>"
puts "              </div>"
  puts "<br>"
puts "            </div>"
puts "            <div class='mb-3'>"
puts "              <textarea name='reviewText' class='form-control' id='userReview' placeholder='Add a review…' required></textarea>"
puts "            </div>"
puts "            <div class='row'>"
puts "              <div class='col'>"

puts "            <section class='Rating'>"

(0...5).each do |i|
 # puts "              <form action='threebuttons.cgi' method='POST'>"
  if (i < episodeRating)
            puts '<button class="fa fa-star" style="color: yellow;"></button>'
          else
            puts '<button class="fa fa-star"></button>'
          end
  puts "                <input type='hidden' name='seriesRating' value='#{i}'>"
  puts "                <input type='hidden' name='seriesID' value='#{seriesId}'>"
  puts "                <input type='hidden' name='seasonNumber' value='#{seasonNumber}'>"
  puts "                <input type='hidden' name='rated' value='TRUE'>"
  puts "                <input type='hidden' name='review' value='true'>"

  #puts "              </form>"
end
puts "            </section>"
puts "              </div>"


puts "                <input type='hidden' name='year' value='#{time.year}'>"
puts "                <input type='hidden' name='month' value='#{time.month}'>"
puts "                <input type='hidden' name='day' value='#{time.day}'>"
=begin
puts "              <div class='col'>"
puts "            <button class='LIKES' style='color: pink;'' id='likeBtn'>&#10084</button>"
puts "              </div>"
puts "            </div>"
=end
puts '<br>'
puts "            <div class='modal-footer'>"
puts "              <button type='button' class='btn btn-secondary' data-bs-dismiss='modal'>Close</button>"
#puts "              <button type='button' class='btn-close' data-bs-dismiss='modal' aria-label='Close'></button>"
puts "              <button type='submit' class='btn btn-primary'>Submit Review</button>"
puts "            </div>"
puts "          </form>"
puts "        </div>"
puts "      </div>"
puts "    </div>"
puts "  </div>"
puts "</div>"

puts "  <script>"
puts "  document.addEventListener('DOMContentLoaded', function () {"
puts "    document.querySelectorAll('.reviewButton').forEach(button => {"
puts "      button.addEventListener('click', function () {"
puts "        const targetModal = document.querySelector(this.getAttribute('data-bs-target'));"
puts "        if (targetModal) {"
puts "          const modalInstance = new bootstrap.Modal(targetModal);"
puts "          modalInstance.show();"
puts "        }"
puts "      });"
puts "    });"
puts "  });"
puts "  </script>"


puts "</body>"
puts "</html>"