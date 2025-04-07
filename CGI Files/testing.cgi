#!/usr/bin/ruby
require 'mysql2'
require 'cgi'
require 'cgi/session'
$stdout.sync = true
$stderr.reopen $stdout
# Print HTTP header
print "Content-type: text/html\r\n\r\n"

# Initialize CGI
cgi = CGI.new
session = CGI::Session.new(cgi)
puts session['username']
session.close