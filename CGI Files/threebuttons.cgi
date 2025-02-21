#!/usr/bin/ruby
$stdout.sync = true
$stderr.reopen $stdout

puts "Content-type: text/html\n\n"
require 'mysql2'
require 'cgi'

cgi = CGI.new
seriesId = cgi['watchedButton']
epId = cgi['watchedEp']
# Start HTML output
puts "<!DOCTYPE html>"
puts "<html lang='en'>"
puts "<head>"
puts "<meta charset='UTF-8'>"
puts "<title>Watched</title>"
puts "<link href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css' rel='stylesheet'>"
puts "</head>"
puts "<body>"
puts "<div class='container mt-5'>"

# Debugging: Print received parameters
puts "<h3>Received Parameters:</h3>"
    puts "<p>Series Id: " + cgi['watchedButton'] + "</p>"
if (epId != "")
    puts "<p>Episode Id: " + cgi['watchedEp'] + "</p>"
end