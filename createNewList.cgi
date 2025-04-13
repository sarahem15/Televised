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

# Fetch existing list details
begin
  list_details = db.query("SELECT * FROM listOwnership WHERE id = #{list_id} AND username = '#{username}'").first
  if list_details.nil?
    puts "<script>alert('List not found or you do not have permission to edit it.'); window.location.href = 'Profile_Lists.cgi';</script>"
    exit
  end
rescue Mysql2::Error => e
  puts "Content-type: text/html\n\n"
  puts "<h1>Error Fetching List Details</h1>"
  puts "<p>MySQL Error: #{e.message}</p>"
  exit
end

# Fetch selected series and seasons for this list
begin
  selected_series = db.query("SELECT * FROM curatedListSeries WHERE listId = #{list_id}").to_a
  selected_seasons = db.query("SELECT * FROM curatedListSeason WHERE listId = #{list_id}").to_a
rescue Mysql2::Error => e
  puts "Content-type: text/html\n\n"
  puts "<h1>Error Fetching Selected Series and Seasons</h1>"
  puts "<p>MySQL Error: #{e.message}</p>"
  exit
end

# Start HTML output for editing the list
puts "Content-type: text/html\n\n"
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

# Handle form submission and saving data
if cgi['saveList'] && !cgi['listName'].empty? && !cgi['description'].empty?
  privacy = cgi['views'] == 'Public' ? 1 : 0

  begin
    # Update the list details
    db.query("UPDATE listOwnership SET listName = '#{db.escape(cgi['listName'])}', description = '#{db.escape(cgi['description'])}', privacy = #{privacy} WHERE id = #{list_id}")

    # Delete old series and seasons
    db.query("DELETE FROM curatedListSeries WHERE listId = #{list_id}")
    db.query("DELETE FROM curatedListSeason WHERE listId = #{list_id}")

    # Insert new series and seasons
    seriesArray = JSON.parse(cgi['seriesArray'])
    seasonArray = JSON.parse(cgi['seasonArray'])

    seriesArray.each do |series|
      db.query("INSERT INTO curatedListSeries (username, seriesId, name, description, privacy, date, listId)
                VALUES ('#{username}', #{series['id']}, '#{db.escape(cgi['listName'])}', '#{db.escape(cgi['description'])}', #{privacy}, NOW(), #{list_id})")
    end

    seasonArray.each do |season|
      db.query("INSERT INTO curatedListSeason (username, seasonId, name, description, privacy, date, listId)
                VALUES ('#{username}', #{season['seasonId']}, '#{db.escape(cgi['listName'])}', '#{db.escape(cgi['description'])}', #{privacy}, NOW(), #{list_id})")
    end

    puts "<script>alert('Your list has been successfully updated!'); window.location.href = 'Profile_Lists.cgi';</script>"
  rescue Mysql2::Error => e
    puts "Content-type: text/html\n\n"
    puts "<h1>Error Updating List</h1>"
    puts "<p>MySQL Error: #{e.message}</p>"
  end

  exit
end

session.close
