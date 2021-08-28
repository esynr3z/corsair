`timescale 1ns/1ps

module tb;

// Clock and reset
logic clk = 1'b0;
always #5 clk <= ~clk;

logic rst = `RESET_ACTIVE;
initial begin
    repeat (5) @(negedge clk);
    rst <= !`RESET_ACTIVE;
end

// DUT
localparam ADDR_W = `DUT_ADDR_W;
localparam DATA_W = `DUT_DATA_W;
localparam STRB_W = DATA_W / 8;

logic              wready = 1'b1;
logic [ADDR_W-1:0] waddr;
logic [DATA_W-1:0] wdata;
logic              wen;
logic [STRB_W-1:0] wstrb;
logic [DATA_W-1:0] rdata = '0;
logic              rvalid = 1'b0;
logic [ADDR_W-1:0] raddr;
logic              ren;

`ifdef DUT_APB
    `include "dut_apb2lb.svh"
`elsif DUT_AXIL
    `include "dut_axil2lb.svh"
`elsif DUT_AMM
    `include "dut_amm2lb.svh"
`elsif DUT_SPI
    `include "dut_spi2lb.svh"
`else
    $error("Unknown bridge!");
`endif

// Test body
int errors = 0;

task validate_write(
    input logic [ADDR_W-1:0] addr,
    input logic [DATA_W-1:0] data,
    input logic [STRB_W-1:0] strb
);
    @(posedge clk);
    wait(wen && wready);
    @(posedge clk);
    if (waddr != addr)
        errors++;
    if (wdata != data)
        errors++;
    if (wstrb != strb)
        errors++;
endtask

task handle_read(
    input  logic [ADDR_W-1:0] addr,
    input  int                waitstates = 1
);
    @(posedge clk);
    wait(ren);
    repeat (waitstates) @(posedge clk);
    rvalid <= 1'b1;
    case (addr)
        'h008: rdata <= 'hdeadbeef;
        'h014: rdata <= 'hc0debabe;
    endcase
    @(posedge clk);
    rdata  <= 0;
    rvalid <= 1'b0;
    @(posedge clk);
    if (ren != 0)
        errors++;
endtask

initial begin : main
    logic [ADDR_W-1:0] addr;
    logic [DATA_W-1:0] data;
    logic [STRB_W-1:0] strb;

    wait(rst == !`RESET_ACTIVE);

    // test simple write
    addr = 'h80000004;
    data = 'hdeadbeef;
    fork
        mst.write(addr, data);
        validate_write(addr, data, {STRB_W{1'b1}});
    join

    // test write with byte strobes
    addr = 'h00c;
    data = 'hcafebabe;
    strb = 'b0110;
    fork
        mst.write(addr, data, strb);
        validate_write(addr, data, strb);
    join

    // test write with wait states
    addr = 'h010;
    data = 'h0acce55;
    fork
        mst.write(addr, data);
        validate_write(addr, data, {STRB_W{1'b1}});
        begin
            wready <= 1'b0;
            repeat (800) @(posedge clk);
            wready <= 1'b1;
        end
    join

    // test read
    addr = 'h014;
    fork
        mst.read(addr, data);
        handle_read(addr);
    join
    if (data != 'hc0debabe)
        errors++;

    // test read with wait states
    addr = 'h008;
    fork
        mst.read(addr, data);
        handle_read(addr, 5);
    join
    if (data != 'hdeadbeef)
        errors++;

    if (errors)
        $display("!@# TEST FAILED - %d ERRORS #@!", errors);
    else
        $display("!@# TEST PASSED #@!");
    $finish;
end

initial begin : timeout
    #50us;
    $display("!@# TEST FAILED - TIMEOUT #@!");
    $finish;
end

endmodule
