//------------------------------------------------------------------------------
// SPI master interface:
//   - mode 0 only
//   - most significant bit transmitted first
//   - byte order from high to low
//
// Transaction format (bit by bit):
//   - address[msb]
//   - ...
//   - address[lsb]
//   - control[7] - 0 - read, 1 - write
//   - control[6:4] - 0
//   - control[3] - write byte strobe for 3rd byte
//   - ...
//   - control[0] - write byte strobe for 0th byte
//   - data[msb]
//   - ...
//   - data[lsb]
//------------------------------------------------------------------------------

interface spi #(
    parameter SCK_FREQ = 4e6,
    parameter ADDR_W   = 8,
    parameter DATA_W   = 8
);

localparam STRB_W = DATA_W / 8;

localparam SCK_PRD            = 1 / SCK_FREQ;

localparam TURNAROUND_W = 1;
localparam CTRL_W       = 8;

logic miso;     // SPI master input / slave output
logic mosi = 0; // SPI master output / slave input
logic sck  = 0; // SPI clock
logic cs_n = 1; // SPI chip select (active low)

bit mst_clk;
initial forever #(0.5ns * SCK_PRD * 1e9) mst_clk <= ~mst_clk;

task write (
    input logic [ADDR_W-1:0] addr,
    input logic [DATA_W-1:0] data,
    input logic [STRB_W-1:0] strb = {STRB_W{1'b1}}
);
    @(posedge mst_clk) cs_n <= 0;
    @(posedge mst_clk);
    fork
        begin : mosi_proc
            // transmit address
            foreach (addr[i]) begin
                if (i != (ADDR_W - 1))
                    @(negedge sck);
                mosi <= addr[i];
            end
            // transmit control word
            @(negedge sck) mosi <= 1; // 1 for write
            repeat (CTRL_W - STRB_W - 1)
                @(negedge sck) mosi <= 0;
            foreach (strb[i])
                @(negedge sck) mosi <= strb[i];
            // transmit data
            foreach (data[i])
                @(negedge sck) mosi <= data[i];
        end
        begin : sck_proc
            repeat (ADDR_W + CTRL_W + DATA_W) begin
                @(posedge mst_clk) sck <= 1;
                @(negedge mst_clk) sck <= 0;
            end
        end
    join
    @(posedge mst_clk);
    @(posedge mst_clk) cs_n <= 1;
endtask

task read (
    input  logic [ADDR_W-1:0] addr,
    output logic [DATA_W-1:0] data
);
    @(posedge mst_clk) cs_n <= 0;
    @(posedge mst_clk);
    fork
        begin : mosi_proc
            // transmit address
            foreach (addr[i]) begin
                if (i != (ADDR_W - 1))
                    @(negedge sck);
                mosi <= addr[i];
            end
            // transmit control word + dummy data
            @(negedge sck) mosi <= 0; // 0 for read
        end
        begin : miso_proc
            // wait address + control word
            repeat (ADDR_W + CTRL_W)
                @(posedge sck);
            // receive data
            foreach (data[i])
                @(posedge sck) data[i] <= miso;
        end
        begin : sck_proc
            // transmit address + control byte
            repeat (ADDR_W + CTRL_W) begin
                @(posedge mst_clk) sck <= 1;
                @(negedge mst_clk) sck <= 0;
            end
            // turnaround delay
            repeat (TURNAROUND_W)
                @(posedge mst_clk);
            // receive data
            repeat (DATA_W) begin
                @(posedge mst_clk) sck <= 1;
                @(negedge mst_clk) sck <= 0;
            end
        end
    join
    @(posedge mst_clk);
    @(posedge mst_clk) cs_n <= 1;
endtask

endinterface