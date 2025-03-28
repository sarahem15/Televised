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
type = cgi['typeSearch']
seriesId = cgi['seriesId']

listName = cgi['listName']
description = cgi['description']
privacy = cgi['views']

db = Mysql2::Client.new(
    host: '10.20.3.4', 
    username: 'seniorproject25', 
    password: 'TV_Group123!', 
    database: 'televised_w25'
)

# If listName is provided, insert it into the database
if listName && !listName.empty?
    db.query("INSERT INTO curatedListSeries (username, name, description, privacy, date) 
              VALUES ('#{username}', '#{db.escape(listName)}', '#{db.escape(description)}', '#{privacy}', NOW())")
    list_id = db.last_id
    
    selected_series = JSON.parse(cgi['seriesArray'] || '[]')
    selected_series.each do |series_id|
        db.query("INSERT INTO curatedListSeries (username, seriesId, name, description, privacy, date, listId)
                  VALUES ('#{username}', '#{series_id}', '#{db.escape(listName)}', '#{db.escape(description)}', '#{privacy}', NOW(), '#{list_id}')")
    end
end

# Check if this is an AJAX search request
if type == "Series" && search != ""
    images = db.query("SELECT showName, imageName, showId FROM series WHERE showName LIKE '#{search}%'")
    if !images.to_a.empty?
        # Only return search results in the response, not the whole page
        images.each do |image|
            puts "<p>#{image['showName']} <img src='#{image['imageName']}' alt='#{image['showName']}' style='height: 50px; width: 35px; object-fit: cover;'>"
            puts "<button class='addToList btn btn-success' data-series-id='#{image['showId']}' data-series-name='#{image['showName']}'>ADD</button></p>"
        end
    else
        puts '<p>We can\'t seem to find this title!</p>'
    end
    exit  # Exit here to prevent the full HTML page from being rendered for AJAX requests
end

# Full page HTML (if it's not an AJAX request)
puts '<!DOCTYPE html>'
puts '<html lang="en">'
puts '<head>'
puts '    <meta charset="UTF-8">'
puts '    <meta name="viewport" content="width=device-width, initial-scale=1.0">'
puts '    <title>Televised</title>'
puts '    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">'
puts '    <link rel="stylesheet" href="Televised.css">'
puts '</head>'

puts '<body id="createNewList">'
puts    '<nav id="changingNav"></nav>'
puts    '<h2 class="text-center mt-3">Create a New List</h2>'
puts    '<div class="container-fluid">'
puts        '<div class="row">'

# Left Column - Form to Create List
puts '<div class="col" id="listRow">'
puts '<h3 class="text-center">List Details</h3>'
puts '<form id="newListForm" method="post" action="createNewList.cgi">'
puts '<label>Name</label>'
puts '<input type="text" name="listName" class="form-control" placeholder="Name">'
puts '<br>'
puts '<label>Who Can View</label>'
puts '<select name="views" class="form-control">'
puts '<option value="Public">Public - anyone can view</option>'
puts '<option value="Private">Private - no one can view</option>'
puts '</select>'
puts '<br>'
puts '<label>Description</label>'
puts '<textarea name="description" class="form-control" rows="5"></textarea>'
puts '<br>'
puts '<input type="hidden" id="seriesArrayInput" name="seriesArray">'
puts '<button id="saveList" class="btn btn-primary" type="submit">CREATE LIST</button>'
puts '</form>'
puts '</div>'

# Middle Column - Selected Series List
puts '<div class="col" id="listColumn">'
puts '<h3 class="text-center">Selected Series</h3>'
puts '<ul id="seriesList" class="list-group"></ul>'
puts '</div>'

# Right Column - Search for Series
puts '<div class="col" id="searchColumn">'
puts '<h3 class="text-center">Search for a Series</h3>'
puts '<form id="searchForm">'
puts '<select id="type" name="typeSearch" class="form-control">'
puts '<option value="Series" selected>Series</option>'
puts '<option value="Seasons">Seasons</option>'
puts '<option value="Episodes">Episodes</option>'
puts '</select>'
puts '<br>'
puts '<input type="text" name="mediaEntered" class="form-control">'
puts '<input type="submit" value="Search" class="btn btn-secondary mt-2">'
puts '</form>'

puts '</div>'
puts '</div>'
puts '</div>'

# JavaScript Section (same as before)
puts '<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>'
puts '<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>'
puts '<script src="Televised.js"></script>'
puts '<script>'
puts 'document.addEventListener("DOMContentLoaded", function () {'

# Your existing JavaScript code here (search functionality, adding/deleting series, etc.)

puts '</script>'

puts '</body>'
puts '</html>'

session.close
