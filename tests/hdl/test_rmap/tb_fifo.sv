`timescale 1ns/1ps

module tb_fifo;

// Test environment with DUT and bridge to LocalBus
`include "env.svh"

// Test body
int errors = 0;
logic [ADDR_W-1:0] addr;
logic [DATA_W-1:0] data;
logic [STRB_W-1:0] strb;

logic [23:0] fifo [$];

task test_wo;
    $display("%t, Start FIFO write only tests!", $time);
    // push 5 elements to the fifo
    fifo.delete();
    addr = 'h68;
    csr_fifowo_data_wready = 1;
    fork
        for (int i=0; i<5; i++) begin
            mst.write(addr, (i + 4096) * i);
        end
        repeat (5) begin
            wait(csr_fifowo_data_wen);
            @(posedge clk);
            fifo.push_front(csr_fifowo_data_out);
            @(posedge clk);
        end
    join
    // push 1 more element after wait
    @(posedge clk);
    csr_fifowo_data_wready = 0;
    fork
        mst.write(addr, 24'hAABBCC);
        begin
            repeat (4) @(posedge clk);
            csr_fifowo_data_wready = 1;
            @(posedge clk);
            if (csr_fifowo_data_wen)
                fifo.push_front(csr_fifowo_data_out);
        end
    join
    // pop data and check
    for (int i=0; i<5; i++) begin
        if (fifo.pop_back() !== ((i + 4096) * i))
            errors++;
    end
    if (fifo.pop_front() != 24'hAABBCC)
        errors++;
endtask

task test_ro;
    $display("%t, Start FIFO read only tests!", $time);
    // push 5 elements to the fifo
    fifo.delete();
    for (int i=0; i<5; i++) begin
        fifo.push_front((i + 4096) * i);
    end
    addr = 'h64;
    // read 5 elements from the fifo with data values control
    fork
        for (int i=0; i<5; i++) begin
            mst.read(addr, data);
            if (data !== ((i + 4096) * i))
                errors++;
        end
        for (int i=0; i<5; i++) begin
            wait (csr_fiforo_data_ren);
            repeat (i+1) @(posedge clk);
            csr_fiforo_data_in <= fifo.pop_back();
            csr_fiforo_data_rvalid <= 1'b1;
            @(posedge clk);
            csr_fiforo_data_rvalid <= 1'b0;
            @(posedge clk);
            @(posedge clk);
        end
    join
endtask

task test_rw;
    $display("%t, Start FIFO read/write tests!", $time);
    // push 5 elements to the fifo
    fifo.delete();
    addr = 'h60;
    csr_fiforw_data_wready = 1;
    fork
        for (int i=0; i<5; i++) begin
            mst.write(addr, (i + 4096) * i);
        end
        repeat (5) begin
            wait(csr_fiforw_data_wen);
            @(posedge clk);
            fifo.push_front(csr_fiforw_data_out);
            @(posedge clk);
        end
    join
    @(posedge clk);
    // read 5 elements from the fifo with data values control
    fork
        for (int i=0; i<5; i++) begin
            mst.read(addr, data);
            if (data !== ((i + 4096) * i))
                errors++;
        end
        for (int i=0; i<5; i++) begin
            wait (csr_fiforw_data_ren);
            repeat (i+1) @(posedge clk);
            csr_fiforw_data_in <= fifo.pop_back();
            csr_fiforw_data_rvalid <= 1'b1;
            @(posedge clk);
            csr_fiforw_data_rvalid <= 1'b0;
            @(posedge clk);
            @(posedge clk);
        end
    join
endtask

initial begin : main
    wait(!rst);
    repeat(5) @(posedge clk);

    test_wo();
    test_ro();
    test_rw();

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
