#!/usr/bin/ruby
puts "Content-type: text/html\n\n"
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
listTitle = cgi['title']

db = Mysql2::Client.new(
    host: '10.20.3.4', 
    username: 'seniorproject25', 
    password: 'TV_Group123!', 
    database: 'televised_w25'
  )

haveWatched = db.query("SELECT seriesId FROM haveWatchedSeries WHERE username = '" + username.to_s + "';")
haveWatched = haveWatched.to_a
listContent = db.query("SELECT imageName, seriesId, showName FROM series JOIN curatedListSeries ON series.showId = curatedListSeries.seriesId WHERE name = '" + listTitle + "';")
listContent = listContent.to_a
displayName = db.query("SELECT displayName FROM account WHERE username = '" + username.to_s + "';")
puts '<!DOCTYPE html>'
puts '<html lang="en">'

puts '<head>'
  puts '<meta charset="UTF-8">'
  puts '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
  puts '<title>Televised</title>'
  puts '<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">'
  puts '<link rel="stylesheet" href="Televised.css">'
puts '</head>'
puts '<body id="listContent">'
  puts '<nav id="changingNav"></nav> <!-- This is where the navbar will be dynamically loaded -->'
  
  puts '<section class="contentList">'
  puts '<section class="UserDisplay" style="max-width: 390px">'
    puts '<img src="./ProfileImages/' + username.to_s + '.jpg" alt="">'
    puts '<h3>List by ' + displayName.first['displayName'].to_s + '</h3>'
  puts '</section>'
  puts '<br>'
  puts '<h1>' + listTitle.to_s + '</h1>'
  puts '<hr>'
  puts '<section class="contents">'
  puts '<div class="listContents">'
  (0...listContent.size).each do |i|
    puts '<div class="listItem">'
        puts '<form action="series.cgi" method="POST">'
          puts '<input type="image" src="' + listContent[i]['imageName'] + '" alt="' + listContent[i]['imageName'] + '">'
          puts '<input type="hidden" name="clicked_image" value="' + listContent[i]['imageName'] + '">'
          puts '<input type="hidden" name="seasonNumber" value="1">'
          puts '<h6 style="text-align: center">' + listContent[i]['showName'] + '</h6>'
       puts ' </form>'
   puts '</div>'
 end
       puts '<br>'
  puts '</div>'

  tempCount = 0
  if (haveWatched.size > 0)
  (0...listContent.size).each do |i|
    (0...haveWatched.size).each do |h|
      if (haveWatched[h]['seriesId'] == listContent[i]['seriesId'])
          tempCount = tempCount + 1
      end
    end
  end
end

  puts "<h6> You've watched " + tempCount.to_s + " of " + listContent.size.to_s + " </h6>"
puts '</section>'
puts '</section>'

   puts '<!-- Scripts -->'
  puts '<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>'
 puts ' <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>'
  puts '<script src="Televised.js"></script>'
puts '</body>'
puts '</html>'
session.close