// REGRW.BFO
logic [2:0] csr_regrw_bfo_out;
// REGRW.BFIOE
logic csr_regrw_bfioe_en = 0;
logic [3:0] csr_regrw_bfioe_in = 0;
logic [3:0] csr_regrw_bfioe_out;
// REGRW.BFIOEA
logic csr_regrw_bfioea_raccess;
logic csr_regrw_bfioea_waccess;
logic csr_regrw_bfioea_en = 0;
logic [1:0] csr_regrw_bfioea_in = 0;
logic [1:0] csr_regrw_bfioea_out;
// REGRW.BFOL
logic csr_regrw_bfol_lock = 0;
logic [7:0] csr_regrw_bfol_out;
// REGRW.BFOS
logic csr_regrw_bfos_set = 0;
logic  csr_regrw_bfos_out;
// REGRW.BFOC
logic csr_regrw_bfoc_clr = 0;
logic  csr_regrw_bfoc_out;
// REGRW.BFN

// REGRWQ.BFIOQ
logic csr_regrwq_bfioq_rvalid = 0;
logic csr_regrwq_bfioq_ren;
logic [11:0] csr_regrwq_bfioq_in = 0;
logic [11:0] csr_regrwq_bfioq_out;
logic csr_regrwq_bfioq_wready = 0;
logic csr_regrwq_bfioq_wen;

// REGRW1X.BFC
logic csr_regrw1x_bfc_set = 0;
// REGRW1X.BFS
logic csr_regrw1x_bfs_clr = 0;

// REGRO.BFI
logic [7:0] csr_regro_bfi_in = 0;
// REGRO.BFF
// REGRO.BFIE
logic csr_regro_bfie_en = 0;
logic [3:0] csr_regro_bfie_in = 0;

// REGROC.BFI
logic csr_regroc_bfie_en = 0;
logic [15:0] csr_regroc_bfie_in = 0;

// REGROQ.BFIQ
logic csr_regroq_bfiq_rvalid = 0;
logic csr_regroq_bfiq_ren;
logic [23:0] csr_regroq_bfiq_in = 0;

// REGROLX.BFLL
logic  csr_regrolx_bfll_in = 1;
// REGROLX.BFLH
logic  csr_regrolx_bflh_in = 0;
// REGROLX.BFLLE
logic csr_regrolx_bflle_en = 0;
logic csr_regrolx_bflle_in = 1;
    // REGROLX.BFLHE
logic csr_regrolx_bflhe_en = 0;
logic csr_regrolx_bflhe_in = 0;

// REGWO.BFWO
logic [3:0] csr_regwo_bfwo_out;
// REGWO.BFSC
logic  csr_regwo_bfsc_out;

// REGWOQ.BFOQ
logic [23:0] csr_regwoq_bfoq_out;
logic csr_regwoq_bfoq_wready = 0;
logic csr_regwoq_bfoq_wen;


regs dut (
    // System
    .clk (clk),
    .rst (rst),
    // REGRW.BFIO
    .csr_regrw_bfo_out (csr_regrw_bfo_out),
    // REGRW.BFIOE
    .csr_regrw_bfioe_en (csr_regrw_bfioe_en),
    .csr_regrw_bfioe_in (csr_regrw_bfioe_in),
    .csr_regrw_bfioe_out (csr_regrw_bfioe_out),
    // REGRW.BFIOEA
    .csr_regrw_bfioea_raccess (csr_regrw_bfioea_raccess),
    .csr_regrw_bfioea_waccess (csr_regrw_bfioea_waccess),
    .csr_regrw_bfioea_en (csr_regrw_bfioea_en),
    .csr_regrw_bfioea_in (csr_regrw_bfioea_in),
    .csr_regrw_bfioea_out (csr_regrw_bfioea_out),
    // REGRW.BFIOL
    .csr_regrw_bfol_lock (csr_regrw_bfol_lock),
    .csr_regrw_bfol_out (csr_regrw_bfol_out),
    // REGRW.BFOS
    .csr_regrw_bfos_set (csr_regrw_bfos_set),
    .csr_regrw_bfos_out (csr_regrw_bfos_out),
    // REGRW.BFOC
    .csr_regrw_bfoc_clr (csr_regrw_bfoc_clr),
    .csr_regrw_bfoc_out (csr_regrw_bfoc_out),
    // REGRW.BFN

    // REGRWQ.BFIOQ
    .csr_regrwq_bfioq_rvalid (csr_regrwq_bfioq_rvalid),
    .csr_regrwq_bfioq_ren (csr_regrwq_bfioq_ren),
    .csr_regrwq_bfioq_in (csr_regrwq_bfioq_in),
    .csr_regrwq_bfioq_out (csr_regrwq_bfioq_out),
    .csr_regrwq_bfioq_wready (csr_regrwq_bfioq_wready),
    .csr_regrwq_bfioq_wen (csr_regrwq_bfioq_wen),

    // REGRW1X.BFC
    .csr_regrw1x_bfc_set (csr_regrw1x_bfc_set),
    // REGRW1X.BFS
    .csr_regrw1x_bfs_clr (csr_regrw1x_bfs_clr),

    // REGRO.BFI
    .csr_regro_bfi_in (csr_regro_bfi_in),
    // REGRO.BFF
    // REGRO.BFIE
    .csr_regro_bfie_en (csr_regro_bfie_en),
    .csr_regro_bfie_in (csr_regro_bfie_in),

    // REGROC.BFI
    .csr_regroc_bfie_en (csr_regroc_bfie_en),
    .csr_regroc_bfie_in (csr_regroc_bfie_in),

    // REGROQ.BFIQ
    .csr_regroq_bfiq_rvalid (csr_regroq_bfiq_rvalid),
    .csr_regroq_bfiq_ren (csr_regroq_bfiq_ren),
    .csr_regroq_bfiq_in (csr_regroq_bfiq_in),

    // REGROLX.BFLL
    .csr_regrolx_bfll_in (csr_regrolx_bfll_in),
    // REGROLX.BFLH
    .csr_regrolx_bflh_in (csr_regrolx_bflh_in),
    // REGROLX.BFLLE
    .csr_regrolx_bflle_en (csr_regrolx_bflle_en),
    .csr_regrolx_bflle_in (csr_regrolx_bflle_in),
    // REGROLX.BFLHE
    .csr_regrolx_bflhe_en (csr_regrolx_bflhe_en),
    .csr_regrolx_bflhe_in (csr_regrolx_bflhe_in),

    // REGWO.BFWO
    .csr_regwo_bfwo_out (csr_regwo_bfwo_out),
    // REGWO.BFSC
    .csr_regwo_bfsc_out (csr_regwo_bfsc_out),

    // REGWOQ.BFOQ
    .csr_regwoq_bfoq_out    (csr_regwoq_bfoq_out),
    .csr_regwoq_bfoq_wready (csr_regwoq_bfoq_wready),
    .csr_regwoq_bfoq_wen    (csr_regwoq_bfoq_wen),

`ifdef INTERFACE_AXIL
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
    .axil_rready  (mst.rready)
);
// AXI-Lite master
axilite #(
    .ADDR_W (ADDR_W),
    .DATA_W (DATA_W),
    .STRB_W (STRB_W)
) mst (
    .clk    (clk)
);
`elsif INTERFACE_APB
    // APB
    .psel    (mst.psel),
    .paddr   (mst.paddr),
    .penable (mst.penable),
    .pwrite  (mst.pwrite),
    .pwdata  (mst.pwdata),
    .pstrb   (mst.pstrb),
    .prdata  (mst.prdata),
    .pready  (mst.pready),
    .pslverr (mst.pslverr)
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
`elsif INTERFACE_AMM
    // Avalon-MM
    .address      (mst.address),
    .read         (mst.read_s),
    .readdata     (mst.readdata),
    .readdatavalid(mst.readdatavalid),
    .byteenable   (mst.byteenable),
    .write        (mst.write_s),
    .writedata    (mst.writedata),
    .waitrequest  (mst.waitrequest)
);
// Avalon-MM master
amm #(
  .ADDR_W(ADDR_W),
  .DATA_W(DATA_W),
  .STRB_W(STRB_W)
) mst (
  .clk(clk),
  .reset(reset)
);
`else
    $error("Unknown interface to register map!");
`endif
