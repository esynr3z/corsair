apb2lb dut (
    // APB
    .psel    (mst.psel),
    .paddr   (mst.paddr),
    .penable (mst.penable),
    .pwrite  (mst.pwrite),
    .pwdata  (mst.pwdata),
    .pstrb   (mst.pstrb),
    .prdata  (mst.prdata),
    .pready  (mst.pready),
    .pslverr (mst.pslverr),
    // Local Bus
    .wready  (wready),
    .waddr   (waddr),
    .wdata   (wdata),
    .wen     (wen),
    .wstrb   (wstrb),
    .rdata   (rdata),
    .rvalid  (rvalid),
    .raddr   (raddr),
    .ren     (ren)
);

// APB master
apb #(
    .ADDR_W (ADDR_W),
    .DATA_W (DATA_W),
    .STRB_W (STRB_W)
) mst (
    .pclk    (clk),
    .presetn (~rst)
);
