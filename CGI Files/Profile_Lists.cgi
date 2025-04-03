#!/usr/bin/ruby
require 'mysql2'
require 'cgi'
require 'cgi/session'

cgi = CGI.new
session = CGI::Session.new(cgi)
username = session['username']

list_id = cgi['listId'].to_i

db = Mysql2::Client.new(
    host: '10.20.3.4', 
    username: 'seniorproject25', 
    password: 'TV_Group123!', 
    database: 'televised_w25'
  )

# Delete from curatedListSeries
db.query("DELETE FROM curatedListSeries WHERE listId = #{list_id};")

# Delete from listOwnership
db.query("DELETE FROM listOwnership WHERE id = #{list_id};")

puts "Content-type: text/html\n\n"
puts "<html><body><script>alert('List deleted successfully.'); window.location.href='Profile_Lists.cgi';</script></body></html>"

session.close
