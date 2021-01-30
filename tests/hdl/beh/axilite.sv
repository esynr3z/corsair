interface axilite #(
  parameter ADDR_W = 16,
  parameter DATA_W = 32,
  parameter STRB_W = DATA_W/8
) (
  // synthesis translate_off
  input logic clk
  // synthesis translate_on
);

  logic [ADDR_W-1:0] awaddr;
  logic [2:0]        awprot;
  logic              awvalid;
  logic              awready;

  logic [DATA_W-1:0] wdata;
  logic [STRB_W-1:0] wstrb;
  logic              wvalid;
  logic              wready;

  logic [1:0]        bresp;
  logic              bvalid;
  logic              bready;

  logic [ADDR_W-1:0] araddr;
  logic [2:0]        arprot;
  logic              arvalid;
  logic              arready;

  logic [DATA_W-1:0] rdata;
  logic [1:0]        rresp;
  logic              rvalid;
  logic              rready;


  modport out (
    input awready, wready, bresp, bvalid, arready, rdata, rresp, rvalid,
    output awaddr, awprot, awvalid, wdata, wstrb, wvalid, bready, araddr, arprot, arvalid, rready
  );
  
  modport in (
    input awaddr, awprot, awvalid, wdata, wstrb, wvalid, bready, araddr, arprot, arvalid, rready,
    output awready, wready, bresp, bvalid, arready, rdata, rresp, rvalid
  );


  // synthesis translate_off

  task master_init;
    awaddr  <= 'b0;
    awprot  <= 'b0;
    awvalid <= 'b0;
    wdata   <= 'b0;
    wstrb   <= 'b0;
    wvalid  <= 'b0;
    bready  <= 'b0;
    araddr  <= 'b0;
    arprot  <= 'b0;
    arvalid <= 'b0;
    rready  <= 'b0;
  endtask

  task write(
    logic [ADDR_W-1:0] addr, 
    logic [DATA_W-1:0] data, 
    logic [STRB_W-1:0] strb = {STRB_W{1'b1}}
  );
    @(posedge clk);
    awvalid <= 1'b1;
    awaddr  <= addr;
    wait(awready == 1'b1);
    @(posedge clk);
    awvalid <= 1'b0;

    wvalid <= 1'b1;
    wdata  <= data;
    wstrb  <= strb;
    wait(wready == 1'b1);
    @(posedge clk);
    wvalid <= 1'b0;

    wait(bvalid == 1'b1);
    @(posedge clk);
    bready <= 1'b1;
    @(posedge clk);
    bready <= 1'b0;
  endtask

  task read(logic [ADDR_W-1:0] addr, output logic [DATA_W-1:0] data);
    
    arvalid <= 1'b1;
    araddr  <= addr;
    wait(arready == 1'b1);
    @(posedge clk);
    arvalid <= 1'b0;

    wait(rvalid == 1'b1);
    @(posedge clk);
    rready <= 1'b1;
    data   <= rdata;
    @(posedge clk);
    rready <= 1'b0;
  endtask

  // synthesis translate_on

endinterface //axilite