amm2lb dut (
  .clk          (clk              ),
  .rst          (reset            ),
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
  .wready       (wready        ),
  .waddr        (waddr         ),
  .wdata        (wdata         ),
  .wen          (wen           ),
  .wstrb        (wstrb         ),
  .rdata        (rdata         ),
  .rvalid       (rvalid        ),
  .raddr        (raddr         ),
  .ren          (ren           )
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
