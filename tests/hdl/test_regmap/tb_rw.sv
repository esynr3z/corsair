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

logic [31:0] csr_lena_val;
logic [15:0] csr_lenb_val;

logic [11:0] csr_cnt_eva;
logic [11:0] csr_cnt_eva_new = 0;
logic csr_cnt_eva_upd = 0;
logic [11:0] csr_cnt_evb;
logic [11:0] csr_cnt_evb_new = 0;
logic csr_cnt_evb_upd = 0;

regs dut (
    // System
    .clk (clk),
    .rst (rst),
    // CSR: LENA
    .csr_lena_val (csr_lena_val),
    // CSR: LENB
    .csr_lenb_val (csr_lenb_val),
    // CSR: CNT
    .csr_cnt_eva     (csr_cnt_eva),
    .csr_cnt_eva_new (csr_cnt_eva_new),
    .csr_cnt_eva_upd (csr_cnt_eva_upd),
    .csr_cnt_evb     (csr_cnt_evb),
    .csr_cnt_evb_new (csr_cnt_evb_new),
    .csr_cnt_evb_upd (csr_cnt_evb_upd),
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
logic [ADDR_W-1:0] addr;
logic [DATA_W-1:0] data;
logic [STRB_W-1:0] strb;

// test RW registers with no modifiers
task test_basic;
    $display("%t, Start basic tests!", $time);
    // test LENA register
    // read after reset
    addr = 'h0;
    apb_mst.read(addr, data);
    if (data != 'h00000000)
        errors++;
    // write with read back
    data = 'hdeadbeef;
    apb_mst.write(addr, data);
    @(posedge clk);
    if (csr_lena_val != 'hdeadbeef)
        errors++;
    data = 'heeeeeeee;
    apb_mst.read(addr, data);
    if (data != 'hdeadbeef)
        errors++;
    // byte write with read back
    data = 'h66778899;
    strb = 'b0110;
    apb_mst.write(addr, data, strb);
    @(posedge clk);
    if (csr_lena_val != 'hde7788ef)
        errors++;
    data = 'heeeeeeee;
    apb_mst.read(addr, data);
    if (data != 'hde7788ef)
        errors++;

    // test LENB register
    // read after reset
    addr = 'h4;
    apb_mst.read(addr, data);
    if (data != 'h00ffff00)
        errors++;
    // write with read back
    data = 'hdeadbeef;
    apb_mst.write(addr, data);
    @(posedge clk);
    if (csr_lenb_val != 'hadbe)
        errors++;
    data = 'heeeeeeee;
    apb_mst.read(addr, data);
    if (data != 'h00adbe00)
        errors++;
    // byte write with read back
    data = 'h66778899;
    strb = 'b0010;
    apb_mst.write(addr, data, strb);
    @(posedge clk);
    if (csr_lenb_val != 'had88)
        errors++;
    data = 'heeeeeeee;
    apb_mst.read(addr, data);
    if (data != 'h00ad8800)
        errors++;
endtask

// test RW registers with external_update modifier
task test_ext_upd;
    $display("%t, Start external update tests!", $time);
    // test CNT register
    // write with read back
    addr = 'h10;
    data = 'hdeadbeef;
    apb_mst.write(addr, data);
    @(posedge clk);
    if (csr_cnt_eva != 'heef)
        errors++;
    if (csr_cnt_evb != 'head)
        errors++;
    data = 'heeeeeeee;
    apb_mst.read(addr, data);
    if (data != 'h0ead0eef)
        errors++;

    // external update EVA bitfield
    @(posedge clk);
    csr_cnt_eva_upd = 1;
    csr_cnt_eva_new = 'hfff;
    @(posedge clk);
    csr_cnt_eva_upd = 0;
    @(posedge clk);
    if (csr_cnt_eva != 'hfff)
        errors++;
    data = 'heeeeeeee;
    apb_mst.read(addr, data);
    if (data != 'h0ead0fff)
        errors++;

    // write priority over external update
    data = 'h06660fff;
    fork
        begin
            @(posedge clk);
            @(posedge clk);
            csr_cnt_evb_upd = 1;
            csr_cnt_evb_new = 'h777;
            @(posedge clk);
            csr_cnt_evb_upd = 0;
        end
        apb_mst.write(addr, data);
    join
    @(posedge clk);
    if (csr_cnt_evb != 'h666)
        errors++;
    data = 'heeeeeeee;
    apb_mst.read(addr, data);
    if (data != 'h06660fff)
        errors++;
endtask

initial begin : main
    wait(!rst);
    repeat(5) @(posedge clk);

    test_basic();
    test_ext_upd();

    repeat(5) @(posedge clk);
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
