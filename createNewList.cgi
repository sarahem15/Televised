#not filling in the list items for edit. Need to create fake episode list table for each of our accounts. When user presses edit on p_l then this needs to populate. 

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
  db = Mysql2::Client.new(
    host: '10.20.3.4', 
    username: 'seniorproject25', 
    password: 'TV_Group123!', 
    database: 'televised_w25'
  )
rescue Mysql2::Error => e
  puts "Content-type: text/html\n\n"
  puts "<h1>Error Connecting to Database</h1>"
  puts "<p>MySQL Error: #{e.message}</p>"
  exit
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

# Fetch the list data to edit (if we have a listId)
list_id = cgi['listId']
if list_id && !list_id.empty?
  begin
    list_details = db.query("SELECT * FROM listOwnership WHERE id = #{db.escape(list_id)} AND username = '#{username}'").first
    if list_details
      listName = list_details['listName']
      description = list_details['description']
      privacy = list_details['privacy'] == 1 ? "Public" : "Private"
      
      # Fetch the series and season items associated with this list
      series_array = db.query("SELECT seriesId FROM curatedListSeries WHERE listId = #{db.escape(list_id)}").to_a
      season_array = db.query("SELECT seasonId FROM curatedListSeason WHERE listId = #{db.escape(list_id)}").to_a

      # Construct arrays for series and season IDs for pre-filling
      seriesArray = series_array.map { |row| { "id" => row['seriesId'] } }
      seasonArray = season_array.map { |row| { "seasonId" => row['seasonId'] } }
    else
      puts "<script>alert('List not found.'); window.location.href = 'Profile_Lists.cgi';</script>"
      exit
    end
  rescue Mysql2::Error => e
    puts "Content-type: text/html\n\n"
    puts "<h1>Error Fetching List Details</h1>"
    puts "<p>MySQL Error: #{e.message}</p>"
    exit
  end
end

# Handle list creation or updating
if cgi['saveList'] && !listName.empty? && !description.empty?
  begin
    if list_id.empty?
      # New list creation
      db.query("INSERT INTO listOwnership (username, listName) VALUES ('#{username}', '#{db.escape(listName)}')")
      list_id = db.last_id
    else
      # Update existing list
      db.query("UPDATE listOwnership SET listName = '#{db.escape(listName)}', description = '#{db.escape(description)}', privacy = #{privacy} WHERE id = #{db.escape(list_id)} AND username = '#{username}'")
    end

    # Update series and season associations
    db.query("DELETE FROM curatedListSeries WHERE listId = #{db.escape(list_id)}")
    seriesArray.each do |series|
      series_id = series["id"].to_i
      db.query("INSERT INTO curatedListSeries (username, seriesId, name, description, privacy, date, listId)
                VALUES ('#{username}', #{series_id}, '#{db.escape(listName)}', '#{db.escape(description)}', #{privacy}, NOW(), #{list_id})")
    end

    db.query("DELETE FROM curatedListSeason WHERE listId = #{db.escape(list_id)}")
    seasonArray.each do |season|
      season_id = season["seasonId"].to_i
      db.query("INSERT INTO curatedListSeason (username, seasonId, name, description, privacy, date, listId)
                VALUES ('#{username}', #{season_id}, '#{db.escape(listName)}', '#{db.escape(description)}', #{privacy}, NOW(), #{list_id})")
    end

    puts "<script>alert('Your list has been successfully saved/updated!'); window.location.href = 'Profile_Lists.cgi';</script>"
    exit

  rescue Mysql2::Error => e
    puts "Content-type: text/html\n\n"
    puts "<h1>Error Saving List</h1>"
    puts "<p>MySQL Error: #{e.message}</p>"
    exit
  end
end

# Start HTML output
puts "Content-type: text/html\n\n"
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
puts "  <h2 class='text-center mt-3'>Create or Edit List</h2>"
puts "  <div class='container-fluid'>"
puts "    <div class='row'>"
puts "      <div class='col-12 col-md-4' id='listRow'>"
puts "        <h3 class='text-center'>List Details</h3>"
puts "        <form id='newListForm' method='post'>"
puts "          <label>Name</label>"
puts "          <input type='text' name='listName' class='form-control' placeholder='Name' value='#{listName}' required>"
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
puts "          <input type='hidden' id='seriesArrayInput' name='seriesArray' value='#{seriesArray.to_json}'>"
puts "          <input type='hidden' id='seasonArrayInput' name='seasonArray' value='#{seasonArray.to_json}'>"
puts "          <button id='saveList' name='saveList' class='btn btn-primary'>SAVE LIST</button>"
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
puts '<script src="Televised.js"></script>'
puts "</body>"
puts "</html>"

session.close
