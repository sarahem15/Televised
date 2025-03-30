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

# Ensure session has a username
if !session['username'] || session['username'].empty?
    puts "<script>alert('You must be logged in to create a list.'); window.location.href='loginPage.cgi';</script>"
    exit
end

username = session['username']

# Only process when "Create List" is clicked
if cgi.has_key?('saveList')
    listName = cgi['listName']
    description = cgi['description']
    privacy = cgi['views'] == "Public" ? 1 : 0  # Convert privacy to 1 for Public, 0 for Private

    # Parse seriesArray safely
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

    # Check if the user already has a list with the same name
    existing_list = db.query("SELECT id FROM listOwnership WHERE username = '#{username}' AND listName = '#{db.escape(listName)}'")

    if existing_list.count > 0
        puts "<script>alert('Sorry, but you already have a list with this name. Try a different name.');</script>"
        exit
    end

    # Insert new list into listOwnership
    db.query("INSERT INTO listOwnership (username, listName) VALUES ('#{username}', '#{db.escape(listName)}')")
    list_id = db.last_id  # Get the inserted list ID

    # Insert series into curatedSeriesList
    seriesArray.each do |series_id|
        db.query("INSERT INTO curatedSeriesList (username, seriesId, name, description, privacy, date, listId)
                  VALUES ('#{username}', '#{series_id}', '#{db.escape(listName)}', '#{db.escape(description)}', '#{privacy}', NOW(), '#{list_id}')")
    end

    # Success message
    puts "<script>alert('Your list has been successfully created!'); window.location.href='createNewList.cgi';</script>"
    session.close
    exit
end

# HTML Page
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

        <!-- Left Column - Form -->
        <div class="col" id="listRow">
            <h3 class="text-center">List Details</h3>
            <form id="newListForm">
                <label>Name</label>
                <input type="text" id="listName" name="listName" class="form-control" placeholder="Name" required>
                <br>
                <label>Who Can View</label>
                <select id="views" name="views" class="form-control">
                    <option value="Public">Public - anyone can view</option>
                    <option value="Private">Private - no one can view</option>
                </select>
                <br>
                <label>Description</label>
                <textarea id="description" name="description" class="form-control" rows="5"></textarea>
                <br>
                <input type="hidden" id="seriesArrayInput" name="seriesArray">
                <button id="saveList" class="btn btn-primary" type="button">CREATE LIST</button>
            </form>
        </div>

        <!-- Middle Column - Selected Series -->
        <div class="col" id="listColumn">
            <h3 class="text-center">Selected Series</h3>
            <ul id="seriesList" class="list-group"></ul>
        </div>

        <!-- Right Column - Search for Series -->
        <div class="col" id="searchColumn">
            <h3 class="text-center">Search for a Series</h3>
            <form id="searchForm">
                <select id="type" name="typeSearch" class="form-control">
                    <option value="Series" selected>Series</option>
                    <option value="Seasons">Seasons</option>
                    <option value="Episodes">Episodes</option>
                </select>
                <br>
                <input type="text" id="mediaEntered" name="mediaEntered" class="form-control">
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
    sessionStorage.setItem("seriesArray", "[]"); // Reset series array

    // AJAX form submission
    document.getElementById("saveList").addEventListener("click", function () {
        let listName = document.getElementById("listName").value;
        let description = document.getElementById("description").value;
        let privacy = document.getElementById("views").value;
        let seriesArray = JSON.parse(sessionStorage.getItem("seriesArray")) || [];

        fetch("createNewList.cgi", {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: new URLSearchParams({
                saveList: "1", 
                listName: listName,
                description: description,
                views: privacy,
                seriesArray: JSON.stringify(seriesArray)
            })
        })
        .then(response => response.text())
        .then(data => { eval(data); }); // Execute alert message from the server
    });

    function updateSeriesList() {
        let listColumn = document.getElementById("seriesList");
        let seriesArray = JSON.parse(sessionStorage.getItem("seriesArray")) || [];
        listColumn.innerHTML = "";
        seriesArray.forEach(series => {
            let listItem = document.createElement("li");
            listItem.innerHTML = series.name;
            listColumn.appendChild(listItem);
        });
        document.getElementById("seriesArrayInput").value = JSON.stringify(seriesArray);
    }

    updateSeriesList();
});
</script>

</body>
</html>
HTML
