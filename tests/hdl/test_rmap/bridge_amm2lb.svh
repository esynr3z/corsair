amm2lb amm2lb (
  .clk          (clk              ),
  .reset        (reset            ),
  // Avalon-MM
  .address      (mst.address      ),
  .read         (mst.read_s       ),
  .readdata     (mst.readdata     ),
  .readdatavalid(mst.readdatavalid),
  .byteenable   (mst.byteenable   ),
  .write        (mst.write_s      ),
  .writedata    (mst.writedata    ),
  .waitrequest  (mst.waitrequest  ),
  // Local Bus
  .wready       (lb_wready        ),
  .waddr        (lb_waddr         ),
  .wdata        (lb_wdata         ),
  .wen          (lb_wen           ),
  .wstrb        (lb_wstrb         ),
  .rdata        (lb_rdata         ),
  .rvalid       (lb_rvalid        ),
  .raddr        (lb_raddr         ),
  .ren          (lb_ren           )
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
