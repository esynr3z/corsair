`timescale 1ns/1ps

module tb_wo;

`include "tb_core.svh"

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
    apb_mst.write(addr, data);
    @(posedge clk);
    if (csr_start_key_out != 'hdead)
        errors++;
    data = 'heeeeeeee;
    apb_mst.read(addr, data);
    if (data != 0)
        errors++;
endtask

task test_self_clear;
    $display("%t, Start self clear tests!", $time);
    // test START register
    // siple write with hardware control
    addr = 'h30;
    data = 1 << 0;
    apb_mst.write(addr, data);
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
