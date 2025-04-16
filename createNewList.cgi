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
list_id = cgi['listId']&.to_i

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

# AJAX Search
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

# Handle saving (new or update)
if cgi['saveList'] && !listName.empty? && !description.empty?
  if list_id
    # Updating existing list
    db.query("UPDATE listOwnership SET listName = '#{db.escape(listName)}' WHERE id = #{list_id} AND username = '#{username}'")
    db.query("DELETE FROM curatedListSeries WHERE listId = #{list_id}")
    db.query("DELETE FROM curatedListSeason WHERE listId = #{list_id}")
  else
    # Creating new list
    existing_list = db.query("SELECT id FROM listOwnership WHERE username = '#{username}' AND listName = '#{db.escape(listName)}'")
    if existing_list.count > 0
      puts "<script>alert('Sorry, but you already have a list with this name. Try a different name.');</script>"
      exit
    end
    db.query("INSERT INTO listOwnership (username, listName) VALUES ('#{username}', '#{db.escape(listName)}')")
    list_id = db.last_id
  end

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

  if seriesArray.empty? && seasonArray.empty?
    puts "<script>alert('Please select at least one series or season before saving.');</script>"
    exit
  end

  puts "<script>alert('Your list has been successfully #{cgi['listId'] ? 'updated' : 'created'}!'); window.location.href = 'Profile_Lists.cgi';</script>"
  exit
end

# If editing, load current data
list_data = {}
series_json = []
season_json = []

if list_id
  result = db.query("SELECT listName, username FROM listOwnership WHERE id = #{list_id}")
  if row = result.first
    redirect_script = "<script>alert('Unauthorized access.'); window.location.href='Profile_Lists.cgi';</script>"
    if row["username"] != username
      puts redirect_script
      exit
    end

    list_data = row
    desc_result = db.query("SELECT description, privacy FROM curatedListSeries WHERE listId = #{list_id} LIMIT 1")
    desc_result = db.query("SELECT description, privacy FROM curatedListSeason WHERE listId = #{list_id} LIMIT 1") if desc_result.count == 0
    if meta = desc_result.first
      list_data['description'] = meta["description"]
      list_data['privacy'] = meta["privacy"]
    end

    series_results = db.query("SELECT seriesId, name FROM curatedListSeries WHERE listId = #{list_id}")
    series_results.each do |s|
      series_json << { id: s["seriesId"], name: s["name"] }
    end

    season_results = db.query("SELECT s.seriesId, sl.name, se.seasonId
                               FROM curatedListSeason sl
                               JOIN season se ON sl.seasonId = se.seasonId
                               JOIN series s ON s.showId = se.seriesId
                               WHERE sl.listId = #{list_id}")
    season_results.each do |s|
      season_json << { seriesId: s["seriesId"], name: s["name"], season: season_json.count { |x| x[:seriesId] == s["seriesId"] } + 1 }
    end
  end
end

# START HTML
puts "<!DOCTYPE html>"
puts "<html lang='en'>"
puts "<head>"
puts "  <meta charset='UTF-8'>"
puts "  <meta name='viewport' content='width=device-width, initial-scale=1.0'>"
puts "  <title>#{list_id ? 'Edit List' : 'Create a New List'}</title>"
puts "  <link href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css' rel='stylesheet'>"
puts "  <link rel='stylesheet' href='Televised.css'>"
puts "  <script src='https://code.jquery.com/jquery-3.6.0.min.js'></script>"
puts "</head>"
puts "<body id='createNewList'>"
puts "  <nav id='changingNav'></nav>"
puts "  <h2 class='text-center mt-3'>#{list_id ? 'Edit Your List' : 'Create a New List'}</h2>"
puts "  <div class='container-fluid'>"
puts "    <div class='row'>"
puts "      <div class='col-12 col-md-4' id='listRow'>"
puts "        <h3 class='text-center'>List Details</h3>"
puts "        <form id='newListForm' method='post'>"
puts "          <input type='hidden' name='listId' value='#{list_id if list_id}'>"
puts "          <label>Name</label>"
puts "          <input type='text' name='listName' class='form-control' value='#{CGI.escapeHTML(list_data['listName'] || '')}' required>"
puts "          <br>"
puts "          <label>Who Can View</label>"
puts "          <select name='views' class='form-control'>"
puts "            <option value='Public' #{list_data['privacy'] == 1 ? 'selected' : ''}>Public</option>"
puts "            <option value='Private' #{list_data['privacy'] == 0 ? 'selected' : ''}>Private</option>"
puts "          </select>"
puts "          <br>"
puts "          <label>Description</label>"
puts "          <textarea name='description' class='form-control' rows='5'>#{CGI.escapeHTML(list_data['description'] || '')}</textarea>"
puts "          <br>"
puts "          <input type='hidden' id='seriesArrayInput' name='seriesArray'>"
puts "          <input type='hidden' id='seasonArrayInput' name='seasonArray'>"
puts "          <button id='saveList' name='saveList' class='btn btn-primary'>#{list_id ? 'SAVE CHANGES' : 'CREATE LIST'}</button>"
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
puts "<script>"
puts "  const prefillSeries = #{series_json.to_json};"
puts "  const prefillSeason = #{season_json.to_json};"
puts "</script>"
puts "<script>"
puts <<~JS
document.addEventListener('DOMContentLoaded', () => {
  if (prefillSeries.length > 0) sessionStorage.setItem("seriesArray", JSON.stringify(prefillSeries));
  if (prefillSeason.length > 0) sessionStorage.setItem("seasonArray", JSON.stringify(prefillSeason));
  updateAllLists();
});
JS
puts "</script>"
puts "<script src='Televised.js'></script>"
puts "<script src='https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js'></script>"
puts "</body>"
puts "</html>"

session.close
