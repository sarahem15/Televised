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

pageNumber = cgi['pageNumber']
sortBy = cgi['sort']

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

puts "<script src=\"https://code.jquery.com/jquery-3.6.0.min.js\"></script>"
    puts "<script src=\"https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js\"></script>"
    puts "<script src=\"Televised.js\"></script>"

if (sortBy == 'genre')

    if (pageNumber.to_i == 1) 
        beginArray = 0
        endArray = 5
    end
    if (pageNumber.to_i == 2)
        beginArray = 5
        endArray = 10
    end
    if (pageNumber.to_i == 3)
        beginArray = 10
        endArray = 14
    end

genres = db.query("SELECT DISTINCT genre FROM series ORDER BY genre ASC;")
genres = genres.to_a

sectionCount = 1;

puts '<section id="discoverGenreOne">'
(beginArray...endArray).each do |j|
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
                puts '<input type="hidden" name="seasonNumber" value="' + 1.to_s + '">'
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
                puts '<input type="hidden" name="seasonNumber" value="' + 1.to_s + '">'
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
                puts '<input type="hidden" name="seasonNumber" value="' + 1.to_s + '">'
            puts '</form>'
            puts '</div>'
        end

        puts '<a href="#section' + (sectionCount+(2*j)).to_s() + '">›</a>'
        puts '</section>'

    puts '</div>'
    sectionCount = sectionCount +1
end

if (pageNumber.to_i == 1)
    puts '<div class="center mt-5">'
    puts '<div class="pagination">'
    puts '<a href="#">&laquo;</a>'
            puts '<a class="active" href="discover.cgi?sort=genre&pageNumber=1">1</a>'
            puts '<a href="discover.cgi?sort=genre&pageNumber=2">2</a>'
            puts '<a href="discover.cgi?sort=genre&pageNumber=3">3</a>'
            puts '<a href="#">&raquo;</a>'
          puts '</div>'
        puts '</div>'
      puts '</div>'
    end
if (pageNumber.to_i == 2)
    puts '<div class="center mt-5">'
    puts '<div class="pagination">'
    puts '<a href="#">&laquo;</a>'
            puts '<a href="discover.cgi?sort=genre&pageNumber=1">1</a>'
            puts '<a class="active" href="discover.cgi?sort=genre&pageNumber=2">2</a>'
            puts '<a href="discover.cgi?sort=genre&pageNumber=3">3</a>'
            puts '<a href="#">&raquo;</a>'
          puts '</div>'
        puts '</div>'
      puts '</div>'
    end
if (pageNumber.to_i == 3)
    puts '<div class="center mt-5">'
    puts '<div class="pagination">'
    puts '<a href="#">&laquo;</a>'
            puts '<a href="discover.cgi?sort=genre&pageNumber=1">1</a>'
            puts '<a href="discover.cgi?sort=genre&pageNumber=2">2</a>'
            puts '<a class="active" href="discover.cgi?sort=genre&pageNumber=3">3</a>'
            puts '<a href="#">&raquo;</a>'
          puts '</div>'
        puts '</div>'
      puts '</div>'
    end

end

if (sortBy == 'az') 

series = db.query("SELECT * FROM series ORDER BY showName ASC;")
size = 0
series = series.to_a
    puts '<section id="discoverAlphabet">'
(0...5).each do |h|
    puts '<div class="wrapper">'
    puts '<section class="carousel-section" id="section' + size.to_s() + '">'
        (0...5).each do |i|
            puts '<div class="item">'
            puts '<form action="series.cgi" method="POST">'
                puts '<input type="image" src="' + series[size]['imageName'] + '" alt="' + series[size]['imageName'] + '">'
                puts '<input type="hidden" name="clicked_image" value="' + series[size]['imageName'] + '">'
                puts '<input type="hidden" name="seasonNumber" value="' + 1.to_s + '">'
                size = size + 1
            puts '</form>'
            puts '</div>'
        end
        puts '</section>'
    puts '</div>'
    puts '<br>'
end

puts '<div class="center mt-5">'
puts '<div class="pagination">'
puts '<a href="#">&laquo;</a>'
        puts '<a class="active" href="discover.cgi?sort=az&pageNumber=1">A-D</a>'
        puts '<a href="##">E-H</a>'
        puts '<a href="#">I-L</a>'
        puts '<a href="#">M-P</a>'
        puts '<a href="#">Q-T</a>'
        puts '<a href="#">U-Z</a>'
        puts '<a href="#">&raquo;</a>'
      puts '</div>'
    puts '</div>'
  puts '</div>'
  puts '<br>'
end

if (sortBy == 'streaming')
if pageNumber.to_i == 1
    service = 'Disney+'
end
if pageNumber.to_i == 2
    service = 'Netflix'
end
if pageNumber.to_i == 3
    service = 'Max'
end
if pageNumber.to_i == 4
    service = 'Hulu'
end
if pageNumber.to_i == 5
    service = 'Prime Video'
end
if pageNumber.to_i == 6
    service = 'Apple TV+'
end

if pageNumber.to_i == 7
    service = 'Peacock'
end

streamings = db.query("SELECT * FROM series WHERE streaming ='" + service + "';")
streamings = streamings.to_a
size = (streamings.size/5)
if (size == 0)
    size = 1
end
beginArray = 0
endArray = 5
#(0...size).each do |i|
    puts '<div class="wrapper">'
    puts '<section class="carousel-section" id="section' + size.to_s() + '">'
        (0...streamings.size).each do |i|
            puts '<div class="item">'
            puts '<form action="series.cgi" method="POST">'
                puts '<input type="image" src="' + streamings[i]['imageName'] + '" alt="' + streamings[i]['imageName'] + '">'
                puts '<input type="hidden" name="clicked_image" value="' + streamings[i]['imageName'] + '">'
                puts '<input type="hidden" name="seasonNumber" value="' + 1.to_s + '">'
            puts '</form>'
            puts '</div>'
        end
        puts '</section>'
    puts '</div>'
    puts '<br>' 
#end



puts '<div class="center mt-5">'
puts '<div class="pagination">'
puts '<a href="#">&laquo;</a>'
        puts '<a class="active" href="discover.cgi?sort=streaming&pageNumber=1">Disney+</a>'
        puts '<a href="discover.cgi?sort=streaming&pageNumber=2">Netflix</a>'
        puts '<a href="discover.cgi?sort=streaming&pageNumber=3">Max</a>'
        puts '<a href="discover.cgi?sort=streaming&pageNumber=4">Hulu</a>'
        puts '<a href="discover.cgi?sort=streaming&pageNumber=5">Prime Video</a>'
        puts '<a href="discover.cgi?sort=streaming&pageNumber=6">Apple TV+</a>'
        puts '<a href="discover.cgi?sort=streaming&pageNumber=7">Peacock</a>'
        puts '<a href="discover.cgi?sort=streaming&pageNumber=8">Tubi</a>'
        puts '<a href="discover.cgi?sort=streaming&pageNumber=9">Hulu</a>'
        puts '<a href="discover.cgi?sort=streaming&pageNumber=10">Paramount+</a>'
        puts '<a href="discover.cgi?sort=streaming&pageNumber=1">&raquo;</a>'
      puts '</div>'
    puts '</div>'
  puts '</div>'
end

 puts '<script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.6/dist/umd/popper.min.js"
    integrity="sha384-oBqDVmMz4fnFO9gybYlQ2X9B5o4j2wJlFczXy33mu6g5U5gF6kZ4GiWfWc6b7pQ1f"
    crossorigin="anonymous"></script>'
 puts '<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>'
 puts '<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>'
 puts '<script src="Televised.js"></script>'

 puts '</body>'
 puts '</html>'