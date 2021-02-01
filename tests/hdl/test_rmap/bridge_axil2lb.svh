axil2lb axil2lb (
    // CLK
    .clk (clk),
    // Reset
    .rst (rst),
    // APB
    .axil_awaddr  (mst.awaddr),
    .axil_awprot  (mst.awprot),
    .axil_awvalid (mst.awvalid),
    .axil_awready (mst.awready),
    .axil_wdata   (mst.wdata),
    .axil_wstrb   (mst.wstrb),
    .axil_wvalid  (mst.wvalid),
    .axil_wready  (mst.wready),
    .axil_bresp   (mst.bresp),
    .axil_bvalid  (mst.bvalid),
    .axil_bready  (mst.bready),
    .axil_araddr  (mst.araddr),
    .axil_arprot  (mst.arprot),
    .axil_arvalid (mst.arvalid),
    .axil_arready (mst.arready),
    .axil_rdata   (mst.rdata),
    .axil_rresp   (mst.rresp),
    .axil_rvalid  (mst.rvalid),
    .axil_rready  (mst.rready),
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

// AXI-Lite master
axilite #(
    .ADDR_W (ADDR_W),
    .DATA_W (DATA_W),
    .STRB_W (STRB_W)
) mst (
    .clk    (clk)
);
