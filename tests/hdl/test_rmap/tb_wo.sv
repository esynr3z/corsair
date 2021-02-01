`timescale 1ns/1ps

module tb_wo;

// Test environment with DUT and bridge to LocalBus
`include "env.svh"

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

task test_write_lock;
    $display("%t, Start write lock tests!", $time);
    // test START register
    addr = 'h30;
    data = 'hdeadbeef;
    mst.write(addr, data);
    @(posedge clk);
    csr_start_wlock = 1'b1;
    data = 'hc0de5432;
    mst.write(addr, data);
    @(posedge clk);
    if (csr_start_key_out != 'hdead)
        errors++;
endtask

initial begin : main
    wait(!rst);
    repeat(5) @(posedge clk);

    test_basic();
    test_self_clear();
    test_write_lock();

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
