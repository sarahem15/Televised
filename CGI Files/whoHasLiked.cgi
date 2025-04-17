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

contentType = cgi['type']
listName = cgi['listName']
listId = cgi['listId']
listCreator = cgi['listCreator']
reviewId = cgi['reviewId']
likes = db.query("SELECT * FROM likedList WHERE listId = '" + listId + "';")
likes = likes.to_a
displayName = db.query("SELECT displayName FROM account WHERE username = '" + listCreator + "';")
listImages = db.query ("SELECT imageName FROM series JOIN curatedListSeries ON curatedListSeries.seriesId = series.showId WHERE curatedListSeries.name ='" + listName + "';")
type = "series"
if listImages.size == 0
    listImages = db.query ("SELECT imageName FROM series JOIN season ON season.seriesId = series.showId JOIN curatedListSeason ON curatedListSeason.seasonId = season.seasonId WHERE curatedListSeason.name ='" + listName + "';")
    type = "seasons"
end
if listImages.size == 0
    listImages = db.query ("SELECT imageName FROM series JOIN season ON season.seriesId = series.showId JOIN episode ON episode.seasonId = season.seasonId JOIN curatedListEpisode ON curatedListEpisode.epId = episode.epId WHERE curatedListEpisode.name ='" + listName + "';")
    type = "episodes"
end
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

    if contentType == "EP"

        reviewContent = db.query("SELECT * FROM seriesReview WHERE id = '" + reviewId + "';")
        if reviewContent.size != 0
            listImage = db.query ("SELECT imageName, showName FROM series WHERE showId ='" + reviewContent.first['seriesId'].to_s + "';")
            likes = db.query("SELECT * FROM likedSeriesReview WHERE reviewId = '" + reviewId + "';")
            likes = likes.to_a

        else
            reviewContent = db.query("SELECT * FROM seasonReview WHERE id = '" + reviewId + "';")
            if reviewContent.size != 0
                listImage = db.query ("SELECT imageName, showName FROM series JOIN season ON season.seriesId = series.showId WHERE showId ='" + reviewContent.first['seasonId'].to_s + "';")
                likes = db.query("SELECT * FROM likedSeasonReview WHERE reviewId = '" + reviewId + "';")
                likes = likes.to_a
            end
            if
                reviewContent = db.query("SELECT * FROM episodeReview WHERE id = '" + reviewId + "';")
                listImage = db.query ("SELECT imageName, showName FROM series JOIN season ON season.seriesId = series.showId JOIN episode ON episode.seasonId = season.seasonId WHERE showId ='" + reviewContent.first['epId'].to_s + "';")
                likes = db.query("SELECT * FROM likedEpisodeReview WHERE reviewId = '" + reviewId + "';")
                likes = likes.to_a
            end
        end
        displayName = db.query("SELECT displayName FROM account WHERE username = '" + reviewContent.first['username'] + "';")
        
=begin 
        if listImages.size == 0
            listImages = db.query ("SELECT imageName FROM series JOIN season ON season.seriesId = series.showId JOIN curatedListSeason ON curatedListSeason.seasonId = season.seasonId WHERE curatedListSeason.name ='" + listName + "';")
            type = "seasons"
        end
        if listImages.size == 0
            listImages = db.query ("SELECT imageName FROM series JOIN season ON season.seriesId = series.showId JOIN episode ON episode.seasonId = season.seasonId JOIN curatedListEpisode ON curatedListEpisode.epId = episode.epId WHERE curatedListEpisode.name ='" + listName + "';")
            type = "episodes"
        end
=end
        puts '<section class="LikesContent" style="margin-left: 5%; margin-right: 5%;">'
    
      puts '<section class="UserDisplay" style="max-width: 390px">'
        puts '<img src="./ProfileImages/' + reviewContent.first['username'] + '.jpg" alt="" style="background-color: gray;">'
        puts '<h3 style="color: #a3afe1;">Likes for <a href="othersProfiles.cgi?username=' +  reviewContent.first['username'] + '">' + displayName.first['displayName'].to_s + '\'s </a> Review</h3>'
      puts '</section>'
      puts '<br>'
      puts '<h3>' + reviewContent.first['review'] + '</h3>'
      puts '<hr style="border-width: 5px; color: #a3afe1;">'
      puts '<div class="Content-type">'
      puts '<section>'
      puts '<h5 id="nameHeader"> Name </h5>'
      puts '<br>'
      if likes.size != 0
        (0...likes.size).each do |i|
            likeDisplayName = db.query("SELECT displayName FROM account JOIN likedSeriesReview ON likedSeriesReview.userWhoLiked = account.username WHERE likedSeriesReview.userWhoLiked = '" + likes[i]['userWhoLiked'] + "';")
            puts '<section class="UserDisplay" style="max-width: 390px">'
                puts '<img src="./ProfileImages/' + likes[i]['userWhoLiked'] + '.jpg" alt="" style="background-color: gray;">'
                puts '<a href="othersProfiles.cgi?username=' + likes[i]['userWhoLiked'] + '"><h3>' + likeDisplayName.first['displayName'].to_s + '</h3></a>'
            puts '</section>'
            puts '<br>'
        end
  else
    puts '<h6>Users who have liked this review will appear here!</h6>'
end
      puts '</section>'
      if listImage.size != 0
          puts '<section>'
            puts '<img src="' + listImage.first['imageName'] + '" alt="" style="width: 50%; height: 80%; object-fit: cover;">'
            puts '<h4>' + listImage.first['showName'] + '</h4>'
          puts '<br>'
          puts '</section>'
          puts '</div>'
        puts '</section>'
    end
    else
    puts '<section class="LikesContent" style="margin-left: 5%; margin-right: 5%;">'
    
      puts '<section class="UserDisplay" style="max-width: 390px">'
        puts '<img src="./ProfileImages/' + listCreator + '.jpg" alt="" style="background-color: gray;">'
        puts '<h3 style="color: #a3afe1;">Likes for ' + displayName.first['displayName'].to_s + '\'s List</h3>'
      puts '</section>'
      puts '<br>'
      puts '<h1>' + listName.gsub("\\'", "'") + '</h1>'
      puts '<hr style="border-width: 5px; color: #a3afe1;">'
      puts '<div class="Content-type">'
      puts '<section>'
      puts '<h5 id="nameHeader"> Name </h5>'
      puts '<br>'
      if likes.size != 0
        (0...likes.size).each do |i|
            likeDisplayName = db.query("SELECT displayName FROM account JOIN likedList ON likedList.userWhoLiked = account.username WHERE likedList.userWhoLiked = '" + likes[i]['userWhoLiked'] + "';")
            puts '<section class="UserDisplay" style="max-width: 390px">'
                puts '<img src="./ProfileImages/' + likes[i]['userWhoLiked'] + '.jpg" alt="" style="background-color: gray;">'
                puts '<a href="othersProfiles.cgi?username=' + likes[i]['userWhoLiked'] + '"><h3>' + likeDisplayName.first['displayName'].to_s + '</h3></a>'
            puts '</section>'
            puts '<br>'
        end

  else
    puts '<h6>Users who have liked this list will appear here!</h6>'
end
      puts '</section>'

      puts '<section>'
      puts '<section class="images">'
      (0...listImages.size).each do |i|
        puts '<img src="' + listImages[i]['imageName'] + '" alt="">'
       end
      puts '</section>'
      puts '<br>'
      puts '<h6 style="text-align: center;">' + listImages.size.to_s + ' ' + type + '</h6>'
      puts '</section>'
      puts '</div>'
    puts '</section>'
end
puts '<!-- Scripts -->'
  puts '<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>'
  puts '<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>'
  puts '<script src="Televised.js"></script>'
puts '</body>'
puts '</html>'
session.close