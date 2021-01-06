`timescale 1ns/1ps

module tb_rw;

`include "tb_core.svh"

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

// test RW registers with write1_to_xxx modifier
task test_write1;
    $display("%t, Start write1 to set/clear/toggle tests!", $time);
    // test CTL register
    // hardware set, then write 1 to clear
    addr = 'h20;
    @(posedge clk);
    csr_ctl_done_upd = 1;
    csr_ctl_done_new = 1;
    @(posedge clk);
    csr_ctl_done_upd = 0;
    @(posedge clk);
    if (csr_ctl_done != 1)
        errors++;
    apb_mst.read(addr, data);
    if (((data >> 3) & 1) != 1)
        errors++;
    data = 1 << 3;
    apb_mst.write(addr, data);
    @(posedge clk);
    if (csr_ctl_done != 0)
        errors++;
    apb_mst.read(addr, data);
    if (((data >> 3) & 1) != 0)
        errors++;

    // write 1 to set, then hardware clear
    data = 1 << 5;
    apb_mst.write(addr, data);
    @(posedge clk);
    if (csr_ctl_gen != 1)
        errors++;
    apb_mst.read(addr, data);
    if (((data >> 5) & 1) != 1)
        errors++;
    @(posedge clk);
    csr_ctl_gen_upd = 1;
    csr_ctl_gen_new = 0;
    @(posedge clk);
    csr_ctl_gen_upd = 0;
    @(posedge clk);
    if (csr_ctl_gen != 0)
        errors++;
    apb_mst.read(addr, data);
    if (((data >> 5) & 1) != 0)
        errors++;

    // write 1 several time to toggle
    data = 1 << 16;
    apb_mst.write(addr, data);
    @(posedge clk);
    if (csr_ctl_mode != 1)
        errors++;
    apb_mst.read(addr, data);
    if (((data >> 16) & 1) != 1)
        errors++;
    apb_mst.write(addr, data);
    @(posedge clk);
    if (csr_ctl_mode != 0)
        errors++;
    apb_mst.read(addr, data);
    if (((data >> 16) & 1) != 0)
        errors++;
endtask

initial begin : main
    wait(!rst);
    repeat(5) @(posedge clk);

    test_basic();
    test_ext_upd();
    test_write1();

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
