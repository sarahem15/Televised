#!/usr/bin/ruby
$stdout.sync = true
$stderr.reopen $stdout

puts "Content-type: text/html\n\n"
require 'mysql2'
require 'cgi'
require 'cgi/session'
require 'json'

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

# Middle Column - Selected Series List (Clears on Page Load)
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
puts '<input type="text" id="mediaEntered" name="mediaEntered" class="form-control">'
puts '<button type="submit" class="btn btn-secondary mt-2">Search</button>'
puts '</form>'
puts '<div id="searchResults"></div>'  # Dynamic Search Results
puts '</div>'
puts '</div>'
puts '</div>'

# JavaScript Section
puts '<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>'
puts '<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>'
puts '<script src="Televised.js"></script>'
puts '<script>'
puts 'document.addEventListener("DOMContentLoaded", function () {'
puts '    let seriesArray = JSON.parse(sessionStorage.getItem("seriesArray")) || [];'
puts '    sessionStorage.removeItem("seriesArray");'  # Clear the middle column on load
puts '    updateSeriesList();'

# AJAX Search Function
puts '    document.getElementById("searchForm").addEventListener("submit", function (event) {'
puts '        event.preventDefault();'
puts '        let formData = new FormData(this);'
puts '        fetch("createNewList.cgi", {'
puts '            method: "POST",'
puts '            body: formData'
puts '        })'
puts '        .then(response => response.text())'
puts '        .then(html => {'
puts '            document.getElementById("searchResults").innerHTML = html;'
puts '        })'
puts '        .catch(error => console.error("Error:", error));'
puts '    });'

# Click event for adding series
puts '    document.addEventListener("click", function (event) {'
puts '        if (event.target.classList.contains("addToList")) {'
puts '            event.preventDefault();'
puts '            let seriesId = event.target.dataset.seriesId;'
puts '            let seriesName = event.target.dataset.seriesName;'
puts '            if (seriesId && !seriesArray.some(s => s.id === seriesId)) {'
puts '                seriesArray.push({ id: seriesId, name: seriesName });'
puts '                sessionStorage.setItem("seriesArray", JSON.stringify(seriesArray));'
puts '                updateSeriesList();'
puts '            }'
puts '        }'
puts '    });'

# Click event for deleting series
puts '    document.addEventListener("click", function (event) {'
puts '        if (event.target.classList.contains("deleteSeries")) {'
puts '            event.preventDefault();'
puts '            let seriesId = event.target.dataset.seriesId;'
puts '            seriesArray = seriesArray.filter(s => s.id !== seriesId);'
puts '            sessionStorage.setItem("seriesArray", JSON.stringify(seriesArray));'
puts '            updateSeriesList();'
puts '        }'
puts '    });'

# Function to update the series list display
puts '    function updateSeriesList() {'
puts '        let listColumn = document.getElementById("seriesList");'
puts '        listColumn.innerHTML = "";'
puts '        seriesArray.forEach(series => {'
puts '            let listItem = document.createElement("li");'
puts '            listItem.className = "list-group-item d-flex justify-content-between align-items-center";'
puts '            listItem.innerHTML = series.name + " <button class=\'btn btn-danger btn-sm deleteSeries\' data-series-id=\'" + series.id + "\'>X</button>";'
puts '            listColumn.appendChild(listItem);'
puts '        });'
puts '        document.getElementById("seriesArrayInput").value = JSON.stringify(seriesArray.map(s => s.id));'
puts '    }'
puts '});'
puts '</script>'

puts '</body>'
puts '</html>'

session.close
