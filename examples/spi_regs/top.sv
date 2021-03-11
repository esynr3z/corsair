//------------------------------------------------------------------------------
// SPI register map project example
//------------------------------------------------------------------------------

module top (
    // SPI
    input  spi_sck,
    input  spi_cs_n,
    input  spi_mosi,
    output spi_miso,
    // LED
    output led_r,
    output led_g,
    output led_b
);

//------------------------------------------------------------------------------
// Clock and reset
//------------------------------------------------------------------------------
// HFOSC 48Mhz clock
logic clk;
SB_HFOSC #(
    .CLKHF_DIV("0b00") // no divide
) hfosc (
    .CLKHFEN(1'b1),
    .CLKHFPU(1'b1),
    .CLKHF(clk)
);

// Synchronous active high reset
logic [5:0] reset_cnt = 0;
logic rst = 1;
always_ff @(posedge clk) begin
    if (reset_cnt < '1) begin
        rst       <= 1;
        reset_cnt <= reset_cnt + 1;
    end else begin
        rst       <= 0;
    end
end

//------------------------------------------------------------------------------
// LED control
// RGB0 - red, RGB1 - green, RGB2 - blue
//------------------------------------------------------------------------------
logic led_r_en, led_g_en, led_b_en;

SB_LED_DRV_CUR rgb_cur (
    .EN    (1'b1),
    .LEDPU (rgb_pu)
);
SB_RGB_DRV #(
   .RGB0_CURRENT ("0b111111"), // 24mA current
   .RGB1_CURRENT ("0b111111"),
   .RGB2_CURRENT ("0b111111")
) rgb_drv (
   .RGBLEDEN (1'b1),
   .RGB0PWM  (led_r_en),
   .RGB1PWM  (led_g_en),
   .RGB2PWM  (led_b_en),
   .RGBPU    (rgb_pu),
   .RGB0     (led_r),
   .RGB1     (led_g),
   .RGB2     (led_b)
);

//------------------------------------------------------------------------------
// Data control for "FIFO"
// Actually, not FIFO, just imitation with simple counter
//------------------------------------------------------------------------------
logic [11:0] fifo_rdata;
logic        fifo_rvalid;
logic        fifo_ren;
logic        fifo_flush;

always_ff @(posedge clk) begin
    if (rst)
        fifo_rvalid <= 0;
    else if (fifo_ren && fifo_rvalid)
         fifo_rvalid <= 0;
    else if (fifo_ren)
         fifo_rvalid <= 1;
end

always_ff @(posedge clk) begin
    if (rst)
        fifo_rdata  <= 0;
    else if (fifo_flush)
        fifo_rdata <= 0;
    else if (fifo_ren && fifo_rvalid)
        fifo_rdata <= fifo_rdata + 1;
end

//------------------------------------------------------------------------------
// CSR map
//------------------------------------------------------------------------------
localparam DATA_W = 16;
localparam ADDR_W = 8;
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

spi2lb_rmap #(
    .ADDR_W (ADDR_W),
    .DATA_W (DATA_W)
) spi2lb (
    // System
    .clk (clk),
    .rst (rst),
    // SPI
    .spi_sck  (spi_sck),
    .spi_cs_n (1'b0),
    .spi_mosi (spi_mosi),
    .spi_miso (spi_miso),
    // Local Bus
    .lb_wready (lb_wready),
    .lb_waddr  (lb_waddr),
    .lb_wdata  (lb_wdata),
    .lb_wen    (lb_wen),
    .lb_wstrb  (lb_wstrb),
    .lb_rdata  (lb_rdata),
    .lb_rvalid (lb_rvalid),
    .lb_raddr  (lb_raddr),
    .lb_ren    (lb_ren)
);

rmap #(
    .ADDR_W (ADDR_W),
    .DATA_W (DATA_W)
) rmap (
    // System
    .clk (clk),
    .rst (rst),
    // CSR: LEDCTRL
    .csr_ledctrl_ren_out (led_r_en),
    .csr_ledctrl_gen_out (led_g_en),
    .csr_ledctrl_ben_out (led_b_en),
    // CSR: RDFIFO
    .csr_rdfifo_data_in     (fifo_rdata),
    .csr_rdfifo_data_rvalid (fifo_rvalid),
    .csr_rdfifo_data_ren    (fifo_ren),
    .csr_rdfifo_flush_out   (fifo_flush),
    // Local Bus
    .lb_waddr  (lb_waddr),
    .lb_wdata  (lb_wdata),
    .lb_wen    (lb_wen),
    .lb_wstrb  (lb_wstrb),
    .lb_wready (lb_wready),
    .lb_raddr  (lb_raddr),
    .lb_ren    (lb_ren),
    .lb_rdata  (lb_rdata),
    .lb_rvalid (lb_rvalid)
);

endmodule
