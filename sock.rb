require 'socket'

class CTFTCPSocket < TCPSocket

    attr_accessor :stdout;
    attr_accessor :stderr;
    attr_accessor :filename;

    def initialize(host, port, to_stdout = true, to_stderr = false, to_file = nil)
        super(host, port)
        @stdout = to_stdout
        @stderr = to_stderr
        @filename = to_file
        updateFile
    end

    def filename=(filename)
        @filename = filename
        updateFile
    end

    def updateFile
        @file_d = @filename ? File.open(@filename, 'w') : nil
    end

    def gets
        str = super.chomp
        $stdout.puts str if @stdout
        $stderr.puts str if @stderr
        @file_d.puts str if @file_d
        str
    end

    def expect(tpl = nil)
        res = []
        while str = gets
            res << str
            cond = (block_given? ? yield(str) : str == tpl)
            break if cond
        end
        res
    end

end
