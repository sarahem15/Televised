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

# Get the listId if editing
list_id = cgi['listId']
is_editing = !list_id.empty?

# Initialize variables for the form
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

# Database connection
db = Mysql2::Client.new(
  host: '10.20.3.4', 
  username: 'seniorproject25', 
  password: 'TV_Group123!', 
  database: 'televised_w25'
)

# Handle AJAX search functionality (no changes here)
# ... (same code for search functionality)

# Handle list creation or updating
if cgi['saveList'] && !listName.empty? && !description.empty?
  if is_editing
    # Update existing list if editing
    db.query("UPDATE listOwnership SET listName = '#{db.escape(listName)}', description = '#{db.escape(description)}', privacy = #{privacy} WHERE id = #{list_id} AND username = '#{username}'")

    # Remove old entries from curatedListSeries and curatedListSeason for this list
    db.query("DELETE FROM curatedListSeries WHERE listId = #{list_id}")
    db.query("DELETE FROM curatedListSeason WHERE listId = #{list_id}")

    # Insert updated series and season data
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

    puts "<script>alert('Your list has been successfully updated!'); window.location.href = 'Profile_Lists.cgi';</script>"
    exit
  else
    # Check if a list with the same name already exists
    existing_list = db.query("SELECT id FROM listOwnership WHERE username = '#{username}' AND listName = '#{db.escape(listName)}'")

    if existing_list.count > 0
      puts "<script>alert('Sorry, but you already have a list with this name. Try a different name.');</script>"
      exit
    end

    # Create a new list if no existing list with that name
    db.query("INSERT INTO listOwnership (username, listName) VALUES ('#{username}', '#{db.escape(listName)}')")
    list_id = db.last_id

    # Insert new series and season data
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

    puts "<script>alert('Your list has been successfully created!'); window.location.href = 'Profile_Lists.cgi';</script>"
    exit
  end
end

# Handle list loading for editing
if is_editing
  list_details = db.query("SELECT listName, description, privacy FROM listOwnership WHERE id = #{list_id} AND username = '#{username}'").first
  if list_details
    listName = list_details["listName"]
    description = list_details["description"]
    privacy = list_details["privacy"] == 1 ? "Public" : "Private"

    # Load series and season data for this list
    seriesArray = db.query("SELECT seriesId, name FROM curatedListSeries WHERE listId = #{list_id}").map { |row| { "id" => row["seriesId"], "name" => row["name"] } }
    seasonArray = db.query("SELECT seasonId, name, seriesId FROM curatedListSeason WHERE listId = #{list_id}").map { |row| { "seriesId" => row["seriesId"], "name" => row["name"], "season" => row["seasonId"] } }
  else
    puts "<script>alert('List not found or you do not have permission to edit it.'); window.location.href = 'Profile_Lists.cgi';</script>"
    exit
  end
end

# Start HTML output (keep your original HTML structure intact)
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
puts "          <input type='hidden' id='seriesArrayInput' name='seriesArray'>"
puts "          <input type='hidden' id='seasonArrayInput' name='seasonArray'>"
puts "          <button id='saveList' name='saveList' class='btn btn-primary'>#{is_editing ? 'Update List' : 'Create List'}</button>"
puts "        </form>"
puts "      </div>"
puts "    </div>"
puts "  </div>"
puts "</body>"
puts "</html>"
