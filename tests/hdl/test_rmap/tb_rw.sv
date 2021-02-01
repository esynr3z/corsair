`timescale 1ns/1ps

module tb_rw;

// Test environment with DUT and bridge to LocalBus
`include "env.svh"

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
    mst.read(addr, data);
    if (data != 'h00000000)
        errors++;
    // write with read back
    data = 'hdeadbeef;
    mst.write(addr, data);
    @(posedge clk);
    if (csr_lena_val_out != 'hdeadbeef)
        errors++;
    data = 'heeeeeeee;
    mst.read(addr, data);
    if (data != 'hdeadbeef)
        errors++;
    // byte write with read back
    data = 'h66778899;
    strb = 'b0110;
    mst.write(addr, data, strb);
    @(posedge clk);
    if (csr_lena_val_out != 'hde7788ef)
        errors++;
    data = 'heeeeeeee;
    mst.read(addr, data);
    if (data != 'hde7788ef)
        errors++;

    // test LENB register
    // read after reset
    addr = 'h4;
    mst.read(addr, data);
    if (data != 'h00ffff00)
        errors++;
    // write with read back
    data = 'hdeadbeef;
    mst.write(addr, data);
    @(posedge clk);
    if (csr_lenb_val_out != 'hadbe)
        errors++;
    data = 'heeeeeeee;
    mst.read(addr, data);
    if (data != 'h00adbe00)
        errors++;
    // byte write with read back
    data = 'h66778899;
    strb = 'b0010;
    mst.write(addr, data, strb);
    @(posedge clk);
    if (csr_lenb_val_out != 'had88)
        errors++;
    data = 'heeeeeeee;
    mst.read(addr, data);
    if (data != 'h00ad8800)
        errors++;
endtask

// test RW registers with hwu modifier
task test_ext_upd;
    $display("%t, Start external update tests!", $time);
    // test CNT register
    // write with read back
    addr = 'h10;
    data = 'hdeadbeef;
    mst.write(addr, data);
    @(posedge clk);
    if (csr_cnt_eva_out != 'heef)
        errors++;
    if (csr_cnt_evb_out != 'head)
        errors++;
    data = 'heeeeeeee;
    mst.read(addr, data);
    if (data != 'h0ead0eef)
        errors++;

    // external update EVA bitfield
    @(posedge clk);
    csr_cnt_eva_upd = 1;
    csr_cnt_eva_in = 'hfff;
    @(posedge clk);
    csr_cnt_eva_upd = 0;
    @(posedge clk);
    if (csr_cnt_eva_out != 'hfff)
        errors++;
    data = 'heeeeeeee;
    mst.read(addr, data);
    if (data != 'h0ead0fff)
        errors++;

    // write priority over external update
    data = 'h06660fff;
    fork
        begin
            @(posedge clk);
            @(posedge clk);
            csr_cnt_evb_upd = 1;
            csr_cnt_evb_in = 'h777;
            @(posedge clk);
            csr_cnt_evb_upd = 0;
        end
        mst.write(addr, data);
    join
    @(posedge clk);
    if (csr_cnt_evb_out != 'h666)
        errors++;
    data = 'heeeeeeee;
    mst.read(addr, data);
    if (data != 'h06660fff)
        errors++;
endtask

// test RW registers with write1_to_xxx modifier
task test_write1;
    $display("%t, Start write1 to set/clear/toggle tests!", $time);
    // test CTL register
    // hardware set, then write 1 to clear
    addr = 'h20;
    @(posedge clk);
    csr_ctl_done_upd = 1;
    csr_ctl_done_in = 1;
    @(posedge clk);
    csr_ctl_done_upd = 0;
    @(posedge clk);
    if (csr_ctl_done_out != 1)
        errors++;
    mst.read(addr, data);
    if (((data >> 3) & 1) != 1)
        errors++;
    data = 1 << 3;
    mst.write(addr, data);
    @(posedge clk);
    if (csr_ctl_done_out != 0)
        errors++;
    mst.read(addr, data);
    if (((data >> 3) & 1) != 0)
        errors++;

    // write 1 to set, then hardware clear
    data = 1 << 5;
    mst.write(addr, data);
    @(posedge clk);
    if (csr_ctl_gen_out != 1)
        errors++;
    mst.read(addr, data);
    if (((data >> 5) & 1) != 1)
        errors++;
    @(posedge clk);
    csr_ctl_gen_upd = 1;
    csr_ctl_gen_in = 0;
    @(posedge clk);
    csr_ctl_gen_upd = 0;
    @(posedge clk);
    if (csr_ctl_gen_out != 0)
        errors++;
    mst.read(addr, data);
    if (((data >> 5) & 1) != 0)
        errors++;

    // write 1 several time to toggle
    data = 1 << 16;
    mst.write(addr, data);
    @(posedge clk);
    if (csr_ctl_mode_out != 1)
        errors++;
    mst.read(addr, data);
    if (((data >> 16) & 1) != 1)
        errors++;
    mst.write(addr, data);
    @(posedge clk);
    if (csr_ctl_mode_out != 0)
        errors++;
    mst.read(addr, data);
    if (((data >> 16) & 1) != 0)
        errors++;
endtask

task test_access_strobes;
    $display("%t, Start access strobe tests!", $time);
    // test CNT register
    // read after reset
    addr = 'h10;
    fork
        mst.read(addr, data);
        begin
            wait(csr_cnt_rstrb);
            @(posedge clk);
            if (csr_cnt_rstrb != 1)
                errors++;
            @(posedge clk);
            if (csr_cnt_rstrb != 0)
                errors++;
        end
    join
    fork
        mst.write(addr, data);
        begin
            wait(csr_cnt_wstrb);
            @(posedge clk);
            if (csr_cnt_wstrb != 1)
                errors++;
            @(posedge clk);
            if (csr_cnt_wstrb != 0)
                errors++;
        end
    join
endtask

task test_write_lock;
    $display("%t, Start write lock tests!", $time);
    // test CNT register
    addr = 'h10;
    data = 12'h777;
    mst.write(addr, data);
    csr_cnt_wlock = 1'b1;
    data = 12'h666;
    mst.write(addr, data);
    mst.read(addr, data);
    if (data != 12'h777)
        errors++;
endtask

initial begin : main
    wait(!rst);
    repeat(5) @(posedge clk);

    test_basic();
    test_ext_upd();
    test_write1();
    test_access_strobes();
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
