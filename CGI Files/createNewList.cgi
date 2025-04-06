#!/usr/bin/ruby
$stdout.sync = true
$stderr.reopen $stdout

require 'mysql2'
require 'cgi'
require 'cgi/session'
require 'json'

cgi = CGI.new
session = CGI::Session.new(cgi)

username = session['username']

print cgi.header(
  'cookie' => CGI::Cookie.new('name' => 'CGISESSID', 'value' => session.session_id, 'httponly' => true, 'secure' => true)
)

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

# Handle AJAX search functionality
if type == "Series" && search != ""
  results = db.query("SELECT showName, imageName, showId FROM series WHERE showName LIKE '#{db.escape(search)}%'")
  
  if results.count > 0
    results.each do |row|
      puts "<p>#{row['showName']} <img src='#{row['imageName']}' alt='#{row['showName']}' style='height: 50px; width: 35px; object-fit: cover;'>"
      puts "<button class='addToList btn btn-success' data-series-id='#{row['showId']}' data-series-name='#{row['showName']}'>ADD</button></p>"
    end
  else
    puts "<p>We can't seem to find this title!</p>"
  end
  exit
end

# Handle list creation when "saveList" is clicked
if cgi['saveList'] && !listName.empty? && !description.empty? && !seriesArray.empty?
  existing_list = db.query("SELECT id FROM listOwnership WHERE username = '#{username}' AND listName = '#{db.escape(listName)}'")

  if existing_list.count > 0
    puts "<script>alert('Sorry, but you already have a list with this name. Try a different name.');</script>"
    exit
  end

  db.query("INSERT INTO listOwnership (username, listName) VALUES ('#{username}', '#{db.escape(listName)}')")
  list_id = db.last_id  

  #  FIXED: Properly extract series ID as an integer before inserting
  seriesArray.each do |series|
    series_id = series["id"].to_i  
    db.query("INSERT INTO curatedListSeries (username, seriesId, name, description, privacy, date, listId)
              VALUES ('#{username}', #{series_id}, '#{db.escape(listName)}', '#{db.escape(description)}', #{privacy}, NOW(), #{list_id})")
  end

  puts "<script>alert('Your list has been successfully created!'); window.location.href = 'Profile_List.cgi';</script>"
  exit
end

# Start HTML Output
puts "<!DOCTYPE html>"
puts "<html lang='en'>"
puts "<head>"
puts "  <meta charset='UTF-8'>"
puts "  <meta name='viewport' content='width=device-width, initial-scale=1.0'>"
puts "  <title>Televised</title>"
puts "  <link href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css' rel='stylesheet'>"
puts "  <link rel='stylesheet' href='Televised.css'>"
puts "  <style>"
puts "    body { margin: 0; padding: 0; }"
puts "    .navbar { margin-bottom: 0; }"
puts "    #listRow, #listColumn, #searchColumn { padding: 15px; }"
puts "    @media (max-width: 768px) {"
puts "      .col { margin-bottom: 20px; }"
puts "    }"
puts "    .container-fluid { padding-left: 0; padding-right: 0; }"
puts "  </style>"
puts "</head>"
puts "<body id='createNewList'>"
puts "  <nav id='changingNav' class='navbar navbar-expand-lg navbar-light bg-light'></nav>"
puts "  <h2 class='text-center mt-3'>Create a New List</h2>"
puts "  <div class='container-fluid'>"
puts "    <div class='row'>"
puts "      <div class='col-12 col-md-4' id='listRow'>"
puts "        <h3 class='text-center'>List Details</h3>"
puts "        <form id='newListForm' method='post'>"
puts "          <label>Name</label>"
puts "          <input type='text' name='listName' class='form-control' placeholder='Name' required>"
puts "          <br>"
puts "          <label>Who Can View</label>"
puts "          <select name='views' class='form-control'>"
puts "            <option value='Public'>Public - anyone can view</option>"
puts "            <option value='Private'>Private - no one can view</option>"
puts "          </select>"
puts "          <br>"
puts "          <label>Description</label>"
puts "          <textarea name='description' class='form-control' rows='5'></textarea>"
puts "          <br>"
puts "          <input type='hidden' id='seriesArrayInput' name='seriesArray'>"
puts "          <button id='saveList' class='btn btn-primary'>CREATE LIST</button>"
puts "        </form>"
puts "      </div>"
puts "      <div class='col-12 col-md-4' id='listColumn'>"
puts "        <h3 class='text-center'>Selected Series</h3>"
puts "        <ul id='seriesList' class='list-group'></ul>"
puts "      </div>"
puts "      <div class='col-12 col-md-4' id='searchColumn'>"
puts "        <h3 class='text-center'>Search for a Series</h3>"
puts "        <form id='searchForm'>"
puts "          <select id='type' name='typeSearch' class='form-control'>"
puts "            <option value='Series' selected>Series</option>"
puts "          </select>"
puts "          <br>"
puts "          <input type='text' name='mediaEntered' class='form-control'>"
puts "          <input type='submit' value='Search' class='btn btn-secondary mt-2'>"
puts "        </form>"
puts "        <div id='searchResults'></div>"
puts "      </div>"
puts "    </div>"
puts "  </div>"
puts "  <script src='https://code.jquery.com/jquery-3.6.0.min.js'></script>"
puts "  <script src='https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js'></script>"
puts "  <script src='Televised.js'></script>"
puts "  <script>"
puts "    document.addEventListener('DOMContentLoaded', function () {"
puts "      // Clear the series list and reset seriesArray on page load"
puts "      sessionStorage.removeItem('seriesArray'); // Clear the session storage array"
puts "      updateSeriesList(); // Clear the displayed list"

puts "      document.getElementById('searchForm').addEventListener('submit', function (event) {"
puts "        event.preventDefault();"
puts "        let searchInput = document.querySelector('input[name=\"mediaEntered\"]').value;"
puts "        let type = document.querySelector('select[name=\"typeSearch\"]').value;"
puts "        fetch('createNewList.cgi', {"
puts "          method: 'POST',"
puts "          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },"
puts "          body: new URLSearchParams({ mediaEntered: searchInput, typeSearch: type })"
puts "        })"
puts "        .then(response => response.text())"
puts "        .then(data => { document.getElementById('searchResults').innerHTML = data; });"
puts "      });"

# Add & Remove Series Handling
puts '    document.addEventListener("click", function (event) {' 
puts '        if (event.target.classList.contains("addToList")) {' 
puts '            event.preventDefault();'
puts '            let seriesId = event.target.dataset.seriesId;'
puts '            let seriesName = event.target.dataset.seriesName;'
puts '            let seriesArray = JSON.parse(sessionStorage.getItem("seriesArray")) || [];'
puts '            if (!seriesArray.some(s => s.id === seriesId)) {' 
puts '                seriesArray.push({ id: seriesId, name: seriesName });' 
puts '                sessionStorage.setItem("seriesArray", JSON.stringify(seriesArray));'
puts '                updateSeriesList();'
puts '            }'
puts '        }'
puts '        if (event.target.classList.contains("removeFromList")) {' 
puts '            event.preventDefault();'
puts '            let seriesId = event.target.dataset.seriesId;'
puts '            let seriesArray = JSON.parse(sessionStorage.getItem("seriesArray")) || [];'
puts '            seriesArray = seriesArray.filter(s => s.id !== seriesId);' 
puts '            sessionStorage.setItem("seriesArray", JSON.stringify(seriesArray));'
puts '            updateSeriesList();'
puts '        }'
puts '    });'
puts "      function updateSeriesList() {"
puts "        let seriesArray = JSON.parse(sessionStorage.getItem('seriesArray')) || [];"
puts "        document.getElementById('seriesArrayInput').value = JSON.stringify(seriesArray);"
puts "        let seriesList = document.getElementById('seriesList');"
puts "        seriesList.innerHTML = ''; // Clear the list in the middle column"
puts "        seriesArray.forEach(function(series) {"
puts "          let li = document.createElement('li');"
puts "          li.classList.add('list-group-item', 'd-flex', 'justify-content-between', 'align-items-center');"
puts "          li.innerHTML = series.name + \" <button class='removeFromList btn btn-danger btn-sm' data-series-id='\" + series.id + \"'>X</button>\";"
puts "          seriesList.appendChild(li);"
puts "        });"
puts "      }"
puts "      updateSeriesList();"
puts "    });"
puts "  </script>"
puts "</body>"
puts "</html>"

session.close
