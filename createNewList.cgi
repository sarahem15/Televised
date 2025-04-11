#!/usr/bin/env ruby
require 'cgi'
require 'mysql2'
require 'date'
require 'json'

cgi = CGI.new
params = cgi.params
saved = false

begin
  db = Mysql2::Client.new(host: "localhost", username: "root", password: "", database: "TVList")
  username = cgi.cookies["user"]&.first || "guest"
  media_type = params["mediaType"][0]
  list_name = params["listName"][0]
  description = params["description"][0]
  privacy = params["privacy"][0] == "Public" ? 1 : 0
  today = Date.today.to_s

  if params["saveList"][0] == "true"
    # Check for duplicate list name
    dup_check = db.query("SELECT * FROM listOwnership WHERE username='#{username}' AND name='#{db.escape(list_name)}'")
    if dup_check.count > 0
      puts cgi.header("type" => "text/html")
      puts "<script>alert('List name already exists. Choose a different name.');</script>"
      exit
    end

    # Insert new list into listOwnership
    db.query("INSERT INTO listOwnership (username, name, description, privacy, date) VALUES ('#{username}', '#{db.escape(list_name)}', '#{db.escape(description)}', #{privacy}, '#{today}')")
    list_id = db.query("SELECT listId FROM listOwnership WHERE username='#{username}' AND name='#{db.escape(list_name)}'").first["listId"]

    # Save series
    if params["seriesArray"] && params["seriesArray"][0] != ""
      series_list = JSON.parse(params["seriesArray"][0])
      series_list.each do |series|
        show_id = db.escape(series["showId"].to_s)
        db.query("INSERT INTO curatedListSeries (listId, username, seriesId, name, description, privacy, date) VALUES (#{list_id}, '#{username}', #{show_id}, '#{db.escape(list_name)}', '#{db.escape(description)}', #{privacy}, '#{today}')")
      end
    end

    # Save seasons
    if params["seasonArray"] && params["seasonArray"][0] != ""
      season_list = JSON.parse(params["seasonArray"][0])
      season_list.each do |season|
        season_id = db.escape(season["seasonId"].to_s)
        db.query("INSERT INTO curatedListSeason (listId, username, seasonId, name, description, privacy, date) VALUES (#{list_id}, '#{username}', #{season_id}, '#{db.escape(list_name)}', '#{db.escape(description)}', #{privacy}, '#{today}')")
      end
    end

    # Save episodes
    if params["episodeArray"] && params["episodeArray"][0] != ""
      episode_list = JSON.parse(params["episodeArray"][0])
      episode_list.each do |ep|
        ep_id = db.escape(ep["epId"].to_s)
        db.query("INSERT INTO curatedListEpisode (listId, username, epId, name, description, privacy, date) VALUES (#{list_id}, '#{username}', #{ep_id}, '#{db.escape(list_name)}', '#{db.escape(description)}', #{privacy}, '#{today}')")
      end
    end

    saved = true
  end
rescue Mysql2::Error => e
  puts cgi.header("type" => "text/html")
  puts "<script>alert('Database error: #{e.message}');</script>"
  exit
end

if saved
  puts <<~HTML
    <html>
    <head>
      <meta charset="UTF-8">
      <script>
        window.onload = function() {
          sessionStorage.removeItem("seriesArray");
          sessionStorage.removeItem("seasonArray");
          sessionStorage.removeItem("episodeArray");
          alert("List saved successfully! Redirecting to your profile...");
          window.location.href = "Profile_List.cgi";
        };
      </script>
    </head>
    <body></body>
    </html>
  HTML
  exit
end

puts cgi.header("type" => "text/html")
puts <<~HTML
<!DOCTYPE html>
<html>
<head>
  <title>Create New List</title>
  <style>
    body { font-family: Arial; display: flex; }
    .column { flex: 1; padding: 20px; border-right: 1px solid #ccc; }
    .column:last-child { border-right: none; }
    img { max-width: 100px; }
    select, input[type="text"] { width: 100%; }
  </style>
  <script>
    let seriesArray = JSON.parse(sessionStorage.getItem("seriesArray") || "[]");
    let seasonArray = JSON.parse(sessionStorage.getItem("seasonArray") || "[]");
    let episodeArray = JSON.parse(sessionStorage.getItem("episodeArray") || "[]");

    function displayArray(arr, containerId) {
      const div = document.getElementById(containerId);
      div.innerHTML = "";
      arr.forEach((item, i) => {
        const p = document.createElement("p");
        let text = "";
        if (item.epName) {
          text = item.showName + ": S" + item.seasonNum + ": " + item.epName;
        } else if (item.seasonNum) {
          text = item.showName + " Season " + item.seasonNum;
        } else {
          text = item.showName;
        }
        p.textContent = text;
        const btn = document.createElement("button");
        btn.textContent = "Remove";
        btn.onclick = function() {
          arr.splice(i, 1);
          sessionStorage.setItem(containerId.replace("Display", "") + "Array", JSON.stringify(arr));
          displayArray(arr, containerId);
        };
        p.appendChild(btn);
        div.appendChild(p);
      });
    }

    function searchMedia() {
      const type = document.querySelector('input[name="mediaType"]:checked').value;
      const query = document.getElementById("searchBox").value;
      fetch("searchMedia.cgi?type=" + type + "&query=" + encodeURIComponent(query))
        .then(res => res.json())
        .then(data => showResults(data, type));
    }

    function showResults(data, type) {
      const container = document.getElementById("searchResults");
      container.innerHTML = "";
      data.forEach(item => {
        const div = document.createElement("div");
        div.innerHTML = `<img src="${item.imageName}" /><p>${item.showName}</p>`;
        if (type === "series") {
          const btn = document.createElement("button");
          btn.textContent = "Add Series";
          btn.onclick = function() {
            seriesArray.push({ showId: item.showId, showName: item.showName });
            sessionStorage.setItem("seriesArray", JSON.stringify(seriesArray));
            displayArray(seriesArray, "seriesDisplay");
          };
          div.appendChild(btn);
        } else if (type === "season") {
          const sel = document.createElement("select");
          for (let i = 1; i <= item.numOfSeasons; i++) {
            const opt = document.createElement("option");
            opt.value = i;
            opt.textContent = "Season " + i;
            sel.appendChild(opt);
          }
          const btn = document.createElement("button");
          btn.textContent = "Add Season";
          btn.onclick = function() {
            const seasonNum = sel.value;
            fetch(`getSeasonId.cgi?showId=${item.showId}&seasonNum=${seasonNum}`)
              .then(res => res.json())
              .then(result => {
                seasonArray.push({
                  showId: item.showId,
                  showName: item.showName,
                  seasonNum: seasonNum,
                  seasonId: result.seasonId
                });
                sessionStorage.setItem("seasonArray", JSON.stringify(seasonArray));
                displayArray(seasonArray, "seasonDisplay");
              });
          };
          div.appendChild(sel);
          div.appendChild(btn);
        } else if (type === "episode") {
          const selSeason = document.createElement("select");
          for (let i = 1; i <= item.numOfSeasons; i++) {
            const opt = document.createElement("option");
            opt.value = i;
            opt.textContent = "Season " + i;
            selSeason.appendChild(opt);
          }
          const selEpisode = document.createElement("select");
          selSeason.onchange = function() {
            fetch(`getEpisodes.cgi?showId=${item.showId}&seasonNum=${selSeason.value}`)
              .then(res => res.json())
              .then(episodes => {
                selEpisode.innerHTML = "";
                episodes.forEach(ep => {
                  const opt = document.createElement("option");
                  opt.value = JSON.stringify(ep);
                  opt.textContent = ep.epName;
                  selEpisode.appendChild(opt);
                });
              });
          };
          selSeason.onchange(); // trigger on load

          const btn = document.createElement("button");
          btn.textContent = "Add Episode";
          btn.onclick = function() {
            const ep = JSON.parse(selEpisode.value);
            episodeArray.push({
              showId: item.showId,
              showName: item.showName,
              epName: ep.epName,
              epId: ep.epId,
              seasonNum: selSeason.value
            });
            sessionStorage.setItem("episodeArray", JSON.stringify(episodeArray));
            displayArray(episodeArray, "episodeDisplay");
          };

          div.appendChild(selSeason);
          div.appendChild(selEpisode);
          div.appendChild(btn);
        }
        container.appendChild(div);
      });
    }

    function submitForm() {
      const form = document.getElementById("mainForm");
      document.getElementById("seriesInput").value = JSON.stringify(seriesArray);
      document.getElementById("seasonInput").value = JSON.stringify(seasonArray);
      document.getElementById("episodeInput").value = JSON.stringify(episodeArray);
      form.submit();
    }

    window.onload = function() {
      displayArray(seriesArray, "seriesDisplay");
      displayArray(seasonArray, "seasonDisplay");
      displayArray(episodeArray, "episodeDisplay");
    };
  </script>
</head>
<body>
  <div class="column">
    <form id="mainForm" method="POST">
      <label>List Name: <input type="text" name="listName" required></label><br>
      <label>Description: <textarea name="description"></textarea></label><br>
      <label>Privacy:
        <select name="privacy">
          <option>Public</option>
          <option>Private</option>
        </select>
      </label><br>
      <label>Type:
        <input type="radio" name="mediaType" value="series" checked> Series
        <input type="radio" name="mediaType" value="season"> Season
        <input type="radio" name="mediaType" value="episode"> Episode
      </label><br>
      <input type="hidden" name="saveList" value="true">
      <input type="hidden" id="seriesInput" name="seriesArray">
      <input type="hidden" id="seasonInput" name="seasonArray">
      <input type="hidden" id="episodeInput" name="episodeArray">
      <button type="button" onclick="submitForm()">Save List</button>
    </form>
  </div>
  <div class="column">
    <h3>Series</h3>
    <div id="seriesDisplay"></div>
    <h3>Seasons</h3>
    <div id="seasonDisplay"></div>
    <h3>Episodes</h3>
    <div id="episodeDisplay"></div>
  </div>
  <div class="column">
    <input type="text" id="searchBox" placeholder="Search...">
    <button type="button" onclick="searchMedia()">Search</button>
    <div id="searchResults"></div>
  </div>
</body>
</html>
HTML
