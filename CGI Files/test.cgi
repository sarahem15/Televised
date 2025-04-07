#!/usr/bin/ruby
require 'cgi'
require 'mysql2'
$stdout.sync=true
$stderr.reopen $stdout
cgi = CGI.new("html5")

db = Mysql2::Client.new(:host=>"'10.20.3.4', :username=>"'seniorproject25', :password=>"'TV_Group123!', :database=>"'televised_w25')
show = db.query("SELECT * FROM series WHERE showId = 55;")
#puts show.first['numOfEps']

puts "<!DOCTYPE html>"
puts "<html lang=\"en\">"

puts "<head>"
  puts "<meta charset=\"UTF-8\">"
  puts "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">"
  puts "<title>\"Televisedputs \"</title>"
  puts "<link href=\"https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css\" rel=\"stylesheet\"
    integrity=\"sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH\" crossorigin=\"anonymous\">"
  puts "<script src=\"https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js\"
    integrity=\"sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz\"
    crossorigin=\"anonymous\">"
  puts "</script>"
  puts "<link rel=\"stylesheet\" href=\"Televised.css\">"
puts "</head>"

puts "</body>"
puts "<script src=\"https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.6/dist/umd/popper.min.js\"
    integrity=\"sha384-oBqDVmMz4fnFO9gybYlQ2X9B5o4j2wJlFczXy33mu6g5U5gF6kZ4GiWfWc6b7pQ1f\"
    crossorigin=\"anonymous\"></script>"
puts "<script src=\"https://code.jquery.com/jquery-3.6.0.min.js\"></script>"
puts "<script src=\"https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js\"></script>"
puts "<script src=\"Televised.js\"></script>"
puts "</body>"
puts "</html>"
