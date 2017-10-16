tables=ARGV.dup
tables.each do |table|
  puts "dropping #{table}"
  begin
    disable table
    drop table
  rescue
    puts "dropping #{table} failed, probably table does not exist"
  end
end
puts "done"
exit