#!/usr/bin/ruby
$stdout.sync = true
$stderr.reopen $stdout

puts "Content-type: text/html\n\n"
require 'mysql2'
require 'cgi'
require 'cgi/session'
require 'json'

cgi = CGI.new
session = CGI::Session.new(cgi)
username = session['username']

search = cgi['mediaEntered']
type = cgi['typeSearch']

listName = cgi['listName']
description = cgi['description']
privacy = cgi['views'] == "Public" ? 1 : 0  # Convert to 1 for Public, 0 for Private

begin
    seriesArray = cgi['seriesArray'] && !cgi['seriesArray'].empty? ? JSON.parse(cgi['seriesArray']) : []
rescue JSON::ParserError
    seriesArray = []
end

db = Mysql2::Client.new(
    host: '10.20.3.4', 
    username: 'seniorproject25', 
    password: 'TV_Group123!', 
    database: 'televised_w25'
)

# Handle AJAX search functionality
if type == "Series" && search != ""
    results = db.query("SELECT showName, imageName, showId FROM series WHERE showName LIKE '#{db.escape(search)}%'")
    
    if results.count > 0
        results.each do |row|
            puts "<p>#{row['showName']} <img src='#{row['imageName']}' alt='#{row['showName']}' style='height: 50px; width: 35px; object-fit: cover;'>"
            puts "<button class='addToList btn btn-success' data-series-id='#{row['showId']}' data-series-name='#{row['showName']}'>ADD</button></p>"
        end
    else
        puts "<p>We can't seem to find this title!</p>"
    end
    exit
end

# Handle list creation when the "saveList" button is clicked
if cgi['saveList'] && !listName.empty? && !description.empty? && !seriesArray.empty?
    existing_list = db.query("SELECT id FROM listOwnership WHERE username = '#{username}' AND listName = '#{db.escape(listName)}'")

    if existing_list.count > 0
        puts "<script>alert('Sorry, but you already have a list with this name. Try a different name.');</script>"
        exit
    end

    # Insert new list into listOwnership
    db.query("INSERT INTO listOwnership (username, listName) VALUES ('#{username}', '#{db.escape(listName)}')")
    list_id = db.last_id  

    # Insert series into curatedListSeries
    seriesArray.each do |series_id|
        db.query("INSERT INTO curatedListSeries (username, seriesId, name, description, privacy, date, listId)
                  VALUES ('#{username}', '#{series_id}', '#{db.escape(listName)}', '#{db.escape(description)}', '#{privacy}', NOW(), '#{list_id}')")
    end

    # Confirmation and redirect
    puts "<script>alert('Your list has been successfully created!'); window.location.href = 'Profile_List.cgi';</script>"
    exit
end

# Full HTML Page
puts <<-HTML
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Televised</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="Televised.css">
</head>
<body id="createNewList">
    <nav id="changingNav"></nav>
    <h2 class="text-center mt-3">Create a New List</h2>
    <div class="container-fluid">
        <div class="row">
            <!-- Left Column - List Form -->
            <div class="col" id="listRow">
                <h3 class="text-center">List Details</h3>
                <form id="newListForm" method="post">
                    <label>Name</label>
                    <input type="text" name="listName" class="form-control" placeholder="Name" required>
                    <br>
                    <label>Who Can View</label>
                    <select name="views" class="form-control">
                        <option value="Public">Public - anyone can view</option>
                        <option value="Private">Private - no one can view</option>
                    </select>
                    <br>
                    <label>Description</label>
                    <textarea name="description" class="form-control" rows="5"></textarea>
                    <br>
                    <input type="hidden" id="seriesArrayInput" name="seriesArray">
                    <button id="saveList" class="btn btn-primary">CREATE LIST</button>
                </form>
            </div>

            <!-- Middle Column - Selected Series -->
            <div class="col" id="listColumn">
                <h3 class="text-center">Selected Series</h3>
                <ul id="seriesList" class="list-group"></ul>
            </div>

            <!-- Right Column - Search -->
            <div class="col" id="searchColumn">
                <h3 class="text-center">Search for a Series</h3>
                <form id="searchForm">
                    <select id="type" name="typeSearch" class="form-control">
                        <option value="Series" selected>Series</option>
                    </select>
                    <br>
                    <input type="text" name="mediaEntered" class="form-control">
                    <input type="submit" value="Search" class="btn btn-secondary mt-2">
                </form>
                <div id="searchResults"></div>
            </div>
        </div>
    </div>

    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
    <script src="Televised.js"></script>
    <script>
        document.addEventListener("DOMContentLoaded", function () {
            // Search functionality
            document.getElementById("searchForm").addEventListener("submit", function (event) { 
                event.preventDefault();
                let searchInput = document.querySelector("input[name='mediaEntered']").value;
                let type = document.querySelector("select[name='typeSearch']").value;

                fetch("createNewList.cgi", {
                    method: "POST",
                    headers: { "Content-Type": "application/x-www-form-urlencoded" },
                    body: new URLSearchParams({ mediaEntered: searchInput, typeSearch: type })
                })
                .then(response => response.text())
                .then(data => { document.getElementById("searchResults").innerHTML = data; });
            });

            // Update series list
            function updateSeriesList() {
                let seriesArray = JSON.parse(sessionStorage.getItem("seriesArray")) || [];
                document.getElementById("seriesArrayInput").value = JSON.stringify(seriesArray);
                let seriesList = document.getElementById("seriesList");
                seriesList.innerHTML = "";

                seriesArray.forEach(function(series) {
                    let li = document.createElement("li");
                    li.classList.add("list-group-item", "d-flex", "justify-content-between", "align-items-center");
                    li.innerHTML = series.name + " <button class='removeFromList btn btn-danger btn-sm' data-series-id='" + series.id + "'>X</button>";
                    seriesList.appendChild(li);
                });
            }
            updateSeriesList();
        });
    </script>
</body>
</html>
HTML

session.close