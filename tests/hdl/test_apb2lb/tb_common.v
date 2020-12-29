`timescale 1ns/1ps

module tb_common;

reg clk = 1'b0;
always #5 clk <= ~clk;

integer errors = 0;

initial begin : main
    $display("Hello from tb_common!");

    #100;

    if (errors)
        $display("!@# TEST FAILED #@!");
    else
        $display("!@# TEST PASSED #@!");
    $finish;
end

`ifdef __ICARUS__
initial begin
    $dumpfile("dump.vcd");
    $dumpvars(0, tb_common);
end
`endif

endmodule