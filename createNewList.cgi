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
  results_html = ""  # To accumulate results as HTML

  if type == "Series"
    results = db.query("SELECT showName, imageName, showId FROM series WHERE showName LIKE '#{db.escape(search)}%'")
    if results.count > 0
      results.each do |row|
        results_html += "<p>#{row['showName']} <img src='#{row['imageName']}' alt='#{row['showName']}' style='height: 50px; width: 35px; object-fit: cover;'>"
        results_html += "<button class='addToList btn btn-success' data-series-id='#{row['showId']}' data-series-name='#{row['showName']}'>ADD</button></p>"
      end
    else
      results_html += "<p>We can't seem to find this title!</p>"
    end
  elsif type == "Season"
    results = db.query("SELECT showName, imageName, showId FROM series WHERE showName LIKE '#{db.escape(search)}%'")
    if results.count > 0
      results.each do |row|
        seasons = db.query("SELECT seasonId FROM season WHERE seriesId = '#{row['showId']}'").to_a
        results_html += "<p>#{row['showName']} <img src='#{row['imageName']}' alt='#{row['showName']}' style='height: 50px; width: 35px; object-fit: cover;'>"
        results_html += "<button class='addToList btn btn-success' data-series-id='#{row['showId']}' data-series-name='#{row['showName']}'>ADD</button>"
        results_html += "<select class='seasonSelect' data-series-id='#{row['showId']}'>"
        seasons.each_with_index do |season, index|
          results_html += "<option value='#{season['seasonId']}'>Season #{index + 1}</option>"
        end
        results_html += "</select></p>"
      end
    else
      results_html += "<p>We can't seem to find this title!</p>"
    end
  elsif type == "Episode"
    results = db.query("SELECT showName, imageName, showId FROM series WHERE showName LIKE '#{db.escape(search)}%'")
    if results.count > 0
      results.each do |row|
        seasons = db.query("SELECT seasonId FROM season WHERE seriesId = '#{row['showId']}'").to_a
        results_html += "<p>#{row['showName']} <img src='#{row['imageName']}' alt='#{row['showName']}' style='height: 50px; width: 35px; object-fit: cover;'>"
        results_html += "<select class='seasonSelect' data-series-id='#{row['showId']}'>"
        seasons.each_with_index do |season, index|
          results_html += "<option value='#{season['seasonId']}'>Season #{index + 1}</option>"
        end
        results_html += "</select>"
        results_html += "<div id='episodeSelect'></div>"
        results_html += "</p>"
      end
    else
      results_html += "<p>We can't seem to find this title!</p>"
    end
  end

  # Output only the results, not the full page
  print results_html
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
      ep_id = episode["epId"].to_i
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
puts "          <input type='hidden' id='episodeArrayInput' name='episodeArray'>"
puts "          <button id='saveList' name='saveList' class='btn btn-primary'>CREATE LIST</button>"
puts "        </form>"
puts "      </div>"

puts "      <div class='col-12 col-md-4' id='searchColumn'>"
puts "        <h3 class='text-center'>Search</h3>"
puts "        <form id='searchForm'>"
puts "          <input type='text' name='mediaEntered' class='form-control' placeholder='Search for series, season, or episode' required><br>"
puts "          <select name='typeSearch' class='form-control'>"
puts "            <option value='Series'>Series</option>"
puts "            <option value='Season'>Season</option>"
puts "            <option value='Episode'>Episode</option>"
puts "          </select><br>"
puts "          <button type='submit' class='btn btn-primary'>Search</button>"
puts "        </form>"
puts "        <div id='searchResults' class='mt-3'></div>"  # This section is now below the search button
puts "      </div>"

puts "    </div>"
puts "  </div>"

puts "  <script>"
puts "    document.addEventListener('DOMContentLoaded', function () {"
puts "      sessionStorage.removeItem('seriesArray');"
puts "      sessionStorage.removeItem('seasonArray');"
puts "      sessionStorage.removeItem('episodeArray');"
puts "      updateAllLists();"
puts "      $('#searchForm').submit(function(event) {"
puts "        event.preventDefault();"
puts "        var search = $('input[name=mediaEntered]').val();"
puts "        var type = $('select[name=typeSearch]').val();"
puts "        $.ajax({"
puts "          type: 'GET',"
puts "          url: '/path/to/your/cgi/script.cgi',"
puts "          data: { mediaEntered: search, typeSearch: type },"
puts "          success: function(response) {"
puts "            $('#searchResults').html(response);"
puts "          },"
puts "          error: function(xhr, status, error) {"
puts "            console.log('Error: ' + error);"
puts "          }"
puts "        });"
puts "      });"
puts "    });"
puts "  </script>"
puts "</body>"
puts "</html>"
session.close
