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

db = Mysql2::Client.new(
  host: '10.20.3.4',
  username: 'seniorproject25',
  password: 'TV_Group123!',
  database: 'televised_w25'
)

# Handle list deletion via edit
if cgi['editList']
  list_name = cgi['editList']
  list_data = {
    listName: list_name,
    description: "",
    views: "Public",
    seriesArray: [],
    seasonArray: []
  }

  # Get list metadata
  description_result = db.query("SELECT description, privacy FROM curatedListSeries WHERE username = '#{username}' AND name = '#{db.escape(list_name)}' LIMIT 1")
  if description_result.count > 0
    row = description_result.first
    list_data[:description] = row["description"]
    list_data[:views] = row["privacy"] == 1 ? "Public" : "Private"
  else
    season_result = db.query("SELECT description, privacy FROM curatedListSeason WHERE username = '#{username}' AND name = '#{db.escape(list_name)}' LIMIT 1")
    if season_result.count > 0
      row = season_result.first
      list_data[:description] = row["description"]
      list_data[:views] = row["privacy"] == 1 ? "Public" : "Private"
    end
  end

  # Fetch series
  series = db.query("SELECT seriesId, name FROM curatedListSeries WHERE username = '#{username}' AND name = '#{db.escape(list_name)}'")
  series.each do |row|
    list_data[:seriesArray] << { id: row["seriesId"].to_s, name: row["name"] }
  end

  # Fetch seasons
  seasons = db.query("SELECT seasonId, name FROM curatedListSeason WHERE username = '#{username}' AND name = '#{db.escape(list_name)}'")
  seasons.each do |row|
    # Convert seasonId to season number
    season_row = db.query("SELECT seriesId FROM season WHERE seasonId = #{row["seasonId"]}").first
    if season_row
      series_id = season_row["seriesId"]
      all_seasons = db.query("SELECT seasonId FROM season WHERE seriesId = #{series_id} ORDER BY seasonId ASC").to_a
      index = all_seasons.find_index { |s| s["seasonId"] == row["seasonId"] }
      season_number = index ? index + 1 : 1
      list_data[:seasonArray] << { seriesId: series_id.to_s, name: row["name"], season: season_number }
    end
  end

  # Delete from DB
  db.query("DELETE FROM curatedListSeries WHERE username = '#{username}' AND name = '#{db.escape(list_name)}'")
  db.query("DELETE FROM curatedListSeason WHERE username = '#{username}' AND name = '#{db.escape(list_name)}'")
  db.query("DELETE FROM listOwnership WHERE username = '#{username}' AND listName = '#{db.escape(list_name)}'")

  # Output JS to set sessionStorage and redirect
  puts "<script>"
  puts "sessionStorage.setItem('listEditData', #{list_data.to_json});"
  puts "window.location.href = 'createNewList.cgi';"
  puts "</script>"
  exit
end

# HTML output (simplified to keep focused)
puts "<!DOCTYPE html>"
puts "<html><head><title>Your Lists</title></head><body>"
puts "<h2>Welcome, #{username}</h2>"

user_lists = db.query("SELECT listName FROM listOwnership WHERE username = '#{username}'")
user_lists.each do |row|
  puts "<div class='listItem'>"
  puts "<h3>#{row['listName']}</h3>"
  puts "<form method='post'>"
  puts "<input type='hidden' name='editList' value='#{row['listName']}'>"
  puts "<button class='btn btn-warning'>Edit</button>"
  puts "</form>"
  puts "</div>"
end

puts "</body></html>"

session.close
