#!/usr/bin/ruby
require 'cgi'
require 'mysql2'
require 'json'

cgi = CGI.new
db_client = Mysql2::Client.new(
  host: "localhost",
  username: "your_db_username",
  password: "your_db_password",
  database: "your_db_name"
)

# Assume session is already started and we can access the user's session
username = cgi.cookies['username'] # Get the logged-in username from cookies

# Fetch the listId (for example, passed via a hidden input or query parameter)
list_id = cgi['listId']
privacy = cgi['privacy'] # Assuming this is passed in form

# Fetch the episodeArray JSON from the form data
episode_array = JSON.parse(cgi['episodeArray']) # episodeArray is a JSON string sent from JS

# Start SQL transaction
db_client.query("START TRANSACTION")

# Insert into curatedListEpisode
episode_array.each do |episode|
  show_id = episode['showId']
  show_name = episode['showName']
  ep_id = episode['epId']
  ep_name = episode['epName']
  season_num = episode['seasonNum']
  
  # SQL to insert episode into curatedListEpisode
  query = "
    INSERT INTO curatedListEpisode (listId, username, showId, showName, epId, epName, seasonNum, privacy, date)
    VALUES (#{list_id}, '#{username}', #{show_id}, '#{show_name}', #{ep_id}, '#{ep_name}', #{season_num}, #{privacy}, NOW())
  "
  
  db_client.query(query)
end

# Commit the transaction
db_client.query("COMMIT")

# Send a success response back
cgi.out("Content-Type" => "application/json") do
  { success: true, message: "Episodes added successfully!" }.to_json
end

# HTML and JS starts here:
cgi.out {
  <<~HTML
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Create New List</title>
      <style>
        body {
          font-family: Arial, sans-serif;
        }
        #formContainer, #arrayContainer, #searchContainer {
          margin: 10px;
        }
        .button {
          background-color: #4CAF50;
          color: white;
          padding: 10px;
          border: none;
          cursor: pointer;
        }
        .button:hover {
          background-color: #45a049;
        }
      </style>
    </head>
    <body>

    <div id="formContainer">
      <h2>Create New List</h2>
      <form id="listForm">
        <label for="listName">List Name:</label><br>
        <input type="text" id="listName" name="listName"><br><br>

        <label for="description">Description:</label><br>
        <textarea id="description" name="description"></textarea><br><br>

        <label for="privacy">Privacy:</label><br>
        <input type="radio" id="public" name="privacy" value="1">
        <label for="public">Public</label>
        <input type="radio" id="private" name="privacy" value="0" checked>
        <label for="private">Private</label><br><br>

        <input type="button" class="button" value="Save List" onclick="saveList()">
      </form>
    </div>

    <div id="arrayContainer">
      <h2>Selected Episodes</h2>
      <ul id="episodeList"></ul>
    </div>

    <div id="searchContainer">
      <h2>Search</h2>
      <label for="seriesSearch">Search Series:</label><br>
      <input type="text" id="seriesSearch" onkeyup="searchSeries()"><br><br>

      <label for="seasonSearch">Search Season:</label><br>
      <input type="text" id="seasonSearch" onkeyup="searchSeason()"><br><br>

      <label for="episodeSearch">Search Episode:</label><br>
      <input type="text" id="episodeSearch" onkeyup="searchEpisode()"><br><br>
    </div>

    <script>
      var episodeArray = [];

      // Example function to add episodes
      function addEpisode(showId, showName, epId, epName, seasonNum) {
        var episode = {
          showId: showId,
          showName: showName,
          epId: epId,
          epName: epName,
          seasonNum: seasonNum
        };
        episodeArray.push(episode);
        displayEpisodeList();
      }

      // Display the selected episodes
      function displayEpisodeList() {
        var episodeList = document.getElementById("episodeList");
        episodeList.innerHTML = ""; // Clear the list before adding updated episodes

        episodeArray.forEach(function(episode, index) {
          var li = document.createElement("li");
          li.textContent = episode.showName + ": S" + episode.seasonNum + " - " + episode.epName;
          var removeBtn = document.createElement("button");
          removeBtn.textContent = "Remove";
          removeBtn.onclick = function() {
            removeEpisode(index);
          };
          li.appendChild(removeBtn);
          episodeList.appendChild(li);
        });
      }

      // Remove episode from array
      function removeEpisode(index) {
        episodeArray.splice(index, 1);
        displayEpisodeList();
      }

      // Search series, season, and episode (this is a simplified example)
      function searchSeries() {
        var query = document.getElementById("seriesSearch").value.toLowerCase();
        // You would filter your series here based on the query
      }

      function searchSeason() {
        var query = document.getElementById("seasonSearch").value.toLowerCase();
        // You would filter your seasons here based on the query
      }

      function searchEpisode() {
        var query = document.getElementById("episodeSearch").value.toLowerCase();
        // You would filter your episodes here based on the query
      }

      // Save the list (episodes and other form data)
      function saveList() {
        var listId = document.getElementById("listId").value;
        var privacy = document.querySelector('input[name="privacy"]:checked').value;

        var xhr = new XMLHttpRequest();
        xhr.open("POST", "createNewList.cgi", true);
        xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

        var data = "listId=" + encodeURIComponent(listId) +
                   "&privacy=" + encodeURIComponent(privacy) +
                   "&episodeArray=" + encodeURIComponent(JSON.stringify(episodeArray));

        xhr.send(data);

        xhr.onload = function() {
          if (xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            if (response.success) {
              alert(response.message);
            } else {
              alert("There was an error: " + response.message);
            }
          }
        };
      }
    </script>

    </body>
    </html>
  HTML
}
