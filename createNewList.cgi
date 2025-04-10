#!/usr/bin/env ruby
require 'cgi'
require 'mysql2'
require 'json'

# Initialize CGI object
cgi = CGI.new
username = cgi.cookies['username']&.value || 'Guest'
type = cgi.params['type']&.first || ''
search = cgi.params['search']&.first || ''

# Connect to the database
db = Mysql2::Client.new(
  host: '10.20.3.4',
  username: 'seniorproject25',
  password: 'TV_Group123!',
  database: 'televised_w25'
)

# Function to escape inputs for SQL queries
def escape_input(input, db)
  db.escape(input)
end

# Handle search and adding series, seasons, or episodes
if search != ""
  if type == "Series"
    results = db.query("SELECT showName, imageName, showId FROM series WHERE showName LIKE '#{escape_input(search, db)}%'")
    if results.count > 0
      results.each do |row|
        puts "<p>#{row['showName']} <img src='#{row['imageName']}' alt='#{row['showName']}' style='height: 50px; width: 35px; object-fit: cover;'>"
        puts "<button class='addToList btn btn-success' data-series-id='#{row['showId']}' data-series-name='#{row['showName']}'>ADD</button></p>"
      end
    else
      puts "<p>We can't seem to find this title!</p>"
    end
  elsif type == "Season"
    results = db.query("SELECT showName, imageName, showId FROM series WHERE showName LIKE '#{escape_input(search, db)}%'")
    if results.count > 0
      results.each do |row|
        seasons = db.query("SELECT seasonId, seasonNum FROM season WHERE seriesId = '#{row['showId']}'").to_a
        puts "<p>#{row['showName']} <img src='#{row['imageName']}' alt='#{row['showName']}' style='height: 50px; width: 35px; object-fit: cover;'>"
        puts "<button class='addToList btn btn-success' data-series-id='#{row['showId']}' data-series-name='#{row['showName']}'>ADD</button>"
        puts "<select class='seasonSelect' data-series-id='#{row['showId']}'>"
        seasons.each_with_index do |season, index|
          puts "<option value='#{season['seasonId']}'>Season #{season['seasonNum']}</option>"
        end
        puts "</select>"
        puts "</p>"
      end
    else
      puts "<p>We can't seem to find this title!</p>"
    end
  elsif type == "Episode"
    results = db.query("SELECT epId, epName, seasonId FROM episode WHERE epName LIKE '#{escape_input(search, db)}%'")
    if results.count > 0
      results.each do |row|
        puts "<p>Episode: #{row['epName']} <button class='addToList btn btn-success' data-episode-id='#{row['epId']}' data-episode-name='#{row['epName']}'>ADD</button></p>"
      end
    else
      puts "<p>We can't seem to find this episode!</p>"
    end
  end
  exit
end

# Handle form submission
if cgi.params['submit']
  seriesArray = JSON.parse(cgi.params['seriesArray'].first)
  seasonArray = JSON.parse(cgi.params['seasonArray'].first)
  episodeArray = JSON.parse(cgi.params['episodeArray'].first)

  # Insert into listOwnership
  listName = cgi.params['listName'].first
  description = cgi.params['description'].first
  privacy = cgi.params['privacy'].first == "Public" ? 1 : 0
  list_id = db.query("INSERT INTO listOwnership (username, name, description, privacy, date) VALUES ('#{escape_input(username, db)}', '#{escape_input(listName, db)}', '#{escape_input(description, db)}', #{privacy}, NOW())")
  list_id = db.last_id

  # Insert series into curatedListSeries
  seriesArray.each do |series|
    series_id = series['id']
    db.query("INSERT INTO curatedListSeries (username, seriesId, name, description, privacy, date, listId) 
              VALUES ('#{escape_input(username, db)}', '#{series_id}', '#{escape_input(listName, db)}', '#{escape_input(description, db)}', #{privacy}, NOW(), #{list_id})")
  end

  # Insert seasons into curatedListSeason
  seasonArray.each do |season|
    season_id = season['seasonId']
    db.query("INSERT INTO curatedListSeason (username, seasonId, name, description, privacy, date, listId) 
              VALUES ('#{escape_input(username, db)}', #{season_id}, '#{escape_input(listName, db)}', '#{escape_input(description, db)}', #{privacy}, NOW(), #{list_id})")
  end

  # Insert episodes into curatedListEpisode
  episodeArray.each do |episode|
    episode_id = episode['id']
    db.query("INSERT INTO curatedListEpisode (username, episodeId, name, description, privacy, date, listId) 
              VALUES ('#{escape_input(username, db)}', #{episode_id}, '#{escape_input(listName, db)}', '#{escape_input(description, db)}', #{privacy}, NOW(), #{list_id})")
  end

  # Redirect to Profile List
  puts cgi.header("type" => "text/html")
  puts "<script>window.location.href = 'Profile_List.cgi';</script>"
end

# Output the HTML Form
puts cgi.header
puts <<-HTML
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Create New List</title>
  <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
  <script>
    document.addEventListener('DOMContentLoaded', function () {
      sessionStorage.removeItem('episodeArray');
      sessionStorage.removeItem('seasonArray');
      sessionStorage.removeItem('seriesArray');

      document.addEventListener('click', function (event) {
        if (event.target.classList.contains('addToList')) {
          event.preventDefault();
          let seriesId = event.target.dataset.seriesId;
          let seriesName = event.target.dataset.seriesName;
          let episodeId = event.target.dataset.episodeId;
          let episodeName = event.target.dataset.episodeName;
          let parent = event.target.closest('p');

          if (parent.querySelector('select.seasonSelect')) {
            let seasonNum = parent.querySelector('select.seasonSelect').selectedIndex + 1;
            let seasonArray = JSON.parse(sessionStorage.getItem('seasonArray')) || [];
            if (!seasonArray.some(s => s.seriesId === seriesId && s.season === seasonNum)) {
              seasonArray.push({ seriesId: seriesId, name: seriesName, season: seasonNum });
              sessionStorage.setItem('seasonArray', JSON.stringify(seasonArray));
              updateAllLists();
            }
          } else if (episodeId) {
            let episodeArray = JSON.parse(sessionStorage.getItem('episodeArray')) || [];
            if (!episodeArray.some(e => e.id === episodeId)) {
              episodeArray.push({ id: episodeId, name: episodeName, seriesId: seriesId });
              sessionStorage.setItem('episodeArray', JSON.stringify(episodeArray));
              updateAllLists();
            }
          } else {
            let seriesArray = JSON.parse(sessionStorage.getItem('seriesArray')) || [];
            if (!seriesArray.some(s => s.id === seriesId)) {
              seriesArray.push({ id: seriesId, name: seriesName });
              sessionStorage.setItem('seriesArray', JSON.stringify(seriesArray));
              updateAllLists();
            }
          }
        }

        if (event.target.classList.contains('removeFromList')) {
          event.preventDefault();
          const type = event.target.dataset.type;
          const index = parseInt(event.target.dataset.index, 10);
          let key = `${type}Array`;
          let arr = JSON.parse(sessionStorage.getItem(key)) || [];
          arr.splice(index, 1);
          sessionStorage.setItem(key, JSON.stringify(arr));
          updateAllLists();
        }
      });

      function updateAllLists() {
        let seriesArray = JSON.parse(sessionStorage.getItem('seriesArray')) || [];
        let seasonArray = JSON.parse(sessionStorage.getItem('seasonArray')) || [];
        let episodeArray = JSON.parse(sessionStorage.getItem('episodeArray')) || [];

        document.getElementById('seriesArrayInput').value = JSON.stringify(seriesArray);
        document.getElementById('seasonArrayInput').value = JSON.stringify(seasonArray);
        document.getElementById('episodeArrayInput').value = JSON.stringify(episodeArray);

        let container = document.getElementById('seriesList');
        container.innerHTML = '';

        seriesArray.forEach((s, i) => {
          container.innerHTML += `<li class='list-group-item d-flex justify-content-between align-items-center'>${s.name} <button class='removeFromList btn btn-danger btn-sm' data-type='series' data-index='${i}'>X</button></li>`;
        });

        seasonArray.forEach((s, i) => {
          container.innerHTML += `<li class='list-group-item d-flex justify-content-between align-items-center'>${s.name} Season ${s.season} <button class='removeFromList btn btn-danger btn-sm' data-type='season' data-index='${i}'>X</button></li>`;
        });

        episodeArray.forEach((e, i) => {
          container.innerHTML += `<li class='list-group-item d-flex justify-content-between align-items-center'>${e.name} <button class='removeFromList btn btn-danger btn-sm' data-type='episode' data-index='${i}'>X</button></li>`;
        });
      }
    });
  </script>
</head>
<body>
  <h1>Create New List</h1>
  <form method="post" action="createNewList.cgi">
    <label for="listName">List Name:</label>
    <input type="text" id="listName" name="listName" required><br>

    <label for="description">Description:</label>
    <textarea id="description" name="description" required></textarea><br>

    <label for="privacy">Privacy:</label>
    <select name="privacy" id="privacy">
      <option value="Public">Public</option>
      <option value="Private">Private</option>
    </select><br><br>

    <label for="search">Search:</label>
    <input type="text" id="search" name="search"><br><br>

    <label for="type">Type:</label>
    <select id="type" name="type">
      <option value="Series">Series</option>
      <option value="Season">Season</option>
      <option value="Episode">Episode</option>
    </select><br><br>

    <div id="seriesList"></div>
    <input type="hidden" id="seriesArrayInput" name="seriesArray">
    <input type="hidden" id="seasonArrayInput" name="seasonArray">
    <input type="hidden" id="episodeArrayInput" name="episodeArray">

    <input type="submit" name="submit" value="Create List">
  </form>
</body>
</html>
