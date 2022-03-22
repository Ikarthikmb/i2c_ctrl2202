// Copyright 2021 Google LLC.
// SPDX-License-Identifier: Apache-2.0
// 
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
// 
//     https://www.apache.org/licenses/LICENSE-2.0
// 
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

`timescale 1ns/1ns

module i2c_ctrl2202(

	input 				i_start,
	input					i_cclk,
	input					i_read,
	input					i_stop,
	input 	      i_sda,
	input		[7:1] i_address,
	input 	[8:1] i_txdata,
	output 	[8:1] i_rxdata,
	output 				o_scl,
	output 	reg		o_busy,
	output 	reg   o_sda

);
	
	reg 			a_ack;
	reg 			d_ack;
	reg 			stop_bit;
	reg [2:0] a_cycle;
	reg [3:0] x_cycle;
	reg [8:1] r_txdata;
	reg [8:1] r_rxdata;
	reg [7:1] r_i_address;
	reg [2:0] state;

	parameter	IDLE	= 3'b000,
						ADDR	= 3'b001,
						MODR 	= 3'b010,
						AACK 	= 3'b011,
						READ	= 3'b100,
						WRTE 	= 3'b101,
						FINL	= 3'b110;

	initial begin
		o_sda        <=  1'b0;
		o_busy       <=  1'b0;
		a_ack        <=  1'b0;
		d_ack        <=  'b0;
		stop_bit     <=  'b0;
		a_cycle      <=  3'b111;
		x_cycle      <=  'd8;
		r_txdata     <=  8'd0;
		r_rxdata     <=  8'd0;
		r_i_address  <=  7'b0;
		state        <=  3'b0;
	end

// State Machine
//==============
	
	always @(posedge i_cclk)
		case(state)
			// IDLE: Idle
			3'b000:	
				begin
					if(!i_start & !i_stop) begin
						o_sda        <=  1'b0;
						state        <=  ADDR;
						a_cycle      <=  3'b111;
						r_i_address  <=  i_address;
						o_busy       <=  1'b0;
					end

					else begin
						o_sda   <=  1'b1;
						state   <=  IDLE;
						o_busy  <=  1'b0;
					end
				end

			// ADDR: Addressing
			3'b001:
				begin
					if(a_cycle >= 3'b001) begin
						o_sda    <=  r_i_address[a_cycle];
						a_cycle  <=  a_cycle - 1'b1;
						state    <=  ADDR;
						o_busy   <=  1'b1;
					end

					else begin
						state   <=  MODR;
						o_busy  <=  1'b0;
					end
				end

			// MODR: Select between Read and Write
			3'b010:
				begin
						state <= AACK;
						o_sda <= i_read;
				end

			// AACK: Address Acknowledgement
			3'b011:
				begin
					if(i_sda) begin
						a_cycle  <=  3'b111;
						state    <=  ADDR;
						o_busy   <=  1'b0;
						o_sda     <=  1'b1;
					end

					else if(!i_sda) begin
						if(!i_read) begin
							state     <=  WRTE;
							x_cycle   <=  4'd8;
							o_sda     <=  1'b0;
							o_busy    <=  1'b0;
							r_txdata  <=  i_txdata;
						end

						else begin
   						state 		<= READ;
							x_cycle   <=  4'd8;
							o_sda     <=  1'b0;
							o_busy    <=  1'b0;
						end
					end
				end

			// READ: Read Operation
			3'b100:
				begin
					if(x_cycle >= 1) begin
							r_rxdata[x_cycle] <= i_sda;
							x_cycle <= x_cycle - 1'b1;
							o_busy <= 1'b1;
							state <= READ;
					end

					else begin
						state <= FINL;
						o_busy <= 1'b0;
						x_cycle <= 4'd8;
					end
				end

			// WRTE: Write Operation
			3'b101:
				begin
					if(x_cycle > 0) begin
							o_sda <= i_txdata[x_cycle];
							x_cycle <= x_cycle - 1'b1;
							o_busy <= 1'b1;
							state <= WRTE;
					end

					else begin
						state <= FINL;
						o_busy <= 1'b0;
						x_cycle <= 4'd8;
					end
				end

			// FINL: Data Acknowledgement and Stop
			3'b110:
				begin
					if(i_sda) begin
						state <= MODR; 
					end

					else begin
						o_sda <= 1'b1;
						state <= IDLE;
					end
				end

			default: state <= IDLE;
		endcase

// Controller clock

	assign o_scl = i_cclk;
	assign i_rxdata = r_rxdata;

endmodule
