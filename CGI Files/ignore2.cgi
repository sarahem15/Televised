#!/usr/bin/ruby
require 'cgi'
$stdout.sync=true
$stderr.reopen $stdout
cgi = CGI.new("html5")
print "content-type: text/html \r\n\r\n"
puts "<!doctype html>"
puts "<html>"
puts "<head><title>HTML + Ruby? Unpossible!</title></head>"
puts "<body>"
puts "<h1> Your favorite class is "+ cgi['fave_class'] + "</h1>"

if cgi['fave_class_explain'] != ''
  puts "You like this class because :" + cgi['fave_class_explain'] + "<br>"
end
if cgi['fave_class'] == 'databases'
  puts "You have great taste, but we can all agree sometimes the professor is a bastard"
end 
puts "</body>"
puts "</html>"
