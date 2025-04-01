#!/usr/bin/ruby
$stdout.sync = true
$stderr.reopen $stdout

puts "Content-type: text/html\n\n"
require 'mysql2'
require 'cgi'
require 'open-uri'
require 'cgi/session'
time = Time.new

cgi = CGI.new
session = CGI::Session.new(cgi)
username = session['username']

episodeName = cgi['ep_name']
showName = cgi['show_name']
epNum = cgi['ep_num']
seasonNumber = cgi['seasonNumber']
seriesId = cgi['seriesID']
db = Mysql2::Client.new(
    host: '10.20.3.4', 
    username: 'seniorproject25', 
    password: 'TV_Group123!', 
    database: 'televised_w25'
  )

#seriesImage = db.query("SELECT imageName FROM series WHERE showName = '" + showName + "';")
episode = db.query("SELECT episode.* FROM episode JOIN season ON episode.seasonId = season.seasonId JOIN series ON season.seriesId = series.showId WHERE episode.epName = '" + episodeName + "' AND series.showName = '" + showName.gsub("'", "\\\\'") + "';")

episodeRating = 0
sumRating = 0
avgRating = 0
ratings = db.query("SELECT rating FROM episodeRating where epId = '" + episode.first['epId'].to_s + "';")
ratings = ratings.to_a
(0...ratings.size).each do |i|
  sumRating = sumRating + ratings[i]['rating'].to_i
end
if ratings.size != 0
  avgRating = sumRating/ratings.size
end

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
    def url_exists?(url)
      begin
        URI.open(url)
        true
      rescue OpenURI::HTTPError, SocketError
        false
      end
    end

    imageSource = "https://cs.transy.edu/Televised/Episodes/" + showName.gsub(" ", "").gsub("'", "") + seasonNumber.to_s + "." + epNum.to_s + "." + 1.to_s + ".jpg"
    valid = url_exists?(imageSource)
    if valid
      (1...4).each do |i|
      puts "<img src=\"Episodes/" + showName.gsub(" ", "").gsub("'", "") + seasonNumber.to_s + "." + epNum.to_s + "." + i.to_s + ".jpg\" alt=\"\">" 
    end

      #puts "<img src=\"./Episodes/" + seriesImage.split('.')[0] + seasonNumber.to_s + "." + epNum.to_s + ".1.jpg\" alt=\"" + seriesImage + "\" width=\"300\" height=\"225\">"
    else
      puts "<img src=\"./Episodes/Televised.jpg\" width=\"300\" height=\"225\" id=\"defaultImage\">"
    end


    #(1...4).each do |i|
    #  puts "<img src=\"Episodes/" + showName.gsub(" ", "").gsub("'", "") + seasonNumber.to_s + "." + epNum.to_s + "." + i.to_s + ".jpg\" alt=\"\">" 
    #end
    puts "<br>"
    puts "<br>"
      puts "<h1 style=\"font-family: 'Times New Roman', Times, serif; color: white; text-align: center;\">" + showName + "</h1>"
      puts "<div class=\"epWords\">"
      puts "<h3> Season 1 </h3>"
      puts "<h3> Episode " + epNum.to_s + "</h3>"
      puts '<section class="avgRating">'
        if avgRating != 0
          (0...5).each do |j|
            if (j < avgRating)
                puts '<i class="fa fa-star" style="color: white;"></i>'
            else
              puts '<i class="fa fa-star"></i>'
            end
          end
        else
            puts '<h3 style="width: 300px;">NO AVG RATING</h3>'
        end
        puts '</section>'
      puts "<h3>" + episode.first['epName'] + "</h3>"
      puts "<h3>" + episode.first['releaseDate'] + "</h3>"
      puts "<h3 style=\"text-align: center;\">" + episode.first['runtime'].to_s + "m</h3>"
    puts "</div>"
   puts "<br>"
  puts "<h4 class=\"epDes\">"
  puts "<span>" + episode.first['description'] + "</span></h4>"
  puts "<br>"
  puts "<br>"
  puts "<div class=\"editButtons\">"
      puts '<form action="threebuttons.cgi" method="POST">'
        alreadyWatchedEpisode = db.query("SELECT * FROM haveWatchedEpisode WHERE username = '" + username.to_s + "'AND epId = '" + episode.first['epId'].to_s + "';")
        if (alreadyWatchedEpisode.to_a.to_s != "[]")
          puts '<button class="watchedButton"><i class="eye-icon fa fa-eye" style="color: #6bdf10;"></i></button>'
        else
          puts '<button class="watchedButton"><i class="eye-icon fa fa-eye"></i></button>'
        end
        #puts "<button class=\"watchedButton\">EYE</button>"

        puts '<input type="hidden" name="seriesID" value="' + seriesId + '">'
        puts '<input type="hidden" name="epID" value="' + episode.first['epId'].to_s + '">'
        puts '<input type="hidden" name="watchedButton" value="TRUE">'
        puts '<input type="hidden" name="seasonNumber" value="' + seasonNumber.to_s + '">'
        puts '<input type="hidden" name="fromIndivEp" value="TRUE">'
        puts '<input type="hidden" name="epNum" value="' + epNum + '">'
        puts '</form>'
        puts "<button class=\"reviewButton\" data-bs-toggle=\"modal\" data-bs-target=\"#CreateEpisodeReview\">&#128488</button>"

        alreadyRatedEpisode = db.query("SELECT * FROM episodeRating WHERE username = '" + username + "' AND epId = '" + episode.first['epId'].to_s + "';")
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
          puts '<input type="hidden" name="epID" value="' + episode.first['epId'].to_s + '">'
          puts '<input type="hidden" name="seasonNumber" value="' + seasonNumber.to_s + '">'
          puts '<input type="hidden" name="rated" value="TRUE">'
          puts '<input type="hidden" name="fromIndivEp" value="TRUE">'
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
        #puts '<input type="hidden" name="seriesID" value="' + seriesId.to_s + '">'
        puts '<input type="hidden" name="seriesID" value="' + seriesId.to_s + '">'
        puts '<input type="hidden" name="epID" value="' + episode.first['epId'].to_s + '">'
        puts '<input type="hidden" name="wantToWatch" value="TRUE">'
        puts '<input type="hidden" name="seasonNumber" value="' + seasonNumber.to_s + '">'
        puts '</form>'
        puts '<form action="threebuttons.cgi" method="POST">'
        puts "<button>Add to Existing List</button>"
        #puts '<input type="hidden" name="seriesID" value="' + seriesId.to_s + '">'
        puts '<input type="hidden" name="seriesID" value="' + seriesId.to_s + '">'
        puts '<input type="hidden" name="epID" value="' + episode.first['epId'].to_s + '">'
        puts '<input type="hidden" name="addToExisting" value="TRUE">'
        puts '<input type="hidden" name="seasonNumber" value="' + seasonNumber.to_s + '">'
        puts '</form>'
        puts '<form action="threebuttons.cgi" method="POST">'
        puts "<button>Add to New List</button>"
        #puts '<input type="hidden" name="seriesID" value="' + seriesId.to_s + '">'
        puts '<input type="hidden" name="seriesID" value="' + seriesId.to_s + '">'
        puts '<input type="hidden" name="epID" value="' + episode.first['epId'].to_s + '">'
        puts '</form>'
        puts '<form action="otherLists.cgi" method="POST">'
        puts "<button>View on Other's Lists</button>"
        #puts '<input type="hidden" name="seriesID" value="' + seriesId.to_s + '">'
        puts '<input type="hidden" name="seriesID" value="' + seriesId.to_s + '">'
        puts '<input type="hidden" name="epID" value="' + episode.first['epId'].to_s + '">'
        puts '<input type="hidden" name="viewOnOthers" value="TRUE">'
        puts '<input type="hidden" name="seasonNumber" value="' + seasonNumber.to_s + '">'
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
  puts '<h4> Reviews </h4>'
epReviews = db.query("SELECT * FROM episodeReview WHERE epId = '" + episode.first['epId'].to_s + "';" )
epReviews = epReviews.to_a
if epReviews.size == 0 
  puts '<h5 style="text-align: center;"> Reviews for this episode will appear here! </h5>'
  puts '<br>'
else
  puts '<section class="epReviews">'
  (0...epReviews.size).each do |i|
    puts '<div class="ReviewIndiv">'
    puts '<div class="ReviewContent">'
    reviewDisplayName = db.query("SELECT displayName FROM account WHERE username = '" + epReviews[i]['username'] + "';")
        puts '<section class="UserDisplay">'
            puts '<img src="./ProfileImages/' + epReviews[i]['username'] + '.jpg" alt="" style="height: 50px; width: 50px; corner-rounding: 100%">'
            puts '<h3>' + reviewDisplayName.first['displayName'] + '</h3>'
            #RATING!
        puts '</section>'
        puts '<br>'
        puts '<br>'
        puts '<h4>' + epReviews[i]['review'] + '</h4>'
        puts '<section class="Likes">'
          puts '<h5 id="Heart">&#9829</h5>'
          puts '<h4>12</h4>' #db query to get likes
        puts '</section>'
    puts '</div>'
  puts '</div>'
end
puts '</section>'
puts "</div>"
end
=begin
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

if valid
  puts "<img src=\"Episodes/" + showName.gsub(" ", "").gsub("'", "") + seasonNumber.to_s + "." + epNum.to_s + ".1.jpg\" alt=\"\" id=\"mediaReviewImage\">" 
else
  puts "<img src=\"./Episodes/Televised.jpg\" width=\"300\" height=\"225\" id=\"mediaReviewImage\">"
end

puts "              </div>"
  puts "<br>"
puts "              <div class='col' id='showInfo'>"
puts "                <p id='reviewHeader'>I WATCHED…</p>"
puts "                <p id='reviewShowTitle'>" + showName + "</p>"
puts "                <p id='reviewSENum'>Season " + seasonNumber.to_s + "</p>"
puts "                <p id='reviewEpName'>" + episode.first['epName'] + "</p>"
puts "              </div>"
  puts "<br>"
puts "            </div>"
puts "            <div class='mb-3'>"
puts "              <textarea name='reviewText' class='form-control' id='userReview' placeholder='Add a review…' required></textarea>"
puts "            </div>"
puts "            <div class='row'>"
puts "              <div class='col'>"

#puts "            <section class='Rating'>"


if episodeRating == 0
   puts '<label for="Rating">You must provide a rating: </label><br>'
                    puts '<select id="rating" name="episodeRating" class="form-control">'

                    puts '<option value="1">1</option>'
                    puts '<option value="2">2</option>'
                    puts '<option value="3">3</option>'
                    puts '<option value="4">4</option>'
                    puts '<option value="5">5</option>'
  puts '</select>'


else 
ratingId = db.query("SELECT id from episodeRating WHERE username = '" + username.to_s + "' AND epId = '" + episode.first['epId'].to_s + "';")
ratingId = ratingId.first['id'].to_s
(0...5).each do |i|
  if (i < episodeRating)
            puts '<i class="fa fa-star" style="font-size:24px;color:yellow"></i>'
          else
            puts '<i class="fa fa-star" style="font-size:24px;color:white"></i>'
          end

end
end

puts "              </div>"


puts "                <input type='hidden' name='year' value='#{time.year}'>"
puts "                <input type='hidden' name='month' value='#{time.month}'>"
puts "                <input type='hidden' name='day' value='#{time.day}'>"

puts "                <input type='hidden' name='seasonRating' value='#{episodeRating}'>"
puts "                <input type='hidden' name='seriesID' value='#{seriesId}'>"
#puts "                <input type='hidden' name='seasonId' value='#{seasonId}'>"
puts "                <input type='hidden' name='seasonNumber' value='#{seasonNumber}'>"
puts "                <input type='hidden' name='epname' value='" + episode.first['epName'] + "'>"
puts "                <input type='hidden' name='rated' value='TRUE'>"
puts "                <input type='hidden' name='review' value='true'>"
puts '                <input type="hidden" name="fromIndivEp" value="TRUE">'

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
=end
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