#!/usr/bin/ruby
$stdout.sync = true
require 'cgi'
require 'cgi/session'
require 'mysql2'
require 'json'

cgi = CGI.new

# Start session handling
begin
  session = CGI::Session.new(cgi)
  username = session['username']
rescue => e
  puts "Content-Type: text/html\n\n"
  puts "<p>Session error: #{e.message}</p>"
  exit
end

# Output the required CGI header
def print_header
  puts "Content-Type: text/html\n\n"
end

# Handle database connection
begin
  db = Mysql2::Client.new(
    host: '10.20.3.4',
    username: 'seniorproject25',
    password: 'TV_Group123!',
    database: 'televised_w25'
  )
rescue Mysql2::Error => e
  print_header
  puts "<p>Database connection failed: #{e.message}</p>"
  exit
end

# Retrieve form input
search = cgi['mediaEntered'].to_s.strip
type = cgi['typeSearch'].to_s.strip
listName = cgi['listName'].to_s.strip
description = cgi['description'].to_s.strip
privacy = (cgi['views'] == "Public" ? 1 : 0)

# Parse series array safely
begin
  seriesArray = cgi['seriesArray'].empty? ? [] : JSON.parse(cgi['seriesArray'])
rescue JSON::ParserError
  seriesArray = []
end

# **AJAX Search Handling**
if type == "Series" && !search.empty?
  print_header
  results = db.query("SELECT showName, imageName, showId FROM series WHERE showName LIKE '#{db.escape(search)}%' LIMIT 10")

  if results.count > 0
    results.each do |row|
      puts "<div class='search-result'>"
      puts "  <p>#{row['showName']} <img src='#{row['imageName']}' alt='#{row['showName']}' style='height: 50px; width: 35px; object-fit: cover;'>"
      puts "  <button class='addToList btn btn-success' data-series-id='#{row['showId']}' data-series-name='#{row['showName']}'>ADD</button></p>"
      puts "</div>"
    end
  else
    puts "<p>No results found.</p>"
  end
  exit
end

# **List Creation**
if cgi['saveList'] && !listName.empty? && !description.empty? && !seriesArray.empty?
  existing_list = db.query("SELECT id FROM listOwnership WHERE username = '#{username}' AND listName = '#{db.escape(listName)}'")

  if existing_list.count > 0
    print_header
    puts "<script>alert('Sorry, but you already have a list with this name. Try a different name.');</script>"
    exit
  end

  db.query("INSERT INTO listOwnership (username, listName) VALUES ('#{username}', '#{db.escape(listName)}')")
  list_id = db.last_id

  seriesArray.each do |series|
    series_id = series["id"]
    db.query("INSERT INTO curatedListSeries (username, seriesId, name, description, privacy, date, listId)
              VALUES ('#{username}', '#{series_id}', '#{db.escape(listName)}', '#{db.escape(description)}', '#{privacy}', NOW(), '#{list_id}')")
  end

  print_header
  puts "<script>alert('Your list has been successfully created!'); window.location.href = 'Profile_List.cgi';</script>"
  exit
end

# **HTML Output**
print_header
puts "<!DOCTYPE html>"
puts "<html lang='en'>"
puts "<head>"
puts "  <meta charset='UTF-8'>"
puts "  <meta name='viewport' content='width=device-width, initial-scale=1.0'>"
puts "  <title>Televised</title>"
puts "  <link href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css' rel='stylesheet'>"
puts "  <link rel='stylesheet' href='Televised.css'>"
puts "</head>"
puts "<body id='createNewList'>"
puts "  <nav id='changingNav'></nav>"
puts "  <h2 class='text-center mt-3'>Create a New List</h2>"
puts "  <div class='container-fluid'>"
puts "    <div class='row'>"
puts "      <div class='col' id='listRow'>"
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
puts "          <button id='saveList' class='btn btn-primary'>CREATE LIST</button>"
puts "        </form>"
puts "      </div>"
puts "      <div class='col' id='listColumn'>"
puts "        <h3 class='text-center'>Selected Series</h3>"
puts "        <ul id='seriesList' class='list-group'></ul>"
puts "      </div>"
puts "      <div class='col' id='searchColumn'>"
puts "        <h3 class='text-center'>Search for a Series</h3>"
puts "        <form id='searchForm'>"
puts "          <input type='text' name='mediaEntered' class='form-control'>"
puts "          <input type='submit' value='Search' class='btn btn-secondary mt-2'>"
puts "        </form>"
puts "        <div id='searchResults'></div>"
puts "      </div>"
puts "    </div>"
puts "  </div>"
puts "  <script src='https://code.jquery.com/jquery-3.6.0.min.js'></script>"
puts "  <script>"
puts "    let seriesArray = [];"

puts "    $(document).on('click', '.addToList', function() {"
puts "      let seriesId = $(this).data('series-id');"
puts "      let seriesName = $(this).data('series-name');"

puts "      if (!seriesArray.some(series => series.id == seriesId)) {"
puts "        seriesArray.push({ id: seriesId, name: seriesName });"
puts "        $('#seriesList').append(`<li class='list-group-item'>${seriesName} <button class='removeFromList btn btn-danger btn-sm' data-series-id='${seriesId}'>REMOVE</button></li>`);"
puts "        console.log('Updated seriesArray:', seriesArray);"
puts "      }"
puts "    });"

puts "    $(document).on('click', '.removeFromList', function() {"
puts "      let seriesId = $(this).data('series-id');"
puts "      seriesArray = seriesArray.filter(series => series.id != seriesId);"
puts "      $(this).parent().remove();"
puts "      console.log('Updated seriesArray:', seriesArray);"
puts "    });"

puts "  </script>"
puts "</body>"
puts "</html>"

session.close
