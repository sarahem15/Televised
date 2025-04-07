#!/usr/bin/ruby
require 'mysql2'
require 'cgi'
require 'cgi/session'

# Enable debugging
$stdout.sync = true
$stderr.reopen $stdout

# Initialize CGI
cgi = CGI.new
session = CGI::Session.new(cgi)
username = session['username']
search = cgi['search']
type = cgi['type']

db = Mysql2::Client.new(
    host: '10.20.3.4', 
    username: 'seniorproject25', 
    password: 'TV_Group123!', 
    database: 'televised_w25'
  )

puts "Content-type: text/html\n\n"
puts '<!DOCTYPE html>'
puts '<html lang="en">'
puts '<head>'
    puts '<meta charset="UTF-8">'
    puts '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
    puts '<title>Televised</title>'
    puts '<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">'
    puts '<link rel="stylesheet" href="Televised.css">'
puts '</head>'


if type == "series"
    images = db.query("SELECT showImage FROM series WHERE showName ='" + search + "';")
end


puts '<body>'
puts '</body>'
puts '<html>'