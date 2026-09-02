# tcl script arguments
set entity_name [lindex $argv 0]
set vhdl_file [lindex $argv 1]
set constraints_file [lindex $argv 2]
set part_name [lindex $argv 3]
set report_dir [lindex $argv 4]
set proj_dir [lindex $argv 5]

# create a new vivado project
set project_name [file join $proj_dir $entity_name]
create_project $project_name -part $part_name

# add files
add_files $vhdl_file

# set VHDL-2008 standard
set_property FILE_TYPE {VHDL 2008} [get_files *.vhd]

add_files $constraints_file

# run synthesis
launch_runs synth_1
wait_on_run synth_1

# check for synthesis errors
if {[get_property PROGRESS [get_runs synth_1]] != "100%"} {
	puts "ERROR: Synthesis failed. Check the log files."

    # copy synthesis log
    set synth_log [file join $proj_dir $entity_name.runs synth_1 runme.log]
    file copy $synth_log [file join $report_dir synth.log]

	close_project
	exit 1
}

# export synthesis reports
open_run synth_1

report_timing -file [file join $report_dir synth_timing.rpt] 
report_utilization -file [file join $report_dir synth_utilization.rpt] 
report_power -file [file join $report_dir synth_power.rpt] 

# copy synthesis log
set synth_log [file join $proj_dir $entity_name.runs synth_1 runme.log]
file copy $synth_log [file join $report_dir synth.log]

# run implementation
launch_runs impl_1
wait_on_run impl_1

# check for implementation errors
if {[get_property PROGRESS [get_runs impl_1]] != "100%"} {
	puts "ERROR: Implementation failed. Check the log files."

    # copy implementation log
    set impl_log [file join $proj_dir $entity_name.runs impl_1 runme.log]
    file copy $impl_log [file join $report_dir impl.log]

	close_project
	exit 2
}

# export implementation reports
open_run impl_1

report_timing -file [file join $report_dir impl_timing.rpt] 
report_utilization -file  [file join $report_dir impl_utilization.rpt] 
report_power -file [file join $report_dir impl_power.rpt] 

# copy implementation log
set impl_log [file join $proj_dir $entity_name.runs impl_1 runme.log]
file copy $impl_log [file join $report_dir impl.log]

# close the project
close_project

# delete the project directory
file delete -force -- $proj_dir

exit 0
