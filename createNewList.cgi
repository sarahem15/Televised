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
list_id = cgi['list_id'].to_i  # Getting the list ID to edit

# Set up the database connection
db = Mysql2::Client.new(
  host: '10.20.3.4',
  username: 'seniorproject25',
  password: 'TV_Group123!',
  database: 'televised_w25'
)

# Fetch existing list details
list_details = db.query("SELECT * FROM listOwnership WHERE id = #{list_id} AND username = '#{username}'").first
if list_details.nil?
  puts "<script>alert('List not found or you do not have permission to edit it.'); window.location.href = 'Profile_Lists.cgi';</script>"
  exit
end

# Fetch selected series and seasons for this list
selected_series = db.query("SELECT * FROM curatedListSeries WHERE listId = #{list_id}").to_a
selected_seasons = db.query("SELECT * FROM curatedListSeason WHERE listId = #{list_id}").to_a

# Start HTML output for editing the list
puts "<!DOCTYPE html>"
puts "<html lang='en'>"
puts "<head>"
puts "  <meta charset='UTF-8'>"
puts "  <meta name='viewport' content='width=device-width, initial-scale=1.0'>"
puts "  <title>Edit List</title>"
puts "  <link href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css' rel='stylesheet'>"
puts "  <link rel='stylesheet' href='Televised.css'>"
puts "</head>"
puts "<body id='editList'>"
puts "  <nav id='changingNav'></nav>"
puts "  <h2 class='text-center mt-3'>Edit List</h2>"
puts "  <div class='container-fluid'>"
puts "    <div class='row'>"
puts "      <div class='col-12 col-md-4' id='listRow'>"
puts "        <h3 class='text-center'>List Details</h3>"
puts "        <form id='editListForm' method='post'>"
puts "          <input type='hidden' name='list_id' value='#{list_id}'>"
puts "          <label>Name</label>"
puts "          <input type='text' name='listName' class='form-control' value='#{list_details["listName"]}' required>"
puts "          <br>"
puts "          <label>Who Can View</label>"
puts "          <select name='views' class='form-control'>"
puts "            <option value='Public' #{'selected' if list_details['privacy'] == 1}>Public - anyone can view</option>"
puts "            <option value='Private' #{'selected' if list_details['privacy'] == 0}>Private - no one can view</option>"
puts "          </select>"
puts "          <br>"
puts "          <label>Description</label>"
puts "          <textarea name='description' class='form-control' rows='5'>#{list_details["description"]}</textarea>"
puts "          <br>"
puts "          <input type='hidden' id='seriesArrayInput' name='seriesArray'>"
puts "          <input type='hidden' id='seasonArrayInput' name='seasonArray'>"
puts "          <button id='saveList' name='saveList' class='btn btn-primary'>SAVE CHANGES</button>"
puts "        </form>"
puts "      </div>"
puts "      <div class='col-12 col-md-4' id='listColumn'>"
puts "        <h3 class='text-center'>Selected Series/Seasons</h3>"
puts "        <ul id='seriesList' class='list-group'>"
puts "          <!-- Pre-populate with the selected series and seasons -->"
puts "        </ul>"
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
puts '<!-- Scripts -->'
puts '<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>'
puts '<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>'
puts '<script src="Televised.js"></script>'
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
      fetch('EditList.cgi', {
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

      const typeSelect = document.getElementById("type");
      if (seriesArray.length > 0) {
        typeSelect.value = "Series";
        typeSelect.disabled = true;
      } else if (seasonArray.length > 0) {
        typeSelect.value = "Season";
        typeSelect.disabled = true;
      } else {
        typeSelect.disabled = false;
      }
    }
  });
</script>
JAVASCRIPT
puts "</body>"
puts "</html>"

# Handle updating list data when the form is submitted
if cgi['saveList'] && !cgi['listName'].empty? && !cgi['description'].empty?
  privacy = cgi['views'] == 'Public' ? 1 : 0

  # Update the list details
  db.query("UPDATE listOwnership SET listName = '#{db.escape(cgi['listName'])}', description = '#{db.escape(cgi['description'])}', privacy = #{privacy} WHERE id = #{list_id}")

  # Update the selected series and seasons
  db.query("DELETE FROM curatedListSeries WHERE listId = #{list_id}")
  db.query("DELETE FROM curatedListSeason WHERE listId = #{list_id}")

  # Add updated series and seasons
  seriesArray = JSON.parse(cgi['seriesArray'])
  seasonArray = JSON.parse(cgi['seasonArray'])

  # Insert series data
  seriesArray.each do |series|
    db.query("INSERT INTO curatedListSeries (username, seriesId, name, description, privacy, date, listId)
              VALUES ('#{username}', #{series['id']}, '#{db.escape(cgi['listName'])}', '#{db.escape(cgi['description'])}', #{privacy}, NOW(), #{list_id})")
  end

  # Insert season data
  seasonArray.each do |season|
    db.query("INSERT INTO curatedListSeason (username, seasonId, name, description, privacy, date, listId)
              VALUES ('#{username}', #{season['seasonId']}, '#{db.escape(cgi['listName'])}', '#{db.escape(cgi['description'])}', #{privacy}, NOW(), #{list_id})")
  end

  puts "<script>alert('Your list has been successfully updated!'); window.location.href = 'Profile_Lists.cgi';</script>"
  exit
end

session.close
