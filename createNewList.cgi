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
puts    '<br><br>'
puts    '<div class="container-fluid">'
puts        '<div class="row">'
puts            '<div class="col" id="listRow">'
puts                '<h3 style="text-align: center;">List Details</h3>'
puts                '<form id="newListForm" method="post" action="newList.cgi">'
puts                    '<label>Name</label>'
puts                    '<input type="text" id="Name" name="listName" class="form-control" placeholder="Name">'
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

# Handle search results
if type == "Series" && search != ""
    images = db.query("SELECT showName, imageName, showId FROM series WHERE showName LIKE '#{search}%';")
    images = images.to_a
    if !images.empty?
        puts 'Is this the title you\'re looking for?'
        puts '<br>'
        images.each do |image|
            puts "#{image['showName']}"
            puts "<img src='#{image['imageName']}' alt='#{image['showName']}' style='height: 50px; width: 35px; object-fit: cover;'>"
            puts "<button class='addToList' data-series-name='#{image['showName']}'>ADD</button>"
        end
    else
        puts 'We can\'t seem to find this title!'
    end
end

puts            '</div>'
puts        '</div>'
puts    '</div>'

# JavaScript section
puts '<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>'
puts '<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>'
puts '<script src="Televised.js"></script>'
puts '<script>'
puts 'document.addEventListener("DOMContentLoaded", function () {'
puts '    let seriesArray = JSON.parse(sessionStorage.getItem("seriesArray")) || [];'
puts '    console.log("Initial seriesArray:", seriesArray);'
puts '    updateSeriesList();'
puts ''
puts '    document.addEventListener("click", function (event) {'
puts '        if (event.target.classList.contains("addToList")) {'
puts '            event.preventDefault();'
puts '            let seriesName = event.target.dataset.seriesName;'
puts ''
puts '            if (seriesName && !seriesArray.includes(seriesName)) {'
puts '                seriesArray.push(seriesName);'
puts '                sessionStorage.setItem("seriesArray", JSON.stringify(seriesArray));'
puts '                updateSeriesList();'
puts '            }'
puts '        }'
puts '    });'
puts ''
puts '    function updateSeriesList() {'
puts '        let listColumn = document.getElementById("seriesList");'
puts '        listColumn.innerHTML = "";'
puts '        seriesArray.forEach(series => {'
puts '            let listItem = document.createElement("li");'
puts '            listItem.className = "list-group-item";'
puts '            listItem.textContent = series;'
puts '            listColumn.appendChild(listItem);'
puts '        });'
puts '    }'
puts '});'
puts '</script>'

puts '</body>'
puts '</html>'

session.close
