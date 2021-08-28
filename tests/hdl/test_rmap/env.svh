`include "regs.vh"
import regs_pkg::*;

// Clock and reset
logic clk = 1'b0;
always #5 clk <= ~clk;

logic rst = `RESET_ACTIVE;
initial begin
    repeat (5) @(negedge clk);
    rst <= !`RESET_ACTIVE;
end

// DUT
localparam ADDR_W = CSR_ADDR_WIDTH;
localparam DATA_W = CSR_DATA_WIDTH;
localparam STRB_W = DATA_W / 8;

logic              wready;
logic [ADDR_W-1:0] waddr;
logic [DATA_W-1:0] wdata;
logic              wen;
logic [STRB_W-1:0] wstrb;
logic [DATA_W-1:0] rdata;
logic              rvalid;
logic [ADDR_W-1:0] raddr;
logic              ren;

// DUT
`include "dut.svh"
