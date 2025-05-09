#!/usr/bin/ruby
# SOURCES:
## FILE TYPE - https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/file
require 'mysql2'
require 'cgi'
require 'cgi/session'


# Enable debugging
$stdout.sync = true
$stderr.reopen $stdout

# Initialize CGI
cgi = CGI.new
session = CGI::Session.new(cgi)
username = session['username']
search = cgi['top5search'].gsub("'", "\\\\'")
type = cgi['typeSearch']
topSeries = cgi['topSeries']
topSeason = cgi['topSeason']
ranking = cgi['rank']
seasonNum = cgi['seasonNum']
selectedSeries = cgi['SELECT']
epNum = cgi['epNum']
seriesQuery = cgi['seriesQuery']
seriesId = cgi['seriesId']
removeSeries = cgi['removeSeries']
removeSeason = cgi['removeSeason']
removeEp = cgi['removeEp']
seasonId = cgi['seasonId']
epId = cgi['epId']
if seasonNum == ""
    seasonNum = "1"
end
seriesQuery = ""
tempCount = 0
db = Mysql2::Client.new(
    host: '10.20.3.4', 
    username: 'seniorproject25', 
    password: 'TV_Group123!', 
    database: 'televised_w25'
  )

displayName = db.query("SELECT displayName FROM account WHERE username = '" + username.to_s + "';")
bio = db.query("SELECT bio FROM account WHERE username = '" + username.to_s + "';")
pronouns =db.query("SELECT pronouns FROM account WHERE username = '" + username.to_s + "';")
replies = db.query("SELECT replies FROM account WHERE username = '" + username.to_s + "';")
topFiveSeries = db.query("SELECT seriesId FROM topFiveSeries WHERE username = '" + username.to_s + "';")
if type == ""
    type = "Series"
end

if removeSeries != ""
    begin
        db.query("DELETE FROM topFiveSeries WHERE username = '" + username.to_s + "' AND seriesId ='" + seriesId + "';")
    rescue => e
    end
elsif removeSeason != ""
    begin
        db.query("DELETE FROM topFiveSeason WHERE username = '" + username.to_s + "' AND seasonId ='" + seasonId + "';")
    rescue => e
    end
elsif removeEp != ""
    begin
        db.query("DELETE FROM topFiveEpisode WHERE username = '" + username.to_s + "' AND epId ='" + epId + "';")
    rescue => e
    end
end

puts "Content-type: text/html\n\n"


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

puts '<body id="profileSettings">'
    puts '<nav id="changingNav"></nav>' # <!-- Navbar dynamically loaded -->
    puts '<div class="container-fluid">'
        puts '<br>'
        puts '<h2 style="text-align: center;">Settings</h2>'
        puts '<br>'
        puts '<div class="container">'
                puts '<div class="col-5" id="profileRow">'
                    puts '<form id="profileSettinsForm" enctype="multipart/form-data" method="post" action="editProfile.cgi">'
                    #puts '<span>Username</span>'
                    puts '<input type="hidden" id="userName" name="userNameX" class="form-control" readonly>'
                    #puts '<br>'
                    puts '<span>Display Name &#128397;</span>'
                    puts '<input type="text" id="displayName" value="' + displayName.first['displayName'].to_s + '" name="displayName" class="form-control" >'
                    puts '<br>'
                    puts '<span>Bio &#128397;</span>'
                    puts '<textarea id="bio" name="bio" class="form-control" rows="5">' + bio.first['bio'].to_s + '</textarea>'
                    puts '<br>'
                    puts '<label for="pronouns">Pronouns &#128397;</label>'
                    puts '<select id="pronouns" name="pronouns" class="form-control">'
                    if pronouns.first['pronouns'].to_s == 'She/Her'
                        puts '<option value="She/Her" selected>She/Her</option>'
                        puts '<option value="She/They">She/They</option>'
                        puts '<option value="He/They">He/They</option>'
                        puts '<option value="He/Him">He/Him</option>'
                        puts '<option value="They/Them">They/Them</option>'
                        puts '<option value="Prefer Not to Answer">Prefer Not to Answer</option>'
                    elsif pronouns.first['pronouns'].to_s == 'She/They'
                        puts '<option value="She/Her">She/Her</option>'
                        puts '<option value="She/They" selected>She/They</option>'
                        puts '<option value="He/They">He/They</option>'
                        puts '<option value="He/Him">He/Him</option>'
                        puts '<option value="They/Them">They/Them</option>'
                        puts '<option value="Prefer Not to Answer">Prefer Not to Answer</option>'
                    elsif pronouns.first['pronouns'].to_s == 'He/They'
                        puts '<option value="She/Her">She/Her</option>'
                        puts '<option value="She/They">She/They</option>'
                        puts '<option value="He/They" selected>He/They</option>'
                        puts '<option value="He/Him">He/Him</option>'
                        puts '<option value="They/Them">They/Them</option>'
                        puts '<option value="Prefer Not to Answer">Prefer Not to Answer</option>'
                    elsif pronouns.first['pronouns'].to_s == 'He/Him'
                        puts '<option value="She/Her">She/Her</option>'
                        puts '<option value="She/They">She/They</option>'
                        puts '<option value="He/They">He/They</option>'
                        puts '<option value="He/Him" selected>He/Him</option>'
                        puts '<option value="They/Them">They/Them</option>'
                        puts '<option value="Prefer Not to Answer">Prefer Not to Answer</option>'
                    elsif pronouns.first['pronouns'].to_s == 'They/Them'
                        puts '<option value="She/Her">She/Her</option>'
                        puts '<option value="She/They">She/They</option>'
                        puts '<option value="He/They">He/They</option>'
                        puts '<option value="He/Him">He/Him</option>'
                        puts '<option value="They/Them" selected>They/Them</option>'
                        puts '<option value="Prefer Not to Answer">Prefer Not to Answer</option>'
                    else 
                        puts '<option value="She/Her">She/Her</option>'
                        puts '<option value="She/They">She/They</option>'
                        puts '<option value="He/They">He/They</option>'
                        puts '<option value="He/Him">He/Him</option>'
                        puts '<option value="They/Them">They/Them</option>'
                        puts '<option value="Prefer Not to Answer" selected>Prefer Not to Answer</option>'
                    end
                    puts '</select>'
                    puts '<br>'
                    puts '<label for="replies">Who can reply to your reviews &#128397;</label>'
                    puts '<select id="replies" name="replies" class="form-control">'

                    if replies.first['replies'].to_i == 1
                        puts '<option value="Public" selected>Public - anyone can reply</option>'
                        puts '<option value="Private">Private - no one can reply</option>'
                    else
                        puts '<option value="Private" selected>Private - no one can reply</option>'
                        puts '<option value="Public">Public - anyone can reply</option>'
                    end
                    puts '</select>'
                    puts '<br>'
                    puts '<span>Avatar <i>(JPEG or PNG)</i> &#128397;</span>'
                    puts '<input type="File" name="fileName" accept="image/png, image/jpeg, image/jpg">'
                    puts '<br>'
                    puts '<br>'
                    puts '<br>'
                    #puts '<input type="hidden" name="seriesQuery" value="' + seriesQuery + '">'
                    puts '<button id="saveProfile" class="btn" style="background-color: #9daef6;" type="submit">Save Changes</button>'
                puts '</form>'
                puts '</div>'

        puts '<div class="TopFiveProfile">'
            puts '<section class="labels">'
                puts '<label>Media Type &#9660</label>'
                if type == "Episodes"
                    puts '<label>Season &#9660</label>'
                end
                puts '<label>Search</label>'
            puts '</section>'
            puts '<form id="imageSearch" method="post" action="Profile_Settings.cgi">'
            puts '<select id="type" name="typeSearch" class="form-control">'
            if type == "Series"
                puts '<option value="Series" selected>Series </option>'
                puts '<option value="Season">Season</option>'
                puts '<option value="Episodes">Episodes</option>'
            elsif type == "Season"
                puts '<option value="Series">Series</option>'
                puts '<option value="Season" selected>Season </option>'
                puts '<option value="Episodes">Episodes</option>'
            else
                puts '<option value="Series">Series</option>'
                puts '<option value="Season">Season</option>'
                puts '<option value="Episodes" selected>Episodes </option>'
            end

            puts '</select>'
            if type == "Episodes"
                puts '<select id="type" name="seasonNum" class="form-control">'
                if seasonNum == '1'
                    puts '<option value="1" selected>1 </option>'
                    puts '<option value="2">2</option>'
                    puts '<option value="3">3</option>'
                elsif seasonNum == '2'
                    puts '<option value="1">1</option>'
                    puts '<option value="2" selected>2 </option>'
                    puts '<option value="3">3</option>'
                else
                    puts '<option value="1">1</option>'
                    puts '<option value="2">2</option>'
                    puts '<option value="3" selected>3</option>'
                end
                puts '</select>'
            end
                puts '<input type="text" name="top5search" class="top5search">'
                puts '<input type="submit" value="Search">'
            puts '</form>'

            puts '<br>'
            if (type == "Series" && search != "")
                images = db.query("SELECT showName, imageName, showId FROM series WHERE showName like '" + search + "%';")
                images = images.to_a
                if (images.first.to_s != "")
                    puts 'Is this the title you\'re looking for?'
                    puts '<br>'
                    arraySize = images.size
                    (0...arraySize).each do |i|
                        puts '<form method="get" action="Profile_Settings.cgi">'
                        puts images[i]['showName']
                        puts '<img src="' + images[i]['imageName'] + '" alt="' + images[i]['imageName'] + '" style=" height: 50px; width: 35px; object-fit: cover;">'
                        puts '<input type="hidden" name="topSeries" value="' + images[i]['showId'].to_s + '">'
                        puts '<input type="hidden" name="typeSearch" value="Series">'
                        puts '<select id="type" name="rank" class="form-control">'
                            puts '<option value="SELECT" selected>RANK</option>'
                            puts '<option value="1">1</option>'
                            puts '<option value="2">2</option>'
                            puts '<option value="3">3</option>'
                            puts '<option value="4">4</option>'
                            puts '<option value="5">5</option>'
                        puts '</select>'
                        puts '<input type="submit" value="SELECT">'
                        #puts '<input type="hidden" name="top5search" value="' + search + '">'
                        puts '</form>'
                        puts '<br>'
                        images[i]['imageName'] = ""
                    end 
                else
                    puts 'We can\'t seem to find this title!'
                end
            elsif (type == "Season" && search != "")
                images = db.query("SELECT showName, imageName, showId FROM series WHERE showName like '" + search + "%';")
                images = images.to_a
                if (images.first.to_s != "")
                    puts 'Is this the title you\'re looking for?'
                    puts '<br>'
                    arraySize = images.size
                    (0...arraySize).each do |i|
                        seasons = db.query("SELECT seasonId from season WHERE seriesId = '" + images[i]['showId'].to_s + "';")
                        seasons = seasons.to_a
                        #puts seasons.first['seasonId'].to_s
                        puts '<form method="get" action="Profile_Settings.cgi">'
                        puts images[i]['showName']
                        puts '<img src="' + images[i]['imageName'] + '" alt="' + images[i]['imageName'] + '" style=" height: 50px; width: 35px; object-fit: cover;">'
                        puts '<input type="hidden" name="topSeason" value="' + images[i]['showId'].to_s + '">'
                        puts '<input type="hidden" name="typeSearch" value="Season">'
                         puts '<select id="typeSeason" name="seasonNum" class="form-control">'
                         puts '<option value="" selected>Season</option>'
                            (0...seasons.size).each do |h|
                                puts '<option value="' + seasons[h]['seasonId'].to_s + '">' + (h+1).to_s + '</option>'
                            end
                        puts '</select>'
                        puts '<select id="type" name="rank" class="form-control">'
                            puts '<option value="SELECT" selected>RANK</option>'
                            puts '<option value="1">1</option>'
                            puts '<option value="2">2</option>'
                            puts '<option value="3">3</option>'
                            puts '<option value="4">4</option>'
                            puts '<option value="5">5</option>'
                        puts '</select>'
                        #puts '<input type="hidden" name="top5search" value="' + search + '">'
                        puts '<input type="submit" value="SELECT">'
                        puts '</form>'
                        puts '<br>'
                        images[i]['imageName'] = ""
                    end 
                else
                    puts 'We can\'t seem to find this title!'
                end
            elsif (type == "Episodes" && search != "")
                images = db.query("SELECT showName, imageName, showId FROM series WHERE showName like '" + search + "%';")
                images = images.to_a
                if (images.first.to_s != "")
                    puts 'Is this the title you\'re looking for?'
                    puts '<br>'
                    arraySize = images.size
                    (0...arraySize).each do |i|
                        seasons = db.query("SELECT seasonId from season WHERE seriesId = '" + images[i]['showId'].to_s + "';")
                        seasons = seasons.to_a
                        #puts seasons.first['seasonId'].to_s
                        puts '<form method="get" action="Profile_Settings.cgi">'
                        puts images[i]['showName']
                        puts '<img src="' + images[i]['imageName'] + '" alt="' + images[i]['imageName'] + '" style=" height: 50px; width: 35px; object-fit: cover;">'
                        puts '<input type="hidden" name="topSeason" value="' + images[i]['showId'].to_s + '">'
                        puts '<input type="hidden" name="typeSearch" value="Episodes">'
                        episodes = db.query("SELECT * FROM episode JOIN season ON season.seasonId = episode.seasonId WHERE seasonNum = '" + seasonNum + "' AND seriesId = '" + images[i]['showId'].to_s + "';")
                        episodes = episodes.to_a
                        puts '<select id="typeSeason" name="epNum" class="form-control">'
                         puts '<option value="" selected>Episode</option>'
                            (0...episodes.size).each do |h|
                                puts '<option value="' + episodes[h]['epId'].to_s + '">' + episodes[h]['epName'] + '</option>'
                            end
                        puts '</select>'
                        puts '<select id="type" name="rank" class="form-control" style="width: 60px;">'
                            puts '<option value="SELECT">Rank</option>'
                            puts '<option value="1">1</option>'
                            puts '<option value="2">2</option>'
                            puts '<option value="3">3</option>'
                            puts '<option value="4">4</option>'
                            puts '<option value="5">5</option>'
                        puts '</select>'
                        puts '<input type="submit" value="select" style="width: 60px;">'
                        #puts '<input type="hidden" name="top5search" value="' + search + '">'
                        puts '</form>'
                        puts '<br>'
                        images[i]['imageName'] = ""
                    end 
                else
                    puts 'We can\'t seem to find this title!'
                end
            end
            if (type == "Series" && ranking != "" && ranking != "SELECT")
                alreadyRated = db.query("SELECT * FROM topFiveSeries WHERE username = '" + username.to_s + "' AND ranking = '" + ranking + "';")
                alreadyAdded = db.query("SELECT * FROM topFiveSeries WHERE username = '" + username.to_s + "' AND seriesId = '" + topSeries + "';")
                if (alreadyRated.to_a.to_s != '[]' && alreadyAdded.to_a.to_s != '[]')
                    db.query("DELETE FROM topFiveSeries WHERE username = '" + username.to_s + "' AND ranking = '" + ranking + "';")
                    db.query("DELETE FROM topFiveSeries WHERE username = '" + username.to_s + "' AND seriesId = '" + topSeries + "';")
                    db.query("INSERT INTO topFiveSeries VALUES('" + username.to_s + "', '" + topSeries + "', '" + ranking + "');")
                    begin
                        db.query("INSERT INTO haveWatchedSeries VALUES ('" + username.to_s + "', '" + topSeries + "');")
                    rescue => e
                    end
                elsif (alreadyRated.to_a.to_s != '[]')
                    db.query("DELETE FROM topFiveSeries WHERE username = '" + username.to_s + "' AND ranking = '" + ranking + "';")
                    db.query("INSERT INTO topFiveSeries VALUES('" + username.to_s + "', '" + topSeries + "', '" + ranking + "');")
                    begin
                        db.query("INSERT INTO haveWatchedSeries VALUES ('" + username.to_s + "', '" + topSeries + "');")
                    rescue => e
                    end
                elsif (alreadyAdded.to_a.to_s != '[]')
                    db.query("DELETE FROM topFiveSeries WHERE username = '" + username.to_s + "' AND seriesId = '" + topSeries + "';")
                    db.query("INSERT INTO topFiveSeries VALUES('" + username.to_s + "', '" + topSeries + "', '" + ranking + "');")
                    begin
                        db.query("INSERT INTO haveWatchedSeries VALUES ('" + username.to_s + "', '" + topSeries + "');")
                    rescue => e
                    end
                else
                    db.query("INSERT INTO topFiveSeries VALUES('" + username.to_s + "', '" + topSeries + "', '" + ranking + "');")
                    begin
                        db.query("INSERT INTO haveWatchedSeries VALUES ('" + username.to_s + "', '" + topSeries + "');")
                    rescue => e
                    end
                end
            elsif (type == "Season" && ranking != "" && ranking != "SELECT" && seasonNum != "")
                alreadyRated = db.query("SELECT * FROM topFiveSeason WHERE username = '" + username.to_s + "' AND ranking = '" + ranking + "';")
                alreadyAdded = db.query("SELECT * FROM topFiveSeason WHERE username = '" + username.to_s + "' AND seasonId = '" + seasonNum + "';")
                if (alreadyRated.to_a.to_s != '[]' && alreadyAdded.to_a.to_s != '[]')
                    db.query("DELETE FROM topFiveSeason WHERE username = '" + username.to_s + "' AND ranking = '" + ranking + "';")
                    db.query("DELETE FROM topFiveSeason WHERE username = '" + username.to_s + "' AND seasonId = '" + seasonNum + "';")
                    db.query("INSERT INTO topFiveSeason VALUES('" + username.to_s + "', '" + seasonNum + "', '" + ranking + "');")
                    begin
                        db.query("INSERT INTO haveWatchedSeason VALUES ('" + username.to_s + "', '" + seasonNum + "');")
                    rescue => e
                    end
                elsif (alreadyRated.to_a.to_s != '[]')
                    db.query("DELETE FROM topFiveSeason WHERE username = '" + username.to_s + "' AND ranking = '" + ranking + "';")
                    db.query("INSERT INTO topFiveSeason VALUES('" + username.to_s + "', '" + seasonNum + "', '" + ranking + "');")
                    begin
                        db.query("INSERT INTO haveWatchedSeason VALUES ('" + username.to_s + "', '" + seasonNum + "');")
                    rescue => e
                    end
                elsif (alreadyAdded.to_a.to_s != '[]')
                    db.query("DELETE FROM topFiveSeason WHERE username = '" + username.to_s + "' AND seasonId = '" + seasonNum + "';")
                    db.query("INSERT INTO topFiveSeason VALUES('" + username.to_s + "', '" + seasonNum + "', '" + ranking + "');")
                    begin
                        db.query("INSERT INTO haveWatchedSeason VALUES ('" + username.to_s + "', '" + seasonNum + "');")
                    rescue => e
                    end
                else
                    db.query("INSERT INTO topFiveSeason VALUES('" + username.to_s + "', '" + seasonNum + "', '" + ranking + "');")
                    begin
                        db.query("INSERT INTO haveWatchedSeason VALUES ('" + username.to_s + "', '" + seasonNum + "');")
                    rescue => e
                    end
                end
            elsif (type == "Episodes" && ranking != "" && ranking != "SELECT" && seasonNum != "" && epNum != "")
                alreadyRated = db.query("SELECT * FROM topFiveEpisode WHERE username = '" + username.to_s + "' AND ranking = '" + ranking + "';")
                alreadyAdded = db.query("SELECT * FROM topFiveEpisode WHERE username = '" + username.to_s + "' AND epId = '" + epNum + "';")
                if (alreadyRated.to_a.to_s != '[]' && alreadyAdded.to_a.to_s != '[]')
                    db.query("DELETE FROM topFiveEpisode WHERE username = '" + username.to_s + "' AND ranking = '" + ranking + "';")
                    db.query("DELETE FROM topFiveEpisode WHERE username = '" + username.to_s + "' AND epId = '" + epNum + "';")
                    db.query("INSERT INTO topFiveEpisode VALUES('" + username.to_s + "', '" + epNum + "', '" + ranking + "');")
                    begin
                        db.query("INSERT INTO haveWatchedEpisode VALUES ('" + username.to_s + "', '" + epNum + "');")
                    rescue => e
                    end
                elsif (alreadyRated.to_a.to_s != '[]')
                    db.query("DELETE FROM topFiveEpisode WHERE username = '" + username.to_s + "' AND ranking = '" + ranking + "';")
                    db.query("INSERT INTO topFiveEpisode VALUES('" + username.to_s + "', '" + epNum + "', '" + ranking + "');")
                    begin
                        db.query("INSERT INTO haveWatchedEpisode VALUES ('" + username.to_s + "', '" + epNum + "');")
                    rescue => e
                    end
                elsif (alreadyAdded.to_a.to_s != '[]')
                    db.query("DELETE FROM topFiveEpisode WHERE username = '" + username.to_s + "' AND epId = '" + epNum + "';")
                    db.query("INSERT INTO topFiveEpisode VALUES('" + username.to_s + "', '" + epNum + "', '" + ranking + "');")
                    begin
                        db.query("INSERT INTO haveWatchedEpisode VALUES ('" + username.to_s + "', '" + epNum + "');")
                    rescue => e
                    end
                else
                    db.query("INSERT INTO topFiveEpisode VALUES('" + username.to_s + "', '" + epNum + "', '" + ranking + "');")
                    begin
                        db.query("INSERT INTO haveWatchedEpisode VALUES ('" + username.to_s + "', '" + epNum + "');")
                    rescue => e
                    end
                end
            end 

            size = 0
            
            #seasons = db.query("SELECT season.* FROM season JOIN series ON season.seriesId = series.showId WHERE series.imageName = '" + seriesImage + "';")
            topSeriesImage = db.query("SELECT series.imageName, series.showName, series.showId, topFiveSeries.ranking FROM series JOIN topFiveSeries ON series.showId = topFiveSeries.seriesId WHERE username = '" + username.to_s + "' ORDER BY ranking ASC;")
            topSeriesImage = topSeriesImage.to_a
            puts '<h3>My Top Five Favs <span class="infoQuestion"><i class="fa fa-question-circle"></i><p class="info" style="font-size: 65%;"> To add to your top five favorite series, seasons, and episodes, use the search bar above and rank them! </p></span></h3>'
            puts '<h5>Shows</h5>'
            puts '<div class="TopFiveSeries">'
                puts '<div class="wrapper">'
                    puts '<section class="carousel-section" id="section' + size.to_s() + '">'
                    (0...5).each do |i|
                        puts '<div class="item">'
                            #puts topSeriesImage.size
                            if (tempCount < topSeriesImage.size)
                                if (topSeriesImage[tempCount]['ranking'].to_i == (i + 1))
                                    puts '<form action="series.cgi" method="POST">'
                                    puts '<input type="image" src="' + topSeriesImage[tempCount]['imageName'] + '" alt="' + topSeriesImage[tempCount]['imageName'] + '" style=" height: 100px; width: 80px">'
                                    puts '<input type="hidden" name="clicked_image" value="' + topSeriesImage[tempCount]['imageName'] + '">'
                                else
                                    puts '<input type="image" src="" alt="" style=" height: 100px; width: 80px">'
                                    puts '<input type="hidden" name="clicked_image" value="">'
                                end
                            else
                                puts '<input type="image" src="" alt="" style=" height: 100px; width: 80px">'
                                puts '<input type="hidden" name="clicked_image" value="">'
                            end
                                puts '<input type="hidden" name="seasonNumber" value="1">'
                                
                            puts '</form>'
                            if topSeriesImage[tempCount] && (topSeriesImage[tempCount]['ranking'].to_i == (i + 1))
                                puts '<h6 style="text-align: center;">' + topSeriesImage[tempCount]['showName'].to_s + '</h6>'
                                puts '<span class="tooltiptext">'
                                puts '<form action="Profile_Settings.cgi" method="POST">'
                                puts' <input type="submit" name="removeSeries" value="X">'
                                puts '<input type="hidden" name="seriesId" value="' + topSeriesImage[tempCount]['showId'].to_s + '">'
                                puts '</form></span>'
                                tempCount = tempCount + 1
                            end
                        puts '</div>'
                    end
                    puts '</section>'
                puts '</div>'
                puts '</div>'
                tempCount = 0
                #Season
                topSeasonImage = db.query("SELECT series.imageName, series.showName, season.seasonNum, season.seasonId, topFiveSeason.ranking FROM series JOIN season ON series.showId = season.seriesId JOIN topFiveSeason ON season.seasonId = topFiveSeason.seasonId WHERE username = '" + username.to_s + "' ORDER BY topFiveSeason.ranking ASC;")
                topSeasonImage = topSeasonImage.to_a
                puts '<h5>Seasons</h5>'
                puts '<div class="TopFiveSeason">'
                puts '<div class="wrapper">'
                    puts '<section class="carousel-section" id="section' + size.to_s() + '">'
                    (0...5).each do |i|
                        puts '<div class="item">'
                            if (tempCount < topSeasonImage.size)
                                if (topSeasonImage[tempCount]['ranking'].to_i == (i + 1))
                                    puts '<form action="series.cgi" method="POST">'
                                    puts '<input type="image" src="' + topSeasonImage[tempCount]['imageName'] + '" alt="" style=" height: 100px; width: 80px">'
                                    puts '<input type="hidden" name="clicked_image" value="' + topSeasonImage[tempCount]['imageName'] + '">'
                                    puts '<input type="hidden" name="seasonNumber" value="' + topSeasonImage[tempCount]['seasonNum'].to_s + '">'
                                else
                                    puts '<input type="image" src="" alt="" style=" height: 100px; width: 80px">'
                                    puts '<input type="hidden" name="clicked_image" value="">'
                                end
                            else
                                puts '<input type="image" src="" alt="" style=" height: 100px; width: 80px">'
                                puts '<input type="hidden" name="clicked_image" value="">'
                            end
                                
                            puts '</form>'
                            if topSeasonImage[tempCount] && (topSeasonImage[tempCount]['ranking'].to_i == (i + 1))
                                puts '<h6 style="text-align: center;">' + topSeasonImage[tempCount]['showName'].to_s + '</h6>'
                                puts '<h6 style="text-align: center;">Season ' + topSeasonImage[tempCount]['seasonNum'].to_s + '</h6>'
                                puts '<span class="tooltiptext">'
                                puts '<form action="Profile_Settings.cgi" method="POST">'
                                puts' <input type="submit" name="removeSeason" value="X">'
                                puts '<input type="hidden" name="seasonId" value="' + topSeasonImage[tempCount]['seasonId'].to_s + '">'
                                puts '</form></span>'
                                tempCount = tempCount + 1
                            end
                        puts '</div>'
                    end
                    puts '</section>'
                puts '</div>'
                puts '</div>'

                tempCount = 0
                episodeNum = 0
                #Episode
                topEpImage = db.query("SELECT series.imageName, series.showName, season.seasonNum, episode.epName, episode.epId, topFiveEpisode.ranking FROM series JOIN season ON series.showId = season.seriesId JOIN episode ON season.seasonId = episode.seasonId JOIN topFiveEpisode ON episode.epId = topFiveEpisode.epId WHERE username = '" + username.to_s + "' ORDER BY topFiveEpisode.ranking ASC;")
                topEpImage = topEpImage.to_a
                puts '<h5>Episodes</h5>'
                puts '<div class="TopFiveEpisode">'
                puts '<div class="wrapper">'
                    puts '<section class="carousel-section" id="section' + size.to_s() + '">'
                    (0...5).each do |i|
                        puts '<div class="item">'
                            if (tempCount < topEpImage.size)
                                if (topEpImage[tempCount]['ranking'].to_i == (i + 1))
                                    allEps = db.query("SELECT epName FROM episode JOIN season ON season.seasonId = episode.seasonId JOIN series ON series.showId = season.seriesId WHERE showName = '" + topEpImage[tempCount]['showName'].gsub("'", "\\\\'") + "';")
                                    allEps = allEps.to_a
                                    (0...allEps.size).each do |j|
                                        if allEps[j]['epName'] == topEpImage[tempCount]['epName']
                                          episodeNum = j + 1
                                        end
                                    end 
                                    puts '<form action="indivEp.cgi" method="POST">'
                                    puts '<input type="image" src="' + topEpImage[tempCount]['imageName'] + '" alt="' + topEpImage[tempCount]['imageName'] + '" style=" height: 100px; width: 80px">'
                                    puts '<input type="hidden" name="ep_name" value="' + topEpImage[tempCount]['epName'] + '">'
                                    puts '<input type="hidden" name="show_name" value="' + topEpImage[tempCount]['showName'] + '">'
                                    puts '<input type="hidden" name="seriesId" value="' + topEpImage[tempCount]['showId'].to_s + '">'
                                    puts '<input type="hidden" name="ep_num" value="' + episodeNum.to_s + '">'
                                    puts '<input type="hidden" name="seasonNumber" value="' + topEpImage[tempCount]['seasonNum'].to_s + '">'
                                else
                                    puts '<input type="image" src="" alt="" style=" height: 100px; width: 80px">'
                                    puts '<input type="hidden" name="clicked_image" value="">'
                                end
                            else
                                puts '<input type="image" src="" alt="" style=" height: 100px; width: 80px">'
                                puts '<input type="hidden" name="clicked_image" value="">'
                            end
                                
                            puts '</form>'
                            if topEpImage[tempCount] && (topEpImage[tempCount]['ranking'].to_i == (i + 1))
                                puts '<h6 style="text-align: center;">' + topEpImage[tempCount]['showName'].to_s + '</h6>'
                                puts '<h6 style="text-align: center;">S' + topEpImage[tempCount]['seasonNum'].to_s + ' ' + topEpImage[tempCount]['epName'].to_s + '</h6>'
                                puts '<span class="tooltiptext">'
                                puts '<form action="Profile_Settings.cgi" method="POST">'
                                puts' <input type="submit" name="removeEp" value="X">'
                                puts '<input type="hidden" name="epId" value="' + topEpImage[tempCount]['epId'].to_s + '">'
                                puts '</form></span>'
                                tempCount = tempCount + 1
                            end
                        puts '</div>'
                    end
                    puts '</section>'
                puts '</div>'
            puts '</div>'
        puts '</div>'
        puts '</div>'


    puts '</div>'
    # <!-- Scripts -->
    puts '<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>'
    puts '<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>'
    puts '<script src="Televised.js"></script>'
    puts '<script>'
    puts "      document.getElementById('imageSearch').addEventListener('submit', function (event) {"
    puts "        event.preventDefault();"
    puts "        }"
    puts '    document.addEventListener("click", function (event) {' 
    puts "        event.preventDefault();"
    puts '        if (event.target.classList.contains("top5search")) {' 
    puts '    let top5search = event.target.dataset.top5search;'

=begin
    puts '            let seriesName = event.target.dataset.seriesName;'
    puts '            let seriesArray = JSON.parse(sessionStorage.getItem("seriesArray")) || [];'
    puts '            if (!seriesArray.some(s => s.id === seriesId)) {' 
    puts '                seriesArray.push({ id: seriesId, name: seriesName });' 
    puts '                sessionStorage.setItem("seriesArray", JSON.stringify(seriesArray));'
    puts '                updateSeriesList();'
    puts '            }'
=end

    puts '}'
    puts "</script>"
    puts '</body>'

puts '</html>'
session.close