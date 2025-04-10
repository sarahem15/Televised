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
    results = db.query("SELECT e.epId, e.epName, e.seasonId, e.releaseDate, s.showName, s.imageName, s.showId FROM episode e JOIN series s ON e.seriesId = s.showId WHERE e.epName LIKE '#{db.escape(search)}%'")
    if results.count > 0
      results.each do |row|
        # Get season number and episode title
        season_info = db.query("SELECT seasonNum FROM season WHERE seasonId = '#{row['seasonId']}'").first
        puts "<p>#{row['showName']} <img src='#{row['imageName']}' alt='#{row['showName']}' style='height: 50px; width: 35px; object-fit: cover;'>"
        puts "Season #{season_info['seasonNum']} - Episode: #{row['epName']}"
        puts "<button class='addToList btn btn-success' data-episode-id='#{row['epId']}' data-episode-name='#{row['epName']}' data-show-id='#{row['showId']}' data-show-name='#{row['showName']}'>ADD</button></p>"
      end
    else
      puts "<p>We can't seem to find this episode!</p>"
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
puts "        body: new URLSearchParams({ search: search, typeSearch: 'Episode' })"
puts "      })"
puts "      .then(response => response.text())"
puts "      .then(data => {"
puts "        document.getElementById('searchResults').innerHTML = data;"
puts "      });"
puts "    } else {"
puts "      document.getElementById('searchResults').innerHTML = '';"
puts "    }"
puts "  });"

puts "  document.addEventListener('click', function (event) {"
puts "    if (event.target.classList.contains('addToList')) {"
puts "      let episodeId = event.target.dataset.episodeId;"
puts "      let episodeName = event.target.dataset.episodeName;"
puts "      let showId = event.target.dataset.showId;"
puts "      let showName = event.target.dataset.showName;"

puts "      let episodeArray = JSON.parse(sessionStorage.getItem('episodeArray')) || [];"
puts "      if (!episodeArray.some(e => e.episodeId === episodeId)) {"
puts "        episodeArray.push({ episodeId: episodeId, episodeName: episodeName, showId: showId, showName: showName });"
puts "        sessionStorage.setItem('episodeArray', JSON.stringify(episodeArray));"
puts "        updateAllLists();"
puts "      }"
puts "    }"
puts "  });"
puts "});"
puts "</script>"

puts "<!-- End of HTML --></body></html>"
