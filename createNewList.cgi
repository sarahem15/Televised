#!/usr/bin/env ruby
require 'cgi'
require 'mysql2'
require 'date'

cgi = CGI.new
search = cgi['mediaEntered']
type = cgi['typeSearch']

def db_client
  Mysql2::Client.new(
    host: "localhost",
    username: "root",
    password: "yourpassword",
    database: "yourdatabase"
  )
end

def search_series(client, query)
  results = client.query("SELECT * FROM series WHERE showName LIKE '%#{client.escape(query)}%'")
  results.map do |row|
    <<~HTML
      <div class="search-result">
        <img src="/images/#{row['imageName']}" alt="#{row['showName']}" style="height:100px;">
        <p>#{row['showName']}</p>
        <button onclick="addSeries('#{row['showId']}', '#{row['showName']}')">Add</button>
      </div>
    HTML
  end.join
end

def search_season(client, query)
  results = client.query("SELECT s.showName, s.imageName, s.showId, se.seasonNum, se.seasonId 
                          FROM series s 
                          JOIN season se ON s.showId = se.seriesId 
                          WHERE s.showName LIKE '%#{client.escape(query)}%' 
                          GROUP BY s.showId")
  results.map do |row|
    season_options = client.query("SELECT seasonNum FROM season WHERE seriesId = #{row['showId']} ORDER BY seasonNum ASC").map do |s|
      "<option value='#{s['seasonNum']}'>Season #{s['seasonNum']}</option>"
    end.join

    <<~HTML
      <div class="search-result">
        <img src="/images/#{row['imageName']}" alt="#{row['showName']}" style="height:100px;">
        <p>#{row['showName']}</p>
        <select onchange="updateSelectedSeason(this)">
          #{season_options}
        </select>
        <button onclick="addSeason('#{row['showId']}', '#{row['showName']}', this.previousElementSibling.value)">Add</button>
      </div>
    HTML
  end.join
end

def search_episode(client, query)
  results = client.query("SELECT DISTINCT s.showName, s.imageName, s.showId 
                          FROM series s 
                          JOIN season se ON s.showId = se.seriesId 
                          JOIN episode e ON se.seasonId = e.seasonId 
                          WHERE s.showName LIKE '%#{client.escape(query)}%'")
  results.map do |row|
    season_options = client.query("SELECT seasonNum, seasonId FROM season WHERE seriesId = #{row['showId']} ORDER BY seasonNum ASC").map do |s|
      "<option value='#{s['seasonId']},#{s['seasonNum']}'>Season #{s['seasonNum']}</option>"
    end.join

    <<~HTML
      <div class="search-result">
        <img src="/images/#{row['imageName']}" alt="#{row['showName']}" style="height:100px;">
        <p>#{row['showName']}</p>
        <select onchange="loadEpisodes(this, #{row['showId']})">
          #{season_options}
        </select>
        <select class="episodeDropdown"></select>
        <button onclick="addEpisode('#{row['showId']}', '#{row['showName']}', this.previousElementSibling.value)">Add</button>
      </div>
    HTML
  end.join
end

# Return only search results if it's an AJAX request
if search != ""
  puts "Content-Type: text/html\n\n"
  client = db_client
  output = case type
           when "Series" then search_series(client, search)
           when "Season" then search_season(client, search)
           when "Episode" then search_episode(client, search)
           else "<p>No valid type selected.</p>"
           end
  puts output
  exit
end

# Default page load: full HTML
puts "Content-Type: text/html\n\n"
puts <<~HTML
<!DOCTYPE html>
<html>
<head>
  <title>Create New List</title>
  <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
  <style>
    .search-result {
      border: 1px solid #ccc;
      padding: 10px;
      margin-bottom: 10px;
    }
  </style>
</head>
<body>
  <h1>Create a New List</h1>

  <form id="searchForm">
    <label for="type">Select Media Type:</label>
    <select id="type" name="typeSearch">
      <option value="Series">Series</option>
      <option value="Season">Season</option>
      <option value="Episode">Episode</option>
    </select><br><br>

    <label for="mediaEntered">Search:</label>
    <input type="text" name="mediaEntered">
    <input type="submit" value="Search">
  </form>

  <div id="searchResults"></div>

  <script>
    $('#searchForm').submit(function(e) {
      e.preventDefault();
      const type = $('#type').val();
      const query = $('input[name="mediaEntered"]').val();

      $.ajax({
        url: 'createNewList.cgi',
        method: 'GET',
        data: { mediaEntered: query, typeSearch: type },
        success: function(response) {
          $('#searchResults').html(response);
        },
        error: function() {
          $('#searchResults').html("<p style='color:red;'>Error loading search results.</p>");
        }
      });
    });

    function addSeries(id, name) {
      alert("Added series: " + name);
      // Add to sessionStorage or DOM as needed
    }

    function addSeason(id, name, seasonNum) {
      alert("Added season: " + name + " Season " + seasonNum);
    }

    function addEpisode(showId, showName, epData) {
      let [epId, epName] = epData.split(',');
      alert("Added episode: " + showName + " - " + epName);
    }

    function updateSelectedSeason(selectEl) {
      // can be used to update display
    }

    function loadEpisodes(seasonSelect, showId) {
      const seasonData = seasonSelect.value;
      const seasonId = seasonData.split(',')[0];
      const dropdown = seasonSelect.nextElementSibling;

      $.ajax({
        url: 'loadEpisodes.cgi', // A separate CGI that returns episode options
        method: 'GET',
        data: { seasonId: seasonId },
        success: function(response) {
          $(dropdown).html(response);
        },
        error: function() {
          $(dropdown).html("<option>Error loading episodes</option>");
        }
      });
    }
  </script>
</body>
</html>
HTML
