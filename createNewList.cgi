#!/usr/bin/env ruby
require 'cgi'
require 'mysql2'
require 'json'

cgi = CGI.new
puts cgi.header("type" => "text/html", "charset" => "utf-8")

client = Mysql2::Client.new(
  :host => "localhost",
  :username => "root",
  :password => "password",
  :database => "tv_shows"
)

series_data = client.query("SELECT showId, showName FROM series").to_a
season_data = client.query("SELECT seasonId, seasonNum, seriesId FROM season").to_a
episode_data = client.query("SELECT epId, epName, seasonId FROM episode").to_a

puts <<~HTML
<html>
<head>
  <title>Create New List</title>
  <style>
    .popup {
      display: none;
      position: fixed;
      top: 10px;
      left: 50%;
      transform: translateX(-50%);
      z-index: 9999;
      padding: 10px;
      border-radius: 5px;
      background-color: #4CAF50;
      color: white;
    }
  </style>
</head>
<body>
  <div class="popup" id="popup"></div>

  <form id="form">
    <input type="text" id="listName" placeholder="List Name" required><br>
    <textarea id="description" placeholder="Description"></textarea><br>
    <select id="privacy">
      <option value="1">Public</option>
      <option value="0">Private</option>
    </select><br>

    <select id="mediaType">
      <option value="series">Series</option>
      <option value="season">Season</option>
      <option value="episode">Episode</option>
    </select><br>

    <div id="seriesSearch">
      <select id="seriesDropdown"></select>
      <button type="button" onclick="addSeries()">Add</button>
    </div>

    <div id="seasonSearch" style="display:none;">
      <select id="seriesDropdownSeason" onchange="populateSeasonDropdown()"></select>
      <select id="seasonDropdown"></select>
      <button type="button" onclick="addSeason()">Add</button>
    </div>

    <div id="episodeSearch" style="display:none;">
      <select id="seriesDropdownEpisode" onchange="populateSeasonDropdown()"></select>
      <select id="seasonDropdownEpisode" onchange="populateEpisodeDropdown()"></select>
      <select id="episodeDropdown"></select>
      <button type="button" onclick="addEpisode()">Add</button>
    </div>

    <button type="submit">Save List</button>
  </form>

  <h3>Selected Series</h3>
  <ul id="seriesList"></ul>
  <h3>Selected Seasons</h3>
  <ul id="seasonList"></ul>
  <h3>Selected Episodes</h3>
  <ul id="episodeList"></ul>

  <script>
    const seriesArray = JSON.parse(sessionStorage.getItem("seriesArray") || "[]");
    const seasonArray = JSON.parse(sessionStorage.getItem("seasonArray") || "[]");
    const episodeArray = JSON.parse(sessionStorage.getItem("episodeArray") || "[]");

    const series = #{series_data.to_json};
    const seasons = #{season_data.to_json};
    const episodes = #{episode_data.to_json};

    function showPopup(message, type) {
      const popup = document.getElementById("popup");
      popup.innerText = message;
      popup.style.backgroundColor = type === 'success' ? '#4CAF50' : '#f44336';
      popup.style.display = "block";
      setTimeout(() => popup.style.display = "none", 3000);
    }

    function renderArray(listId, array, removeFn) {
      const list = document.getElementById(listId);
      list.innerHTML = "";
      array.forEach((item, index) => {
        const li = document.createElement("li");
        li.textContent = item.display;
        const btn = document.createElement("button");
        btn.textContent = "Remove";
        btn.onclick = () => removeFn(index);
        li.appendChild(btn);
        list.appendChild(li);
      });
    }

    function addSeries() {
      const select = document.getElementById("seriesDropdown");
      const option = select.options[select.selectedIndex];
      const id = option.value;
      const name = option.text;
      if (!seriesArray.some(s => s.id === id)) {
        seriesArray.push({ id, name, display: name });
        sessionStorage.setItem("seriesArray", JSON.stringify(seriesArray));
        renderArray("seriesList", seriesArray, i => {
          seriesArray.splice(i, 1);
          sessionStorage.setItem("seriesArray", JSON.stringify(seriesArray));
          renderArray("seriesList", seriesArray, arguments.callee);
        });
      }
    }

    function addSeason() {
      const seriesSelect = document.getElementById("seriesDropdownSeason");
      const seasonSelect = document.getElementById("seasonDropdown");
      const seriesName = seriesSelect.options[seriesSelect.selectedIndex].text;
      const seasonId = seasonSelect.value;
      const seasonNum = seasonSelect.options[seasonSelect.selectedIndex].dataset.seasonnum;

      if (!seasonArray.some(s => s.seasonId === seasonId)) {
        seasonArray.push({ seasonId, display: `${seriesName} Season ${seasonNum}` });
        sessionStorage.setItem("seasonArray", JSON.stringify(seasonArray));
        renderArray("seasonList", seasonArray, i => {
          seasonArray.splice(i, 1);
          sessionStorage.setItem("seasonArray", JSON.stringify(seasonArray));
          renderArray("seasonList", seasonArray, arguments.callee);
        });
      }
    }

    function addEpisode() {
      const seriesSelect = document.getElementById("seriesDropdownEpisode");
      const seasonSelect = document.getElementById("seasonDropdownEpisode");
      const episodeSelect = document.getElementById("episodeDropdown");

      const showName = seriesSelect.options[seriesSelect.selectedIndex].text;
      const seasonNum = seasonSelect.options[seasonSelect.selectedIndex].dataset.seasonnum;
      const epName = episodeSelect.options[episodeSelect.selectedIndex].text;
      const epId = episodeSelect.value;

      if (!episodeArray.some(e => e.epId === epId)) {
        episodeArray.push({ epId, display: `${showName}: S${seasonNum}: ${epName}` });
        sessionStorage.setItem("episodeArray", JSON.stringify(episodeArray));
        renderArray("episodeList", episodeArray, i => {
          episodeArray.splice(i, 1);
          sessionStorage.setItem("episodeArray", JSON.stringify(episodeArray));
          renderArray("episodeList", episodeArray, arguments.callee);
        });
      }
    }

    function populateDropdowns() {
      ["seriesDropdown", "seriesDropdownSeason", "seriesDropdownEpisode"].forEach(id => {
        const dropdown = document.getElementById(id);
        dropdown.innerHTML = "";
        series.forEach(s => {
          dropdown.innerHTML += `<option value="${s.showId}">${s.showName}</option>`;
        });
      });
    }

    function populateSeasonDropdown() {
      const type = document.getElementById("mediaType").value;
      const seriesSelect = document.getElementById(type === "season" ? "seriesDropdownSeason" : "seriesDropdownEpisode");
      const seasonSelect = document.getElementById(type === "season" ? "seasonDropdown" : "seasonDropdownEpisode");

      const seriesId = seriesSelect.value;
      seasonSelect.innerHTML = "";
      seasons.filter(s => s.seriesId == seriesId).forEach(s => {
        seasonSelect.innerHTML += `<option value="${s.seasonId}" data-seasonnum="${s.seasonNum}" data-seriesid="${s.seriesId}">Season ${s.seasonNum}</option>`;
      });

      if (type === "episode") populateEpisodeDropdown();
    }

    function populateEpisodeDropdown() {
      const seasonSelect = document.getElementById("seasonDropdownEpisode");
      const episodeSelect = document.getElementById("episodeDropdown");
      const seasonId = seasonSelect.value;
      episodeSelect.innerHTML = "";
      episodes.filter(e => e.seasonId == seasonId).forEach(e => {
        episodeSelect.innerHTML += `<option value="${e.epId}">${e.epName}</option>`;
      });
    }

    document.getElementById("mediaType").addEventListener("change", () => {
      const type = document.getElementById("mediaType").value;
      document.getElementById("seriesSearch").style.display = type === "series" ? "block" : "none";
      document.getElementById("seasonSearch").style.display = type === "season" ? "block" : "none";
      document.getElementById("episodeSearch").style.display = type === "episode" ? "block" : "none";
    });

    document.getElementById("form").addEventListener("submit", e => {
      e.preventDefault();
      const button = document.querySelector("button[type='submit']");
      button.disabled = true;

      const payload = {
        listName: document.getElementById("listName").value,
        description: document.getElementById("description").value,
        privacy: document.getElementById("privacy").value,
        mediaType: document.getElementById("mediaType").value,
        seriesArray,
        seasonArray,
        episodeArray
      };

      fetch("saveList.cgi", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      }).then(res => res.json())
        .then(data => {
          if (data.success) {
            sessionStorage.clear();
            document.getElementById("form").reset();
            document.getElementById("seriesList").innerHTML = '';
            document.getElementById("seasonList").innerHTML = '';
            document.getElementById("episodeList").innerHTML = '';
            localStorage.setItem("message", "List created successfully!");
            window.location.href = "Profile_List.cgi";
          } else {
            showPopup(data.error || "An error occurred.", "error");
            button.disabled = false;
          }
        }).catch(() => {
          showPopup("Network error.", "error");
          button.disabled = false;
        });
    });

    // Initialize
    renderArray("seriesList", seriesArray, i => seriesArray.splice(i, 1));
    renderArray("seasonList", seasonArray, i => seasonArray.splice(i, 1));
    renderArray("episodeList", episodeArray, i => episodeArray.splice(i, 1));
    populateDropdowns();
    populateSeasonDropdown();
    populateEpisodeDropdown();

    // Show message from previous page if available
    const msg = localStorage.getItem("message");
    if (msg) {
      showPopup(msg, "success");
      localStorage.removeItem("message");
    }
  </script>
</body>
</html>
HTML
