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
search = cgi['top5search']
type = "Series"
type = cgi['typeSearch']
topSeries = cgi['topSeries']
ranking = cgi['rank']
selectedSeries = cgi['SELECT']
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
#topFiveSeries = db.query("SELECT imageName FROM TopFiveSeries WHERE username = '" + username.to_s + "';")
puts "Content-type: text/html\n\n"


puts '<!DOCTYPE html>'
puts '<html lang="en">'

puts '<head>'
    puts '<meta charset="UTF-8">'
    puts '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
    puts '<title>Televised</title>'
    puts '<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">'
    puts '<link rel="stylesheet" href="Televised.css">'
puts '</head>'

puts '<body id="profileSettings">'
    puts '<nav id="changingNav"></nav>' # <!-- Navbar dynamically loaded -->
    puts '<div class="container-fluid">'
        puts '<br>'
        puts '<h2 style="text-align: center;">Profile Settings</h2>'
        puts '<br>'
        puts '<div class="container">'
                puts '<div class="col-5" id="profileRow">'
                    puts '<form id="profileSettinsForm" enctype="multipart/form-data" method="post" action="editProfile.cgi">'
                    puts '<span>Username</span>'
                    puts '<input type="text" id="userName" name="userNameX" class="form-control" readonly>'
                    puts '<br>'
                    puts '<span>Display Name</span>'
                    puts '<input type="text" id="displayName" value="' + displayName.first['displayName'].to_s + '" name="displayName" class="form-control" >'
                    puts '<br>'
                    puts '<span>Bio</span>'
                    puts '<textarea id="bio" name="bio" class="form-control" rows="5">' + bio.first['bio'].to_s + '</textarea>'
                    puts '<br>'
                    puts '<label for="pronouns">Pronouns</label>'
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
                    puts '<label for="replies">Replies</label>'
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
                    puts '<span>Avatar</span>'
                    puts '<input type="File" name="fileName" accept="image/png, image/jpeg">'
                    puts '<br>'
                    puts '<br>'
                    puts '<br>'
                    puts '<button id="saveProfile" class="btn" style="background-color: #9daef6;" type="submit">Save Changes</button>'
                puts '</form>'
                puts '</div>'

        puts '<div class="TopFiveProfile">'
            puts '<form method="post" action="Profile_Settings.cgi">'
            puts '<select id="type" name="typeSearch" class="form-control">'
                puts '<option value="Series" selected>Series</option>'
                puts '<option value="Seasons">Season</option>'
                puts '<option value="Episodes">Episodes</option>'
            puts '</select>'
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
                        #puts '<input type="hidden" name="topSeries" value="' + images.first['showId'] + '">'
                        puts '<select id="type" name="rank" class="form-control">'
                            puts '<option value="1" selected> 1</option>'
                            puts '<option value="2">2</option>'
                            puts '<option value="3">3</option>'
                            puts '<option value="4">4</option>'
                            puts '<option value="5">5</option>'
                        puts '</select>'
                        puts '<input type="submit" value="SELECT">'
                        puts '</form>'
                        puts '<br>'
                        #db.query("INSERT INTO topFiveSeries VALUES('" + username.to_s + "', '" + images.first['showId'] + "', '" + ranking + "');")
                        images[i]['imageName'] = ""
                    end

                    if (selectedSeries != "")
                        #db.query("INSERT INTO topFiveSeries VALUES('" + username.to_s + "', '" + topSeries + "', '" + ranking + "');")
                    end
                else
                    puts 'We can\'t seem to find this title!'
                end
            end


            size = 0
            #topSeriesImages = db.query("SELECT ")
            (0...3).each do |h|
            puts '<div class="TopFiveSeries">'
                puts '<div class="wrapper">'
                    puts '<section class="carousel-section" id="section' + size.to_s() + '">'
                    (0...5).each do |i|
                        puts '<div class="item">'
                            puts '<form action="series.cgi" method="POST">'
                                puts '<input type="image" src="" alt="" style=" height: 100px; width: 80px">'
                                puts '<input type="hidden" name="clicked_image" value="">'
                                puts '<input type="hidden" name="seasonNumber" value="">'
                            puts '</form>'
                        puts '</div>'
                    end
                    puts '</section>'
            puts '</div>'
            end
            puts '</div>'
        puts '</div>'
        puts '</div>'


    puts '</div>'
    # <!-- Scripts -->
    puts '<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>'
    puts '<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>'
    puts '<script src="Televised.js"></script>'
puts '</body>'

puts '</html>'
session.close