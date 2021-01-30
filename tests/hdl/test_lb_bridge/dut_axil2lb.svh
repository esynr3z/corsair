axil2lb dut (
    // CLK
    .clk (clk),
    // Reset
    .rst (rst),
    // APB
    .AXIL_AWADDR  (mst.AWADDR),
    .AXIL_AWPROT  (mst.AWPROT),
    .AXIL_AWVALID (mst.AWVALID),
    .AXIL_AWREADY (mst.AWREADY),
    .AXIL_WDATA   (mst.WDATA),
    .AXIL_WSTRB   (mst.WSTRB),
    .AXIL_WVALID  (mst.WVALID),
    .AXIL_WREADY  (mst.WREADY),
    .AXIL_BRESP   (mst.BRESP),
    .AXIL_BVALID  (mst.BVALID),
    .AXIL_BREADY  (mst.BREADY),
    .AXIL_ARADDR  (mst.ARADDR),
    .AXIL_ARPROT  (mst.ARPROT),
    .AXIL_ARVALID (mst.ARVALID),
    .AXIL_ARREADY (mst.ARREADY),
    .AXIL_RDATA   (mst.RDATA),
    .AXIL_RRESP   (mst.RRESP),
    .AXIL_RVALID  (mst.RVALID),
    .AXIL_RREADY  (mst.RREADY),
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
