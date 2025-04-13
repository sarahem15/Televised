#!/usr/bin/ruby
require 'cgi'
require 'mysql2'

cgi = CGI.new
username = cgi.cookies['username'].value
db = Mysql2::Client.new(host: 'localhost', username: 'root', database: 'your_database')

# Fetch the user's lists
user_lists = db.query("SELECT * FROM listOwnership WHERE username = '#{username}'").to_a

# Check if the user is attempting to edit a list
list_id = cgi['listId']
is_edit_mode = !list_id.nil? && !list_id.empty?

if is_edit_mode
  list_data = db.query("SELECT listName, description, privacy FROM listOwnership WHERE id = #{db.escape(list_id)} AND username = '#{username}'").first
  if list_data.nil?
    puts "<script>alert('You are not authorized to edit this list.'); window.location.href = 'Profile_Lists.cgi';</script>"
    exit
  end
end

# Handle deletion of lists
if cgi['deleteList'] && !list_id.nil?
  db.query("DELETE FROM listOwnership WHERE id = #{db.escape(list_id)} AND username = '#{username}'")
  db.query("DELETE FROM curatedListSeries WHERE listId = #{db.escape(list_id)}")
  db.query("DELETE FROM curatedListSeason WHERE listId = #{db.escape(list_id)}")
  puts "<script>alert('List deleted successfully.'); window.location.href = 'Profile_Lists.cgi';</script>"
  exit
end

# Output HTML for the list page
puts "Content-Type: text/html\n\n"
puts "<!DOCTYPE html>"
puts "<html lang='en'>"
puts "<head>"
puts "    <meta charset='UTF-8'>"
puts "    <meta name='viewport' content='width=device-width, initial-scale=1.0'>"
puts "    <title>Your Lists</title>"
puts "    <link rel='stylesheet' href='styles.css'>"
puts "</head>"
puts "<body>"
puts "    <h1>Your Curated Lists</h1>"
puts "    <table>"
puts "        <thead>"
puts "            <tr>"
puts "                <th>List Name</th>"
puts "                <th>Description</th>"
puts "                <th>Privacy</th>"
puts "                <th>Actions</th>"
puts "            </tr>"
puts "        </thead>"
puts "        <tbody>"

user_lists.each do |list|
  privacy = list['privacy'] == 1 ? 'Public' : 'Private'
  puts "<tr>"
  puts "    <td>#{CGI.escapeHTML(list['listName'])}</td>"
  puts "    <td>#{CGI.escapeHTML(list['description'])}</td>"
  puts "    <td>#{privacy}</td>"
  puts "    <td>"
  puts "        <a href='createNewList.cgi?listId=#{list['id']}' class='btn btn-secondary'>Edit</a>"
  puts "        <form method='post' style='display:inline;'>"
  puts "            <input type='hidden' name='deleteList' value='#{list['id']}'>"
  puts "            <button type='submit' class='btn btn-danger'>Delete</button>"
  puts "        </form>"
  puts "    </td>"
  puts "</tr>"
end

puts "        </tbody>"
puts "    </table>"

# If we are in edit mode, display the edit form
if is_edit_mode
  puts "<h2>Edit List</h2>"
  puts "<form method='post' action='createNewList.cgi'>"
  puts "    <input type='hidden' name='listId' value='#{list_id}'>"
  puts "    <label for='listName'>List Name</label>"
  puts "    <input type='text' name='listName' value='#{CGI.escapeHTML(list_data['listName'])}' required>"

  puts "    <label for='description'>Description</label>"
  puts "    <textarea name='description' rows='4' required>#{CGI.escapeHTML(list_data['description'])}</textarea>"

  puts "    <label for='views'>Privacy</label>"
  puts "    <select name='views'>"
  puts "        <option value='Public' #{'selected' if list_data['privacy'] == 1}>Public</option>"
  puts "        <option value='Private' #{'selected' if list_data['privacy'] == 0}>Private</option>"
  puts "    </select>"

  puts "    <button type='submit' name='saveList'>Save Changes</button>"
  puts "</form>"
end

puts "</body>"
puts "</html>"
