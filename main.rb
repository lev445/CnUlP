# GPL-3 License
# Writed on ruby
# Main-point (client-side)

# Why not match-case?
# I'm not yanderedev, but this script, because. This not game =33
# Yanderedev, it's just joke, dont ban in your discord, lol

# require 'rbconfig'
require 'readline'

def main
  puts "Working..."
  system "clear"
  puts "Welcome to CnUlP net. I'm waiting for commands."
  begin
    loop do
      prompt = Readline.readline("cnulp0> ", true)
      if prompt == "help"
        puts "help\nstart  - starting network\ncredits  - who created net\nversion  - type program version\nbreak  - exit"
      elsif prompt == "credits"
        puts "credits\nlevvashuck  - created everything you see"
      elsif prompt == "version"
        puts "version\n1.0.0.a"
      elsif prompt == "start"
        puts "Checking python interpreter.."
        warn "SUPPORT ONLY PYTHON3"
        py_inte = RbConfig::CONFIG['bindir'] + '/python3'
        # I'm use linux-zen btw ;0
        py_inte = `which python3`.chomp unless File.executable?(py_inte)
        
        if File.executable?(py_inte)
          puts "Python3 found! #{py_inte}"
          unless File.file?("ioctl_manager.py")
            raise "FILE NOT FOUND: ioctl_manager.py. Reinstall program."
          end
          puts "STARTING IN 5 SECONDS..."
          puts "Ready! ;0" # Are you ready? ;0
          sleep 5 # SLEEP. Checking readiness user!
          system "clear"
          system "sudo #{py_inte} ioctl_manager.py"
        else  
          raise "python3 interpreter not found! Install it, please."
        end
      elsif prompt == "break"
        warn "Killing cnulp0 client-side (main.rb)..."
        break # I'm confused by this spaghetti code.... I put break on my eye...
      else
        warn "Command not found!"
        puts '--> Type "help" for help-page'
      end
    end
  rescue Interrupt
    puts "\n[0x00] ^C detected. Exiting gracefully..."
    exit
  end
end

main if __FILE__ == $0 # Call main point. Nothing special.
