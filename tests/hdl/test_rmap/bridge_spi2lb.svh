spi2lb spi2lb (
    // System
    .clk        (clk),
    .rst        (rst),
    // SPI
    .spi_miso   (mst.miso),
    .spi_mosi   (mst.mosi),
    .spi_sck    (mst.sck),
    .spi_cs_n   (mst.cs_n),
    // Local Bus
    .lb_wready  (lb_wready),
    .lb_waddr   (lb_waddr),
    .lb_wdata   (lb_wdata),
    .lb_wen     (lb_wen),
    .lb_wstrb   (lb_wstrb),
    .lb_rdata   (lb_rdata),
    .lb_rvalid  (lb_rvalid),
    .lb_raddr   (lb_raddr),
    .lb_ren     (lb_ren)
);

// SPI master
spi #(
    .SCK_FREQ (10e6),
    .ADDR_W (ADDR_W),
    .DATA_W (DATA_W)
) mst ();
