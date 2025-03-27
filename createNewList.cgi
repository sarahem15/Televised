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

# Connect to the database
db = Mysql2::Client.new(
    host: '10.20.3.4', 
    username: 'seniorproject25', 
    password: 'TV_Group123!', 
    database: 'televised_w25'
)

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
puts    '<br>'
puts    '<br>'
puts    '<div class="container-fluid">'
puts        '<div class="row">'

# Form for creating a new list
puts            '<div class="col" id="listRow">'
puts                '<h3 style="text-align: center;">List Details</h3>'
puts                '<form id="newListForm" method="post" action="saveList.cgi">'
puts                    '<label>Name</label>'
puts                    '<input type="text" id="Name" name="listName" class="form-control" placeholder="Name" required>'
puts                    '<br>'
puts                    '<label>Type</label>'
puts                    '<select id="Type" name="type" class="form-control">'
puts                        '<option value="Series">Series</option>'
puts                        '<option value="Seasons">Seasons</option>'
puts                        '<option value="Episodes">Episodes</option>'
puts                    '</select>'
puts                    '<br>'
puts                    '<label>Who Can View</label>'
puts                    '<select id="views" name="views" class="form-control">'
puts                        '<option value="Public">Public - anyone can view</option>'
puts                        '<option value="Private">Private - no one can view</option>'
puts                    '</select>'
puts                    '<br>'
puts                    '<label>Description</label>'
puts                    '<textarea id="Description" name="description" class="form-control" rows="5"></textarea>'
puts                    '<br>'
puts                    '<input type="hidden" id="seriesArrayInput" name="seriesArray">'
puts                    '<button id="saveList" class="btn btn-primary" type="submit">CREATE LIST</button>'
puts                '</form>'
puts            '</div>'

# Selected series list
puts            '<div class="col" id="listColumn">'
puts                '<h3 style="text-align: center;">Selected Series</h3>'
puts                '<ul id="seriesList" class="list-group"></ul>'
puts            '</div>'

# Search column
puts            '<div class="col" id="searchColumn">'
puts                '<h3 style="text-align: center;">Search for a Series</h3>'
puts                '<br>'
puts                '<form method="post" action="createNewList.cgi" class="TopFiveProfile">'
puts                    '<select id="type" name="typeSearch" class="form-control">'
puts                        '<option value="Series" selected>Series</option>'
puts                        '<option value="Seasons">Seasons</option>'
puts                        '<option value="Episodes">Episodes</option>'
puts                    '</select>'
puts                    '<br>'
puts                    '<input type="text" name="mediaEntered" class="top5search">'
puts                    '<input type="submit" value="Search">'
puts                '</form>'

# Display search results dynamically
if cgi['mediaEntered'] && cgi['typeSearch'] == "Series"
    search = cgi['mediaEntered']
    results = db.query("SELECT showName, showId FROM series WHERE showName LIKE '#{search}%'")
    results.each do |row|
        puts "<div class='searchResult'>"
        puts "  <span>#{row['showName']}</span>"
        puts "  <button class='btn btn-success addToList' data-series-id='#{row['showId']}' data-series-name='#{row['showName']}'>ADD</button>"
        puts "</div>"
    end
end

puts            '</div>'  # End search column
puts        '</div>'  # End row
puts    '</div>'  # End container

# JavaScript for list functionality
puts '<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>'
puts '<script>'
puts 'document.addEventListener("DOMContentLoaded", function () {'
puts '    let seriesArray = JSON.parse(sessionStorage.getItem("seriesArray")) || [];'
puts '    updateSeriesList();'

# Add to list functionality
puts '    document.addEventListener("click", function (event) {'
puts '        if (event.target.classList.contains("addToList")) {'
puts '            event.preventDefault();'
puts '            let seriesName = event.target.dataset.seriesName;'
puts '            let seriesId = event.target.dataset.seriesId;'
puts ''
puts '            if (seriesName && !seriesArray.some(series => series.id === seriesId)) {'
puts '                seriesArray.push({ id: seriesId, name: seriesName });'
puts '                sessionStorage.setItem("seriesArray", JSON.stringify(seriesArray));'
puts '                updateSeriesList();'
puts '            }'
puts '        }'
puts '    });'

# Delete from list functionality
puts '    document.addEventListener("click", function (event) {'
puts '        if (event.target.classList.contains("deleteSeries")) {'
puts '            let seriesId = event.target.dataset.seriesId;'
puts '            seriesArray = seriesArray.filter(series => series.id !== seriesId);'
puts '            sessionStorage.setItem("seriesArray", JSON.stringify(seriesArray));'
puts '            updateSeriesList();'
puts '        }'
puts '    });'

# Update displayed list
puts '    function updateSeriesList() {'
puts '        let listColumn = document.getElementById("seriesList");'
puts '        listColumn.innerHTML = "";'
puts '        seriesArray.forEach(series => {'
puts '            let listItem = document.createElement("li");'
puts '            listItem.className = "list-group-item d-flex justify-content-between align-items-center";'
puts '            listItem.innerHTML = series.name + '
puts '                " <button class=\'btn btn-danger btn-sm deleteSeries\' data-series-id=\'" + series.id + "\'>X</button>";'
puts '            listColumn.appendChild(listItem);'
puts '        });'
puts '        document.getElementById("seriesArrayInput").value = JSON.stringify(seriesArray.map(s => s.id));'
puts '    }'

# Clear session storage after form submission
puts '    document.getElementById("newListForm").addEventListener("submit", function () {'
puts '        sessionStorage.clear();'
puts '    });'
puts '});'
puts '</script>'

puts '</body>'
puts '</html>'

session.close
