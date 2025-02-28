#!/usr/bin/ruby
$stdout.sync = true
$stderr.reopen $stdout

puts "Content-type: text/html\n\n"
require 'mysql2'
require 'cgi'
require 'cgi/session'

cgi = CGI.new
session = CGI::Session.new(cgi)
username = session['username']


puts '<!DOCTYPE html>'
puts '<html lang="en">'

puts '<head>'
    puts '<meta charset="UTF-8">'
    puts '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
    puts '<title>Televised</title>'
    puts '<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">'
    puts '<link rel="stylesheet" href="Televised.css">'
puts '</head>'

puts '<body id="createNewList">'
    puts '<nav id="changingNav"></nav> <!-- Navbar dynamically loaded -->'
    puts '<div class="container-fluid">'
        puts '<br>'
        puts '<h2 style="text-align: center;">Create a New List</h2>'
        puts '<br>'
        puts '<div class="container">'
                puts '<div class="col-5" id="listRow">'
                    puts '<form id="newListForm" method="post" action="newList.cgi">'
                    puts '<span>Name</span>'
                    puts '<input type="text" id="Name" name="listName" class="form-control">'
                    puts '<br>'
        
                    puts '<label for="Type">Type</label>'
                    puts '<select id="Type" name="type" class="form-control">'
                        puts '<option value="Series">Series</option>'
                        puts '<option value="Seasons">Seasons</option>'
                        puts '<option value="Episodes">Episodes</option>'
                    puts '</select>'
                    puts '<br>'
                    puts '<label for="Views">Who Can View</label>'
                    puts '<select id="views" name="views" class="form-control">'
                        puts '<option value="Public">Public - anyone can view</option>'
                        puts '<option value="Private">Private - no one can view</option>'
                    puts '</select>'
                    puts '<br>'

                    puts '<span>Description</span>'
                    puts '<textarea id="Description" name="description" class="form-control" rows="10"></textarea>'
                    puts '<br>'
                    puts '<br>'
                    puts '<button id="saveList" class="btn" style="background-color: #9daef6;" type="submit">CREATE LIST</button>'
                puts '</form>'
                puts '</div>'
        puts '</div>'
    puts '</div>'
    puts '<br>'

    puts '<!-- Scripts -->'
    puts '<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>'
    puts '<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>'
    puts '<script src="Televised.js"></script>'
puts '</body>'
puts '</html>'

session.close