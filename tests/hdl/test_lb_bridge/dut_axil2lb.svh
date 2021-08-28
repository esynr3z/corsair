axil2lb dut (
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

// AXI-Lite master
axilite #(
    .ADDR_W (ADDR_W),
    .DATA_W (DATA_W),
    .STRB_W (STRB_W)
) mst (
    .clk    (clk)
);
