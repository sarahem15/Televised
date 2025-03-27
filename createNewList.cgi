#!/usr/bin/ruby
$stdout.sync = true
$stderr.reopen $stdout

puts "Content-type: text/html\n\n"
require 'mysql2'
require 'cgi'
require 'cgi/session'
require 'securerandom'

cgi = CGI.new
session = CGI::Session.new(cgi)
username = session['username']

# Capture form inputs
listName = cgi['listName']
description = cgi['description']
privacy = cgi['views']
seriesArray = cgi.params['seriesArray']

db = Mysql2::Client.new(
    host: '10.20.3.4', 
    username: 'seniorproject25', 
    password: 'TV_Group123!', 
    database: 'televised_w25'
)

# Handle list submission
if listName && !listName.empty? && !seriesArray.empty?
    listId = SecureRandom.uuid  # Generate a unique ID for the list
    date = Time.now.strftime("%Y-%m-%d")

    seriesArray.each do |seriesId|
        db.query("INSERT INTO curatedListSeries (username, seriesId, name, description, privacy, date, listId)
                  VALUES ('#{db.escape(username)}', '#{db.escape(seriesId)}', '#{db.escape(listName)}',
                          '#{db.escape(description)}', '#{db.escape(privacy)}', '#{date}', '#{listId}')")
    end

    puts '<script>'
    puts '    sessionStorage.clear();'  # Clear stored list
    puts '    alert("List successfully created!");'
    puts '    window.location.href = "createNewList.cgi";'  # Refresh the page
    puts '</script>'
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
puts    '<br><br>'
puts    '<div class="container-fluid">'
puts        '<div class="row">'
puts            '<div class="col" id="listRow">'
puts                '<h3 style="text-align: center;">List Details</h3>'
puts                '<form id="newListForm" method="post" action="createNewList.cgi">'
puts                    '<label>Name</label>'
puts                    '<input type="text" id="Name" name="listName" class="form-control" placeholder="Name" required>'
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
puts                    '<button id="saveList" class="btn" style="background-color: #9daef6;" type="submit">CREATE LIST</button>'
puts                '</form>'
puts            '</div>'

puts            '<div class="col" id="listColumn">'
puts                '<h3 style="text-align: center;">Selected Series</h3>'
puts                '<ul id="seriesList" class="list-group"></ul>'
puts            '</div>'

puts            '<div class="col" id="searchColumn">'
puts                '<h3 style="text-align: center;">Search for a Series</h3>'
puts                '<br>'
puts                '<form id="searchForm" method="post" action="createNewList.cgi" class="TopFiveProfile">'
puts                '<select id="type" name="typeSearch" class="form-control">'
puts                    '<option value="Series" selected>Series</option>'
puts                    '<option value="Seasons">Seasons</option>'
puts                    '<option value="Episodes">Episodes</option>'
puts                '</select>'
puts                    '<br>'
puts                    '<input type="text" name="mediaEntered" class="top5search">'
puts                    '<input type="submit" value="Search">'
puts                '</form>'

puts '</div>'
puts '</div>'
puts '</div>'

# JavaScript section
puts '<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>'
puts '<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>'
puts '<script src="Televised.js"></script>'
puts '<script>'
puts 'document.addEventListener("DOMContentLoaded", function () {'
puts '    let seriesArray = JSON.parse(sessionStorage.getItem("seriesArray")) || [];'
puts '    updateSeriesList();'

# Handle adding series to the list
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

# Function to update the displayed list
puts '    function updateSeriesList() {'
puts '        let listColumn = document.getElementById("seriesList");'
puts '        listColumn.innerHTML = "";'
puts '        seriesArray.forEach(series => {'
puts '            let listItem = document.createElement("li");'
puts '            listItem.className = "list-group-item";'
puts '            listItem.textContent = series.name;'
puts '            listColumn.appendChild(listItem);'
puts '        });'
puts '        document.getElementById("seriesArrayInput").value = JSON.stringify(seriesArray.map(s => s.id));'
puts '    }'

# Handle list submission
puts '    document.getElementById("newListForm").addEventListener("submit", function () {'
puts '        sessionStorage.clear();'
puts '    });'
puts '});'
puts '</script>'

puts '</body>'
puts '</html>'

session.close
