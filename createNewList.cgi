#!/usr/bin/env ruby
require 'cgi'
require 'mysql2'
require 'json'
require 'date'

cgi = CGI.new
puts cgi.header("type" => "text/html", "charset" => "utf-8")

begin
  client = Mysql2::Client.new(
    host: '10.20.3.4', 
    username: 'seniorproject25', 
    password: 'TV_Group123!', 
    database: 'televised_w25'
  )
rescue Mysql2::Error => e
  puts "<p>Database connection error: #{e.message}</p>"
  exit
end

# HTML STARTS HERE
puts <<-HTML
<!DOCTYPE html>
<html>
<head>
  <title>Create New List</title>
  <style>
    body { font-family: Arial; }
    .container { display: flex; justify-content: space-between; padding: 20px; }
    .column { width: 30%; }
    .item-box { border: 1px solid #ccc; padding: 10px; margin-bottom: 10px; }
    .remove-btn { color: red; cursor: pointer; float: right; }
  </style>
</head>
<body>
  <h1>Create a New List</h1>
  <div class="container">
    <div class="column" id="formColumn">
      <form id="listForm">
        <label>List Name:</label><br>
        <input type="text" id="listName"><br><br>
        <label>Description:</label><br>
        <textarea id="description" rows="4" cols="30"></textarea><br><br>
        <label>Privacy:</label><br>
        <select id="privacy">
          <option value="1">Public</option>
          <option value="0">Private</option>
        </select><br><br>
        <label>Media Type:</label><br>
        <select id="mediaType" onchange="changeSearchType()">
          <option value="series">Series</option>
          <option value="season">Season</option>
          <option value="episode">Episode</option>
        </select><br><br>
        <button type="button" onclick="submitList()">Save List</button>
      </form>
    </div>

    <div class="column" id="listDisplay">
      <h3>Selected Items</h3>
      <div id="seriesDisplay"></div>
      <div id="seasonDisplay"></div>
      <div id="episodeDisplay"></div>
    </div>

    <div class="column" id="searchColumn">
      <h3>Search</h3>
      <input type="text" id="searchBox">
      <button onclick="search()">Search</button>
      <div id="searchResults"></div>
    </div>
  </div>
HTML

# JS block
puts <<-JAVASCRIPT
<script>
  let seriesArray = JSON.parse(sessionStorage.getItem("seriesArray") || "[]");
  let seasonArray = JSON.parse(sessionStorage.getItem("seasonArray") || "[]");
  let episodeArray = JSON.parse(sessionStorage.getItem("episodeArray") || "[]");
  let epOptions = [];

  window.onload = function() {
    displayArray(seriesArray, "seriesDisplay");
    displayArray(seasonArray, "seasonDisplay");
    displayArray(episodeArray, "episodeDisplay");
  };

  function changeSearchType() {
    document.getElementById("searchResults").innerHTML = "";
  }

  function search() {
    const query = document.getElementById("searchBox").value;
    const type = document.getElementById("mediaType").value;

    fetch(`/searchMedia.cgi?query=${encodeURIComponent(query)}&type=${type}`)
      .then(res => res.json())
      .then(data => renderSearch(data, type));
  }

  function renderSearch(data, type) {
    const container = document.getElementById("searchResults");
    container.innerHTML = "";

    data.forEach(item => {
      const div = document.createElement("div");
      div.className = "item-box";
      const img = document.createElement("img");
      img.src = `/images/${item.imageName}`;
      img.style.width = "100px";
      div.appendChild(img);

      const name = document.createElement("div");
      name.textContent = item.showName;
      div.appendChild(name);

      if (type === "series") {
        const btn = document.createElement("button");
        btn.textContent = "Add";
        btn.onclick = () => {
          seriesArray.push(item);
          sessionStorage.setItem("seriesArray", JSON.stringify(seriesArray));
          displayArray(seriesArray, "seriesDisplay");
        };
        div.appendChild(btn);
      }

      if (type === "season") {
        const sel = document.createElement("select");
        for (let i = 1; i <= item.numOfSeasons; i++) {
          const opt = document.createElement("option");
          opt.value = i;
          opt.textContent = `Season ${i}`;
          sel.appendChild(opt);
        }
        const btn = document.createElement("button");
        btn.textContent = "Add";
        btn.onclick = () => {
          seasonArray.push({
            showId: item.showId,
            showName: item.showName,
            seasonNum: sel.value
          });
          sessionStorage.setItem("seasonArray", JSON.stringify(seasonArray));
          displayArray(seasonArray, "seasonDisplay");
        };
        div.appendChild(sel);
        div.appendChild(btn);
      }

      if (type === "episode") {
        const selSeason = document.createElement("select");
        for (let i = 1; i <= item.numOfSeasons; i++) {
          const opt = document.createElement("option");
          opt.value = i;
          opt.textContent = `Season ${i}`;
          selSeason.appendChild(opt);
        }

        const selEpisode = document.createElement("select");
        const updateEpisodes = () => {
          fetch(`/getEpisodes.cgi?seriesId=${item.showId}&seasonNum=${selSeason.value}`)
            .then(res => res.json())
            .then(episodes => {
              epOptions = episodes;
              selEpisode.innerHTML = episodes.map(ep =>
                `<option value='\${ep.epId}'>\${ep.epName}</option>`
              ).join("");
            });
        };

        selSeason.onchange = updateEpisodes;
        updateEpisodes();

        const btn = document.createElement("button");
        btn.textContent = "Add";
        btn.onclick = () => {
          const selectedEpId = selEpisode.value;
          const ep = epOptions.find(e => e.epId == selectedEpId);
          if (ep) {
            episodeArray.push({
              showId: item.showId,
              showName: item.showName,
              epName: ep.epName,
              epId: ep.epId,
              seasonNum: selSeason.value
            });
            sessionStorage.setItem("episodeArray", JSON.stringify(episodeArray));
            displayArray(episodeArray, "episodeDisplay");
          }
        };

        div.appendChild(selSeason);
        div.appendChild(selEpisode);
        div.appendChild(btn);
      }

      container.appendChild(div);
    });
  }

  function displayArray(arr, targetId) {
    const container = document.getElementById(targetId);
    container.innerHTML = "";
    arr.forEach((item, index) => {
      const div = document.createElement("div");
      div.className = "item-box";
      let text = "";
      if (targetId === "seriesDisplay") {
        text = item.showName;
      } else if (targetId === "seasonDisplay") {
        text = \`\${item.showName} - Season \${item.seasonNum}\`;
      } else if (targetId === "episodeDisplay") {
        text = \`\${item.showName}: S\${item.seasonNum} - \${item.epName}\`;
      }
      div.textContent = text;

      const btn = document.createElement("span");
      btn.textContent = "✖";
      btn.className = "remove-btn";
      btn.onclick = () => {
        arr.splice(index, 1);
        sessionStorage.setItem(targetId.replace("Display", "Array"), JSON.stringify(arr));
        displayArray(arr, targetId);
      };
      div.appendChild(btn);
      container.appendChild(div);
    });
  }

  function submitList() {
    const name = document.getElementById("listName").value;
    const desc = document.getElementById("description").value;
    const priv = document.getElementById("privacy").value;

    const payload = {
      name: name,
      description: desc,
      privacy: priv,
      seriesArray: seriesArray,
      seasonArray: seasonArray,
      episodeArray: episodeArray
    };

    fetch("/saveList.cgi", {
      method: "POST",
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })
    .then(res => res.json())
    .then(res => {
      alert(res.message);
      if (res.success) {
        sessionStorage.clear();
        window.location.href = "/Profile_List.cgi";
      }
    });
  }
</script>
</body>
</html>
JAVASCRIPT
