###############################################################################
# Created by write_sdc
# Tue Mar 22 08:08:42 2022
###############################################################################
current_design i2c_ctrl2202
###############################################################################
# Timing Constraints
###############################################################################
create_clock -name i_cclk -period 10.0000 [get_ports {i_cclk}]
set_clock_transition 0.1500 [get_clocks {i_cclk}]
set_clock_uncertainty 0.2500 i_cclk
set_propagated_clock [get_clocks {i_cclk}]
set_input_delay 2.0000 -clock [get_clocks {i_cclk}] -add_delay [get_ports {i_address[1]}]
set_input_delay 2.0000 -clock [get_clocks {i_cclk}] -add_delay [get_ports {i_address[2]}]
set_input_delay 2.0000 -clock [get_clocks {i_cclk}] -add_delay [get_ports {i_address[3]}]
set_input_delay 2.0000 -clock [get_clocks {i_cclk}] -add_delay [get_ports {i_address[4]}]
set_input_delay 2.0000 -clock [get_clocks {i_cclk}] -add_delay [get_ports {i_address[5]}]
set_input_delay 2.0000 -clock [get_clocks {i_cclk}] -add_delay [get_ports {i_address[6]}]
set_input_delay 2.0000 -clock [get_clocks {i_cclk}] -add_delay [get_ports {i_address[7]}]
set_input_delay 2.0000 -clock [get_clocks {i_cclk}] -add_delay [get_ports {i_read}]
set_input_delay 2.0000 -clock [get_clocks {i_cclk}] -add_delay [get_ports {i_sda}]
set_input_delay 2.0000 -clock [get_clocks {i_cclk}] -add_delay [get_ports {i_start}]
set_input_delay 2.0000 -clock [get_clocks {i_cclk}] -add_delay [get_ports {i_stop}]
set_input_delay 2.0000 -clock [get_clocks {i_cclk}] -add_delay [get_ports {i_txdata[1]}]
set_input_delay 2.0000 -clock [get_clocks {i_cclk}] -add_delay [get_ports {i_txdata[2]}]
set_input_delay 2.0000 -clock [get_clocks {i_cclk}] -add_delay [get_ports {i_txdata[3]}]
set_input_delay 2.0000 -clock [get_clocks {i_cclk}] -add_delay [get_ports {i_txdata[4]}]
set_input_delay 2.0000 -clock [get_clocks {i_cclk}] -add_delay [get_ports {i_txdata[5]}]
set_input_delay 2.0000 -clock [get_clocks {i_cclk}] -add_delay [get_ports {i_txdata[6]}]
set_input_delay 2.0000 -clock [get_clocks {i_cclk}] -add_delay [get_ports {i_txdata[7]}]
set_input_delay 2.0000 -clock [get_clocks {i_cclk}] -add_delay [get_ports {i_txdata[8]}]
set_output_delay 2.0000 -clock [get_clocks {i_cclk}] -add_delay [get_ports {i_rxdata[1]}]
set_output_delay 2.0000 -clock [get_clocks {i_cclk}] -add_delay [get_ports {i_rxdata[2]}]
set_output_delay 2.0000 -clock [get_clocks {i_cclk}] -add_delay [get_ports {i_rxdata[3]}]
set_output_delay 2.0000 -clock [get_clocks {i_cclk}] -add_delay [get_ports {i_rxdata[4]}]
set_output_delay 2.0000 -clock [get_clocks {i_cclk}] -add_delay [get_ports {i_rxdata[5]}]
set_output_delay 2.0000 -clock [get_clocks {i_cclk}] -add_delay [get_ports {i_rxdata[6]}]
set_output_delay 2.0000 -clock [get_clocks {i_cclk}] -add_delay [get_ports {i_rxdata[7]}]
set_output_delay 2.0000 -clock [get_clocks {i_cclk}] -add_delay [get_ports {i_rxdata[8]}]
set_output_delay 2.0000 -clock [get_clocks {i_cclk}] -add_delay [get_ports {o_busy}]
set_output_delay 2.0000 -clock [get_clocks {i_cclk}] -add_delay [get_ports {o_scl}]
set_output_delay 2.0000 -clock [get_clocks {i_cclk}] -add_delay [get_ports {o_sda}]
###############################################################################
# Environment
###############################################################################
set_load -pin_load 0.0334 [get_ports {o_busy}]
set_load -pin_load 0.0334 [get_ports {o_scl}]
set_load -pin_load 0.0334 [get_ports {o_sda}]
set_load -pin_load 0.0334 [get_ports {i_rxdata[8]}]
set_load -pin_load 0.0334 [get_ports {i_rxdata[7]}]
set_load -pin_load 0.0334 [get_ports {i_rxdata[6]}]
set_load -pin_load 0.0334 [get_ports {i_rxdata[5]}]
set_load -pin_load 0.0334 [get_ports {i_rxdata[4]}]
set_load -pin_load 0.0334 [get_ports {i_rxdata[3]}]
set_load -pin_load 0.0334 [get_ports {i_rxdata[2]}]
set_load -pin_load 0.0334 [get_ports {i_rxdata[1]}]
set_driving_cell -lib_cell sky130_fd_sc_hd__inv_2 -pin {Y} -input_transition_rise 0.0000 -input_transition_fall 0.0000 [get_ports {i_cclk}]
set_driving_cell -lib_cell sky130_fd_sc_hd__inv_2 -pin {Y} -input_transition_rise 0.0000 -input_transition_fall 0.0000 [get_ports {i_read}]
set_driving_cell -lib_cell sky130_fd_sc_hd__inv_2 -pin {Y} -input_transition_rise 0.0000 -input_transition_fall 0.0000 [get_ports {i_sda}]
set_driving_cell -lib_cell sky130_fd_sc_hd__inv_2 -pin {Y} -input_transition_rise 0.0000 -input_transition_fall 0.0000 [get_ports {i_start}]
set_driving_cell -lib_cell sky130_fd_sc_hd__inv_2 -pin {Y} -input_transition_rise 0.0000 -input_transition_fall 0.0000 [get_ports {i_stop}]
set_driving_cell -lib_cell sky130_fd_sc_hd__inv_2 -pin {Y} -input_transition_rise 0.0000 -input_transition_fall 0.0000 [get_ports {i_address[7]}]
set_driving_cell -lib_cell sky130_fd_sc_hd__inv_2 -pin {Y} -input_transition_rise 0.0000 -input_transition_fall 0.0000 [get_ports {i_address[6]}]
set_driving_cell -lib_cell sky130_fd_sc_hd__inv_2 -pin {Y} -input_transition_rise 0.0000 -input_transition_fall 0.0000 [get_ports {i_address[5]}]
set_driving_cell -lib_cell sky130_fd_sc_hd__inv_2 -pin {Y} -input_transition_rise 0.0000 -input_transition_fall 0.0000 [get_ports {i_address[4]}]
set_driving_cell -lib_cell sky130_fd_sc_hd__inv_2 -pin {Y} -input_transition_rise 0.0000 -input_transition_fall 0.0000 [get_ports {i_address[3]}]
set_driving_cell -lib_cell sky130_fd_sc_hd__inv_2 -pin {Y} -input_transition_rise 0.0000 -input_transition_fall 0.0000 [get_ports {i_address[2]}]
set_driving_cell -lib_cell sky130_fd_sc_hd__inv_2 -pin {Y} -input_transition_rise 0.0000 -input_transition_fall 0.0000 [get_ports {i_address[1]}]
set_driving_cell -lib_cell sky130_fd_sc_hd__inv_2 -pin {Y} -input_transition_rise 0.0000 -input_transition_fall 0.0000 [get_ports {i_txdata[8]}]
set_driving_cell -lib_cell sky130_fd_sc_hd__inv_2 -pin {Y} -input_transition_rise 0.0000 -input_transition_fall 0.0000 [get_ports {i_txdata[7]}]
set_driving_cell -lib_cell sky130_fd_sc_hd__inv_2 -pin {Y} -input_transition_rise 0.0000 -input_transition_fall 0.0000 [get_ports {i_txdata[6]}]
set_driving_cell -lib_cell sky130_fd_sc_hd__inv_2 -pin {Y} -input_transition_rise 0.0000 -input_transition_fall 0.0000 [get_ports {i_txdata[5]}]
set_driving_cell -lib_cell sky130_fd_sc_hd__inv_2 -pin {Y} -input_transition_rise 0.0000 -input_transition_fall 0.0000 [get_ports {i_txdata[4]}]
set_driving_cell -lib_cell sky130_fd_sc_hd__inv_2 -pin {Y} -input_transition_rise 0.0000 -input_transition_fall 0.0000 [get_ports {i_txdata[3]}]
set_driving_cell -lib_cell sky130_fd_sc_hd__inv_2 -pin {Y} -input_transition_rise 0.0000 -input_transition_fall 0.0000 [get_ports {i_txdata[2]}]
set_driving_cell -lib_cell sky130_fd_sc_hd__inv_2 -pin {Y} -input_transition_rise 0.0000 -input_transition_fall 0.0000 [get_ports {i_txdata[1]}]
set_timing_derate -early 0.9500
set_timing_derate -late 1.0500
###############################################################################
# Design Rules
###############################################################################
set_max_fanout 5.0000 [current_design]
