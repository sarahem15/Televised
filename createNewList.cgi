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
        images.each do |image|
            puts "<p>#{image['showName']} <img src='#{image['imageName']}' alt='#{image['showName']}' style='height: 50px; width: 35px; object-fit: cover;'>"
            puts "<button class='addToList btn btn-success' data-series-id='#{image['showId']}' data-series-name='#{image['showName']}'>ADD</button></p>"
        end
    else
        puts '<p>We can\'t seem to find this title!</p>'
    end
    exit
end

# Full page HTML
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
puts '<nav id="changingNav"></nav>'
puts '<h2 class="text-center mt-3">Create a New List</h2>'
puts '<div class="container-fluid">'
puts '<div class="row">'

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

# Placeholder for search results
puts '<div id="searchResults"></div>'

puts '</div>'
puts '</div>'
puts '</div>'

# JavaScript Section (Updated for Removing Items)
puts '<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>'
puts '<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>'
puts '<script src="Televised.js"></script>'
puts '<script>'
puts 'document.addEventListener("DOMContentLoaded", function () {'

# AJAX Search Handling
puts '    document.getElementById("searchForm").addEventListener("submit", function (event) {'
puts '        event.preventDefault();'
puts '        let searchInput = document.querySelector("input[name=\'mediaEntered\']").value;' 
puts '        let type = document.querySelector("select[name=\'typeSearch\']").value;'

puts '        fetch("createNewList.cgi", {'
puts '            method: "POST",'
puts '            headers: { "Content-Type": "application/x-www-form-urlencoded" },'
puts '            body: new URLSearchParams({ mediaEntered: searchInput, typeSearch: type })'
puts '        })'
puts '        .then(response => response.text())'
puts '        .then(data => { document.getElementById("searchResults").innerHTML = data; });'
puts '    });'

# Add & Remove Series Handling
puts '    document.addEventListener("click", function (event) {'
puts '        if (event.target.classList.contains("addToList")) {'
puts '            event.preventDefault();'
puts '            let seriesId = event.target.dataset.seriesId;'
puts '            let seriesName = event.target.dataset.seriesName;'
puts '            let seriesArray = JSON.parse(sessionStorage.getItem("seriesArray")) || [];'
puts '            if (seriesId && !seriesArray.some(s => s.id === seriesId)) {'
puts '                seriesArray.push({ id: seriesId, name: seriesName });'
puts '                sessionStorage.setItem("seriesArray", JSON.stringify(seriesArray));'
puts '                updateSeriesList();'
puts '            }'
puts '        } else if (event.target.classList.contains("deleteSeries")) {'
puts '            event.preventDefault();'
puts '            let seriesId = event.target.dataset.seriesId;'
puts '            let seriesArray = JSON.parse(sessionStorage.getItem("seriesArray")) || [];'
puts '            seriesArray = seriesArray.filter(series => series.id !== seriesId);'
puts '            sessionStorage.setItem("seriesArray", JSON.stringify(seriesArray));'
puts '            updateSeriesList();'
puts '        }'
puts '    });'

# Function to Update List
puts '    function updateSeriesList() {'
puts '        let listColumn = document.getElementById("seriesList");'
puts '        let seriesArray = JSON.parse(sessionStorage.getItem("seriesArray")) || [];'
puts '        listColumn.innerHTML = "";'
puts '        seriesArray.forEach(series => {'
puts '            let listItem = document.createElement("li");'
puts '            listItem.className = "list-group-item d-flex justify-content-between align-items-center";'
puts '            listItem.innerHTML = series.name + " <button class=\'btn btn-danger btn-sm deleteSeries\' data-series-id=\'" + series.id + "\'>X</button>";'
puts '            listColumn.appendChild(listItem);'
puts '        });'
puts '        document.getElementById("seriesArrayInput").value = JSON.stringify(seriesArray);'
puts '    }'

puts '    updateSeriesList();'
puts '});'
puts '</script>'

puts '</body>'
puts '</html>'

session.close
