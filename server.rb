# server.rb
require "xmlrpc/server"
require 'whole_history_rating'

$whr = WholeHistoryRating::Base.new(:w2 => 60)

class WHR
	def iterate(n)
		$whr.iterate(n)
		return n
	end
	def create_game(a,b,c,d,e)
		$whr.create_game(a,b,c,d,e)
		return 0
	end
	def ratings_for_player(n)
		$whr.ratings_for_player(n)
	end
	def run_one_iteration
		$whr.run_one_iteration
	end
end

server = XMLRPC::Server.new( 1234 )
server.add_handler("WHR", WHR.new)
server.add_multicall()
server.serve
