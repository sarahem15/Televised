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
  seasonArray = cgi['seasonArray'] && !cgi['seasonArray'].empty? ? JSON.parse(cgi['seasonArray']) : []
  episodeArray = cgi['episodeArray'] && !cgi['episodeArray'].empty? ? JSON.parse(cgi['episodeArray']) : []
rescue JSON::ParserError
  seriesArray = []
  seasonArray = []
  episodeArray = []
end

db = Mysql2::Client.new(
  host: '10.20.3.4', 
  username: 'seniorproject25', 
  password: 'TV_Group123!', 
  database: 'televised_w25'
)

# Handle AJAX search functionality for Series, Seasons, and Episodes
if type == "Series" && search != ""
  results = db.query("SELECT showName, imageName, showId FROM series WHERE showName LIKE '#{db.escape(search)}%'")
  
  if results.count > 0
    results.each do |row|
      puts "<p>#{row['showName']} <img src='#{row['imageName']}' alt='#{row['showName']}' style='height: 50px; width: 35px; object-fit: cover;'>"
      puts "<button class='addToList btn btn-success' data-series-id='#{row['showId']}' data-series-name='#{row['showName']}'>ADD</button>"
      puts "<button class='viewSeasons btn btn-info' data-series-id='#{row['showId']}'>View Seasons</button></p>"
    end
  else
    puts "<p>We can't seem to find this title!</p>"
  end
  exit
elsif type == "Season" && search != ""
  results = db.query("SELECT seasonId, seasonNum FROM season WHERE seriesId = '#{search}'")
  
  if results.count > 0
    results.each do |row|
      puts "<p>Season #{row['seasonNum']} <button class='addSeason btn btn-success' data-season-id='#{row['seasonId']}' data-season-num='#{row['seasonNum']}'>ADD</button></p>"
    end
  else
    puts "<p>No seasons found for this series!</p>"
  end
  exit
elsif type == "Episode" && search != ""
  results = db.query("SELECT epId, epName FROM episode WHERE seasonId = '#{search}'")
  
  if results.count > 0
    results.each do |row|
      puts "<p>Episode: #{row['epName']} <button class='addEpisode btn btn-success' data-ep-id='#{row['epId']}' data-ep-name='#{row['epName']}'>ADD</button></p>"
    end
  else
    puts "<p>No episodes found for this season!</p>"
  end
  exit
end

# Handle list creation when "saveList" is clicked
if cgi['saveList'] && !listName.empty? && !description.empty? && (!seriesArray.empty? || !seasonArray.empty? || !episodeArray.empty?)
  existing_list = db.query("SELECT id FROM listOwnership WHERE username = '#{username}' AND listName = '#{db.escape(listName)}'")

  if existing_list.count > 0
    puts "<script>alert('Sorry, but you already have a list with this name. Try a different name.');</script>"
    exit
  end

  db.query("INSERT INTO listOwnership (username, listName) VALUES ('#{username}', '#{db.escape(listName)}')")
  list_id = db.last_id  

  # Insert Series, Seasons, and Episodes
  seriesArray.each do |series_id|
    db.query("INSERT INTO curatedListSeries (username, seriesId, name, description, privacy, date, listId)
              VALUES ('#{username}', '#{series_id}', '#{db.escape(listName)}', '#{db.escape(description)}', '#{privacy}', NOW(), '#{list_id}')")
  end

  seasonArray.each do |season_id|
    db.query("INSERT INTO curatedListSeason (username, seasonId, name, description, privacy, date, listId)
              VALUES ('#{username}', '#{season_id}', '#{db.escape(listName)}', '#{db.escape(description)}', '#{privacy}', NOW(), '#{list_id}')")
  end

  episodeArray.each do |episode_id|
    db.query("INSERT INTO curatedListEpisode (username, episodeId, name, description, privacy, date, listId)
              VALUES ('#{username}', '#{episode_id}', '#{db.escape(listName)}', '#{db.escape(description)}', '#{privacy}', NOW(), '#{list_id}')")
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
puts "          <input type='hidden' id='seasonArrayInput' name='seasonArray'>"
puts "          <input type='hidden' id='episodeArrayInput' name='episodeArray'>"
puts "          <button id='saveList' class='btn btn-primary'>CREATE LIST</button>"
puts "        </form>"
puts "      </div>"
puts "      <div class='col' id='listColumn'>"
puts "        <h3 class='text-center'>Selected Series</h3>"
puts "        <ul id='seriesList' class='list-group'></ul>"
puts "        <h3 class='text-center'>Selected Seasons</h3>"
puts "        <ul id='seasonList' class='list-group'></ul>"
puts "        <h3 class='text-center'>Selected Episodes</h3>"
puts "        <ul id='episodeList' class='list-group'></ul>"
puts "      </div>"
puts "      <div class='col' id='searchColumn'>"
puts "        <h3 class='text-center'>Search for a Series</h3>"
puts "        <form id='searchForm'>"
puts "          <select id='type' name='typeSearch' class='form-control'>"
puts "            <option value='Series' selected>Series</option>"
puts "            <option value='Season'>Season</option>"
puts "            <option value='Episode'>Episode</option>"
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
puts '        if (event.target.classList.contains("addSeason")) {' 
puts '            event.preventDefault();'
puts '            let seasonId = event.target.dataset.seasonId;'
puts '            let seasonNum = event.target.dataset.seasonNum;'
puts '            let seasonArray = JSON.parse(sessionStorage.getItem("seasonArray")) || [];'
puts '            if (!seasonArray.some(s => s.id === seasonId)) {' 
puts '                seasonArray.push({ id: seasonId, seasonNum: seasonNum });' 
puts '                sessionStorage.setItem("seasonArray", JSON.stringify(seasonArray));'
puts '                updateSeasonList();'
puts '            }'
puts '        }'
puts '        if (event.target.classList.contains("addEpisode")) {' 
puts '            event.preventDefault();'
puts '            let epId = event.target.dataset.epId;'
puts '            let epName = event.target.dataset.epName;'
puts '            let episodeArray = JSON.parse(sessionStorage.getItem("episodeArray")) || [];'
puts '            if (!episodeArray.some(e => e.id === epId)) {' 
puts '                episodeArray.push({ id: epId, epName: epName });' 
puts '                sessionStorage.setItem("episodeArray", JSON.stringify(episodeArray));'
puts '                updateEpisodeList();'
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
puts "        seriesList.innerHTML = '';"
puts "        seriesArray.forEach(function(series) {"
puts "          let li = document.createElement('li');"
puts "          li.classList.add('list-group-item', 'd-flex', 'justify-content-between', 'align-items-center');"
puts "          li.innerHTML = series.name + \" <button class='removeFromList btn btn-danger btn-sm' data-series-id='\" + series.id + \"'>X</button>\";"
puts "          seriesList.appendChild(li);"
puts "        });"
puts "      }"

puts "      function updateSeasonList() {"
puts "        let seasonArray = JSON.parse(sessionStorage.getItem('seasonArray')) || [];"
puts "        document.getElementById('seasonArrayInput').value = JSON.stringify(seasonArray);"
puts "        let seasonList = document.getElementById('seasonList');"
puts "        seasonList.innerHTML = '';"
puts "        seasonArray.forEach(function(season) {"
puts "          let li = document.createElement('li');"
puts "          li.classList.add('list-group-item', 'd-flex', 'justify-content-between', 'align-items-center');"
puts "          li.innerHTML = 'Season ' + season.seasonNum + \" <button class='removeFromList btn btn-danger btn-sm' data-season-id='\" + season.id + \"'>X</button>\";"
puts "          seasonList.appendChild(li);"
puts "        });"
puts "      }"

puts "      function updateEpisodeList() {"
puts "        let episodeArray = JSON.parse(sessionStorage.getItem('episodeArray')) || [];"
puts "        document.getElementById('episodeArrayInput').value = JSON.stringify(episodeArray);"
puts "        let episodeList = document.getElementById('episodeList');"
puts "        episodeList.innerHTML = '';"
puts "        episodeArray.forEach(function(episode) {"
puts "          let li = document.createElement('li');"
puts "          li.classList.add('list-group-item', 'd-flex', 'justify-content-between', 'align-items-center');"
puts "          li.innerHTML = episode.epName + \" <button class='removeFromList btn btn-danger btn-sm' data-ep-id='\" + episode.id + \"'>X</button>\";"
puts "          episodeList.appendChild(li);"
puts "        });"
puts "      }"
puts "    });"
puts "  </script>"
puts "</body>"
puts "</html>"
