#!/usr/bin/env ruby
require 'cgi'
require 'mysql2'
require 'json'
require 'date'

cgi = CGI.new
params = cgi.params

# --- AJAX: SEARCH ---
if params["action"]&.first == "search"
  term = cgi['term']
  type = cgi['mediaType']
  client = Mysql2::Client.new(host: "localhost", username: "your_username", password: "your_password", database: "your_database")
  results = []
  series_query = client.prepare("SELECT * FROM series WHERE showName LIKE ?")
  series_query.execute("%#{term}%").each do |row|
    item = { showId: row["showId"], showName: row["showName"], imageName: row["imageName"] }
    if type == "season" || type == "episode"
      seasons = []
      season_query = client.prepare("SELECT seasonId, seasonNum FROM season WHERE seriesId = ?")
      season_query.execute(row["showId"]).each { |s| seasons << { seasonId: s["seasonId"], seasonNum: s["seasonNum"] } }
      item[:seasons] = seasons
    end
    results << item
  end
  puts cgi.header("type" => "application/json")
  puts results.to_json
  exit
end

# --- AJAX: GET EPISODES ---
if params["action"]&.first == "getEpisodes"
  client = Mysql2::Client.new(host: "localhost", username: "your_username", password: "your_password", database: "your_database")
  season_id = cgi['seasonId']
  stmt = client.prepare("SELECT epId, epName FROM episode WHERE seasonId = ?")
  result = stmt.execute(season_id).map { |ep| { epId: ep["epId"], epName: ep["epName"] } }
  puts cgi.header("type" => "application/json")
  puts result.to_json
  exit
end

# --- AJAX: SAVE LIST ---
if params["action"]&.first == "saveList"
  client = Mysql2::Client.new(host: "localhost", username: "your_username", password: "your_password", database: "your_database")

  username = "test_user" # Replace with session value if applicable
  list_name = cgi['listName']
  description = cgi['description']
  privacy = cgi['privacy'] == "Public" ? 1 : 0
  media_type = cgi['mediaType']
  items = JSON.parse(cgi['items'])
  today = Date.today.to_s

  # Check for duplicate list name
  check = client.prepare("SELECT * FROM listOwnership WHERE username = ? AND listName = ?")
  exists = check.execute(username, list_name).count > 0
  if exists
    puts cgi.header("type" => "application/json")
    puts({ success: false, message: "List name already exists." }.to_json)
    exit
  end

  # Insert into listOwnership
  insert_owner = client.prepare("INSERT INTO listOwnership (username, listName, description, privacy, date) VALUES (?, ?, ?, ?, ?)")
  insert_owner.execute(username, list_name, description, privacy, today)

  # Get listId
  get_id = client.prepare("SELECT listId FROM listOwnership WHERE username = ? AND listName = ?")
  list_id = get_id.execute(username, list_name).first["listId"]

  if media_type == "series"
    stmt = client.prepare("INSERT INTO curatedListSeries (username, seriesId, name, description, privacy, date, listId) VALUES (?, ?, ?, ?, ?, ?, ?)")
    items.each { |s| stmt.execute(username, s["showId"], list_name, description, privacy, today, list_id) }

  elsif media_type == "season"
    stmt = client.prepare("INSERT INTO curatedListSeason (username, seasonId, name, description, privacy, date, listId) VALUES (?, ?, ?, ?, ?, ?, ?)")
    items.each { |s| stmt.execute(username, s["seasonId"], list_name, description, privacy, today, list_id) }

  elsif media_type == "episode"
    stmt = client.prepare("INSERT INTO curatedListEpisode (username, epId, name, description, privacy, date, listId) VALUES (?, ?, ?, ?, ?, ?, ?)")
    items.each { |e| stmt.execute(username, e["epId"], list_name, description, privacy, today, list_id) }
  end

  puts cgi.header("type" => "application/json")
  puts({ success: true, message: "List saved successfully!" }.to_json)
  exit
end

# --- MAIN PAGE HTML ---
puts cgi.header("type" => "text/html", "charset" => "utf-8")
puts <<~HTML
<!DOCTYPE html>
<html>
<head>
  <title>Create New List</title>
  <style>
    body { font-family: Arial, sans-serif; }
    #searchResults { margin-top: 10px; }
    .resultBlock { border: 1px solid #ccc; padding: 10px; margin: 5px 0; }
    .resultImage { width: 100px; }
    select, button { margin-top: 5px; }
  </style>
</head>
<body>
  <h1>Create New List</h1>

  <form id="listForm" onsubmit="event.preventDefault(); saveList();">
    <label>List Name:</label>
    <input type="text" id="listName" required><br><br>

    <label>Description:</label><br>
    <textarea id="description" rows="3" cols="40"></textarea><br><br>

    <label>Privacy:</label>
    <select id="privacy">
      <option value="Public">Public</option>
      <option value="Private">Private</option>
    </select><br><br>

    <label>Media Type:</label>
    <select id="mediaType">
      <option value="series">Series</option>
      <option value="season">Season</option>
      <option value="episode">Episode</option>
    </select><br><br>

    <label>Search:</label>
    <input type="text" id="searchBox">
    <button type="button" onclick="performSearch()">Search</button>
    <button type="submit">Save List</button>
  </form>

  <div id="searchResults"></div>

  <script>
    let mediaType, seriesArray = [], seasonArray = [], episodeArray = [];

    function performSearch() {
      const term = document.getElementById('searchBox').value;
      mediaType = document.getElementById('mediaType').value;
      if (!term) return;

      fetch(`createNewList.cgi?action=search&term=${encodeURIComponent(term)}&mediaType=${mediaType}`)
        .then(response => response.json())
        .then(data => {
          const container = document.getElementById('searchResults');
          container.innerHTML = '';

          data.forEach(item => {
            const block = document.createElement('div');
            block.className = 'resultBlock';

            const title = document.createElement('h3');
            title.textContent = item.showName;
            block.appendChild(title);

            const image = document.createElement('img');
            image.src = '/images/' + item.imageName;
            image.className = 'resultImage';
            block.appendChild(image);

            let seasonDropdown, epDropdown;

            if (mediaType === 'season') {
              seasonDropdown = document.createElement('select');
              item.seasons.forEach(season => {
                const option = document.createElement('option');
                option.value = JSON.stringify({ seasonId: season.seasonId, seasonNum: season.seasonNum });
                option.textContent = 'Season ' + season.seasonNum;
                seasonDropdown.appendChild(option);
              });
              block.appendChild(seasonDropdown);
            }

            if (mediaType === 'episode') {
              seasonDropdown = document.createElement('select');
              epDropdown = document.createElement('select');

              seasonDropdown.onchange = function () {
                const seasonId = JSON.parse(this.value).seasonId;
                fetch(`createNewList.cgi?action=getEpisodes&seasonId=${seasonId}`)
                  .then(res => res.json())
                  .then(episodes => {
                    epDropdown.innerHTML = '';
                    episodes.forEach(ep => {
                      const option = document.createElement('option');
                      option.value = JSON.stringify({ epId: ep.epId, epName: ep.epName });
                      option.textContent = ep.epName;
                      epDropdown.appendChild(option);
                    });
                  });
              };

              item.seasons.forEach(season => {
                const option = document.createElement('option');
                option.value = JSON.stringify({ seasonId: season.seasonId, seasonNum: season.seasonNum });
                option.textContent = 'Season ' + season.seasonNum;
                seasonDropdown.appendChild(option);
              });

              block.appendChild(seasonDropdown);
              block.appendChild(epDropdown);
            }

            const addBtn = document.createElement('button');
            addBtn.textContent = 'Add';
            addBtn.onclick = function () {
              if (mediaType === 'series') {
                seriesArray.push({ showId: item.showId, showName: item.showName });
              } else if (mediaType === 'season') {
                const selected = JSON.parse(seasonDropdown.value);
                seasonArray.push({ seasonId: selected.seasonId, seasonNum: selected.seasonNum });
              } else if (mediaType === 'episode') {
                const season = JSON.parse(seasonDropdown.value);
                const ep = JSON.parse(epDropdown.value);
                episodeArray.push({ epId: ep.epId, epName: ep.epName, seasonNum: season.seasonNum });
              }
              alert("Item added.");
            };
            block.appendChild(addBtn);

            container.appendChild(block);
          });
        });
    }

    function saveList() {
      const listName = document.getElementById('listName').value;
      const description = document.getElementById('description').value;
      const privacy = document.getElementById('privacy').value;
      const mediaType = document.getElementById('mediaType').value;

      let items;
      if (mediaType === 'series') items = seriesArray;
      else if (mediaType === 'season') items = seasonArray;
      else if (mediaType === 'episode') items = episodeArray;

      fetch('createNewList.cgi?action=saveList', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({
          listName, description, privacy, mediaType,
          items: JSON.stringify(items)
        })
      })
        .then(res => res.json())
        .then(data => {
          alert(data.message);
          if (data.success) {
            seriesArray = [];
            seasonArray = [];
            episodeArray = [];
            document.getElementById('listForm').reset();
            document.getElementById('searchResults').innerHTML = '';
          }
        });
    }
  </script>
</body>
</html>
HTML
