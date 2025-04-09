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

begin
  seasonArray = cgi['seasonArray'] && !cgi['seasonArray'].empty? ? JSON.parse(cgi['seasonArray']) : []
rescue JSON::ParserError
  seasonArray = []
end

begin
  episodeArray = cgi['episodeArray'] && !cgi['episodeArray'].empty? ? JSON.parse(cgi['episodeArray']) : []
rescue JSON::ParserError
  episodeArray = []
end

db = Mysql2::Client.new(
  host: '10.20.3.4',
  username: 'seniorproject25',
  password: 'TV_Group123!',
  database: 'televised_w25'
)

# Handle adding to the series, season, or episode list
if cgi['addSeries']
  seriesArray.push({ "id" => cgi['seriesId'], "name" => cgi['seriesName'] })
elsif cgi['removeSeries']
  seriesArray.reject! { |series| series['id'] == cgi['seriesId'].to_i }
elsif cgi['addSeason']
  seasonArray.push({ "seriesId" => cgi['seriesId'], "season" => cgi['seasonNum'] })
elsif cgi['removeSeason']
  seasonArray.reject! { |season| season['seriesId'] == cgi['seriesId'].to_i && season['season'] == cgi['seasonNum'].to_i }
elsif cgi['addEpisode']
  episodeArray.push({ "id" => cgi['epId'], "name" => cgi['epName'], "seasonId" => cgi['seasonId'] })
elsif cgi['removeEpisode']
  episodeArray.reject! { |ep| ep['id'] == cgi['epId'].to_i }
end

# Save list
if cgi['saveList'] && !listName.empty? && !description.empty?
  existing_list = db.query("SELECT id FROM listOwnership WHERE username = '#{username}' AND listName = '#{db.escape(listName)}'")
  if existing_list.count > 0
    puts "<script>alert('Sorry, but you already have a list with this name. Try a different name.');</script>"
    exit
  end

  db.query("INSERT INTO listOwnership (username, listName) VALUES ('#{username}', '#{db.escape(listName)}')")
  list_id = db.last_id

  unless seriesArray.empty?
    seriesArray.each do |series|
      series_id = series["id"].to_i
      db.query("INSERT INTO curatedListSeries (username, seriesId, name, description, privacy, date, listId)
                VALUES ('#{username}', #{series_id}, '#{db.escape(listName)}', '#{db.escape(description)}', #{privacy}, NOW(), #{list_id})")
    end
  end

  unless seasonArray.empty?
    seasonArray.each do |season|
      show_id = season["seriesId"].to_i
      season_num = season["season"].to_i
      result = db.query("SELECT seasonId FROM season WHERE seriesId = #{show_id} ORDER BY seasonId ASC LIMIT 1 OFFSET #{season_num - 1}")
      if result.count > 0
        season_id = result.first["seasonId"].to_i
        db.query("INSERT INTO curatedListSeason (username, seasonId, name, description, privacy, date, listId)
                  VALUES ('#{username}', #{season_id}, '#{db.escape(listName)}', '#{db.escape(description)}', #{privacy}, NOW(), #{list_id})")
      end
    end
  end

  unless episodeArray.empty?
    episodeArray.each do |episode|
      ep_id = episode["id"].to_i
      db.query("INSERT INTO curatedListEpisode (username, epId, name, description, privacy, date, listId)
                VALUES ('#{username}', #{ep_id}, '#{db.escape(listName)}', '#{db.escape(description)}', #{privacy}, NOW(), #{list_id})")
    end
  end

  if seriesArray.empty? && seasonArray.empty? && episodeArray.empty?
    puts "<script>alert('Please select at least one series, season, or episode before saving.');</script>"
    exit
  end

  puts "<script>alert('Your list has been successfully created!'); window.location.href = 'Profile_Lists.cgi';</script>"
  exit
end

# Handle search dynamically
if search && type
  search_results = []
  case type
  when 'Series'
    search_results = db.query("SELECT showId, showName FROM series WHERE showName LIKE '%#{db.escape(search)}%'")
  when 'Season'
    search_results = db.query("SELECT seasonId, seasonNum FROM season WHERE seasonNum LIKE '%#{db.escape(search)}%'")
  when 'Episode'
    search_results = db.query("SELECT epId, epName FROM episode WHERE epName LIKE '%#{db.escape(search)}%'")
  end

  results_html = "<ul class='list-group'>"
  search_results.each do |result|
    results_html += "<li class='list-group-item'>#{result['showName'] || result['seasonNum'] || result['epName']}</li>"
  end
  results_html += "</ul>"

  # Return the results as the response
  print results_html
  exit
end

# HTML layout
puts "<!DOCTYPE html>"
puts "<html lang='en'>"
puts "<head>"
puts "  <meta charset='UTF-8'>"
puts "  <meta name='viewport' content='width=device-width, initial-scale=1.0'>"
puts "  <title>Televised</title>"
puts "  <link href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css' rel='stylesheet'>"
puts "  <link rel='stylesheet' href='Televised.css'>"
puts "  <script src='https://code.jquery.com/jquery-3.6.0.min.js'></script>"
puts "  <script>"
puts "    $(document).ready(function() {"
puts "      $('#searchForm').submit(function(event) {"
puts "        event.preventDefault();"
puts "        var searchText = $('#mediaSearch').val();"
puts "        var type = $('#type').val();"
puts "        $.ajax({"
puts "          url: '',"
puts "          type: 'GET',"
puts "          data: { mediaEntered: searchText, typeSearch: type },"
puts "          success: function(response) {"
puts "            $('#searchResults').html(response);"
puts "          }"
puts "        });"
puts "      });"
puts "    });"
puts "  </script>"
puts "</head>"
puts "<body id='createNewList'>"
puts "  <nav id='changingNav'></nav>"
puts "  <h2 class='text-center mt-3'>Create a New List</h2>"
puts "  <div class='container-fluid'>"
puts "    <div class='row'>"
puts "      <div class='col-12 col-md-4' id='listRow'>"
puts "        <h3 class='text-center'>List Details</h3>"
puts "        <form id='newListForm' method='post'>"
puts "          <label>Name</label>"
puts "          <input type='text' name='listName' class='form-control' placeholder='Name' required><br>"
puts "          <label>Who Can View</label>"
puts "          <select name='views' class='form-control'>"
puts "            <option value='Public'>Public - anyone can view</option>"
puts "            <option value='Private'>Private - no one can view</option>"
puts "          </select><br>"
puts "          <label>Description</label>"
puts "          <textarea name='description' class='form-control' rows='5'></textarea><br>"
puts "          <input type='hidden' id='seriesArrayInput' name='seriesArray'>"
puts "          <input type='hidden' id='seasonArrayInput' name='seasonArray'>"
puts "          <input type='hidden' id='episodeArrayInput' name='episodeArray'>"
puts "          <button id='saveList' name='saveList' class='btn btn-primary'>CREATE LIST</button>"
puts "        </form>"
puts "      </div>"

puts "      <div class='col-12 col-md-4' id='listColumn'>"
puts "        <h3 class='text-center'>Selected Series/Seasons/Episodes</h3>"
puts "        <ul id='seriesList' class='list-group'></ul>"
puts "      </div>"

puts "      <div class='col-12 col-md-4' id='searchColumn'>"
puts "        <h3 class='text-center'>Search for a Series/Season/Episode</h3>"
puts "        <form id='searchForm' method='get' action=''>"
puts "          <select id='type' name='typeSearch' class='form-control'>"
puts "            <option value='Series' selected>Series</option>"
puts "            <option value='Season'>Season</option>"
puts "            <option value='Episode'>Episode</option>"
puts "          </select><br>"
puts "          <input type='text' id='mediaSearch' name='mediaEntered' class='form-control' placeholder='Search for a show, season, or episode...'>"
puts "          <button type='submit' class='btn btn-primary mt-2'>Search</button>"
puts "        </form>"
puts "        <div id='searchResults'></div>"
puts "      </div>"
puts "    </div>"
puts "  </div>"
puts "</body>"
puts "</html>"








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

begin
  seasonArray = cgi['seasonArray'] && !cgi['seasonArray'].empty? ? JSON.parse(cgi['seasonArray']) : []
rescue JSON::ParserError
  seasonArray = []
end

db = Mysql2::Client.new(
  host: '10.20.3.4',
  username: 'seniorproject25',
  password: 'TV_Group123!',
  database: 'televised_w25'
)

# Handle AJAX search
if search != ""
  if type == "Series"
    results = db.query("SELECT showName, imageName, showId FROM series WHERE showName LIKE '#{db.escape(search)}%'")
    if results.count > 0
      results.each do |row|
        puts "<p>#{row['showName']} <img src='#{row['imageName']}' alt='#{row['showName']}' style='height: 50px; width: 35px; object-fit: cover;'>"
        puts "<button class='addToList btn btn-success' data-series-id='#{row['showId']}' data-series-name='#{row['showName']}'>ADD</button></p>"
      end
    else
      puts "<p>We can't seem to find this title!</p>"
    end
  elsif type == "Season"
    results = db.query("SELECT showName, imageName, showId FROM series WHERE showName LIKE '#{db.escape(search)}%'")
    if results.count > 0
      results.each do |row|
        seasons = db.query("SELECT seasonId FROM season WHERE seriesId = '#{row['showId']}'").to_a
        puts "<p>#{row['showName']} <img src='#{row['imageName']}' alt='#{row['showName']}' style='height: 50px; width: 35px; object-fit: cover;'>"
        puts "<button class='addToList btn btn-success' data-series-id='#{row['showId']}' data-series-name='#{row['showName']}'>ADD</button>"
        puts "<select class='seasonSelect' data-series-id='#{row['showId']}'>"
        seasons.each_with_index do |season, index|
          puts "<option value='#{season['seasonId']}'>Season #{index + 1}</option>"
        end
        puts "</select></p>"
      end
    else
      puts "<p>We can't seem to find this title!</p>"
    end
  end
  exit
end

# Save list
if cgi['saveList'] && !listName.empty? && !description.empty?
  existing_list = db.query("SELECT id FROM listOwnership WHERE username = '#{username}' AND listName = '#{db.escape(listName)}'")
  if existing_list.count > 0
    puts "<script>alert('Sorry, but you already have a list with this name. Try a different name.');</script>"
    exit
  end

  db.query("INSERT INTO listOwnership (username, listName) VALUES ('#{username}', '#{db.escape(listName)}')")
  list_id = db.last_id

  unless seriesArray.empty?
    seriesArray.each do |series|
      series_id = series["id"].to_i
      db.query("INSERT INTO curatedListSeries (username, seriesId, name, description, privacy, date, listId)
                VALUES ('#{username}', #{series_id}, '#{db.escape(listName)}', '#{db.escape(description)}', #{privacy}, NOW(), #{list_id})")
    end
  end

  unless seasonArray.empty?
    seasonArray.each do |season|
      show_id = season["seriesId"].to_i
      season_num = season["season"].to_i
      result = db.query("SELECT seasonId FROM season WHERE seriesId = #{show_id} ORDER BY seasonId ASC LIMIT 1 OFFSET #{season_num - 1}")
      if result.count > 0
        season_id = result.first["seasonId"].to_i
        db.query("INSERT INTO curatedListSeason (username, seasonId, name, description, privacy, date, listId)
                  VALUES ('#{username}', #{season_id}, '#{db.escape(listName)}', '#{db.escape(description)}', #{privacy}, NOW(), #{list_id})")
      end
    end
  end

  if seriesArray.empty? && seasonArray.empty?
    puts "<script>alert('Please select at least one series or season before saving.');</script>"
    exit
  end

  puts "<script>alert('Your list has been successfully created!'); window.location.href = 'Profile_Lists.cgi';</script>"
  exit
end

# HTML layout
puts "<!DOCTYPE html>"
puts "<html lang='en'>"
puts "<head>"
puts "  <meta charset='UTF-8'>"
puts "  <meta name='viewport' content='width=device-width, initial-scale=1.0'>"
puts "  <title>Televised</title>"
puts "  <link href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css' rel='stylesheet'>"
puts "  <link rel='stylesheet' href='Televised.css'>"
puts "  <script src='https://code.jquery.com/jquery-3.6.0.min.js'></script>"
puts "</head>"
puts "<body id='createNewList'>"
puts "  <nav id='changingNav'></nav>"
puts "  <h2 class='text-center mt-3'>Create a New List</h2>"
puts "  <div class='container-fluid'>"
puts "    <div class='row'>"
puts "      <div class='col-12 col-md-4' id='listRow'>"
puts "        <h3 class='text-center'>List Details</h3>"
puts "        <form id='newListForm' method='post'>"
puts "          <label>Name</label>"
puts "          <input type='text' name='listName' class='form-control' placeholder='Name' required><br>"
puts "          <label>Who Can View</label>"
puts "          <select name='views' class='form-control'>"
puts "            <option value='Public'>Public - anyone can view</option>"
puts "            <option value='Private'>Private - no one can view</option>"
puts "          </select><br>"
puts "          <label>Description</label>"
puts "          <textarea name='description' class='form-control' rows='5'></textarea><br>"
puts "          <input type='hidden' id='seriesArrayInput' name='seriesArray'>"
puts "          <input type='hidden' id='seasonArrayInput' name='seasonArray'>"
puts "          <button id='saveList' name='saveList' class='btn btn-primary'>CREATE LIST</button>"
puts "        </form>"
puts "      </div>"

puts "      <div class='col-12 col-md-4' id='listColumn'>"
puts "        <h3 class='text-center'>Selected Series/Seasons</h3>"
puts "        <ul id='seriesList' class='list-group'></ul>"
puts "      </div>"

puts "      <div class='col-12 col-md-4' id='searchColumn'>"
puts "        <h3 class='text-center'>Search for a Series</h3>"
puts "        <form id='searchForm'>"
puts "          <select id='type' name='typeSearch' class='form-control'>"
puts "            <option value='Series' selected>Series</option>"
puts "            <option value='Season'>Season</option>"
puts "          </select><br>"
puts "          <input type='text' name='mediaEntered' class='form-control'>"
puts "          <input type='submit' value='Search' class='btn btn-secondary mt-2'>"
puts "        </form>"
puts "        <div id='searchResults'></div>"
puts "      </div>"

puts "    </div>"
puts "  </div>"

# Embedded JavaScript
  puts '<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>'
  puts '<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>'
  puts '<script src="Televised.js"></script>'
puts "<script>"
puts "document.addEventListener('DOMContentLoaded', function () {"
puts "  sessionStorage.removeItem('seriesArray');"
puts "  sessionStorage.removeItem('seasonArray');"
puts "  sessionStorage.removeItem('episodeArray');"
puts "  updateAllLists();"

puts "  document.getElementById('searchForm').addEventListener('submit', function (event) {"
puts "    event.preventDefault();"
puts "    let searchInput = document.querySelector('input[name=\"mediaEntered\"]').value;"
puts "    let type = document.querySelector('select[name=\"typeSearch\"]').value;"
puts "    fetch('createNewList.cgi', {"
puts "      method: 'POST',"
puts "      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },"
puts "      body: new URLSearchParams({ mediaEntered: searchInput, typeSearch: type })"
puts "    })"
puts "    .then(response => response.text())"
puts "    .then(data => { document.getElementById('searchResults').innerHTML = data; });"
puts "  });"

puts "  document.addEventListener('click', function (event) {"
puts "    if (event.target.classList.contains('addToList')) {"
puts "      event.preventDefault();"
puts "      let seriesId = event.target.dataset.seriesId;"
puts "      let seriesName = event.target.dataset.seriesName;"
puts "      let parent = event.target.closest('p');"

puts "      if (parent.querySelector('select.seasonSelect')) {"
puts "        let seasonNum = parent.querySelector('select.seasonSelect').selectedIndex + 1;"
puts "        let seasonArray = JSON.parse(sessionStorage.getItem('seasonArray')) || [];"
puts "        if (!seasonArray.some(s => s.seriesId === seriesId && s.season === seasonNum)) {"
puts "          seasonArray.push({ seriesId: seriesId, name: seriesName, season: seasonNum });"
puts "          sessionStorage.setItem('seasonArray', JSON.stringify(seasonArray));"
puts "          updateAllLists();"
puts "        }"
puts "      } else {"
puts "        let seriesArray = JSON.parse(sessionStorage.getItem('seriesArray')) || [];"
puts "        if (!seriesArray.some(s => s.id === seriesId)) {"
puts "          seriesArray.push({ id: seriesId, name: seriesName });"
puts "          sessionStorage.setItem('seriesArray', JSON.stringify(seriesArray));"
puts "          updateAllLists();"
puts "        }"
puts "      }"
puts "    }"

puts "    if (event.target.classList.contains('removeFromList')) {"
puts "      event.preventDefault();"
puts "      const type = event.target.dataset.type;"
puts "      const index = parseInt(event.target.dataset.index, 10);"
puts "      let key = `${type}Array`;"
puts "      let arr = JSON.parse(sessionStorage.getItem(key)) || [];"
puts "      arr.splice(index, 1);"
puts "      sessionStorage.setItem(key, JSON.stringify(arr));"
puts "      updateAllLists();"
puts "    }"
puts "  });"

puts "  function updateAllLists() {"
puts "    let seriesArray = JSON.parse(sessionStorage.getItem('seriesArray')) || [];"
puts "    let seasonArray = JSON.parse(sessionStorage.getItem('seasonArray')) || [];"

puts "    document.getElementById('seriesArrayInput').value = JSON.stringify(seriesArray);"
puts "    document.getElementById('seasonArrayInput').value = JSON.stringify(seasonArray);"

puts "    let container = document.getElementById('seriesList');"
puts "    container.innerHTML = '';"

puts "    seriesArray.forEach((s, i) => {"
puts "      container.innerHTML += `<li class='list-group-item d-flex justify-content-between align-items-center'>${s.name} <button class='removeFromList btn btn-danger btn-sm' data-type='series' data-index='${i}'>X</button></li>`;"
puts "    });"

puts "    seasonArray.forEach((s, i) => {"
puts "      container.innerHTML += `<li class='list-group-item d-flex justify-content-between align-items-center'>${s.name} Season ${s.season} <button class='removeFromList btn btn-danger btn-sm' data-type='season' data-index='${i}'>X</button></li>`;"
puts "    });"

puts "    const typeSelect = document.getElementById('type');"
puts "    if (seriesArray.length > 0) {"
puts "      typeSelect.value = 'Series';"
puts "      typeSelect.disabled = true;"
puts "    } else if (seasonArray.length > 0) {"
puts "      typeSelect.value = 'Season';"
puts "      typeSelect.disabled = true;"
puts "    } else {"
puts "      typeSelect.disabled = false;"
puts "    }"
puts "  }"
puts "});"
puts "</script>"

puts "</body>"
puts "</html>"

session.close
