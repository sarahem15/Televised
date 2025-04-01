#!/usr/bin/env ruby
$stdout.sync = true
$stderr.reopen($stdout)

require 'mysql2'
require 'cgi'
require 'cgi/session'
require 'json'

cgi = CGI.new
begin
  session = CGI::Session.new(cgi)
  username = session['username'] || ''
rescue => e
  puts "Content-Type: text/html\n\n"
  puts "<p>Session error: #{e.message}</p>"
  exit
end

# Ensure CGI header is only printed when needed
def print_header
  puts "Content-Type: text/html\n\n"
end

# Parse `seriesArray` safely
begin
  seriesArray = cgi['seriesArray'] && !cgi['seriesArray'].empty? ? JSON.parse(cgi['seriesArray']) : []
rescue JSON::ParserError
  seriesArray = []
end

# Console debug message (visible in logs)
puts "<script>console.log('Series Array:', #{seriesArray.to_json});</script>"

# Database connection with error handling
begin
  db = Mysql2::Client.new(
    host: '10.20.3.4', 
    username: 'seniorproject25', 
    password: 'TV_Group123!', 
    database: 'televised_w25'
  )
rescue Mysql2::Error => e
  print_header
  puts "<p>Database Connection Failed: #{e.message}</p>"
  exit
end

search = cgi['mediaEntered'] || ''
type = cgi['typeSearch'] || ''
listName = cgi['listName'] || ''
description = cgi['description'] || ''
privacy = cgi['views'] == "Public" ? 1 : 0  

# **AJAX Search Functionality**
if type == "Series" && !search.strip.empty?
  print_header  # Ensure proper CGI header for AJAX response
  
  results = db.query("SELECT showName, imageName, showId FROM series WHERE showName LIKE '#{db.escape(search)}%'")
  
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
  exit  # Stop further execution for AJAX requests
end

# **Handle list creation**
if cgi['saveList'] && !listName.strip.empty? && !description.strip.empty? && !seriesArray.empty?
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

# **Start HTML Output**
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
puts "          <select id='type' name='typeSearch' class='form-control'>"
puts "            <option value='Series' selected>Series</option>"
puts "          </select>"
puts "          <br>"
puts "          <input type='text' name='mediaEntered' class='form-control'>"
puts "          <input type='submit' value='Search' class='btn btn-secondary mt-2'>"
puts "        </form>"
puts "        <div id='searchResults'></div>"
puts "      </div>"
puts "    </div>"
puts "  </div>"
puts "  <script src='https://code.jquery.com/jquery-3.6.0.min.js'></script>"
puts "  <script src='https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js'></script>"
puts "  <script src='Televised.js'></script>"
puts "  <script>"
puts "    document.addEventListener('DOMContentLoaded', function () {"
puts "      document.getElementById('searchForm').addEventListener('submit', function (event) {"
puts "        event.preventDefault();"
puts "        let searchInput = document.querySelector('input[name=\"mediaEntered\"]').value;"
puts "        let type = document.querySelector('select[name=\"typeSearch\"]').value;"
puts "        fetch('createNewList.cgi?mediaEntered=' + encodeURIComponent(searchInput) + '&typeSearch=' + encodeURIComponent(type), {"
puts "          method: 'GET',"
puts "        })"
puts "        .then(response => response.text())"
puts "        .then(data => {"
puts "          document.getElementById('searchResults').innerHTML = data;"
puts "        });"
puts "      });"
puts "    });"
puts "  </script>"
puts "</body>"
puts "</html>"

session.close
