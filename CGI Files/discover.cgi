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
if (pageNumber.to_i == 1)
    puts '<div class="center mt-5">'
    puts '<div class="pagination">'
            puts '<a class="active" href="discover.cgi?sort=genre&pageNumber=1">1</a>'
            puts '<a href="discover.cgi?sort=genre&pageNumber=2">2</a>'
            puts '<a href="discover.cgi?sort=genre&pageNumber=3">3</a>'
          puts '</div>'
        puts '</div>'
      puts '</div>'
    end
if (pageNumber.to_i == 2)
    puts '<div class="center mt-5">'
    puts '<div class="pagination">'
            puts '<a href="discover.cgi?sort=genre&pageNumber=1">1</a>'
            puts '<a class="active" href="discover.cgi?sort=genre&pageNumber=2">2</a>'
            puts '<a href="discover.cgi?sort=genre&pageNumber=3">3</a>'
          puts '</div>'
        puts '</div>'
      puts '</div>'
    end
if (pageNumber.to_i == 3)
    puts '<div class="center mt-5">'
    puts '<div class="pagination">'
            puts '<a href="discover.cgi?sort=genre&pageNumber=1">1</a>'
            puts '<a href="discover.cgi?sort=genre&pageNumber=2">2</a>'
            puts '<a class="active" href="discover.cgi?sort=genre&pageNumber=3">3</a>'
          puts '</div>'
        puts '</div>'
      puts '</div>'
    end
(beginArray...endArray).each do |j|
    series = db.query("SELECT imageName, showName FROM series WHERE genre = '" + genres[j]['genre'] + "';")
    series = series.to_a

    

    puts '<h3 style="margin-left: 12%;">' + genres[j]['genre'] + '</h3>'
    puts '<div class="wrapper">'

        puts '<section class="carousel-section" id="section' + (sectionCount+(2*j)).to_s() + '">'
        puts '<a href="#section' + ((sectionCount+2)+(2*j)).to_s() + '">‹</a>'

        (0...5).each do |i|
            puts '<div class="item">'
            puts '<form action="series.cgi" method="POST">'
                puts '<input type="image" src="' + series[i]['imageName'] + '" alt="' + series[i]['imageName'] + '">'
                puts '<input type="hidden" name="clicked_image" value="' + series[i]['imageName'] + '">'
                puts '<input type="hidden" name="seasonNumber" value="' + 1.to_s + '">'
                puts '<h5 style="text-align: center;">' + series[i]['showName'].gsub("Fucking", "F***ing") + '</h5>'
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
                puts '<h5 style="text-align: center;">' + series[i]['showName'].gsub("Fucking", "F***ing") + '</h5>'
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
                puts '<h5 style="text-align: center;">' + series[i]['showName'].gsub("Fucking", "F***ing") + '</h5>'
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
            puts '<a class="active" href="discover.cgi?sort=genre&pageNumber=1">1</a>'
            puts '<a href="discover.cgi?sort=genre&pageNumber=2">2</a>'
            puts '<a href="discover.cgi?sort=genre&pageNumber=3">3</a>'
          puts '</div>'
        puts '</div>'
      puts '</div>'
    end
if (pageNumber.to_i == 2)
    puts '<div class="center mt-5">'
    puts '<div class="pagination">'
            puts '<a href="discover.cgi?sort=genre&pageNumber=1">1</a>'
            puts '<a class="active" href="discover.cgi?sort=genre&pageNumber=2">2</a>'
            puts '<a href="discover.cgi?sort=genre&pageNumber=3">3</a>'
          puts '</div>'
        puts '</div>'
      puts '</div>'
    end
if (pageNumber.to_i == 3)
    puts '<div class="center mt-5">'
    puts '<div class="pagination">'
            puts '<a href="discover.cgi?sort=genre&pageNumber=1">1</a>'
            puts '<a href="discover.cgi?sort=genre&pageNumber=2">2</a>'
            puts '<a class="active" href="discover.cgi?sort=genre&pageNumber=3">3</a>'
          puts '</div>'
        puts '</div>'
      puts '</div>'
    end

end

#AZ
if (sortBy == 'az') 
    if (pageNumber.to_i == 1)
        firstCharacterSort = db.query("SELECT imageName, showName from series where showName like 'a%' or showName like 'b%' or showName like 'c%' or showName like 'd%' ORDER BY showName ASC;")
    elsif (pageNumber.to_i == 2)
        firstCharacterSort = db.query("SELECT imageName, showName from series where showName like 'e%' or showName like 'f%' or showName like 'g%' or showName like 'h%' ORDER BY showName ASC;")
    elsif (pageNumber.to_i == 3)
        firstCharacterSort = db.query("SELECT imageName, showName from series where showName like 'i%' or showName like 'j%' or showName like 'k%' or showName like 'l%' ORDER BY showName ASC;")
    elsif (pageNumber.to_i == 4)
        firstCharacterSort = db.query("SELECT imageName, showName from series where showName like 'm%' or showName like 'n%' or showName like 'o%' or showName like 'p%' ORDER BY showName ASC;")
    elsif (pageNumber.to_i == 5)
        firstCharacterSort = db.query("SELECT imageName, showName from series where showName like 'q%' or showName like 'r%' or showName like 's%' or showName like 't%' ORDER BY showName ASC;")
    else 
        firstCharacterSort = db.query("SELECT imageName, showName from series where showName like 'u%' or showName like 'v%' or showName like 'w%' or showName like 'x%' or showName like 'y%'or showName like 'z%' ORDER BY showName ASC;")
    end

        firstCharacterSort = firstCharacterSort.to_a
        size = 0
        

        puts '<div class="center mt-5">'
    puts '<div class="pagination">'
    if (pageNumber.to_i == 1)
        puts '<a class="active" href="discover.cgi?sort=az&pageNumber=1">A-D</a>'
    else
        puts '<a href="discover.cgi?sort=az&pageNumber=1">A-D</a>'
    end
    if (pageNumber.to_i == 2)
        puts '<a class="active" href="discover.cgi?sort=az&pageNumber=2">E-H</a>'
    else
        puts '<a href="discover.cgi?sort=az&pageNumber=2">E-H</a>'
    end
    if (pageNumber.to_i == 3)
        puts '<a class="active" href="discover.cgi?sort=az&pageNumber=3">I-L</a>'
    else
        puts '<a href="discover.cgi?sort=az&pageNumber=3">I-L</a>'
    end
    if (pageNumber.to_i == 4)
        puts '<a class="active" href="discover.cgi?sort=az&pageNumber=4">M-P</a>'
    else
        puts '<a href="discover.cgi?sort=az&pageNumber=4">M-P</a>'
    end
    if (pageNumber.to_i == 5)
        puts '<a class="active" href="discover.cgi?sort=az&pageNumber=5">Q-T</a>'
    else
        puts '<a href="discover.cgi?sort=az&pageNumber=5">Q-T</a>'
    end
    if (pageNumber.to_i == 6)
        puts '<a class="active" href="discover.cgi?sort=az&pageNumber=6">U-Z</a>'
    else
        puts '<a href="discover.cgi?sort=az&pageNumber=6">U-Z</a>'
    end
          puts '</div>'
        puts '</div>'
        
        (0...firstCharacterSort.size).each do |h|
            if (firstCharacterSort[size])
            puts '<div class="wrapper">'
            puts '<section class="carousel-section" id="section' + size.to_s() + '">'
                (0...5).each do |i|
                    if (firstCharacterSort[size])
                    puts '<div class="item">'
                    puts '<form action="series.cgi" method="POST">'
                        puts '<input type="image" src="' + firstCharacterSort[size]['imageName'] + '" alt="' + firstCharacterSort[size]['imageName'] + '">'
                        puts '<input type="hidden" name="clicked_image" value="' + firstCharacterSort[size]['imageName'] + '">'
                        puts '<input type="hidden" name="seasonNumber" value="' + 1.to_s + '">'
                        puts '<h5 style="text-align: center;">' + firstCharacterSort[size]['showName'].gsub("Fucking", "F***ing") + '</h5>'
                        size = size + 1
                    puts '</form>'
                    puts '</div>'
                    else
                        puts '<div class="Nothing">'
                            puts 'spacer'
                        puts '</div>'
                    end
                end
                puts '</section>'
            puts '</div>'
            puts '<br>'
        end
    end


    puts '<div class="center mt-5">'
    puts '<div class="pagination">'
    if (pageNumber.to_i == 1)
        puts '<a class="active" href="discover.cgi?sort=az&pageNumber=1">A-D</a>'
    else
        puts '<a href="discover.cgi?sort=az&pageNumber=1">A-D</a>'
    end
    if (pageNumber.to_i == 2)
        puts '<a class="active" href="discover.cgi?sort=az&pageNumber=2">E-H</a>'
    else
        puts '<a href="discover.cgi?sort=az&pageNumber=2">E-H</a>'
    end
    if (pageNumber.to_i == 3)
        puts '<a class="active" href="discover.cgi?sort=az&pageNumber=3">I-L</a>'
    else
        puts '<a href="discover.cgi?sort=az&pageNumber=3">I-L</a>'
    end
    if (pageNumber.to_i == 4)
        puts '<a class="active" href="discover.cgi?sort=az&pageNumber=4">M-P</a>'
    else
        puts '<a href="discover.cgi?sort=az&pageNumber=4">M-P</a>'
    end
    if (pageNumber.to_i == 5)
        puts '<a class="active" href="discover.cgi?sort=az&pageNumber=5">Q-T</a>'
    else
        puts '<a href="discover.cgi?sort=az&pageNumber=5">Q-T</a>'
    end
    if (pageNumber.to_i == 6)
        puts '<a class="active" href="discover.cgi?sort=az&pageNumber=6">U-Z</a>'
    else
        puts '<a href="discover.cgi?sort=az&pageNumber=6">U-Z</a>'
    end
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
if pageNumber.to_i == 8
    service = 'Tubi'
end
if pageNumber.to_i == 9
    service = 'Paramount+'
end


    puts '<div class="center mt-5">'
puts '<div class="pagination">'
    if pageNumber.to_i == 1 
        puts '<a class="active" href="discover.cgi?sort=streaming&pageNumber=1">Disney+</a>'
    else
        puts '<a href="discover.cgi?sort=streaming&pageNumber=1">Disney+</a>'
    end
    if pageNumber.to_i == 2 
        puts '<a class="active" href="discover.cgi?sort=streaming&pageNumber=2">Netflix</a>'
    else
        puts '<a href="discover.cgi?sort=streaming&pageNumber=2">Netflix</a>'
    end
    if pageNumber.to_i == 3 
        puts '<a class="active" href="discover.cgi?sort=streaming&pageNumber=3">Max</a>'
    else
        puts '<a href="discover.cgi?sort=streaming&pageNumber=3">Max</a>'
    end
    if pageNumber.to_i == 4 
        puts '<a class="active" href="discover.cgi?sort=streaming&pageNumber=4">Hulu</a>'
    else
        puts '<a href="discover.cgi?sort=streaming&pageNumber=4">Hulu</a>'
    end
    if pageNumber.to_i == 5 
        puts '<a class="active" href="discover.cgi?sort=streaming&pageNumber=5">Prime Video</a>'
    else
        puts '<a href="discover.cgi?sort=streaming&pageNumber=5">Prime Video</a>'
    end
    if pageNumber.to_i == 6 
        puts '<a class="active" href="discover.cgi?sort=streaming&pageNumber=6">Apple TV+</a>'
    else
        puts '<a href="discover.cgi?sort=streaming&pageNumber=6">Apple TV+</a>'
    end
    if pageNumber.to_i == 7 
        puts '<a class="active" href="discover.cgi?sort=streaming&pageNumber=7">Peacock</a>'
    else
        puts '<a href="discover.cgi?sort=streaming&pageNumber=7">Peacock</a>'
    end
    if pageNumber.to_i == 8 
        puts '<a class="active" href="discover.cgi?sort=streaming&pageNumber=8">Tubi</a>'
    else
        puts '<a href="discover.cgi?sort=streaming&pageNumber=8">Tubi</a>'
    end
    if pageNumber.to_i == 9
        puts '<a class="active" href="discover.cgi?sort=streaming&pageNumber=10">Paramount+</a>'
    else
        puts '<a href="discover.cgi?sort=streaming&pageNumber=10">Paramount+</a>'
    end
      puts '</div>'
    puts '</div>'

series = db.query("SELECT series.imageName, series.showName FROM streaming JOIN series ON streaming.seriesid = series.showid WHERE streaming.service = '" + service.to_s + "';")
streamings = series.to_a
size = streamings.size
size = 0
beginArray = 0
endArray = 5
(0...streamings.size).each do |i|
    if (streamings[size])
    puts '<div class="wrapper">'
    puts '<section class="carousel-section" id="section' + size.to_s() + '">'
        (0...5).each do |i|
            if (streamings[size])
            puts '<div class="item">'
            puts '<form action="series.cgi" method="POST">'
                puts '<input type="image" src="' + streamings[size]['imageName'] + '" alt="' + streamings[size]['imageName'] + '">'
                puts '<input type="hidden" name="clicked_image" value="' + streamings[size]['imageName'] + '">'
                puts '<input type="hidden" name="seasonNumber" value="1">'
                puts '<h5 style="text-align: center;">' + streamings[size]['showName'].gsub("Fucking", "F***ing") + '</h5>'
                size = size + 1
            puts '</form>'
            puts '</div>'
            else
                puts '<div class="Nothing">'
                puts 'spacer'
                puts '</div>'
            end
        end
        puts '</section>'
    puts '</div>'
    puts '<br>'
end 
end



puts '<div class="center mt-5">'
puts '<div class="pagination">'
    if pageNumber.to_i == 1 
        puts '<a class="active" href="discover.cgi?sort=streaming&pageNumber=1">Disney+</a>'
    else
        puts '<a href="discover.cgi?sort=streaming&pageNumber=1">Disney+</a>'
    end
    if pageNumber.to_i == 2 
        puts '<a class="active" href="discover.cgi?sort=streaming&pageNumber=2">Netflix</a>'
    else
        puts '<a href="discover.cgi?sort=streaming&pageNumber=2">Netflix</a>'
    end
    if pageNumber.to_i == 3 
        puts '<a class="active" href="discover.cgi?sort=streaming&pageNumber=3">Max</a>'
    else
        puts '<a href="discover.cgi?sort=streaming&pageNumber=3">Max</a>'
    end
    if pageNumber.to_i == 4 
        puts '<a class="active" href="discover.cgi?sort=streaming&pageNumber=4">Hulu</a>'
    else
        puts '<a href="discover.cgi?sort=streaming&pageNumber=4">Hulu</a>'
    end
    if pageNumber.to_i == 5 
        puts '<a class="active" href="discover.cgi?sort=streaming&pageNumber=5">Prime Video</a>'
    else
        puts '<a href="discover.cgi?sort=streaming&pageNumber=5">Prime Video</a>'
    end
    if pageNumber.to_i == 6 
        puts '<a class="active" href="discover.cgi?sort=streaming&pageNumber=6">Apple TV+</a>'
    else
        puts '<a href="discover.cgi?sort=streaming&pageNumber=6">Apple TV+</a>'
    end
    if pageNumber.to_i == 7 
        puts '<a class="active" href="discover.cgi?sort=streaming&pageNumber=7">Peacock</a>'
    else
        puts '<a href="discover.cgi?sort=streaming&pageNumber=7">Peacock</a>'
    end
    if pageNumber.to_i == 8 
        puts '<a class="active" href="discover.cgi?sort=streaming&pageNumber=8">Tubi</a>'
    else
        puts '<a href="discover.cgi?sort=streaming&pageNumber=8">Tubi</a>'
    end
    if pageNumber.to_i == 9
        puts '<a class="active" href="discover.cgi?sort=streaming&pageNumber=10">Paramount+</a>'
    else
        puts '<a href="discover.cgi?sort=streaming&pageNumber=10">Paramount+</a>'
    end
      puts '</div>'
    puts '</div>'
  puts '</div>'
  puts '<br>'
end

 puts '<script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.6/dist/umd/popper.min.js"
    integrity="sha384-oBqDVmMz4fnFO9gybYlQ2X9B5o4j2wJlFczXy33mu6g5U5gF6kZ4GiWfWc6b7pQ1f"
    crossorigin="anonymous"></script>'
 puts '<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>'
 puts '<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>'
 puts '<script src="Televised.js"></script>'

 puts '</body>'
 puts '</html>'