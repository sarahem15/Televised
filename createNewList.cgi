#!/usr/bin/ruby

require 'cgi'
require 'mysql2'
require 'json'

# Initialize CGI and database connection
cgi = CGI.new
db = Mysql2::Client.new(
  host: 'localhost', 
  username: 'root', 
  password: 'password', 
  database: 'your_database'
)

# Function to escape user inputs for SQL queries
def escape_input(input)
  CGI.escapeHTML(input)
end

# Handle form submission for series, season, and episode search
search = cgi.params['search']&.first.to_s.strip
type = cgi.params['typeSearch']&.first.to_s.strip
mediaEntered = cgi.params['mediaEntered']&.first.to_s.strip

# Handle AJAX search for series, season, and episode
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
        seasons = db.query("SELECT seasonId, seasonNum FROM season WHERE seriesId = '#{row['showId']}'").to_a
        puts "<p>#{row['showName']} <img src='#{row['imageName']}' alt='#{row['showName']}' style='height: 50px; width: 35px; object-fit: cover;'>"
        puts "<button class='addToList btn btn-success' data-series-id='#{row['showId']}' data-series-name='#{row['showName']}'>ADD</button>"
        puts "<select class='seasonSelect' data-series-id='#{row['showId']}'>"
        seasons.each_with_index do |season, index|
          puts "<option value='#{season['seasonId']}'>Season #{season['seasonNum']}</option>"
        end
        puts "</select></p>"
      end
    else
      puts "<p>We can't seem to find this title!</p>"
    end
  elsif type == "Episode"
    results = db.query("SELECT showName, imageName, showId FROM series WHERE showName LIKE '#{db.escape(search)}%'")
    if results.count > 0
      results.each do |row|
        seasons = db.query("SELECT seasonId, seasonNum FROM season WHERE seriesId = '#{row['showId']}'").to_a
        puts "<p>#{row['showName']} <img src='#{row['imageName']}' alt='#{row['showName']}' style='height: 50px; width: 35px; object-fit: cover;'>"
        puts "<select class='seasonSelect' data-series-id='#{row['showId']}'>"
        seasons.each_with_index do |season, index|
          puts "<option value='#{season['seasonId']}'>Season #{season['seasonNum']}</option>"
        end
        puts "</select>"
        puts "<select class='episodeSelect' style='display:none;' data-series-id='#{row['showId']}'></select>"
        puts "<button class='addToList btn btn-success' data-series-id='#{row['showId']}' data-series-name='#{row['showName']}'>ADD</button>"
        puts "</p>"
      end
    else
      puts "<p>We can't seem to find this title!</p>"
    end
  end
  exit
end

# Main form for creating a new list
puts "Content-type: text/html\n\n"
puts "<html><head><title>Create New List</title></head><body>"

puts "<h1>Create New List</h1>"
puts "<form method='POST' action='createNewList.cgi'>"
puts "<input type='text' name='listName' placeholder='List Name'><br>"
puts "<textarea name='description' placeholder='Description'></textarea><br>"
puts "<label for='privacy'>Privacy:</label>"
puts "<select name='privacy' id='privacy'><option value='1'>Public</option><option value='0'>Private</option></select><br>"
puts "<input type='text' id='search' name='search' placeholder='Search Series, Season, Episode'><br>"

puts "<div id='searchResults'></div>"

# Display the button for saving the list
puts "<button type='submit' name='saveList'>Save List</button>"
puts "</form>"

# JavaScript for handling episode dropdown population
puts "<script>"
puts "document.addEventListener('DOMContentLoaded', function () {"
puts "  document.getElementById('search').addEventListener('input', function () {"
puts "    let search = this.value;"
puts "    if (search.length > 0) {"
puts "      fetch('createNewList.cgi', {"
puts "        method: 'POST',"
puts "        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },"
puts "        body: new URLSearchParams({ search: search, typeSearch: 'Series' })"
puts "      })"
puts "      .then(response => response.text())"
puts "      .then(data => {"
puts "        document.getElementById('searchResults').innerHTML = data;"
puts "      });"
puts "    } else {"
puts "      document.getElementById('searchResults').innerHTML = '';"
puts "    }"
puts "  });"

puts "  document.addEventListener('change', function (event) {"
puts "    if (event.target.classList.contains('seasonSelect')) {"
puts "      let seriesId = event.target.dataset.seriesId;"
puts "      let seasonId = event.target.value;"
puts "      let episodeSelect = event.target.closest('p').querySelector('.episodeSelect');"
puts "      episodeSelect.style.display = 'block';"
puts "      fetch('createNewList.cgi', {"
puts "        method: 'POST',"
puts "        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },"
puts "        body: new URLSearchParams({ mediaEntered: '', typeSearch: 'Episode', seriesId: seriesId, seasonId: seasonId })"
puts "      })"
puts "      .then(response => response.text())"
puts "      .then(data => {"
puts "        episodeSelect.innerHTML = data;"
puts "      });"
puts "    }"
puts "  });"

puts "  document.addEventListener('click', function (event) {"
puts "    if (event.target.classList.contains('addToList')) {"
puts "      let seriesId = event.target.dataset.seriesId;"
puts "      let seriesName = event.target.dataset.seriesName;"
puts "      let seasonSelect = event.target.closest('p').querySelector('.seasonSelect');"
puts "      let episodeSelect = event.target.closest('p').querySelector('.episodeSelect');"
puts "      let seasonId = seasonSelect.value;"
puts "      let episodeId = episodeSelect.value;"
puts "      let episodeName = episodeSelect.options[episodeSelect.selectedIndex].text;"

puts "      let episodeArray = JSON.parse(sessionStorage.getItem('episodeArray')) || [];"
puts "      if (!episodeArray.some(e => e.seriesId === seriesId && e.seasonId === seasonId && e.episodeId === episodeId)) {"
puts "        episodeArray.push({ seriesId: seriesId, seriesName: seriesName, seasonId: seasonId, episodeId: episodeId, episodeName: episodeName });"
puts "        sessionStorage.setItem('episodeArray', JSON.stringify(episodeArray));"
puts "        updateAllLists();"
puts "      }"
puts "    }"
puts "  });"
puts "});"
puts "</script>"

puts "<!-- End of HTML --></body></html>"

