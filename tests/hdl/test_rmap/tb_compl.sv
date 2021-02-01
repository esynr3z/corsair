`timescale 1ns/1ps

module tb_compl;

// Test environment with DUT and bridge to LocalBus
`include "env.svh"

// Test body
int errors = 0;
logic [ADDR_W-1:0] addr;
logic [DATA_W-1:0] data;
logic [STRB_W-1:0] strb;

task test_read;
    $display("%t, Start read tests!", $time);
    // test INTSTAT register
    // simple read with hardware control
    addr = 'h50;
    csr_intstat_ch0_in = 1;
    csr_intstat_ch1_in = 1;
    mst.read(addr, data);
    if ((data & 3) != 3)
        errors++;
    csr_intstat_ch0_in = 0;
    csr_intstat_ch1_in = 0;
    mst.read(addr, data);
    if ((data & 3) != 0)
        errors++;
endtask

task test_write;
    $display("%t, Start write tests!", $time);
    // test INTCLR register
    // siple write with hardware control
    addr = 'h50;
    data = 1 << 0;
    mst.write(addr, data);
    @(posedge clk);
    if (csr_intclr_ch0_out != 1)
        errors++;
    @(posedge clk);
    if (csr_intclr_ch0_out != 0)
        errors++;
    data = 1 << 1;
    mst.write(addr, data);
    @(posedge clk);
    if (csr_intclr_ch1_out != 1)
        errors++;
    @(posedge clk);
    if (csr_intclr_ch1_out != 0)
        errors++;
endtask

initial begin : main
    wait(!rst);
    repeat(5) @(posedge clk);

    test_read();
    test_write();

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
