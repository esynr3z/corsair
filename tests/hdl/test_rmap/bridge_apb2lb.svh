apb2lb apb2lb (
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
    .wready  (lb_wready),
    .waddr   (lb_waddr),
    .wdata   (lb_wdata),
    .wen     (lb_wen),
    .wstrb   (lb_wstrb),
    .rdata   (lb_rdata),
    .rvalid  (lb_rvalid),
    .raddr   (lb_raddr),
    .ren     (lb_ren)
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