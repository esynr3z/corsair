`timescale 1ns/1ps

module tb_wo;

// Clock and reset
logic clk = 1'b0;
always #5 clk <= ~clk;

logic rst = 1'b1;
initial begin
    repeat (5) @(negedge clk);
    rst <= 1'b0;
end

// DUT
localparam ADDR_W = `DUT_ADDR_W;
localparam DATA_W = `DUT_DATA_W;
localparam STRB_W = DATA_W / 8;

logic              lb_wready;
logic [ADDR_W-1:0] lb_waddr;
logic [DATA_W-1:0] lb_wdata;
logic              lb_wen;
logic [STRB_W-1:0] lb_wstrb;
logic [DATA_W-1:0] lb_rdata;
logic              lb_rvalid;
logic [ADDR_W-1:0] lb_raddr;
logic              lb_ren;

// DUT
`include "dut.svh"

// Bridge to Local Bus
`ifdef BRIDGE_APB
    `include "bridge_apb2lb.svh"
`else
    $error("Unknown bridge!");
`endif

// Test body
int errors = 0;
logic [ADDR_W-1:0] addr;
logic [DATA_W-1:0] data;
logic [STRB_W-1:0] strb;

// test WO registers with no modifiers
task test_basic;
    $display("%t, Start basic tests!", $time);
    // test START register
    // simple write with hardware control
    addr = 'h30;
    data = 'hdeadbeef;
    mst.write(addr, data);
    @(posedge clk);
    if (csr_start_key_out != 'hdead)
        errors++;
    data = 'heeeeeeee;
    mst.read(addr, data);
    if (data != 0)
        errors++;
endtask

task test_self_clear;
    $display("%t, Start self clear tests!", $time);
    // test START register
    // siple write with hardware control
    addr = 'h30;
    data = 1 << 0;
    mst.write(addr, data);
    @(posedge clk);
    if (csr_start_en_out != 1)
        errors++;
    @(posedge clk);
    if (csr_start_en_out != 0)
        errors++;
endtask

initial begin : main
    wait(!rst);
    repeat(5) @(posedge clk);

    test_basic();
    test_self_clear();

    repeat(5) @(posedge clk);
    if (errors)
        $display("!@# TEST FAILED - %d ERRORS #@!", errors);
    else
        $display("!@# TEST PASSED #@!");
    $finish;
end

initial begin : timeout
    #5000;
    $display("!@# TEST FAILED - TIMEOUT #@!");
    $finish;
end

endmodule
