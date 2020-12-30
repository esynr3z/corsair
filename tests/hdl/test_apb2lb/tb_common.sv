`timescale 1ns/1ps

module tb_common;

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

logic              lb_wready = 1'b1;
logic [ADDR_W-1:0] lb_waddr;
logic [DATA_W-1:0] lb_wdata;
logic              lb_wen;
logic [STRB_W-1:0] lb_wstrb;
logic [DATA_W-1:0] lb_rdata = '0;
logic              lb_rvalid = 1'b0;
logic [ADDR_W-1:0] lb_raddr;
logic              lb_ren;

apb2lb dut (
    // APB
    .psel    (apb_mst.psel),
    .paddr   (apb_mst.paddr),
    .penable (apb_mst.penable),
    .pwrite  (apb_mst.pwrite),
    .pwdata  (apb_mst.pwdata),
    .pstrb   (apb_mst.pstrb),
    .prdata  (apb_mst.prdata),
    .pready  (apb_mst.pready),
    .pslverr (apb_mst.pslverr),
    // Local Bus
    .wready  (lb_wready),
    .waddr   (lb_waddr),
    .wdata   (lb_wdata),
    .wen     (lb_wen),
    .wstrb   (lb_wstrb),
    .rdata   (lb_rdata),
    .rvalid  (lb_rvalid),
    .raddr   (lb_raddr),
    .ren     (lb_ren)
);

// APB master
apb #(
    .ADDR_W (ADDR_W),
    .DATA_W (DATA_W),
    .STRB_W (STRB_W)
) apb_mst (
    .pclk    (clk),
    .presetn (~rst)
);

// Test body
int errors = 0;

task validate_write(
    input logic [ADDR_W-1:0] addr,
    input logic [DATA_W-1:0] data,
    input logic [STRB_W-1:0] strb
);
    @(posedge clk);
    wait(lb_wen && lb_wready);
    @(posedge clk);
    if (lb_waddr != addr)
        errors++;
    if (lb_wdata != data)
        errors++;
    if (lb_wstrb != strb)
        errors++;
endtask

task handle_read(
    input  logic [ADDR_W-1:0] addr,
    input  int                waitstates = 1
);
    @(posedge clk);
    wait(lb_ren);
    repeat (waitstates) @(posedge clk);
    lb_rvalid <= 1'b1;
    case (addr)
        'h008: lb_rdata <= 'hdeadbeef;
        'h014: lb_rdata <= 'hc0debabe;
    endcase
    @(posedge clk);
    lb_rdata  <= 0;
    lb_rvalid <= 1'b0;
endtask

initial begin : main
    logic [ADDR_W-1:0] addr;
    logic [DATA_W-1:0] data;
    logic [STRB_W-1:0] strb;

    wait(!rst);

    // test simple write
    addr = 'h004;
    data = 'hdeadbeef;
    fork
        apb_mst.write(addr, data);
        validate_write(addr, data, {STRB_W{1'b1}});
    join

    // test write with byte strobes
    addr = 'h00c;
    data = 'hcafebabe;
    strb = 'b0110;
    fork
        apb_mst.write(addr, data, strb);
        validate_write(addr, data, strb);
    join

    // test write with wait states
    addr = 'h010;
    data = 'h0acce55;
    fork
        apb_mst.write(addr, data);
        validate_write(addr, data, {STRB_W{1'b1}});
        begin
            lb_wready <= 1'b0;
            repeat (5) @(posedge clk);
            lb_wready <= 1'b1;
        end
    join

    // test read
    addr = 'h014;
    fork
        apb_mst.read(addr, data);
        handle_read(addr);
    join
    if (data != 'hc0debabe)
        errors++;

    // test read with wait states
    addr = 'h008;
    fork
        apb_mst.read(addr, data);
        handle_read(addr, 5);
    join
    if (data != 'hdeadbeef)
        errors++;

    if (errors)
        $display("!@# TEST FAILED #@!");
    else
        $display("!@# TEST PASSED #@!");
    $finish;
end

`ifdef __ICARUS__
initial begin
    $dumpfile("dump.vcd");
    $dumpvars(0, `TOP_NAME);
end
`endif

endmodule
