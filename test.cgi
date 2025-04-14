#!/usr/bin/ruby
$stdout.sync = true
$stderr.reopen $stdout

puts "Content-type: text/html\n\n"
require 'mysql2'
require 'cgi'
require 'stringio'

db = Mysql2::Client.new(:host=>'10.20.3.4', :username=>'seniorproject25', :password=>'TV_Group123!', :database=>'televised_w25')

cgi = CGI.new
query = cgi['query']
query = query.gsub("=", "\=")

if query != ""
	query = query.gsub("=", "\=")
	puts query
end

puts"<html>"
puts"<head><title> Query Form </title></head>"
puts"<body>"
puts"	<h2> Query Form </h2>"

puts"	<form id='tags' name='dataEntryTags' action='test.cgi' method='post'>"
puts"   		Enter your MySQL query below. Please exlcude the semicolon (;) at the end. "
puts"   		<br>"
puts"   		<textarea name='query' class='form-control' rows='3' cols='100' required></textarea>"
puts"   		<br>"
puts"   		<br>"
puts"		<input type= 'submit' value='Submit'>"
puts"   	</form>"
puts"</body>"
puts"</html>"