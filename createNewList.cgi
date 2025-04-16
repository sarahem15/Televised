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

list_id = cgi['list_id'] # Get the list ID if we are editing an existing list

# Check if we're editing an existing list
if list_id
  # Fetch existing list details
  list_details = db.query("SELECT * FROM listOwnership WHERE id = #{list_id} AND username = '#{username}'").first
  if list_details
    listName = list_details["listName"]
    description = list_details["description"]
    privacy = list_details["privacy"] == 1 ? "Public" : "Private"

    # Fetch existing series for the list
    seriesArray = db.query("SELECT seriesId, name FROM curatedListSeries WHERE listId = #{list_id} AND username = '#{username}'").map do |row|
      { "id" => row["seriesId"], "name" => row["name"] }
    end

    # Fetch existing seasons for the list
    seasonArray = db.query("SELECT seasonId, seriesId, name, season FROM curatedListSeason WHERE listId = #{list_id} AND username = '#{username}'").map do |row|
      { "seriesId" => row["seriesId"], "name" => row["name"], "season" => row["season"] }
    end
  end
end

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

# Handle list creation or updating
if cgi['saveList'] && !listName.empty? && !description.empty?
  if list_id # Updating an existing list
    db.query("UPDATE listOwnership SET listName = '#{db.escape(listName)}', description = '#{db.escape(description)}', privacy = #{privacy} WHERE id = #{list_id}")
  else # Creating a new list
    existing_list = db.query("SELECT id FROM listOwnership WHERE username = '#{username}' AND listName = '#{db.escape(listName)}'")
    if existing_list.count > 0
      puts "<script>alert('Sorry, but you already have a list with this name. Try a different name.');</script>"
      exit
    end
    db.query("INSERT INTO listOwnership (username, listName) VALUES ('#{username}', '#{db.escape(listName)}')")
    list_id = db.last_id
  end

  # Clear existing series and seasons before adding new ones
  db.query("DELETE FROM curatedListSeries WHERE listId = #{list_id} AND username = '#{username}'")
  db.query("DELETE FROM curatedListSeason WHERE listId = #{list_id} AND username = '#{username}'")

  # Insert new series
  if !seriesArray.empty?
    seriesArray.each do |series|
      series_id = series["id"].to_i
      db.query("INSERT INTO curatedListSeries (username, seriesId, name, description, privacy, date, listId)
                VALUES ('#{username}', #{series_id}, '#{db.escape(listName)}', '#{db.escape(description)}', #{privacy}, NOW(), #{list_id})")
    end
  end

  # Insert new seasons
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

  puts "<script>alert('Your list has been successfully #{list_id ? 'updated' : 'created'}!'); window.location.href = 'Profile_Lists.cgi';</script>"
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
puts "  <h2 class='text-center mt-3'>#{list_id ? 'Edit List' : 'Create a New List'}</h2>"
puts "  <div class='container-fluid'>"
puts "    <div class='row'>"
puts "      <div class='col-12 col-md-4' id='listRow'>"
puts "        <h3 class='text-center'>List Details</h3>"
puts "        <form id='newListForm' method='post'>"
puts "          <label>Name</label>"
puts "          <input type='text' name='listName' class='form-control' placeholder='Name' required value='#{listName}'>"
puts "          <br>"
puts "          <label>Who Can View</label>"
puts "          <select name='views' class='form-control'>"
puts "            <option value='Public' #{'selected' if privacy == 'Public'}>Public - anyone can view</option>"
puts "            <option value='Private' #{'selected' if privacy == 'Private'}>Private - no one can view</option>"
puts "          </select>"
puts "          <br>"
puts "          <label>Description</label>"
puts "          <textarea name='description' class='form-control' rows='5'>#{description}</textarea>"
puts "          <br>"
puts "          <input type='hidden' id='seriesArrayInput' name='seriesArray'>"
puts "          <input type='hidden' id='seasonArrayInput' name='seasonArray'>"
puts "          <button id='saveList' name='saveList' class='btn btn-primary'>#{list_id ? 'Update List' : 'Create List'}</button>"
puts "        </form>"
puts "      </div>"
puts "      <div class='col-12 col-md-4' id='listColumn'>"
puts "        <h3 class='text-center'>Selected Series/Seasons</h3>"
puts "        <form id='searchForm' class='mb-3'>"
puts "          <input type='text' name='mediaEntered' class='form-control' placeholder='Search for Series' required>"
puts "          <select name='typeSearch' class='form-control mt-2'>"
puts "            <option value='Series'>Series</option>"
puts "            <option value='Season'>Season</option>"
puts "          </select>"
puts "          <button type='submit' class='btn btn-primary mt-2'>Search</button>"
puts "        </form>"
puts "        <div id='searchResults'></div>"
puts "        <ul id='seriesList' class='list-group'></ul>"
puts "      </div>"
puts "    </div>"
puts "  </div>"
puts "<script src='Televised.js'></script>"
puts "</body>"
puts "</html>"

# Close the session when done
session.close
