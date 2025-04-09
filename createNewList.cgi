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

#episodeSearch
  elsif type == "Episode"
    results = db.query("SELECT showName, imageName, showId FROM series WHERE showName LIKE '#{db.escape(search)}%'")

    if results.count > 0
      results.each do |row|
        seasons = db.query("SELECT seasonId from season WHERE seriesId = '" + images[i]['showId'].to_s + "';")
        seasons = seasons.to_a
        puts "<p>#{row['showName']} <img src='#{row['imageName']}' alt='#{row['showName']}' style='height: 50px; width: 35px; object-fit: cover;'>"
        puts "<button class='addToList btn btn-success' data-series-id='#{row['showId']}' data-series-name='#{row['showName']}'>ADD</button>"
        puts "<select class='seasonSelect' data-series-id='#{row['showId']}'>"
        seasons.each_with_index do |season, index|
          puts "<option value='#{season['seasonId']}'>Season #{index + 1}</option>"
        end
        episodes = db.query("SELECT * FROM episode JOIN season ON season.seasonId = episode.seasonId WHERE seasonNum = '" + seasonNum + "' AND seriesId = '" + images[i]['showId'].to_s + "';")
        episodes = episodes.to_a
        puts '<select id="typeSeason" name="epNum" class="form-control">'
        puts '<option value="" selected>Episode</option>'
              (0...episodes.size).each do |h|
              puts '<option value="' + episodes[h]['epId'].to_s + '">' + episodes[h]['epName'] + '</option>'
            end
          puts '</select>'
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

  unless episodeArray.empty?
    episodeArray.each do |episode|
      show_id = episode["seriesId"].to_i
      season_num = episode["season"].to_i
      ep_name = episode["epName"]
      result = db.query("SELECT seasonId FROM season WHERE seriesId = #{show_id} ORDER BY seasonId ASC LIMIT 1 OFFSET #{season_num - 1}")
      if result.count > 0
        season_id = result.first["seasonId"].to_i
        db.query("INSERT INTO curatedListEpisode (username, seasonId, epName, name, description, privacy, date, listId)
                  VALUES ('#{username}', #{season_id}, #{epName}, '#{db.escape(listName)}', '#{db.escape(description)}', #{privacy}, NOW(), #{list_id})")
      end
    end
  end

  if seriesArray.empty? && seasonArray.empty? && episodeArray.empty?
    puts "<script>alert('Please select at least one series, season, or episode before saving.');</script>"
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
puts "        <h3 class='text-center'>Selected Series/Seasons?Episodes</h3>"
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








#!/usr/bin/env ruby
require 'cgi'
require 'mysql2'
require 'json'
require 'date'

cgi = CGI.new
puts cgi.header("type" => "text/html", "charset" => "utf-8")

# --- Session Handling ---
session = CGI::Cookie::new("name" => "user", "value" => "", "path" => "/")
username = cgi.cookies["user"]&.first

# --- HTML Output Start ---
puts <<-HTML
<html>
<head>
  <title>Create New List</title>
  <script>
    let seriesArray = [];
    let seasonArray = [];
    let episodeArray = [];

    function updateDisplay() {
      document.getElementById("seriesList").innerHTML = seriesArray.map((s, i) =>
        `<li>${s}<button onclick="removeFromArray(${i}, 'series')">Remove</button></li>`).join("");
      document.getElementById("seasonList").innerHTML = seasonArray.map((s, i) =>
        `<li>${s}<button onclick="removeFromArray(${i}, 'season')">Remove</button></li>`).join("");
      document.getElementById("episodeList").innerHTML = episodeArray.map((ep, i) =>
        `<li>${ep.showName}: S${ep.seasonNumber}: ${ep.epName} <button onclick="removeFromArray(${i}, 'episode')">Remove</button></li>`).join("");
    }

    function removeFromArray(index, type) {
      if (type === 'series') seriesArray.splice(index, 1);
      else if (type === 'season') seasonArray.splice(index, 1);
      else if (type === 'episode') episodeArray.splice(index, 1);
      updateDisplay();
    }

    function addSeries() {
      const series = document.getElementById("seriesInput").value;
      if (series && !seriesArray.includes(series)) {
        seriesArray.push(series);
        updateDisplay();
      }
    }

    function addSeason() {
      const series = document.getElementById("seriesInput").value;
      const season = document.getElementById("seasonInput").value;
      if (series && season) {
        const entry = `${series} Season ${season}`;
        if (!seasonArray.includes(entry)) {
          seasonArray.push(entry);
          updateDisplay();
        }
      }
    }

    function fetchSeasons() {
      const showId = document.getElementById("episodeSeries").value;
      fetch(`/getSeasons.cgi?showId=${showId}`)
        .then(res => res.json())
        .then(data => {
          const dropdown = document.getElementById("episodeSeason");
          dropdown.innerHTML = "";
          data.forEach(season => {
            const opt = document.createElement("option");
            opt.value = season.seasonId;
            opt.text = "Season " + season.seasonNum;
            dropdown.add(opt);
          });
        });
    }

    function fetchEpisodes() {
      const seasonId = document.getElementById("episodeSeason").value;
      fetch(`/getEpisodes.cgi?seasonId=${seasonId}`)
        .then(res => res.json())
        .then(data => {
          const dropdown = document.getElementById("episodeName");
          dropdown.innerHTML = "";
          data.forEach(ep => {
            const opt = document.createElement("option");
            opt.value = ep.epId;
            opt.text = ep.epName;
            dropdown.add(opt);
          });
        });
    }

    function addEpisode() {
      const seriesDropdown = document.getElementById("episodeSeries");
      const seasonDropdown = document.getElementById("episodeSeason");
      const episodeDropdown = document.getElementById("episodeName");

      const showId = seriesDropdown.value;
      const showName = seriesDropdown.options[seriesDropdown.selectedIndex].text;
      const seasonNumber = seasonDropdown.options[seasonDropdown.selectedIndex].text.replace("Season ", "");
      const epId = episodeDropdown.value;
      const epName = episodeDropdown.options[episodeDropdown.selectedIndex].text;

      const entry = { showId, showName, epId, epName, seasonNumber };
      if (!episodeArray.some(e => e.epId === epId)) {
        episodeArray.push(entry);
        updateDisplay();
      }

      document.getElementById("mediaSelect").disabled = true;
    }

    function submitForm() {
      const mediaType = document.getElementById("mediaSelect").value;
      const name = document.getElementById("listName").value;
      const description = document.getElementById("description").value;
      const privacy = document.querySelector('input[name="privacy"]:checked').value;

      fetch("createNewList.cgi", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          mediaType, name, description, privacy,
          seriesArray, seasonArray, episodeArray
        })
      })
      .then(res => res.json())
      .then(data => {
        alert(data.message);
        if (data.success) {
          document.getElementById("listName").value = "";
          document.getElementById("description").value = "";
          seriesArray = [];
          seasonArray = [];
          episodeArray = [];
          updateDisplay();
          document.getElementById("mediaSelect").disabled = false;
          window.location.href = "Profile_List.cgi";
        }
      });
    }
  </script>
</head>
<body onload="updateDisplay()">
  <h1>Create New List</h1>
  <label for="mediaSelect">Media Type:</label>
  <select id="mediaSelect">
    <option value="series">Series</option>
    <option value="season">Season</option>
    <option value="episode">Episode</option>
  </select><br><br>

  <label for="seriesInput">Series Name:</label>
  <input type="text" id="seriesInput">
  <button onclick="addSeries()">Add Series</button><br><br>

  <label for="seasonInput">Season #:</label>
  <input type="number" id="seasonInput">
  <button onclick="addSeason()">Add Season</button><br><br>

  <label>Episode Selection:</label><br>
  Series: 
  <select id="episodeSeries" onchange="fetchSeasons()">
    <!-- Filled from DB -->
HTML

# --- Database for episode dropdowns ---
begin
  client = Mysql2::Client.new(:host => "localhost", :username => "youruser", :password => "yourpass", :database => "yourdb")
  results = client.query("SELECT showId, showName FROM series")
  results.each do |row|
    puts "<option value='#{row["showId"]}'>#{row["showName"]}</option>"
  end
rescue => e
  puts "<option disabled>Error loading series</option>"
end

puts <<-HTML
  </select>
  Season: <select id="episodeSeason" onchange="fetchEpisodes()"></select>
  Episode: <select id="episodeName"></select>
  <button onclick="addEpisode()">Add Episode</button><br><br>

  <label for="listName">List Name:</label>
  <input type="text" id="listName"><br><br>

  <label for="description">Description:</label><br>
  <textarea id="description" rows="4" cols="50"></textarea><br><br>

  <label>Privacy:</label>
  <input type="radio" name="privacy" value="1" checked> Public
  <input type="radio" name="privacy" value="0"> Private<br><br>

  <button onclick="submitForm()">Save List</button><br><br>

  <h3>Series List:</h3>
  <ul id="seriesList"></ul>

  <h3>Season List:</h3>
  <ul id="seasonList"></ul>

  <h3>Episode List:</h3>
  <ul id="episodeList"></ul>
</body>
</html>
HTML

# --- Backend logic (only run for POST) ---
if ENV["REQUEST_METHOD"] == "POST"
  request = JSON.parse($stdin.read)
  mediaType = request["mediaType"]
  name = request["name"]
  description = request["description"]
  privacy = request["privacy"].to_i
  date = Date.today.to_s

  begin
    list_exists = client.query("SELECT listId FROM listOwnership WHERE username='#{username}' AND name='#{client.escape(name)}'")
    if list_exists.count > 0
      puts({ success: false, message: "List with this name already exists." }.to_json)
    else
      client.query("INSERT INTO listOwnership (username, name) VALUES ('#{username}', '#{client.escape(name)}')")
      listId = client.last_id

      case mediaType
      when "series"
        request["seriesArray"].each do |title|
          res = client.query("SELECT showId FROM series WHERE showName='#{client.escape(title)}'")
          if row = res.first
            client.query("INSERT INTO curatedListSeries (username, seriesId, name, description, privacy, date, listId) VALUES ('#{username}', #{row["showId"]}, '#{client.escape(name)}', '#{client.escape(description)}', #{privacy}, '#{date}', #{listId})")
          end
        end
      when "season"
        request["seasonArray"].each do |entry|
          show, season = entry.split(" Season ")
          res = client.query("SELECT seasonId FROM season JOIN series ON season.seriesId = series.showId WHERE series.showName='#{client.escape(show)}' AND season.seasonNum=#{season.to_i}")
          if row = res.first
            client.query("INSERT INTO curatedListSeason (username, seasonId, name, description, privacy, date, listId) VALUES ('#{username}', #{row["seasonId"]}, '#{client.escape(name)}', '#{client.escape(description)}', #{privacy}, '#{date}', #{listId})")
          end
        end
      when "episode"
        request["episodeArray"].each do |ep|
          client.query("INSERT INTO curatedListEpisode (username, epId, name, description, privacy, date, listId) VALUES ('#{username}', #{ep["epId"]}, '#{client.escape(name)}', '#{client.escape(description)}', #{privacy}, '#{date}', #{listId})")
        end
      end

      puts({ success: true, message: "List saved successfully!" }.to_json)
    end
  rescue => e
    puts({ success: false, message: "Error: #{e.message}" }.to_json)
  end
end

