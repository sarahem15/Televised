 puts '<div class="TopFiveProfile">'
            puts '<form id="imageSearch" method="post" action="Profile_Settings.cgi">'
            puts '<select id="type" name="typeSearch" class="form-control">'
            if type == "Series"
                puts '<option value="Series" selected>Series &#9660</option>'
                puts '<option value="Season">Season</option>'
                puts '<option value="Episodes">Episodes</option>'
            elsif type == "Season"
                puts '<option value="Series">Series</option>'
                puts '<option value="Season" selected>Season &#9660</option>'
                puts '<option value="Episodes">Episodes</option>'
            else
                puts '<option value="Series">Series</option>'
                puts '<option value="Season">Season</option>'
                puts '<option value="Episodes" selected>Episodes &#9660</option>'
            end
            puts '</select>'
            if type == "Episodes"
                puts '<select id="type" name="seasonNum" class="form-control">'
                if seasonNum == '1'
                    puts '<option value="1" selected>1</option>'
                    puts '<option value="2">2</option>'
                    puts '<option value="3">3</option>'
                elsif seasonNum == '2'
                    puts '<option value="1">1</option>'
                    puts '<option value="2" selected>2</option>'
                    puts '<option value="3">3</option>'
                else
                    puts '<option value="1">1</option>'
                    puts '<option value="2">2</option>'
                    puts '<option value="3" selected>3</option>'
                end
                puts '</select>'
            end
                puts '<input type="text" name="top5search" class="top5search">'
                puts '<input type="submit" value="Search">'
            puts '</form>'

            puts '<br>'
            if (type == "Series" && search != "")
                images = db.query("SELECT showName, imageName, showId FROM series WHERE showName like '" + search + "%';")
                images = images.to_a
                if (images.first.to_s != "")
                    puts 'Is this the title you\'re looking for?'
                    puts '<br>'
                    arraySize = images.size
                    (0...arraySize).each do |i|
                        puts '<form method="get" action="Profile_Settings.cgi">'
                        puts images[i]['showName']
                        puts '<img src="' + images[i]['imageName'] + '" alt="' + images[i]['imageName'] + '" style=" height: 50px; width: 35px; object-fit: cover;">'
                        puts '<input type="hidden" name="topSeries" value="' + images[i]['showId'].to_s + '">'
                        puts '<input type="hidden" name="typeSearch" value="Series">'
                        puts '<input type="submit" value="SELECT">'
                        #puts '<input type="hidden" name="top5search" value="' + search + '">'
                        puts '</form>'
                        puts '<br>'
                        images[i]['imageName'] = ""
                    end 
                else
                    puts 'We can\'t seem to find this title!'
                end
            elsif (type == "Season" && search != "")
                images = db.query("SELECT showName, imageName, showId FROM series WHERE showName like '" + search + "%';")
                images = images.to_a
                if (images.first.to_s != "")
                    puts 'Is this the title you\'re looking for?'
                    puts '<br>'
                    arraySize = images.size
                    (0...arraySize).each do |i|
                        seasons = db.query("SELECT seasonId from season WHERE seriesId = '" + images[i]['showId'].to_s + "';")
                        seasons = seasons.to_a
                        #puts seasons.first['seasonId'].to_s
                        puts '<form method="get" action="Profile_Settings.cgi">'
                        puts images[i]['showName']
                        puts '<img src="' + images[i]['imageName'] + '" alt="' + images[i]['imageName'] + '" style=" height: 50px; width: 35px; object-fit: cover;">'
                        puts '<input type="hidden" name="topSeason" value="' + images[i]['showId'].to_s + '">'
                        puts '<input type="hidden" name="typeSearch" value="Season">'
                         puts '<select id="typeSeason" name="seasonNum" class="form-control">'
                         puts '<option value="" selected>Season</option>'
                            (0...seasons.size).each do |h|
                                puts '<option value="' + seasons[h]['seasonId'].to_s + '">' + (h+1).to_s + '</option>'
                            end
                        puts '</select>'
                        #puts '<input type="hidden" name="top5search" value="' + search + '">'
                        puts '</form>'
                        puts '<br>'
                        images[i]['imageName'] = ""
                    end 
                else
                    puts 'We can\'t seem to find this title!'
                end
            elsif (type == "Episodes" && search != "")
                images = db.query("SELECT showName, imageName, showId FROM series WHERE showName like '" + search + "%';")
                images = images.to_a
                if (images.first.to_s != "")
                    puts 'Is this the title you\'re looking for?'
                    puts '<br>'
                    arraySize = images.size
                    (0...arraySize).each do |i|
                        seasons = db.query("SELECT seasonId from season WHERE seriesId = '" + images[i]['showId'].to_s + "';")
                        seasons = seasons.to_a
                        #puts seasons.first['seasonId'].to_s
                        puts '<form method="get" action="Profile_Settings.cgi">'
                        puts images[i]['showName']
                        puts '<img src="' + images[i]['imageName'] + '" alt="' + images[i]['imageName'] + '" style=" height: 50px; width: 35px; object-fit: cover;">'
                        puts '<input type="hidden" name="topSeason" value="' + images[i]['showId'].to_s + '">'
                        puts '<input type="hidden" name="typeSearch" value="Episodes">'
                        episodes = db.query("SELECT * FROM episode JOIN season ON season.seasonId = episode.seasonId WHERE seasonNum = '" + seasonNum + "' AND seriesId = '" + images[i]['showId'].to_s + "';")
                        episodes = episodes.to_a
                        puts '<select id="typeSeason" name="epNum" class="form-control">'
                         puts '<option value="" selected>Episode</option>'
                            (0...episodes.size).each do |h|
                                puts '<option value="' + episodes[h]['epId'].to_s + '">' + episodes[h]['epName'] + '</option>'
                            end
                        puts '</select>'
                        #puts '<input type="hidden" name="top5search" value="' + search + '">'
                        puts '</form>'
                        puts '<br>'
                        images[i]['imageName'] = ""
                    end 
                else
                    puts 'We can\'t seem to find this title!'
                end
            end
    # <!-- Scripts -->
    puts '<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>'
    puts '<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>'
    puts '<script src="Televised.js"></script>'
    puts '<script>'
    puts "      document.getElementById('imageSearch').addEventListener('submit', function (event) {"
    puts "        }"
    puts '    document.addEventListener("click", function (event) {' 
    puts '        if (event.target.classList.contains("top5search")) {' 
    puts '    let top5search = event.target.dataset.top5search;'
    puts '}'
    puts "</script>"
    puts '</body>'

puts '</html>'
session.close
