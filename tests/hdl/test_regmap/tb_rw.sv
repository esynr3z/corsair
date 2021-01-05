`timescale 1ns/1ps

module tb_rw;

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

logic [31:0] csr_len_val;
logic [15:0] csr_cnt_val;

regs dut (
    // System
    .clk (clk),
    .rst (rst),
    // CSR: LEN
    .csr_len_val (csr_len_val),
    // CSR: CNT
    .csr_cnt_val (csr_cnt_val),
    // Local Bus
    .lb_waddr   (lb_waddr),
    .lb_wdata   (lb_wdata),
    .lb_wen     (lb_wen),
    .lb_wstrb   (lb_wstrb),
    .lb_wready  (lb_wready),
    .lb_raddr   (lb_raddr),
    .lb_ren     (lb_ren),
    .lb_rdata   (lb_rdata),
    .lb_rvalid  (lb_rvalid)
);

// Bridge to Local Bus
apb2lb apb2lb (
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

initial begin : main
    logic [ADDR_W-1:0] addr;
    logic [DATA_W-1:0] data;
    logic [STRB_W-1:0] strb;

    wait(!rst);

    // test LEN register
    // read after reset
    addr = 'h0;
    apb_mst.read(addr, data);
    if (data != 'h00000000)
        errors++;
    // write with read back
    data = 'hdeadbeef;
    apb_mst.write(addr, data);
    data = 'heeeeeeee;
    apb_mst.read(addr, data);
    if (data != 'hdeadbeef)
        errors++;
    // byte write with read back
    data = 'h66778899;
    strb = 'b0110;
    apb_mst.write(addr, data, strb);
    data = 'heeeeeeee;
    apb_mst.read(addr, data);
    if (data != 'hde7788ef)
        errors++;

    // test CNT register
    // read after reset
    addr = 'h4;
    apb_mst.read(addr, data);
    if (data != 'h00ffff00)
        errors++;
    // write with read back
    data = 'hdeadbeef;
    apb_mst.write(addr, data);
    data = 'heeeeeeee;
    apb_mst.read(addr, data);
    if (data != 'h00adbe00)
        errors++;
    // byte write with read back
    data = 'h66778899;
    strb = 'b0010;
    apb_mst.write(addr, data, strb);
    data = 'heeeeeeee;
    apb_mst.read(addr, data);
    if (data != 'h00ad8800)
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
