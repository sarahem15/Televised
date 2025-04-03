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

# Print the necessary headers
print cgi.header(
  'cookie' => CGI::Cookie.new('name' => 'CGISESSID', 'value' => session.session_id, 'httponly' => true, 'secure' => true)
)

search = cgi['mediaEntered'] || ''
type = cgi['typeSearch'] || ''

listName = cgi['listName']
description = cgi['description']
privacy = cgi['views'] == "Public" ? 1 : 0  

# Parse seriesArray safely
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
if type && search != ""
  results = db.query("SELECT showName, imageName, showId FROM series WHERE showName LIKE '#{db.escape(search)}%'")

  print "Content-type: text/html\n\n"

  if results.count > 0
    results.each do |row|
      puts "<div class='search-result'>"
      puts "  <p>#{row['showName']} <img src='#{row['imageName']}' alt='#{row['showName']}' style='height: 50px; width: 35px; object-fit: cover;'>"
      puts "  <button class='addToList btn btn-success' data-series-id='#{row['showId']}' data-series-name='#{row['showName']}'>ADD</button></p>"
      puts "</div>"
    end
  else
    puts "<p>No results found.</p>"
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

  seriesArray.each do |series|
    series_id = series["id"]
    db.query("INSERT INTO curatedListSeries (username, seriesId, name, description, privacy, date, listId)
              VALUES ('#{username}', '#{series_id}', '#{db.escape(listName)}', '#{db.escape(description)}', '#{privacy}', NOW(), '#{list_id}')")
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
puts "</head>"
puts "<body id='createNewList'>"
puts "  <nav id='changingNav'></nav>"
puts "  <h2 class='text-center mt-3'>Create a New List</h2>"
puts "  <div class='container-fluid'>"
puts "    <div class='row'>"
puts "      <div class='col' id='listRow'>"
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
puts "      <div class='col' id='listColumn'>"
puts "        <h3 class='text-center'>Selected Series</h3>"
puts "        <ul id='seriesList' class='list-group'></ul>"
puts "      </div>"
puts "      <div class='col' id='searchColumn'>"
puts "        <h3 class='text-center'>Search for a Series</h3>"
puts "        <form id='searchForm'>"
puts "          <select id='type' name='typeSearch' class='form-control'>"
puts "            <option value='Series' selected>Series</option>"
puts "            <option value='Seasons'>Seasons</option>"
puts "            <option value='Episodes'>Episodes</option>"
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
puts "  <script src='Televised.js' defer></script>"

# JavaScript for add/remove/update
puts "<script>"
puts "document.addEventListener('DOMContentLoaded', function () {"
puts "    let seriesArray = [];"
puts "    const seriesList = document.getElementById('seriesList');"
puts "    function updateSeriesArray() { document.getElementById('seriesArrayInput').value = JSON.stringify(seriesArray); }"
puts "    function addSeries(seriesId, seriesName) {"
puts "        if (seriesArray.some(series => series.id === seriesId)) { alert('Already added!'); return; }"
puts "        seriesArray.push({ id: seriesId, name: seriesName }); updateSeriesList();"
puts "    }"
puts "    function removeSeries(seriesId) { seriesArray = seriesArray.filter(series => series.id !== seriesId); updateSeriesList(); }"
puts "    function updateSeriesList() {"
puts "        seriesList.innerHTML = '';"
puts "        seriesArray.forEach(series => {"
puts "            let listItem = `<li class='list-group-item'>${series.name} <button class='removeSeries btn btn-danger btn-sm' data-series-id='${series.id}'>REMOVE</button></li>`;"
puts "            seriesList.innerHTML += listItem;"
puts "        }); updateSeriesArray();"
puts "    }"
puts "    document.getElementById('searchResults').addEventListener('click', event => {"
puts "        if (event.target.classList.contains('addToList')) addSeries(event.target.dataset.seriesId, event.target.dataset.seriesName);"
puts "    });"
puts "    seriesList.addEventListener('click', event => {"
puts "        if (event.target.classList.contains('removeSeries')) removeSeries(event.target.dataset.seriesId);"
puts "    });"
puts "});"
puts "</script>"

puts "</body></html>"
session.close
