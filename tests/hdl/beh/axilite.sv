interface axilite #(
  parameter ADDR_W = 16,
  parameter DATA_W = 32,
  parameter STRB_W = DATA_W/8
) (
  // synthesis translate_off
  input logic clk
  // synthesis translate_on
);

  logic [ADDR_W-1:0] AWADDR;
  logic [2:0]        AWPROT;
  logic              AWVALID;
  logic              AWREADY;

  logic [DATA_W-1:0] WDATA;
  logic [STRB_W-1:0] WSTRB;
  logic              WVALID;
  logic              WREADY;

  logic [1:0]        BRESP;
  logic              BVALID;
  logic              BREADY;

  logic [ADDR_W-1:0] ARADDR;
  logic [2:0]        ARPROT;
  logic              ARVALID;
  logic              ARREADY;

  logic [DATA_W-1:0] RDATA;
  logic [1:0]        RRESP;
  logic              RVALID;
  logic              RREADY;


  modport out (
    input AWREADY, WREADY, BRESP, BVALID, ARREADY, RDATA, RRESP, RVALID,
    output AWADDR, AWPROT, AWVALID, WDATA, WSTRB, WVALID, BREADY, ARADDR, ARPROT, ARVALID, RREADY
  );
  
  modport in (
    input AWADDR, AWPROT, AWVALID, WDATA, WSTRB, WVALID, BREADY, ARADDR, ARPROT, ARVALID, RREADY,
    output AWREADY, WREADY, BRESP, BVALID, ARREADY, RDATA, RRESP, RVALID
  );


  // synthesis translate_off

  task master_init;
    AWADDR  <= 'b0;
    AWPROT  <= 'b0;
    AWVALID <= 'b0;
    WDATA   <= 'b0;
    WSTRB   <= 'b0;
    WVALID  <= 'b0;
    BREADY  <= 'b0;
    ARADDR  <= 'b0;
    ARPROT  <= 'b0;
    ARVALID <= 'b0;
    RREADY  <= 'b0;
  endtask

  task write(
    logic [ADDR_W-1:0] addr, 
    logic [DATA_W-1:0] data, 
    logic [STRB_W-1:0] strb = {STRB_W{1'b1}}
  );
    @(posedge clk);
    AWVALID <= 1'b1;
    AWADDR  <= addr;
    wait(AWREADY == 1'b1);
    @(posedge clk);
    AWVALID <= 1'b0;

    WVALID <= 1'b1;
    WDATA  <= data;
    WSTRB  <= strb;
    wait(WREADY == 1'b1);
    @(posedge clk);
    WVALID <= 1'b0;

    wait(BVALID == 1'b1);
    @(posedge clk);
    BREADY <= 1'b1;
    @(posedge clk);
    BREADY <= 1'b0;
  endtask

  task read(logic [ADDR_W-1:0] addr, output logic [DATA_W-1:0] data);
    
    ARVALID <= 1'b1;
    ARADDR  <= addr;
    wait(ARREADY == 1'b1);
    @(posedge clk);
    ARVALID <= 1'b0;

    wait(RVALID == 1'b1);
    @(posedge clk);
    RREADY <= 1'b1;
    data   <= RDATA;
    @(posedge clk);
    RREADY <= 1'b0;
  endtask

  // synthesis translate_on

endinterface //axilite