`timescale 1ns/1ps

module tb_fifo;

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

// DUT
`include "dut.svh"

// Bridge to Local Bus
`ifdef BRIDGE_APB
    `include "bridge_apb2lb.svh"
`else
    $error("Unknown bridge!");
`endif

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
            repeat (i) @(posedge clk);
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
            repeat (i) @(posedge clk);
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
    #5000;
    $display("!@# TEST FAILED - TIMEOUT #@!");
    $finish;
end

endmodule
