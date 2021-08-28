interface apb #(
    parameter ADDR_W = 12,
    parameter DATA_W = 32,
    parameter STRB_W = DATA_W/8
)(
    input logic pclk,
    input logic presetn
);

logic              psel    = 1'b0;
logic [ADDR_W-1:0] paddr   = '0;
logic              penable = 1'b0;
logic              pwrite  = 1'b0;
logic [DATA_W-1:0] pwdata  = '0;
logic [STRB_W-1:0] pstrb   = '0;

logic [DATA_W-1:0] prdata;
logic              pready;
logic              pslverr;

task read (
    input  logic [ADDR_W-1:0] addr,
    output logic [DATA_W-1:0] data
);
    @(posedge pclk);
    paddr  <= addr;
    pwrite <= 1'b0;
    psel   <= 1'b1;

    @(posedge pclk);
    penable <= 1'b1;

    do @(posedge pclk);
    while (!pready);
    penable <= 1'b0;
    psel    <= 1'b0;

    data = prdata;
endtask

task write (
    input logic [ADDR_W-1:0] addr,
    input logic [DATA_W-1:0] data,
    input logic [STRB_W-1:0] strb = {STRB_W{1'b1}}
);
    @(posedge pclk);
    paddr  <= addr;
    pwdata <= data;
    pwrite <= 1'b1;
    pstrb  <= strb;
    psel   <= 1'b1;

    @(posedge pclk);
    penable <= 1'b1;

    do @(posedge pclk);
    while (!pready);
    pwdata  <= '0;
    penable <= 1'b0;
    pwrite  <= 1'b0;
    pstrb   <= '0;
    psel    <= 1'b0;
endtask

endinterface