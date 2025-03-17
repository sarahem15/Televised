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
search = cgi['mediaEntered']
type = "Series"
type = cgi['typeSearch']
seriesId = cgi['seriesId']

listName = cgi['listName']
description = cgi['description']
privacy = cgi['']

db = Mysql2::Client.new(
    host: '10.20.3.4', 
    username: 'seniorproject25', 
    password: 'TV_Group123!', 
    database: 'televised_w25'
  )

if seriesId != ""
    #db.query("INSERT INTO curatedList VALUES('" + username.to_s + "', '" + images.first['showId'] + "', '" + ranking + "');")
end

puts '<!DOCTYPE html>'
puts '<html lang="en">'

puts '<head>'
    puts '<meta charset="UTF-8">'
    puts '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
    puts '<title>Televised</title>'
    puts '<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">'
    puts '<link rel="stylesheet" href="Televised.css">'
puts '</head>'

puts '<body id="createNewList">'
    puts '<nav id="changingNav"></nav> <!-- Navbar dynamically loaded -->'
    puts '<br>'
        puts '<h2 style="text-align: center;">Create a New List</h2>'
        puts '<br>'
    puts '<div class="container-fluid">'
        
        puts '<div class="container">'
                puts '<div class="col-5" id="listRow">'
                    puts '<form id="newListForm" method="post" action="newList.cgi">'
                    puts '<span>Name</span>'
                    puts '<input type="text" id="Name" name="listName" class="form-control">'
                    puts '<br>'
        
                    puts '<label for="Type">Type</label>'
                    puts '<select id="Type" name="type" class="form-control">'
                        puts '<option value="Series">Series</option>'
                        puts '<option value="Seasons">Seasons</option>'
                        puts '<option value="Episodes">Episodes</option>'
                    puts '</select>'
                    puts '<br>'
                    puts '<label for="Views">Who Can View</label>'
                    puts '<select id="views" name="views" class="form-control">'
                        puts '<option value="Public">Public - anyone can view</option>'
                        puts '<option value="Private">Private - no one can view</option>'
                    puts '</select>'
                    puts '<br>'

                    puts '<span>Description</span>'
                    puts '<textarea id="Description" name="description" class="form-control" rows="10"></textarea>'
                    puts '<br>'
                    puts '<br>'
                    puts '<button id="saveList" class="btn" style="background-color: #9daef6;" type="submit">CREATE LIST</button>'
                puts '</form>'
                puts '</div>'
        puts '</div>'
        puts '<div>'
    puts '<div class="TopFiveProfile">'
            puts '<form method="post" action="createNewList.cgi">'
            puts '<select id="type" name="typeSearch" class="form-control">'
                puts '<option value="Series" selected>Series</option>'
                puts '<option value="Seasons">Season</option>'
                puts '<option value="Episodes">Episodes</option>'
            puts '</select>'
                puts '<input type="text" name="mediaEntered" class="top5search">'
                puts '<input type="submit" value="Search">'
            puts '</form>'
    puts '</div>'

    if (type == "Series" && search != "")
        images = db.query("SELECT showName, imageName, showId FROM series WHERE showName like '" + search + "%';")
        images = images.to_a
        if (images.first.to_s != "")
            puts 'Is this the title you\'re looking for?'
            puts '<br>'
            arraySize = images.size
            (0...arraySize).each do |i|
                puts images[i]['showName']
                print '<img src="' + images[i]['imageName'] + '" alt="' + images[i]['imageName'] + '" style=" height: 50px; width: 35px; object-fit: cover;">'
                #puts '<br>'
                #db.query("INSERT INTO topFiveSeries VALUES('" + username.to_s + "', '" + images.first['showId'] + "', '" + ranking + "');")
                images[i]['imageName'] = ""
                puts '<form action="createNewList.cgi" method="POST">'
                puts "<button>ADD</button>"
                puts '<input type="hidden" name="seriesID" value="' + images[i]['seriesId'].to_s + '">'
                #puts '<input type="hidden" name="wantToWatch" value="TRUE">'
                #puts '<input type="hidden" name="seasonNumber" value="' + seasonNumber.to_s + '">'
                puts '</form>'
            end
        else
            puts 'We can\'t seem to find this title!'
        end
    end
    puts '</div>'
    puts '</div>'
    

    
    puts '<!-- Scripts -->'
    puts '<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>'
    puts '<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>'
    puts '<script src="Televised.js"></script>'
puts '</body>'
puts '</html>'

session.close