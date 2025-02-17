#!/usr/bin/ruby

# Enable debugging
$stdout.sync = true
$stderr.reopen $stdout

puts "Content-type: text/html\n\n"
require 'mysql2'
require 'cgi'

# Initialize CGI
cgi = CGI.new

db = Mysql2::Client.new(
    host: '10.20.3.4', 
    username: 'seniorproject25', 
    password: 'TV_Group123!', 
    database: 'televised_w25'
  )

genres = db.query("SELECT DISTINCT genre FROM series ORDER BY genre ASC;")
genres = genres.to_a

sectionCount = 1;

puts "<!DOCTYPE html>"
puts '<html lang="en">'

puts "<head>"
puts '<meta charset="UTF-8">'
puts  '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
puts  '<title>Televised</title>'
puts  '<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet"
    integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">'
puts  '<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"
    integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz"
    crossorigin="anonymous"></script>'
puts  '<link rel="stylesheet" href="Televised.css">'
puts '</head>'


puts '<body id="discoverPage">'
puts '<nav id="changingNav"></nav>'
puts '<div class="container-fluid">'
puts '<h1 class="text-center text-white mt-5">Discover Something New!</h1>'
puts '<section id="discoverGenreOne">'


(0...5).each do |j|
    series = db.query("SELECT imageName FROM series WHERE genre = '" + genres[j]['genre'] + "';")
    series = series.to_a

    puts '<h3 class="text-white ms-4">' + genres[j]['genre'] + '</h3>'
    puts '<div class="wrapper">'

        puts '<section class="carousel-section" id="section' + (sectionCount+(2*j)).to_s() + '">'
        puts '<a href="#section' + ((sectionCount+2)+(2*j)).to_s() + '">‹</a>'

        (0...5).each do |i|
            puts '<div class="item">'
            puts '<form action="series.cgi" method="POST">'
                puts '<input type="image" src="' + series[i]['imageName'] + '" alt="' + series[i]['imageName'] + '">'
                puts '<input type="hidden" name="clicked_image" value="' + series[i]['imageName'] + '">'
            puts '</form>'
            puts '</div>'
        end

        puts '<a href="#section' + ((sectionCount+1)+(2*j)).to_s() + '">›</a>'
        puts '</section>'

        puts '<section class="carousel-section" id="section' + ((sectionCount+1)+(2*j)).to_s() + '">'
        puts '<a href="#section' + (sectionCount+(2*j)).to_s() + '">‹</a>'

        (0...5).each do |i|
            puts '<div class="item">'
            puts '<form action="series.cgi" method="POST">'
                puts '<input type="image" src="' + series[i]['imageName'] + '" alt="' + series[i]['imageName'] + '">'
                puts '<input type="hidden" name="clicked_image" value="' + series[i]['imageName'] + '">'
            puts '</form>'
            puts '</div>'
        end

        puts '<a href="#section' + ((sectionCount+2)+(2*j)).to_s() + '">›</a>'
        puts '</section>'

        puts '<section class="carousel-section" id="section' + ((sectionCount+2)+(2*j)).to_s() + '">'
        puts '<a href="#section' + ((sectionCount+1)+(2*j)).to_s() + '">‹</a>'

        (0...5).each do |i|
            puts '<div class="item">'
            puts '<form action="series.cgi" method="POST">'
                puts '<input type="image" src="' + series[i]['imageName'] + '" alt="' + series[i]['imageName'] + '">'
                puts '<input type="hidden" name="clicked_image" value="' + series[i]['imageName'] + '">'
            puts '</form>'
            puts '</div>'
        end

        puts '<a href="#section' + (sectionCount+(2*j)).to_s() + '">›</a>'
        puts '</section>'

    puts '</div>'
    sectionCount = sectionCount +1
end

puts '<div class="center mt-5">'
puts '<div class="pagination">'
puts '<a href="#">&laquo;</a>'
        puts '<a class="active" href="discover.cgi">1</a>'
        puts '<a href="discover2.cgi">2</a>'
        puts '<a href="#">3</a>'
        puts '<a href="#">4</a>'
        puts '<a href="#">5</a>'
        puts '<a href="#">&raquo;</a>'
      puts '</div>'
    puts '</div>'
  puts '</div>'


 puts '<script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.6/dist/umd/popper.min.js"
    integrity="sha384-oBqDVmMz4fnFO9gybYlQ2X9B5o4j2wJlFczXy33mu6g5U5gF6kZ4GiWfWc6b7pQ1f"
    crossorigin="anonymous"></script>'
 puts '<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>'
 puts '<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>'
 puts '<script src="Televised.js"></script>'

 puts '</body>'
 puts '</html>'