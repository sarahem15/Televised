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
list_id = cgi['listId']&.to_i

print cgi.header(
  'cookie' => CGI::Cookie.new('name' => 'CGISESSID', 'value' => session.session_id, 'httponly' => true, 'secure' => true, 'sameSite' => 'Lax')
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

# AJAX Search
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

# Handle saving
if cgi['saveList'] && !listName.empty? && !description.empty?
  if list_id
    db.query("UPDATE listOwnership SET listName = '#{db.escape(listName)}' WHERE id = #{list_id} AND username = '#{username}'")
    db.query("DELETE FROM curatedListSeries WHERE listId = #{list_id}")
    db.query("DELETE FROM curatedListSeason WHERE listId = #{list_id}")
  else
    existing_list = db.query("SELECT id FROM listOwnership WHERE username = '#{username}' AND listName = '#{db.escape(listName)}'")
    if existing_list.count > 0
      puts "<script>alert('Sorry, but you already have a list with this name. Try a different name.');</script>"
      exit
    end
    db.query("INSERT INTO listOwnership (username, listName) VALUES ('#{username}', '#{db.escape(listName)}')")
    list_id = db.last_id
  end

  if !seriesArray.empty?
    seriesArray.each do |series|
      series_id = series["id"].to_i
      db.query("INSERT INTO curatedListSeries (username, seriesId, name, description, privacy, date, listId)
                VALUES ('#{username}', #{series_id}, '#{db.escape(listName)}', '#{db.escape(description)}', #{privacy}, NOW(), #{list_id})")
    end
  end

  if !seasonArray.empty?
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

  puts "<script>alert('Your list has been successfully #{cgi['listId'] ? 'updated' : 'created'}!'); window.location.href = 'Profile_Lists.cgi';</script>"
  exit
end

# Autofill data for editing
list_data = {}
series_json = []
season_json = []

if list_id
  result = db.query("SELECT listName, username FROM listOwnership WHERE id = #{list_id}")
  if row = result.first
    if row["username"] != username
      puts "<script>alert('Unauthorized access.'); window.location.href='Profile_Lists.cgi';</script>"
      exit
    end

    list_data = row
    desc_result = db.query("SELECT description, privacy FROM curatedListSeries WHERE listId = #{list_id} LIMIT 1")
    desc_result = db.query("SELECT description, privacy FROM curatedListSeason WHERE listId = #{list_id} LIMIT 1") if desc_result.count == 0
    if meta = desc_result.first
      list_data['description'] = meta["description"]
      list_data['privacy'] = meta["privacy"]
    end

    series_results = db.query("SELECT seriesId, name FROM curatedListSeries WHERE listId = #{list_id}")
    series_results.each do |s|
      series_json << { id: s["seriesId"], name: s["name"] }
    end

    season_results = db.query("SELECT s.seriesId, sl.name, se.seasonId
                               FROM curatedListSeason sl
                               JOIN season se ON sl.seasonId = se.seasonId
                               JOIN series s ON s.showId = se.seriesId
                               WHERE sl.listId = #{list_id}")
    season_results.each do |s|
      season_json << { seriesId: s["seriesId"], name: s["name"], season: season_json.count { |x| x[:seriesId] == s["seriesId"] } + 1 }
    end
  end
end

# START HTML
puts <<~HTML
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>#{list_id ? 'Edit List' : 'Create a New List'}</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
  <link rel="stylesheet" href="Televised.css">
  <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
</head>
<body id="createNewList">
  <nav id="changingNav"></nav>
  <h2 class="text-center mt-3">#{list_id ? 'Edit Your List' : 'Create a New List'}</h2>
  <div class="container-fluid">
    <div class="row">
      <div class="col-12 col-md-4" id="listRow">
        <h3 class="text-center">List Details</h3>
        <form id="newListForm" method="post">
          <input type="hidden" name="listId" value="#{list_id if list_id}">
          <label>Name</label>
          <input type="text" name="listName" class="form-control" value="#{CGI.escapeHTML(list_data['listName'] || '')}" required>
          <br>
          <label>Who Can View</label>
          <select name="views" class="form-control">
            <option value="Public" #{list_data['privacy'] == 1 ? 'selected' : ''}>Public</option>
            <option value="Private" #{list_data['privacy'] == 0 ? 'selected' : ''}>Private</option>
          </select>
          <br>
          <label>Description</label>
          <textarea name="description" class="form-control" rows="5">#{CGI.escapeHTML(list_data['description'] || '')}</textarea>
          <br>
          <input type="hidden" id="seriesArrayInput" name="seriesArray">
          <input type="hidden" id="seasonArrayInput" name="seasonArray">
          <button id="saveList" name="saveList" class="btn btn-primary">#{list_id ? 'SAVE CHANGES' : 'CREATE LIST'}</button>
        </form>
      </div>
      <div class="col-12 col-md-4" id="listColumn">
        <h3 class="text-center">Selected Series/Seasons</h3>
        <ul id="seriesList" class="list-group"></ul>
      </div>
      <div class="col-12 col-md-4" id="searchColumn">
        <h3 class="text-center">Search for a Series</h3>
        <form id="searchForm">
          <select id="type" name="typeSearch" class="form-control">
            <option value="Series" selected>Series</option>
            <option value="Season">Season</option>
          </select>
          <br>
          <input type="text" name="mediaEntered" class="form-control">
          <input type="submit" value="Search" class="btn btn-secondary mt-2">
        </form>
        <div id="searchResults"></div>
      </div>
    </div>
  </div>

  <script>
    const prefillSeries = #{series_json.to_json};
    const prefillSeason = #{season_json.to_json};

    function updateAllLists() {
      const seriesList = document.getElementById('seriesList');
      seriesList.innerHTML = '';

      const seriesArray = JSON.parse(sessionStorage.getItem('seriesArray') || '[]');
      const seasonArray = JSON.parse(sessionStorage.getItem('seasonArray') || '[]');

      seriesArray.forEach(series => {
        const li = document.createElement('li');
        li.className = 'list-group-item';
        li.textContent = series.name + ' (Series)';
        seriesList.appendChild(li);
      });

      seasonArray.forEach(season => {
        const li = document.createElement('li');
        li.className = 'list-group-item';
        li.textContent = season.name + ' - Season ' + season.season;
        seriesList.appendChild(li);
      });
    }

    document.addEventListener('DOMContentLoaded', () => {
      if (prefillSeries.length > 0) sessionStorage.setItem("seriesArray", JSON.stringify(prefillSeries));
      if (prefillSeason.length > 0) sessionStorage.setItem("seasonArray", JSON.stringify(prefillSeason));
      updateAllLists();
    });
  </script>

  <script src="Televised.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
HTML

session.close
