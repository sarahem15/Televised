#!/usr/bin/ruby
# Switch images to queries from the database
# Enable debugging
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
type = cgi['type']
db = Mysql2::Client.new(
    host: '10.20.3.4', 
    username: 'seniorproject25', 
    password: 'TV_Group123!', 
    database: 'televised_w25'
  )

displayName = db.query("SELECT displayName FROM account WHERE username = '" + username.to_s + "';")
bio = db.query("SELECT bio FROM account WHERE username = '" + username.to_s + "';")
pronouns = db.query("SELECT pronouns FROM account WHERE username = '" + username.to_s + "';")
likedLists = db.query("SELECT * FROM likedList WHERE userWhoLiked = '" + username.to_s + "';")
likedLists = likedLists.to_a
likeCount = 0
if type == ""
  type = "REVIEW"
end
listType = 'SERIES'
listDisplayName = ""
info = ""
puts '<!DOCTYPE html>'
puts '<html lang="en">'

puts '<head>'
puts '<meta charset="UTF-8">'
  puts '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
  puts '<title>Televised</title>'
  puts '<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">'
  puts '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">'
  puts '<link rel="stylesheet" href="Televised.css">'
puts '</head>'

puts '<body id="profile">'
  puts '<nav id="changingNav"></nav> <!-- This is where the navbar will be dynamically loaded -->'
  puts '<div class="container-fluid">'
  puts '<br>'
  puts '<section class="ProfileInfo">'
  puts '<section class="UserDisplay">'
    puts '<img src="ProfileImages/' + username.to_s + '.jpg" alt="">'
    puts '<h3 id="DisplayName">' + displayName.first['displayName'].to_s + '</h3>'
  puts '</section>'
  puts '<h4>' + pronouns.first['pronouns'].to_s + '</h4>'
  puts '<h4>' + bio.first['bio'].to_s + '</h4>'
  puts '</section>'
  puts '<hr>'
     puts '<div class="profileHeader">'
      puts '<a href="Profile.cgi">Favorites</a>'
      puts '<a href="Have_Watched.cgi">Have Watched</a>'
      puts '<a href="Want_to_Watch.cgi">Want to Watch</a>'
      puts '<a href="Profile_Lists.cgi">Lists</a>'
      puts '<a href="Profile_Reviews.cgi">Reviews</a>'
      puts '<a href="#" class="active">Likes</a>'
      puts '<a href="Profile_Ratings.cgi">Ratings</a>'
    puts '</div>'
  puts '<hr>'
  puts '<br>'
  
  puts '<div class="profileListHeader">'
  if type == "REVIEW"
      puts '<a href="#!" class="active">Reviews</a>'
      puts '<a href="Likes_Lists.cgi?type=LIST">Lists</a>'
  elsif type == "LIST"
      puts '<a href="Likes_Lists.cgi">Reviews</a>'
      puts '<a href="#!" class="active">Lists</a>'
  end
    puts '</div>'

puts '<hr style="margin-left: 80px; margin-right: 80px">'
if type == "LIST"
(0...likedLists.size).each do |i|
  seriesImages = db.query("SELECT series.imageName FROM series JOIN curatedListSeries ON curatedListSeries.seriesId = series.showId WHERE curatedListSeries.listId ='" + likedLists[i]['listId'].to_s + "';")
  seriesImages = seriesImages.to_a
  info = db.query("SELECT DISTINCT * FROM curatedListSeries WHERE listId = '" + likedLists[i]['listId'].to_s + "';")
  
  #info = info.to_a
  if info.size != 0
    listDisplayName = db.query("SELECT displayName FROM account WHERE username = '" + info.first['username'] + "';")
    #puts info.first['name']
  elsif info.size == 0
    seriesImages = db.query("SELECT series.imageName FROM series JOIN season ON season.seriesId = series.showId JOIN episode ON episode.seasonId = season.seasonId JOIN curatedListEpisode ON curatedListEpisode.epId = episode.epId WHERE curatedListEpisode.listId ='" + likedLists[i]['listId'].to_s + "';")
    seriesImages = seriesImages.to_a
    info = db.query("SELECT * FROM curatedListEpisode WHERE listId = '" + likedLists[i]['listId'].to_s + "';")
    #info = info.to_a
    if info.size != 0
      listDisplayName = db.query("SELECT displayName FROM account WHERE username = '" + info.first['username'] + "';")
    end
    listType = 'EP'
  end


  puts '<div class="listImages">'
    puts '<div class="listWrapper">'
        puts '<section class="carousel-section" id="listsPlease">'
        (0...5).each do |j|
          if j < seriesImages.size
            puts '<div class="itemS">'
                puts '<img src="' + seriesImages[j]['imageName'] + '" alt="" style="height:270px; object-fit: cover;">'
            puts '</div>'
          end
        end
      puts '</section>'
      puts '</div>'
      puts '<div>'
      puts '<section class="titleDate">'
      if info.first
      puts '<a href="listContents.cgi?title=' + info.first['name'] + '&contentType=' + listType + '"><h3>' + info.first['name'] + '</h3></a>'
      puts '<i><h4>' + info.first['date'].to_s + '</h4></i>'
      puts '</section>'
      puts '<br>'
      puts '<section class="listInfo">'
        puts '<section class="UserDisplay">'
          puts '<img src="./ProfileImages/' + info.first['username'] + '.jpg" alt="" style="background-color: gray;">'
          puts '<a href="othersProfiles.cgi?username=' + info.first['username'] + '"><h3 id="DisplayName">' + listDisplayName.first['displayName'] + '</h3></a>'
        puts '</section>'
      puts '<h3> series </h3>'
      listId = db.query("SELECT id FROM listOwnership WHERE username = '" + info.first['username'] + "' AND listName = '" + info.first['name'] + "';")
      puts '<form action="threebuttons.cgi" method="post">'
      alreadyLiked = db.query("SELECT * FROM likedList WHERE userWhoLiked = '" + username.to_s + "' AND userWhoCreated = '" + info.first['username'] + "' AND listId = '" + listId.first['id'].to_s + "';")
        puts '<button class="LIKES" style="color: pink;">&#10084</button>'
        currentLikes = db.query("SELECT * FROM likedList WHERE listId = '" + listId.first['id'].to_s + "';")
        (0...currentLikes.size).each do |i|
        likeCount = likeCount + 1
      end
        puts '<a href="whoHasLiked.cgi?listName=' + info.first['name'] + '&listCreator=' + info.first['username'] + '&listId=' + listId.first['id'].to_s + '">' + likeCount.to_s + '</a>'
        puts '<input type="hidden" name="likedList" value="TRUE">'
        puts '<input type="hidden" name="profileLikedList" value="TRUE">'
        puts '<input type="hidden" name="listId" value="' + listId.first['id'].to_s + '">'
        puts '<input type="hidden" name="likeUser" value="' + username.to_s + '">'
        puts '<input type="hidden" name="listCreator" value="' + info.first['username'] + '">'
        
    puts '</form>'
      puts '</section>'
      puts '<br>'
      puts '<h3>' + info.first['description'] + '</h3>'
      puts '</div>'
    puts '</div>'

     puts '<br>'
puts '<hr style="margin-left: 80px; margin-right: 80px">'
  end
likeCount = 0
end
else
  #####Series######
  reviews = db.query("SELECT * FROM likedSeriesReview where userWhoLiked = '" + username.to_s + "';")
  reviews = reviews.to_a
  (0...reviews.size).each do |i|
    seriesImage = db.query("SELECT imageName, showName, year FROM series JOIN seriesReview ON series.showId = seriesReview.seriesId WHERE seriesReview.id= '" + reviews[i]['reviewId'].to_s + "';")
    reviewRating = db.query("SELECT rating FROM seriesRating JOIN seriesReview ON seriesRating.id = seriesReview.ratingId WHERE seriesReview.id = '" + reviews[i]['reviewId'].to_s + "';")
    reviewContent = db.query("SELECT * FROM seriesReview WHERE id = '" + reviews[i]['reviewId'].to_s + "';")
    reviewDisplayName = db.query("SELECT displayName FROM account WHERE username = '" + reviews[i]['userWhoReviewed'] + "';")
    puts '<div class="content-L">'
    puts '<form action="series.cgi" method="POST" style="padding: 0;">'
    puts "<input type='image' src=\"" + seriesImage.first['imageName'] + "\"alt=\"" + seriesImage.first['imageName'] + "\" style='height: 270px; width: 200px; object-fit: cover; padding: 1;'>" 
    puts '<input type="hidden" name="clicked_image" value="' + seriesImage.first['imageName'] + '"">'
    puts '<input type="hidden" name="seasonNumber" value="1">'
    puts '</form>'
    puts '<div class="content-R">'
    puts '<section class="UserDisplay">'
         puts '<img src="./ProfileImages/' + reviewContent.first['username'] + '.jpg" alt="" style="background-color: gray;">'
          puts '<a href="othersProfiles.cgi?username=' + reviewContent.first['username'].to_s + '"><h3>' + reviewDisplayName.first['displayName'] + '</h3></a>'
      puts '</section>'
      puts '<br>'
      puts '<section class="NameAndYear">'
      puts '<a href="reviewIndiv.cgi?reviewId=' + reviews[i]['reviewId'].to_s + '">'
      puts '<h3>' + seriesImage.first['showName'] + '</h3></a>'
      puts '<h3 style="color: #436eb1;">' + seriesImage.first['year'].to_s + '</h3>'
      puts '</section>'
  puts '<section class="Rating">'
          (0...5).each do |i|
            if (i < reviewRating.first['rating'].to_i)
                puts '<i class="fa fa-star" style="color: white;"></i>'
              else
                puts '<i class="fa fa-star"></i>'
              end
          end
        puts '</section>'
       puts '<h3>' + reviewContent.first['review'] + '</h3>'


      likes = db.query("SELECT * FROM likedSeriesReview WHERE reviewId = '" + reviews[i]['reviewId'].to_s + "';")
      likes = likes.to_a
      (0...likes.size).each do |i|
        likeCount = likeCount + 1
    end

    puts '<form class="LikeAndCount" action="Likes_Lists.cgi" method="POST">'
    puts '<button class="LIKES" style="color: pink;">&#10084</button>'
    puts '<input type="hidden" name="likedReview" value="TRUE">'
    puts '<a href="whoHasLiked.cgi?reviewId=' + reviews[i]['reviewId'].to_s + '&type=EP">' + likeCount.to_s + '</a>'
    #puts likeCount.to_s
    puts '<input type="hidden" name="reviewId" value="' + reviews[i]['reviewId'].to_s + '">'
    puts '<input type="hidden" name="reviewCreator" value="' + reviews[i]['userWhoReviewed'].to_s + '">'
    puts '</form>'

       puts '<i><h5 style="color: #436eb1; text-align: right;">' + reviewContent.first['date'].to_s + '</h5></i>'
  puts '</div>'
puts '</div>'
puts '<hr style="margin-left: 80px; margin-right: 80px">'
  likeCount = 0
  end
   #########Seasons############
    reviews = db.query("SELECT * FROM likedSeasonReview where userWhoLiked = '" + username.to_s + "';")
    reviews = reviews.to_a
  (0...reviews.size).each do |i|
    seriesImage = db.query("SELECT imageName, showName, series.year, season.seasonNum FROM series JOIN season ON season.seriesId = series.showId JOIN seasonReview ON season.seasonId = seasonReview.seasonId WHERE seasonReview.id = '" + reviews[i]['reviewId'].to_s + "';")
    reviewRating = db.query("SELECT rating FROM seasonRating JOIN seasonReview ON seasonRating.id = seasonReview.ratingId WHERE seasonReview.id = '" + reviews[i]['reviewId'].to_s + "';")
    reviewContent = db.query("SELECT * FROM seasonReview WHERE id = '" + reviews[i]['reviewId'].to_s + "';")
    reviewDisplayName = db.query("SELECT displayName FROM account WHERE username = '" + reviews[i]['userWhoReviewed'] + "';")
    puts '<div class="content-L">'
    puts '<form action="series.cgi" method="POST" style="padding: 0;">'
    puts "<input type='image' src=\"" + seriesImage.first['imageName'] + "\"alt=\"" + seriesImage.first['imageName'] + "\" style='height: 300px; width: 250px; object-fit: cover; padding: 1;'>" 
    puts '<input type="hidden" name="clicked_image" value="' + seriesImage.first['imageName'] + '"">'
    puts '<input type="hidden" name="seasonNumber" value="' + seriesImage.first['seasonNum'].to_s + '">'
    puts '</form>'
    puts '<div class="content-R">'
    puts '<section class="UserDisplay">'
         puts '<img src="./ProfileImages/' + reviewContent.first['username'] + '.jpg" alt="" style="background-color: gray;">'
          puts '<a href="othersProfiles.cgi?username=' + reviewContent.first['username'].to_s + '"><h3>' + reviewDisplayName.first['displayName'] + '</h3></a>'
      puts '</section>'
      puts '<br>'
      puts '<section class="NameAndYear">'
      puts '<a href="reviewIndiv.cgi?reviewId=' + reviews[i]['reviewId'].to_s + '&contentType=SEASON">'
      puts '<h3>' + seriesImage.first['showName'] + '</h3>'
      puts '<h3>Season ' + seriesImage.first['seasonNum'].to_s + '</h3></a>'
      puts '<h3 style="color: #436eb1;">' + seriesImage.first['year'].to_s + '</h3>'
      puts '</section>'
  puts '<section class="Rating">'
          (0...5).each do |i|
            if (i < reviewRating.first['rating'].to_i)
                puts '<i class="fa fa-star" style="color: white;"></i>'
              else
                puts '<i class="fa fa-star"></i>'
              end
          end
        puts '</section>'
       puts '<h3>' + reviewContent.first['review'] + '</h3>'


      likes = db.query("SELECT * FROM likedSeasonReview WHERE reviewId = '" + reviews[i]['reviewId'].to_s + "';")
      likes = likes.to_a
      (0...likes.size).each do |i|
        likeCount = likeCount + 1
    end
    puts '<form  class="LikeAndCount" action="Likes_Lists.cgi" method="POST">'
    puts '<button class="LIKES" style="color: pink;">&#10084</button>'
    puts '<input type="hidden" name="likedReview" value="TRUE">'
    puts '<a href="whoHasLiked.cgi?reviewId=' + reviews[i]['reviewId'].to_s + '&type=EP">' + likeCount.to_s + '</a>'
    #puts likeCount.to_s
    puts '<input type="hidden" name="reviewId" value="' + reviews[i]['reviewId'].to_s + '">'
    puts '<input type="hidden" name="reviewCreator" value="' + reviews[i]['userWhoReviewed'].to_s + '">'
    puts '</form>'

       puts '<i><h5 style="color: #436eb1; text-align: right;">' + reviewContent.first['date'].to_s + '</h5></i>'
  puts '</div>'
puts '</div>'
puts '<hr style="margin-left: 80px; margin-right: 80px">'
  likeCount = 0
  end

#########Episodes############
    reviews = db.query("SELECT * FROM likedEpisodeReview where userWhoLiked = '" + username.to_s + "';")
    reviews = reviews.to_a
  (0...reviews.size).each do |i|
    seriesImage = db.query("SELECT imageName, showName, series.year, season.seasonNum, episode.epName FROM series JOIN season ON season.seriesId = series.showId JOIN episode ON episode.seasonId = season.seasonId JOIN episodeReview ON episode.epId = episodeReview.epId WHERE episodeReview.id = '" + reviews[i]['reviewId'].to_s + "';")
    reviewRating = db.query("SELECT rating FROM seasonRating JOIN seasonReview ON seasonRating.id = seasonReview.ratingId WHERE seasonReview.id = '" + reviews[i]['reviewId'].to_s + "';")
    reviewContent = db.query("SELECT * FROM episodeReview WHERE id = '" + reviews[i]['reviewId'].to_s + "';")
    reviewDisplayName = db.query("SELECT displayName FROM account WHERE username = '" + reviews[i]['userWhoReviewed'] + "';")
    puts '<div class="content-L">'
    puts '<form action="series.cgi" method="POST" style="padding: 0; width: 250px;">'
    puts "<input type='image' src=\"" + seriesImage.first['imageName'] + "\"alt=\"" + seriesImage.first['imageName'] + "\" style='height: 300px; width: 250px; object-fit: cover; padding: 1;'>" 
    puts '<input type="hidden" name="clicked_image" value="' + seriesImage.first['imageName'] + '"">'
    puts '<input type="hidden" name="seasonNumber" value="' + seriesImage.first['seasonNum'].to_s + '">'
    puts '</form>'
    puts '<div class="content-R">'
    puts '<section class="UserDisplay">'
         puts '<img src="./ProfileImages/' + reviewContent.first['username'] + '.jpg" alt="" style="background-color: gray;">'
          puts '<a href="othersProfiles.cgi?username=' + reviewContent.first['username'].to_s + '"><h3>' + reviewDisplayName.first['displayName'] + '</h3></a>'
      puts '</section>'
      puts '<br>'
      puts '<section class="NameAndYear">'
      puts '<a href="reviewIndiv.cgi?reviewId=' + reviews[i]['reviewId'].to_s + '&contentType=EP">'
      puts '<h3>' + seriesImage.first['showName'] + '</h3>'
      puts '<h3>S' + seriesImage.first['seasonNum'].to_s + ' ' + seriesImage.first['epName'] + '</h3></a>'
      puts '<h3 style="color: #436eb1;">' + seriesImage.first['year'].to_s + '</h3>'
      puts '</section>'
  puts '<section class="Rating">'
          (0...5).each do |i|
            if (i < reviewRating.first['rating'].to_i)
                puts '<i class="fa fa-star" style="color: white;"></i>'
              else
                puts '<i class="fa fa-star"></i>'
              end
          end
        puts '</section>'
       puts '<h3>' + reviewContent.first['review'] + '</h3>'

      likes = db.query("SELECT * FROM likedEpisodeReview WHERE reviewId = '" + reviews[i]['reviewId'].to_s + "';")
      likes = likes.to_a
      (0...likes.size).each do |i|
        likeCount = likeCount + 1
    end
    puts '<form  class="LikeAndCount" action="Likes_Lists.cgi" method="POST">'
    puts '<button class="LIKES" style="color: pink;">&#10084</button>'
    puts '<input type="hidden" name="likedReview" value="TRUE">'
    puts '<a href="whoHasLiked.cgi?reviewId=' + reviews[i]['reviewId'].to_s + '&type=EP">' + likeCount.to_s + '</a>'
    #puts likeCount.to_s
    puts '<input type="hidden" name="reviewId" value="' + reviews[i]['reviewId'].to_s + '">'
    puts '<input type="hidden" name="reviewCreator" value="' + reviews[i]['userWhoReviewed'].to_s + '">'
    puts '</form>'

       puts '<i><h5 style="color: #436eb1; text-align: right;">' + reviewContent.first['date'].to_s + '</h5></i>'
  puts '</div>'
puts '</div>'
puts '<hr style="margin-left: 80px; margin-right: 80px">'
  likeCount = 0
  end
end
 puts '<br>'
  puts '<br>'
    puts '<!-- Scripts -->'
  puts '<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>'
  puts '<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>'
  puts '<script src="Televised.js"></script>'
puts '</body>'
puts '</html>'