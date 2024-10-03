`timescale 1ns/1ps

module tb_ro;

// Test environment with DUT and bridge to LocalBus
`include "env.svh"
`define DBG 1
    
// Test body
int errors = 0;
logic [ADDR_W-1:0] addr;
logic [DATA_W-1:0] data;
logic [STRB_W-1:0] strb;

task test_ro_i;
    $display("%0t, Start RO+I tests!", $time);
    addr = CSR_REGRO_ADDR;
    `ifdef DBG
        $display("address %0x", addr);
    `endif
    // read
    mst.read(addr, data);
    if (data[CSR_REGRO_BFI_LSB+:CSR_REGRO_BFI_WIDTH] != 0)
    begin    
        errors++;
        $display("%0t, Expected 0, got %0x", $time, data);
    end    
    // update hardware value
    @(posedge clk);
    csr_regro_bfi_in = 100;
    // read again
    mst.read(addr, data);
    if (data[CSR_REGRO_BFI_LSB+:CSR_REGRO_BFI_WIDTH] != 100)
    begin    
        errors++;
        $display("%0t, Expected 100, got %0x", $time, data);
    end    
    // write has no effect
    data = 200 << CSR_REGRO_BFI_LSB;
    mst.write(addr, data);
    mst.read(addr, data);
    if (data[CSR_REGRO_BFI_LSB+:CSR_REGRO_BFI_WIDTH] != 100)
    begin
        errors++;
        $display("%0t, Expected 100, got %0x", $time, data);
    end    
    $display("%0t, %0d errors", $time, errors);
endtask

task test_ro_ie;
    $display("%0t, Start RO+IE tests!", $time);
    addr = CSR_REGRO_ADDR;
    // read
    mst.read(addr, data);
    if (data[CSR_REGRO_BFIE_LSB+:CSR_REGRO_BFIE_WIDTH] != 0)
        errors++;
    // update hardware value without enable
    @(posedge clk);
    csr_regro_bfie_in = 10;
    // read again
    mst.read(addr, data);
    if (data[CSR_REGRO_BFIE_LSB+:CSR_REGRO_BFIE_WIDTH] == 10)
        errors++;
    // update hardware value with enable
    @(posedge clk);
    csr_regro_bfie_en = 1;
    csr_regro_bfie_in = 13;
    @(posedge clk);
    csr_regro_bfie_en = 0;
    // read again
    mst.read(addr, data);
    if (data[CSR_REGRO_BFIE_LSB+:CSR_REGRO_BFIE_WIDTH] != 13)
        errors++;
    // write has no effect
    data = 9 << CSR_REGRO_BFIE_LSB;
    mst.write(addr, data);
    mst.read(addr, data);
    if (data[CSR_REGRO_BFIE_LSB+:CSR_REGRO_BFIE_WIDTH] != 13)
        errors++;
    $display("%0t, %0d errors", $time, errors);
endtask

task test_ro_f;
    $display("%0t, Start RO+F tests!", $time);
    addr = CSR_REGRO_ADDR;
    // read
    mst.read(addr, data);
    if (data[CSR_REGRO_BFF_LSB+:CSR_REGRO_BFF_WIDTH] != CSR_REGRO_BFF_RESET)
        errors++;
    // write has no effect
    data = 9 << CSR_REGRO_BFF_LSB;
    mst.write(addr, data);
    mst.read(addr, data);
    if (data[CSR_REGRO_BFF_LSB+:CSR_REGRO_BFF_WIDTH] != CSR_REGRO_BFF_RESET)
        errors++;
    $display("%0t, %0d errors", $time, errors);
endtask

task test_roc_ie;
    $display("%0t, Start ROC+IE tests!", $time);
    addr = CSR_REGROC_ADDR;
    // update hardware value
    @(posedge clk);
    csr_regroc_bfie_en = 1;
    csr_regroc_bfie_in = 13;
    @(posedge clk);
    csr_regroc_bfie_en = 0;
    // read
    mst.read(addr, data);
    if (data[CSR_REGROC_BFIE_LSB+:CSR_REGROC_BFIE_WIDTH] != 13)
        errors++;
    // read again
    mst.read(addr, data);
    if (data[CSR_REGROC_BFIE_LSB+:CSR_REGROC_BFIE_WIDTH] != 0)
        errors++;
    $display("%0t, %0d errors", $time, errors);
endtask

logic [CSR_REGROQ_BFIQ_WIDTH-1:0] fifo [$];
task test_ro_iq;
    $display("%0t, Start RO+IQ tests!", $time);
    // push 5 elements to the fifo
    fifo.delete();
    for (int i=1; i<6; i++) begin
        fifo.push_front((i + 4096) * i);
    end
    addr = CSR_REGROQ_ADDR;
    // read 5 elements from the fifo with data values control
    fork
        for (int i=1; i<6; i++) begin
            mst.read(addr, data);
            if (data !== ((i + 4096) * i))
                errors++;
        end
        csr_regroq_bfiq_rvalid <= 1'b1;
        csr_regroq_bfiq_in <= fifo.pop_back();
        for (int i=0; i<5; i++) begin
            wait (csr_regroq_bfiq_ren);
            repeat (i+1) @(posedge clk);
            if (i != 0) begin
                csr_regroq_bfiq_in <= fifo.pop_back();
                csr_regroq_bfiq_rvalid <= 1'b1;
            end
            @(posedge clk);
            csr_regroq_bfiq_rvalid <= 1'b0;
            @(posedge clk);
            @(posedge clk);
        end
    join
    $display("%0t, %0d errors", $time, errors);
endtask

task test_roll_i;
    $display("%0t, Start ROLL+I tests!", $time);
    addr = CSR_REGROLX_ADDR;
    // check latched value
    @(posedge clk);
    if (csr_regrolx_bfll_in != 1)
        errors++;
    mst.read(addr, data);
    if (data[CSR_REGROLX_BFLL_LSB+:CSR_REGROLX_BFLL_WIDTH] != 1)
        errors++;
    // latch value
    @(posedge clk);
    csr_regrolx_bfll_in <= 1'b0;
    mst.read(addr, data);
    if (data[CSR_REGROLX_BFLL_LSB+:CSR_REGROLX_BFLL_WIDTH] != 0)
        errors++;
    // check that is stucked at 0
    @(posedge clk);
    csr_regrolx_bfll_in <= 1'b1;
    mst.read(addr, data);
    if (data[CSR_REGROLX_BFLL_LSB+:CSR_REGROLX_BFLL_WIDTH] != 0)
        errors++;
    // read again
    mst.read(addr, data);
    if (data[CSR_REGROLX_BFLL_LSB+:CSR_REGROLX_BFLL_WIDTH] != 1)
        errors++;

    // check simultanious reading & latching -- latched value should not be reset
    fork
        mst.read(addr, data);
        begin // simultanious read with latching new tick
            @(posedge tb_ro.dut.csr_regrolx_ren);
            csr_regrolx_bfll_in <= 1'b0;
            @(posedge clk);
            csr_regrolx_bfll_in <= 1'b1;
        end
    join
    if (data[CSR_REGROLX_BFLL_LSB+:CSR_REGROLX_BFLL_WIDTH] != 1) errors++;
    mst.read(addr, data); // reading once more time to check that latch was not reset
    if (data[CSR_REGROLX_BFLL_LSB+:CSR_REGROLX_BFLL_WIDTH] != 0) errors++;

    // check latching just after read operation
    fork
        mst.read(addr, data);
        begin // simultanious read with latching new tick
            @(posedge tb_ro.dut.csr_regrolx_ren);
            @(posedge clk);
            csr_regrolx_bfll_in <= 1'b0;
            @(posedge clk);
            csr_regrolx_bfll_in <= 1'b1;
        end
    join
    if (data[CSR_REGROLX_BFLL_LSB+:CSR_REGROLX_BFLL_WIDTH] != 1) errors++;
    mst.read(addr, data); // reading once more time to check that latch was not reset
        if (data[CSR_REGROLX_BFLL_LSB+:CSR_REGROLX_BFLL_WIDTH] != 0) errors++;

    $display("%0t, %0d errors", $time, errors);
endtask

task test_rolh_i;
    $display("%0t, Start ROLH+I tests!", $time);
    addr = CSR_REGROLX_ADDR;
    // check latched value
    @(posedge clk);
    if (csr_regrolx_bflh_in != 0)
        errors++;
    mst.read(addr, data);
    if (data[CSR_REGROLX_BFLH_LSB+:CSR_REGROLX_BFLH_WIDTH] != 0)
        errors++;
    // latch value
    @(posedge clk);
    csr_regrolx_bflh_in <= 1'b1;
    mst.read(addr, data);
    if (data[CSR_REGROLX_BFLH_LSB+:CSR_REGROLX_BFLH_WIDTH] != 1)
        errors++;
    // check that is stucked at 1
    @(posedge clk);
    csr_regrolx_bflh_in <= 1'b0;
    mst.read(addr, data);
    if (data[CSR_REGROLX_BFLH_LSB+:CSR_REGROLX_BFLH_WIDTH] != 1)
        errors++;
    // read again
    mst.read(addr, data);
    if (data[CSR_REGROLX_BFLH_LSB+:CSR_REGROLX_BFLH_WIDTH] != 0)
        errors++;

    // check simultanious reading & latching -- latched value should not be reset
    fork
        mst.read(addr, data);
        begin // simultanious read with latching new tick
            @(posedge tb_ro.dut.csr_regrolx_ren);
            csr_regrolx_bflh_in <= 1'b1;
            @(posedge clk);
            csr_regrolx_bflh_in <= 1'b0;
        end
    join
    if (data[CSR_REGROLX_BFLH_LSB+:CSR_REGROLX_BFLH_WIDTH] != 0) errors++;
    mst.read(addr, data); // reading once more time to check that latch was not reset
    if (data[CSR_REGROLX_BFLH_LSB+:CSR_REGROLX_BFLH_WIDTH] != 1) errors++;

    // check latching just after read operation
    fork
        mst.read(addr, data);
        begin // simultanious read with latching new tick
            @(posedge tb_ro.dut.csr_regrolx_ren);
            @(posedge clk);
            csr_regrolx_bflh_in <= 1'b1;
            @(posedge clk);
            csr_regrolx_bflh_in <= 1'b0;
        end
    join
    if (data[CSR_REGROLX_BFLH_LSB+:CSR_REGROLX_BFLH_WIDTH] != 0) errors++;
    mst.read(addr, data); // reading once more time to check that latch was not reset
    if (data[CSR_REGROLX_BFLH_LSB+:CSR_REGROLX_BFLH_WIDTH] != 1) errors++;

    $display("%0t, %0d errors", $time, errors);
endtask

task test_roll_ie;
    $display("%0t, Start ROLL+IE tests!", $time);
    addr = CSR_REGROLX_ADDR;
    // check original value
    mst.read(addr, data);
    if (data[CSR_REGROLX_BFLLE_LSB+:CSR_REGROLX_BFLLE_WIDTH] != 1)
        errors++;
    // latch value without enable
    @(posedge clk);
    csr_regrolx_bflle_in <= 1'b0;
    mst.read(addr, data);
    if (data[CSR_REGROLX_BFLLE_LSB+:CSR_REGROLX_BFLLE_WIDTH] != 1)
        errors++;
    // latch value with enable
    @(posedge clk);
    csr_regrolx_bflle_en <= 1'b1;
    csr_regrolx_bflle_in <= 1'b0;
    @(posedge clk);
    csr_regrolx_bflle_en <= 1'b0;
    mst.read(addr, data);
    if (data[CSR_REGROLX_BFLLE_LSB+:CSR_REGROLX_BFLLE_WIDTH] != 0)
        errors++;
    // check that is stucked at 0
    @(posedge clk);
    csr_regrolx_bflle_en <= 1'b1;
    @(posedge clk);
    csr_regrolx_bflle_en <= 1'b0;
    @(posedge clk);
    csr_regrolx_bflle_in <= 1'b1;
    csr_regrolx_bflle_en <= 1'b1;
    @(posedge clk);
    csr_regrolx_bflle_en <= 1'b0;
    mst.read(addr, data);
    if (data[CSR_REGROLX_BFLLE_LSB+:CSR_REGROLX_BFLLE_WIDTH] != 0)
        errors++;
    // read again
    mst.read(addr, data);
    if (data[CSR_REGROLX_BFLLE_LSB+:CSR_REGROLX_BFLLE_WIDTH] != 1)
        errors++;
    
    // check simultanious reading & latching -- latched value should not be reset
    fork
        mst.read(addr, data);
        begin // simultanious read with latching new tick
            @(posedge tb_ro.dut.csr_regrolx_ren);
            csr_regrolx_bflle_in <= 1'b0;
            csr_regrolx_bflle_en <= 1'b1;
            @(posedge clk);
            csr_regrolx_bflle_in <= 1'b1;
            csr_regrolx_bflle_en <= 1'b0;
        end
    join
    if (data[CSR_REGROLX_BFLLE_LSB+:CSR_REGROLX_BFLLE_WIDTH] != 1) errors++;
    mst.read(addr, data); // reading once more time to check that latch was not reset
    if (data[CSR_REGROLX_BFLLE_LSB+:CSR_REGROLX_BFLLE_WIDTH] != 0) errors++;

    // check latching just after read operation
    fork
        mst.read(addr, data);
        begin // simultanious read with latching new tick
            @(posedge tb_ro.dut.csr_regrolx_ren);
            @(posedge clk);
            csr_regrolx_bflle_in <= 1'b0;
            csr_regrolx_bflle_en <= 1'b1;
            @(posedge clk);
            csr_regrolx_bflle_in <= 1'b1;
            csr_regrolx_bflle_en <= 1'b0;
        end
    join
    if (data[CSR_REGROLX_BFLLE_LSB+:CSR_REGROLX_BFLLE_WIDTH] != 1) errors++;
    mst.read(addr, data); // reading once more time to check that latch was not reset
    if (data[CSR_REGROLX_BFLLE_LSB+:CSR_REGROLX_BFLLE_WIDTH] != 0) errors++;

    $display("%0t, %0d errors", $time, errors);
endtask

task test_rolh_ie;
    $display("%0t, Start ROLH+IE tests!", $time);
    addr = CSR_REGROLX_ADDR;
    // check original value
    mst.read(addr, data);
    if (data[CSR_REGROLX_BFLHE_LSB+:CSR_REGROLX_BFLHE_WIDTH] != 0)
        errors++;
    // latch value without enable
    @(posedge clk);
    csr_regrolx_bflhe_in <= 1'b1;
    mst.read(addr, data);
    if (data[CSR_REGROLX_BFLHE_LSB+:CSR_REGROLX_BFLHE_WIDTH] != 0)
        errors++;
    // latch value with enable
    @(posedge clk);
    csr_regrolx_bflhe_en <= 1'b1;
    csr_regrolx_bflhe_in <= 1'b1;
    @(posedge clk);
    csr_regrolx_bflhe_en <= 1'b0;
    mst.read(addr, data);
    if (data[CSR_REGROLX_BFLHE_LSB+:CSR_REGROLX_BFLHE_WIDTH] != 1)
        errors++;
    // check that is stucked at 1
    @(posedge clk);
    csr_regrolx_bflhe_en <= 1'b1;
    @(posedge clk);
    csr_regrolx_bflhe_en <= 1'b0;
    @(posedge clk);
    csr_regrolx_bflhe_in <= 1'b0;
    csr_regrolx_bflhe_en <= 1'b1;
    @(posedge clk);
    csr_regrolx_bflhe_en <= 1'b0;
    mst.read(addr, data);
    if (data[CSR_REGROLX_BFLHE_LSB+:CSR_REGROLX_BFLHE_WIDTH] != 1)
        errors++;
    // read again
    mst.read(addr, data);
    if (data[CSR_REGROLX_BFLHE_LSB+:CSR_REGROLX_BFLHE_WIDTH] != 0)
        errors++;
    
    // check simultanious reading & latching -- latched value should not be reset
    fork
        mst.read(addr, data);
        begin // simultanious read with latching new tick
            @(posedge tb_ro.dut.csr_regrolx_ren);
            csr_regrolx_bflhe_in <= 1'b1;
            csr_regrolx_bflhe_en <= 1'b1;
            @(posedge clk);
            csr_regrolx_bflhe_in <= 1'b0;
            csr_regrolx_bflhe_en <= 1'b0;
        end
    join
    if (data[CSR_REGROLX_BFLHE_LSB+:CSR_REGROLX_BFLHE_WIDTH] != 0) errors++;
    mst.read(addr, data); // reading once more time to check that latch was not reset
    if (data[CSR_REGROLX_BFLHE_LSB+:CSR_REGROLX_BFLHE_WIDTH] != 1) errors++;

    // check latching just after read operation
    fork
        mst.read(addr, data);
        begin // simultanious read with latching new tick
            @(posedge tb_ro.dut.csr_regrolx_ren);
            @(posedge clk);
            csr_regrolx_bflhe_in <= 1'b1;
            csr_regrolx_bflhe_en <= 1'b1;
            @(posedge clk);
            csr_regrolx_bflhe_in <= 1'b0;
            csr_regrolx_bflhe_en <= 1'b0;
        end
    join
    if (data[CSR_REGROLX_BFLHE_LSB+:CSR_REGROLX_BFLHE_WIDTH] != 0) errors++;
    mst.read(addr, data); // reading once more time to check that latch was not reset
    if (data[CSR_REGROLX_BFLHE_LSB+:CSR_REGROLX_BFLHE_WIDTH] != 1) errors++;
    
    $display("%0t, %0d errors", $time, errors);
endtask

initial begin : main
    wait(!rst);
    repeat(5) @(posedge clk);

    test_ro_i();
    test_ro_ie();
    test_ro_f();
    test_roc_ie();
    test_ro_iq();
    test_roll_i();
    test_rolh_i();
    test_roll_ie();
    test_rolh_ie();

    repeat(5) @(posedge clk);
    if (errors)
        $display("!@# TEST FAILED - %d ERRORS #@!", errors);
    else
        $display("!@# TEST PASSED #@!");
    $finish;
end

initial begin : timeout
    #500us;
    $display("!@# TEST FAILED - TIMEOUT #@!");
    $finish;
end

endmodule
