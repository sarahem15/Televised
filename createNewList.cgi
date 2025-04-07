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

# Handle AJAX search functionality
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

# Handle list creation
if cgi['saveList'] && !listName.empty? && !description.empty?
  existing_list = db.query("SELECT id FROM listOwnership WHERE username = '#{username}' AND listName = '#{db.escape(listName)}'")

  if existing_list.count > 0
    puts "<script>alert('Sorry, but you already have a list with this name. Try a different name.');</script>"
    exit
  end

  db.query("INSERT INTO listOwnership (username, listName) VALUES ('#{username}', '#{db.escape(listName)}')")
  list_id = db.last_id

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

  puts "<script>alert('Your list has been successfully created!'); window.location.href = 'Profile_Lists.cgi';</script>"
  exit
end

# Start HTML output
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
puts "          </select>"
puts "          <br>"
puts "          <input type='text' name='mediaEntered' class='form-control'>"
puts "          <input type='submit' value='Search' class='btn btn-secondary mt-2'>"
puts "        </form>"
puts "        <div id='searchResults'></div>"
puts "      </div>"
puts "    </div>"
puts "  </div>"
puts <<~JAVASCRIPT
<script>
  document.addEventListener('DOMContentLoaded', function () {
    sessionStorage.removeItem('seriesArray');
    sessionStorage.removeItem('seasonArray');
    sessionStorage.removeItem('episodeArray');
    updateAllLists();

    document.getElementById('searchForm').addEventListener('submit', function (event) {
      event.preventDefault();
      let searchInput = document.querySelector('input[name="mediaEntered"]').value;
      let type = document.querySelector('select[name="typeSearch"]').value;
      fetch('createNewList.cgi', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({ mediaEntered: searchInput, typeSearch: type })
      })
      .then(response => response.text())
      .then(data => { document.getElementById('searchResults').innerHTML = data; });
    });

    document.addEventListener("click", function (event) {
      if (event.target.classList.contains("addToList")) {
        event.preventDefault();
        let seriesId = event.target.dataset.seriesId;
        let seriesName = event.target.dataset.seriesName;
        let parent = event.target.closest("p");

        if (document.querySelector("select.seasonSelect", parent)) {
          let seasonNum = parent.querySelector("select.seasonSelect").selectedIndex + 1;
          let seasonArray = JSON.parse(sessionStorage.getItem("seasonArray")) || [];
          if (!seasonArray.some(s => s.seriesId === seriesId && s.season === seasonNum)) {
            seasonArray.push({ seriesId: seriesId, name: seriesName, season: seasonNum });
            sessionStorage.setItem("seasonArray", JSON.stringify(seasonArray));
            updateAllLists();
          }
        } else {
          let seriesArray = JSON.parse(sessionStorage.getItem("seriesArray")) || [];
          if (!seriesArray.some(s => s.id === seriesId)) {
            seriesArray.push({ id: seriesId, name: seriesName });
            sessionStorage.setItem("seriesArray", JSON.stringify(seriesArray));
            updateAllLists();
          }
        }
      }

      if (event.target.classList.contains("removeFromList")) {
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
      let seriesArray = JSON.parse(sessionStorage.getItem("seriesArray")) || [];
      let seasonArray = JSON.parse(sessionStorage.getItem("seasonArray")) || [];

      document.getElementById('seriesArrayInput').value = JSON.stringify(seriesArray);
      document.getElementById('seasonArrayInput').value = JSON.stringify(seasonArray);

      let container = document.getElementById("seriesList");
      container.innerHTML = "";

      seriesArray.forEach((s, i) => {
        container.innerHTML += `<li class='list-group-item d-flex justify-content-between align-items-center'>
          \${s.name} <button class='removeFromList btn btn-danger btn-sm' data-type='series' data-index='\${i}'>X</button>
        </li>`;
      });

      seasonArray.forEach((s, i) => {
        container.innerHTML += `<li class='list-group-item d-flex justify-content-between align-items-center'>
          \${s.name} Season \${s.season} <button class='removeFromList btn btn-danger btn-sm' data-type='season' data-index='\${i}'>X</button>
        </li>`;
      });
    }
  });
</script>
JAVASCRIPT
puts "</body>"
puts "</html>"

session.close
