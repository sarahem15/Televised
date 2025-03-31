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
privacy = cgi['views'] == "Public" ? 1 : 0  # Convert privacy to 1 for Public, 0 for Private

begin
    seriesArray = cgi['seriesArray'] && !cgi['seriesArray'].empty? ? JSON.parse(cgi['seriesArray']) : []
rescue JSON::ParserError
    seriesArray = []  # Default to an empty array if JSON is invalid
end

db = Mysql2::Client.new(
    host: '10.20.3.4', 
    username: 'seniorproject25', 
    password: 'TV_Group123!', 
    database: 'televised_w25'
)

# Handle search functionality via AJAX
if type == "Series" && search != ""
    images = db.query("SELECT showName, imageName, showId FROM series WHERE showName LIKE '#{db.escape(search)}%'")
    if !images.to_a.empty?
        images.each do |image|
            puts "<p>#{image['showName']} <img src='#{image['imageName']}' alt='#{image['showName']}' style='height: 50px; width: 35px; object-fit: cover;'>"
            puts "<button class='addToList btn btn-success' data-series-id='#{image['showId']}' data-series-name='#{image['showName']}'>ADD</button></p>"
        end
    else
        puts '<p>We can\'t seem to find this title!</p>'
    end
    exit
end

# Process list creation only when "saveList" is clicked
if cgi['saveList'] && !listName.empty? && !description.empty? && !seriesArray.empty?
    # Check if the user already has a list with the same name
    existing_list = db.query("SELECT id FROM listOwnership WHERE username = '#{username}' AND listName = '#{db.escape(listName)}'")

    if existing_list.count > 0
        puts "<script>alert('Sorry, but you already have a list with this name. Try a different name to submit a new list.');</script>"
        exit
    end

    # Insert new list into listOwnership
    db.query("INSERT INTO listOwnership (username, listName) VALUES ('#{username}', '#{db.escape(listName)}')")
    list_id = db.last_id  # Get the inserted list ID

    # Insert list details into curatedListSeries
    seriesArray.each do |series_id|
        db.query("INSERT INTO curatedListSeries (username, seriesId, name, description, privacy, date, listId)
                  VALUES ('#{username}', '#{series_id}', '#{db.escape(listName)}', '#{db.escape(description)}', '#{privacy}', NOW(), '#{list_id}')")
    end

    # Clear sessionStorage, form fields, and redirect using JavaScript
    puts <<-JS
        <script>
            alert('Your list has been successfully created!');
            sessionStorage.removeItem("seriesArray");  // Clear stored series
            document.getElementById("newListForm").reset(); // Reset the form
            document.getElementById("seriesList").innerHTML = ""; // Clear displayed list
            window.location.href = 'Profile_List.cgi'; // Redirect
        </script>
    JS
    exit
end

# Full page HTML
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
            <div class="col" id="listRow">
                <h3 class="text-center">List Details</h3>
                <form id="newListForm" method="post">
                    <label>Name</label>
                    <input type="text" name="listName" class="form-control" required>
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

            <div class="col" id="listColumn">
                <h3 class="text-center">Selected Series</h3>
                <ul id="seriesList" class="list-group"></ul>
            </div>

            <div class="col" id="searchColumn">
                <h3 class="text-center">Search for a Series</h3>
                <form id="searchForm">
                    <select id="type" name="typeSearch" class="form-control">
                        <option value="Series" selected>Series</option>
                        <option value="Seasons">Seasons</option>
                        <option value="Episodes">Episodes</option>
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
        document.getElementById("saveList").addEventListener("click", function(event) {
            event.preventDefault(); // Prevent default form submission

            let formData = new FormData(document.getElementById("newListForm"));
            formData.append("seriesArray", sessionStorage.getItem("seriesArray") || "[]");

            fetch("createNewList.cgi", {
                method: "POST",
                body: formData
            })
            .then(response => response.text())
            .then(data => {
                document.body.innerHTML += data; // Handle response
            });
        });

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
    </script>
</body>
</html>
HTML

session.close
