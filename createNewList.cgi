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

listName = cgi['listName']
description = cgi['description']
privacy = cgi['views'] == "Public" ? 1 : 0

begin
    seriesArray = cgi['seriesArray'] && !cgi['seriesArray'].empty? ? JSON.parse(cgi['seriesArray']) : []
rescue JSON::ParserError
    seriesArray = []
end

db = Mysql2::Client.new(
    host: '10.20.3.4',
    username: 'seniorproject25',
    password: 'TV_Group123!',
    database: 'televised_w25'
)

# Handle AJAX search
if type == "Series" && search != ""
    images = db.query("SELECT showName, imageName, showId FROM series WHERE showName LIKE '#{db.escape(search)}%'")
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

# Process list creation
if cgi['saveList'] && !listName.empty? && !description.empty? && !seriesArray.empty?
    existing_list = db.query("SELECT id FROM listOwnership WHERE username = '#{username}' AND listName = '#{db.escape(listName)}'")
    
    if existing_list.count > 0
        puts "<script>alert('Sorry, you already have a list with this name. Try a different name.');</script>"
        exit
    end

    db.query("INSERT INTO listOwnership (username, listName) VALUES ('#{username}', '#{db.escape(listName)}')")
    list_id = db.last_id

    seriesArray.each do |series_id|
        db.query("INSERT INTO curatedListSeries (username, seriesId, name, description, privacy, date, listId)
                  VALUES ('#{username}', '#{series_id}', '#{db.escape(listName)}', '#{db.escape(description)}', '#{privacy}', NOW(), '#{list_id}')")
    end

    puts "<script>
            alert('Your list has been successfully created!');
            sessionStorage.removeItem('seriesArray');
            document.getElementById('newListForm').reset();
            document.getElementById('seriesList').innerHTML = '';
            window.location.href = 'Profile_List.cgi';
          </script>"
    exit
end

# Generate HTML Page
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
puts '    <nav id="changingNav"></nav>'
puts '    <h2 class="text-center mt-3">Create a New List</h2>'
puts '    <div class="container-fluid">'
puts '        <div class="row">'
puts '            <div class="col" id="listRow">'
puts '                <h3 class="text-center">List Details</h3>'
puts '                <form id="newListForm" method="post">'
puts '                    <label>Name</label>'
puts '                    <input type="text" name="listName" class="form-control" required>'
puts '                    <br>'
puts '                    <label>Who Can View</label>'
puts '                    <select name="views" class="form-control">'
puts '                        <option value="Public">Public - anyone can view</option>'
puts '                        <option value="Private">Private - no one can view</option>'
puts '                    </select>'
puts '                    <br>'
puts '                    <label>Description</label>'
puts '                    <textarea name="description" class="form-control" rows="5"></textarea>'
puts '                    <br>'
puts '                    <input type="hidden" id="seriesArrayInput" name="seriesArray">'
puts '                    <button id="saveList" class="btn btn-primary">CREATE LIST</button>'
puts '                </form>'
puts '            </div>'
puts '            <div class="col" id="listColumn">'
puts '                <h3 class="text-center">Selected Series</h3>'
puts '                <ul id="seriesList" class="list-group"></ul>'
puts '            </div>'
puts '            <div class="col" id="searchColumn">'
puts '                <h3 class="text-center">Search for a Series</h3>'
puts '                <form id="searchForm">'
puts '                    <select id="type" name="typeSearch" class="form-control">'
puts '                        <option value="Series" selected>Series</option>'
puts '                        <option value="Seasons">Seasons</option>'
puts '                        <option value="Episodes">Episodes</option>'
puts '                    </select>'
puts '                    <br>'
puts '                    <input type="text" name="mediaEntered" class="form-control">'
puts '                    <input type="submit" value="Search" class="btn btn-secondary mt-2">'
puts '                </form>'
puts '                <div id="searchResults"></div>'
puts '            </div>'
puts '        </div>'
puts '    </div>'
puts '    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>'
puts '    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>'
puts '    <script src="Televised.js"></script>'
puts '    <script>'
puts '        document.getElementById("saveList").addEventListener("click", function(event) {'
puts '            event.preventDefault();'
puts '            let formData = new FormData(document.getElementById("newListForm"));'
puts '            formData.append("seriesArray", sessionStorage.getItem("seriesArray") || "[]");'
puts '            fetch("createNewList.cgi", { method: "POST", body: formData })'
puts '                .then(response => response.text())'
puts '                .then(data => { document.body.innerHTML += data; });'
puts '        });'
puts '        function updateSeriesList() {'
puts '            let seriesArray = JSON.parse(sessionStorage.getItem("seriesArray")) || [];'
puts '            document.getElementById("seriesArrayInput").value = JSON.stringify(seriesArray);'
puts '            let seriesList = document.getElementById("seriesList");'
puts '            seriesList.innerHTML = "";'
puts '            seriesArray.forEach(function(series) {'
puts '                let li = document.createElement("li");'
puts '                li.classList.add("list-group-item", "d-flex", "justify-content-between", "align-items-center");'
puts '                li.innerHTML = series.name + " <button class=\'removeFromList btn btn-danger btn-sm\' data-series-id=\'" + series.id + "\'>X</button>";'
puts '                seriesList.appendChild(li);'
puts '            });'
puts '        }'
puts '        updateSeriesList();'
puts '    </script>'
puts '</body>'
puts '</html>'

session.close
