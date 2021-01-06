`timescale 1ns/1ps

module tb_ro;

`include "tb_core.svh"

// Test body
int errors = 0;
logic [ADDR_W-1:0] addr;
logic [DATA_W-1:0] data;
logic [STRB_W-1:0] strb;

// test RO registers with no modifiers
task test_basic;
    $display("%t, Start basic tests!", $time);
    // test STATUS register
    // simple read with hardware control
    addr = 'h40;
    csr_status_dir = 0;
    apb_mst.read(addr, data);
    if ((data >> 4) & 1 != 0)
        errors++;
    csr_status_dir = 1;
    apb_mst.read(addr, data);
    if ((data >> 4) & 1 != 1)
        errors++;
endtask

// test RO registers with external update
task test_ext_upd;
    $display("%t, Start external update tests!", $time);
    // test STATUS register
    addr = 'h40;
    // hardware update and read (also check that write has no action)
    apb_mst.read(addr, data);
    if (((data >> 8) & 1) != 0)
        errors++;
    @(posedge clk);
    csr_status_err_new = 1'b1;
    csr_status_err_upd = 1'b1;
    @(posedge clk);
    csr_status_err_upd = 1'b0;
    apb_mst.read(addr, data);
    if (((data >> 8) & 1) != 1)
        errors++;
    data = 0;
    apb_mst.write(addr, data);
    apb_mst.read(addr, data);
    if (((data >> 8) & 1) != 1)
        errors++;
endtask

// test RO registers with self clear
task test_self_clear;
    $display("%t, Start self clear tests!", $time);
    // test STATUS register
    addr = 'h40;
    // hardware control and several reads to validate self clear action (also check that write has no action)
    apb_mst.read(addr, data);
    if (((data >> 16) & 'hFFF) != 0)
        errors++;
    @(posedge clk);
    csr_status_cap_new = 'habc;
    csr_status_cap_upd = 1'b1;
    @(posedge clk);
    csr_status_cap_upd = 1'b0;
    data = 'hffffffff;
    apb_mst.write(addr, data);
    apb_mst.read(addr, data);
    if (((data >> 16) & 'hFFF) != 'habc)
        errors++;
    apb_mst.read(addr, data);
    if (((data >> 16) & 'hFFF) != 0)
        errors++;
endtask

// test RO registers with constants
task test_const;
    $display("%t, Start constatnts tests!", $time);
    // test VERSION register
    addr = 'h44;
    data = 'heeeeeeee;
    apb_mst.write(addr, data);
    apb_mst.read(addr, data);
    if (data != 'h00020010)
        errors++;
endtask

initial begin : main
    wait(!rst);
    repeat(5) @(posedge clk);

    test_basic();
    test_ext_upd();
    test_self_clear();
    test_const();

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
