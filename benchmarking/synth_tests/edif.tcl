# tcl script arguments
set module_name [lindex $argv 0]
set edif_file [lindex $argv 1]
set constraints_file [lindex $argv 2]
set part_name [lindex $argv 3]
set report_dir [lindex $argv 4]

#read the edif file
read_edif $edif_file

# read the constraints file
read_xdc $constraints_file

# link design
link_design -part $part_name

# synthesis reports
report_timing -file [file join $report_dir synth_timing.rpt]
report_utilization -file [file join $report_dir synth_utilization.rpt]
report_power -file [file join $report_dir synth_power.rpt]

# run implementation
if { [catch { opt_design } result] } {
    puts "ERROR: opt_design command failed: $result"
    exit 1
}
if { [catch { place_design } result] } {
    puts "ERROR: place_design command failed: $result"
    exit 1
}
if { [catch { route_design } result] } {
    puts "ERROR: route_design command failed: $result"
    exit 1
}

# implementation reports
report_timing -file [file join $report_dir impl_timing.rpt] 
report_utilization -file [file join $report_dir impl_utilization.rpt] 
report_power -file [file join $report_dir impl_power.rpt]


exit 0
