`timescale 1ns/1ps

module tb_rw;

// Test environment with DUT and bridge to LocalBus
`include "env.svh"

// Test body
int errors = 0;
logic [ADDR_W-1:0] addr;
logic [DATA_W-1:0] data;
logic [STRB_W-1:0] strb;

task test_rw_o;
    $display("%0t, Start RW+O tests!", $time);
    // read after reset
    addr = CSR_REGRW_ADDR;
    mst.read(addr, data);
    if (data != CSR_REGRW_RESET)
        errors++;
    if (data[CSR_REGRW_BFO_LSB+:CSR_REGRW_BFO_WIDTH] != CSR_REGRW_BFO_RESET)
        errors++;
    // write with read back
    data = 3 << CSR_REGRW_BFO_LSB;
    mst.write(addr, data);
    @(posedge clk);
    if (csr_regrw_bfo_out != 3)
        errors++;
    mst.read(addr, data);
    if (data[CSR_REGRW_BFO_LSB+:CSR_REGRW_BFO_WIDTH] != 3)
        errors++;
    $display("%0t, %0d errors", $time, errors);
endtask

task test_rw_ioe;
    $display("%0t, Start RW+IOE tests!", $time);
    addr = CSR_REGRW_ADDR;
    // write with read back
    data = 10 << CSR_REGRW_BFIOE_LSB;
    mst.write(addr, data);
    @(posedge clk);
    if (csr_regrw_bfioe_out != 10)
        errors++;
    mst.read(addr, data);
    if (data[CSR_REGRW_BFIOE_LSB+:CSR_REGRW_BFIOE_WIDTH] != 10)
        errors++;
    // update bitfield from hardware
    @(posedge clk);
    csr_regrw_bfioe_en = 1;
    csr_regrw_bfioe_in = 12;
    @(posedge clk);
    csr_regrw_bfioe_en = 0;
    @(posedge clk);
    if (csr_regrw_bfioe_out != 12)
        errors++;
    mst.read(addr, data);
    if (data[CSR_REGRW_BFIOE_LSB+:CSR_REGRW_BFIOE_WIDTH] != 12)
        errors++;
    $display("%0t, %0d errors", $time, errors);
endtask

task test_rw_ioea;
    $display("%0t, Start RW+IOEA tests!", $time);
    addr = CSR_REGRW_ADDR;
    // write with read back
    data = 2 << CSR_REGRW_BFIOEA_LSB;
    mst.write(addr, data);
    @(posedge clk);
    if (csr_regrw_bfioea_out != 2)
        errors++;
    fork
        mst.read(addr, data);
        begin
            wait(csr_regrw_bfioea_raccess);
            @(posedge clk);
            if (csr_regrw_bfioea_raccess != 1)
                errors++;
            @(posedge clk);
            if (csr_regrw_bfioea_raccess != 0)
                errors++;
        end
    join
    if (data[CSR_REGRW_BFIOEA_LSB+:CSR_REGRW_BFIOEA_WIDTH] != 2)
        errors++;
    // update bitfield from hardware
    @(posedge clk);
    csr_regrw_bfioea_en = 1;
    csr_regrw_bfioea_in = 1;
    @(posedge clk);
    csr_regrw_bfioea_en = 0;
    @(posedge clk);
    if (csr_regrw_bfioea_out != 1)
        errors++;
    mst.read(addr, data);
    if (data[CSR_REGRW_BFIOEA_LSB+:CSR_REGRW_BFIOEA_WIDTH] != 1)
        errors++;
    $display("%0t, %0d errors", $time, errors);
endtask

task test_rw_ol;
    $display("%0t, Start RW+OL tests!", $time);
    addr = CSR_REGRW_ADDR;
    // write when locked
    csr_regrw_bfol_lock = 1;
    data = 128 << CSR_REGRW_BFOL_LSB;
    mst.write(addr, data);
    @(posedge clk);
    if (csr_regrw_bfol_out == 128)
        errors++;
    mst.read(addr, data);
    if (data[CSR_REGRW_BFOL_LSB+:CSR_REGRW_BFOL_WIDTH] == 128)
        errors++;
    // write when unlocked
    csr_regrw_bfol_lock = 0;
    data = 200 << CSR_REGRW_BFOL_LSB;
    mst.write(addr, data);
    @(posedge clk);
    if (csr_regrw_bfol_out != 200)
        errors++;
    mst.read(addr, data);
    if (data[CSR_REGRW_BFOL_LSB+:CSR_REGRW_BFOL_WIDTH] != 200)
        errors++;
    $display("%0t, %0d errors", $time, errors);
endtask

task test_rw_os;
    $display("%0t, Start RW+OS tests!", $time);
    addr = CSR_REGRW_ADDR;
    // read
    mst.read(addr, data);
    if (data[CSR_REGRW_BFOS_LSB+:CSR_REGRW_BFOS_WIDTH] != 0)
        errors++;
    // update by hardware
    @(posedge clk);
    csr_regrw_bfos_set = 1;
    @(posedge clk);
    csr_regrw_bfos_set = 0;
    @(posedge clk);
    if (csr_regrw_bfos_out != 1)
        errors++;
    mst.read(addr, data);
    if (data[CSR_REGRW_BFOS_LSB+:CSR_REGRW_BFOS_WIDTH] != 1)
        errors++;
    // write
    data = 0 << CSR_REGRW_BFOS_LSB;
    mst.write(addr, data);
    @(posedge clk);
    if (csr_regrw_bfos_out != 0)
        errors++;
    mst.read(addr, data);
    if (data[CSR_REGRW_BFOS_LSB+:CSR_REGRW_BFOS_WIDTH] != 0)
        errors++;
    $display("%0t, %0d errors", $time, errors);
endtask

task test_rw_oc;
    $display("%0t, Start RW+OC tests!", $time);
    addr = CSR_REGRW_ADDR;
    // write
    data = 1 << CSR_REGRW_BFOC_LSB;
    mst.write(addr, data);
    @(posedge clk);
    if (csr_regrw_bfoc_out != 1)
        errors++;
    mst.read(addr, data);
    if (data[CSR_REGRW_BFOC_LSB+:CSR_REGRW_BFOC_WIDTH] != 1)
        errors++;
    // update by hardware
    @(posedge clk);
    csr_regrw_bfoc_clr = 1;
    @(posedge clk);
    csr_regrw_bfoc_clr = 0;
    @(posedge clk);
    if (csr_regrw_bfoc_out != 0)
        errors++;
    mst.read(addr, data);
    if (data[CSR_REGRW_BFOC_LSB+:CSR_REGRW_BFOC_WIDTH] != 0)
        errors++;
    $display("%0t, %0d errors", $time, errors);
endtask

task test_rw_n;

    $display("%0t, Start RW+N tests!", $time);
    addr = CSR_REGRW_ADDR;
    // write
    data = 200 << CSR_REGRW_BFN_LSB;
    mst.write(addr, data);
    @(posedge clk);
    mst.read(addr, data);
    if (data[CSR_REGRW_BFN_LSB+:CSR_REGRW_BFN_WIDTH] != 200)
        errors++;
    $display("%0t, %0d errors", $time, errors);
endtask

logic [CSR_REGRWQ_BFIOQ_WIDTH-1:0] fifo [$];
task test_rw_q;
    $display("%0t, Start RW+Q tests!", $time);
    // push 5 elements to the fifo
    fifo.delete();
    addr = CSR_REGRWQ_ADDR;
    csr_regrwq_bfioq_wready = 1;
    fork
        for (int i=0; i<5; i++) begin
            mst.write(addr, (i + 200) * i);
        end
        repeat (5) begin
            wait(csr_regrwq_bfioq_wen);
            @(posedge clk);
            fifo.push_front(csr_regrwq_bfioq_out);
            @(posedge clk);
        end
    join
    @(posedge clk);
    // read 5 elements from the fifo with data values control
    fork
        for (int i=0; i<5; i++) begin
            mst.read(addr, data);
            if (data !== ((i + 200) * i))
                errors++;
        end
        for (int i=0; i<5; i++) begin
            wait (csr_regrwq_bfioq_ren);
            repeat (i+1) @(posedge clk);
            csr_regrwq_bfioq_in <= fifo.pop_back();
            csr_regrwq_bfioq_rvalid <= 1'b1;
            @(posedge clk);
            csr_regrwq_bfioq_rvalid <= 1'b0;
            @(posedge clk);
            @(posedge clk);
        end
    join
    $display("%0t, %0d errors", $time, errors);
endtask

task test_rw1c_s;
    $display("%0t, Start RW1C+S tests!", $time);
    addr = CSR_REGRW1X_ADDR;
    // read
    mst.read(addr, data);
    if (data[CSR_REGRW1X_BFC_LSB+:CSR_REGRW1X_BFC_WIDTH] != 0)
        errors++;
    // update by hardware
    @(posedge clk);
    csr_regrw1x_bfc_set = 1;
    @(posedge clk);
    csr_regrw1x_bfc_set = 0;
    @(posedge clk);
    mst.read(addr, data);
    if (data[CSR_REGRW1X_BFC_LSB+:CSR_REGRW1X_BFC_WIDTH] != 1)
        errors++;
    // write to clear
    data = 1 << CSR_REGRW1X_BFC_LSB;
    mst.write(addr, data);
    mst.read(addr, data);
    if (data[CSR_REGRW1X_BFC_LSB+:CSR_REGRW1X_BFC_WIDTH] != 0)
        errors++;
    $display("%0t, %0d errors", $time, errors);
endtask

task test_rw1s_c;
    $display("%0t, Start RW1S+C tests!", $time);
    addr = CSR_REGRW1X_ADDR;
    // read
    mst.read(addr, data);
    if (data[CSR_REGRW1X_BFS_LSB+:CSR_REGRW1X_BFS_WIDTH] != 1)
        errors++;
    // update by hardware
    @(posedge clk);
    csr_regrw1x_bfs_clr = 1;
    @(posedge clk);
    csr_regrw1x_bfs_clr = 0;
    @(posedge clk);
    mst.read(addr, data);
    if (data[CSR_REGRW1X_BFS_LSB+:CSR_REGRW1X_BFS_WIDTH] != 0)
        errors++;
    // write to set
    data = 1 << CSR_REGRW1X_BFS_LSB;
    mst.write(addr, data);
    mst.read(addr, data);
    if (data[CSR_REGRW1X_BFS_LSB+:CSR_REGRW1X_BFS_WIDTH] != 1)
        errors++;
    $display("%0t, %0d errors", $time, errors);
endtask

initial begin : main
    wait(!rst);
    repeat(5) @(posedge clk);

    test_rw_o();
    test_rw_ioe();
    test_rw_ioea();
    test_rw_ol();
    test_rw_os();
    test_rw_oc();
    test_rw_n();
    test_rw_q();
    test_rw1c_s();
    test_rw1s_c();

    repeat(5) @(posedge clk);
    if (errors)
        $display("!@# TEST FAILED - %0d ERRORS #@!", errors);
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
