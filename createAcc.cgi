#!/usr/bin/ruby
require 'mysql2'
require 'cgi'
require 'bcrypt'

# Enable CGI and debugging
$stdout.sync = true
$stderr.reopen($stdout)
cgi = CGI.new

# Get input values from the form
username = cgi.params['unameCreateInput'][0] || ""
password = cgi.params['passCreateInput'][0] || ""

# Print HTTP header
print "Content-type: text/html\r\n\r\n"

# Start HTML output
puts "<!DOCTYPE html>"
puts "<html lang='en'>"
puts "<head>"
puts "<meta charset='UTF-8'>"
puts "<title>Account Creation</title>"
puts "<link href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css' rel='stylesheet'>"
puts "</head>"
puts "<body>"
puts "<div class='container mt-5'>"

# Debugging: Print received parameters
puts "<h3>Received Parameters:</h3>"
puts "<p>Username: #{CGI.escapeHTML(username)}</p>"
puts "<p>Password: #{CGI.escapeHTML(password)}</p>"

# Check if username and password are provided
if username.strip.empty? || password.strip.empty?
  puts "<h2>Error: Username and password are required.</h2>"
  puts "</div></body></html>"
  exit
end

# Connect to MySQL and insert data
begin
  db = Mysql2::Client.new(
    host: 'localhost', 
    username: 'root', 
    password: 'TV_Group123!', 
    database: 'media'
  )

  # Securely hash the password
  hashed_password = BCrypt::Password.create(password)

  # Use prepared statements to prevent SQL injection
  stmt = db.prepare("INSERT INTO accounts (username, password) VALUES (?, ?)")
  stmt.execute(username, hashed_password)

  puts "<h2>Account successfully created!</h2>"

rescue Mysql2::Error => e
  puts "<h2>Database error: #{CGI.escapeHTML(e.message)}</h2>"
ensure
  db.close if db
end

# End HTML output
puts "</div></body></html>"
