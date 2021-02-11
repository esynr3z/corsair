interface amm #(
  parameter ADDR_W = 16,
  parameter DATA_W = 32,
  parameter STRB_W = DATA_W/8
) (
  // synthesis translate_off
  input clk,
  input reset
  // synthesis translate_on
);

  logic [ADDR_W-1:0] address      ;
  logic              read_s       ;
  logic [DATA_W-1:0] readdata     ;
  logic              readdatavalid;
  logic [STRB_W-1:0] byteenable   ;
  logic              write_s      ;
  logic [DATA_W-1:0] writedata    ;
  logic              waitrequest  ;

  task write(
    input logic [ADDR_W-1:0] addr,
    input logic [DATA_W-1:0] data,
    input logic [STRB_W-1:0] strb = {STRB_W{1'b1}}
  );
    @(posedge clk);
    address = addr;
    writedata = data;
    byteenable = strb;
    write_s = 1;
    wait(~waitrequest);
    @(posedge clk);
    write_s = 0;
    address = 0;
    writedata = 0;
    byteenable = 0;
  endtask : write


  task read(
    input logic [ADDR_W-1:0] addr,
    output logic [DATA_W-1:0] data
  );
    @(posedge clk);
    address = addr;
    read_s = 1;
    wait(~waitrequest);
    @(posedge clk);
    read_s = 0;
    wait(readdatavalid);
    @(posedge clk);
    data = readdata;
  endtask : read

endinterface