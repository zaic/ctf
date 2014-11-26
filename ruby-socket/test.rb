require_relative 'sock.rb'

#
# Simple example
#
sock = CTFTCPSocket.new('localhost', 1807)
sock.puts 'hi'

# print recieved message to stdout
sock.gets

# print message to stderr
sock.stdout = false
sock.stderr = true
sock.gets

# print to file 'log.txt' and to stderr
sock.filename = 'log.txt'
sock.gets

# read lines from the socket until 'end' will be recieved
sock.expect 'end'

# read lines from the socket until number will be recieved
sock.expect { |s| s =~ /^\d+$/ }

sock.puts 'good bye'
