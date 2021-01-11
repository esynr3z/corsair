// Clock and reset
logic clk = 1'b0;
always #5 clk <= ~clk;

logic rst = 1'b1;
initial begin
    repeat (5) @(negedge clk);
    rst <= 1'b0;
end

// DUT
localparam ADDR_W = `DUT_ADDR_W;
localparam DATA_W = `DUT_DATA_W;
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

logic [31:0] csr_lena_val_out;
logic [15:0] csr_lenb_val_out;

logic [11:0] csr_cnt_eva_out;
logic [11:0] csr_cnt_eva_in = 0;
logic csr_cnt_eva_upd = 0;
logic [11:0] csr_cnt_evb_out;
logic [11:0] csr_cnt_evb_in = 0;
logic csr_cnt_evb_upd = 0;

logic csr_ctl_done_out;
logic csr_ctl_done_in = 0;
logic csr_ctl_done_upd = 0;
logic csr_ctl_gen_out;
logic csr_ctl_gen_in = 0;
logic csr_ctl_gen_upd = 0;
logic csr_ctl_mode_out;
logic csr_ctl_mode_in = 0;
logic csr_ctl_mode_upd = 0;

logic csr_start_en_out;
logic [15:0] csr_start_key_out;

logic csr_status_dir_in = 0;
logic csr_status_err_in = 0;
logic csr_status_err_upd = 0;
logic [11:0] csr_status_cap_in = 0;
logic csr_status_cap_upd = 0;

regs dut (
    // System
    .clk (clk),
    .rst (rst),
    // CSR: LENA
    .csr_lena_val_out (csr_lena_val_out),
    // CSR: LENB
    .csr_lenb_val_out (csr_lenb_val_out),
    // CSR: CNT
    .csr_cnt_eva_out     (csr_cnt_eva_out),
    .csr_cnt_eva_in (csr_cnt_eva_in),
    .csr_cnt_eva_upd (csr_cnt_eva_upd),
    .csr_cnt_evb_out     (csr_cnt_evb_out),
    .csr_cnt_evb_in (csr_cnt_evb_in),
    .csr_cnt_evb_upd (csr_cnt_evb_upd),
    // CSR: CTL
    .csr_ctl_done_out     (csr_ctl_done_out),
    .csr_ctl_done_in (csr_ctl_done_in),
    .csr_ctl_done_upd (csr_ctl_done_upd),
    .csr_ctl_gen_out      (csr_ctl_gen_out),
    .csr_ctl_gen_in  (csr_ctl_gen_in),
    .csr_ctl_gen_upd  (csr_ctl_gen_upd),
    .csr_ctl_mode_out     (csr_ctl_mode_out),
    .csr_ctl_mode_in (csr_ctl_mode_in),
    .csr_ctl_mode_upd (csr_ctl_mode_upd),
    // CSR: START
    .csr_start_en_out   (csr_start_en_out),
    .csr_start_key_out  (csr_start_key_out),
    // CSR: STATUS
    .csr_status_dir_in     (csr_status_dir_in),
    .csr_status_err_in (csr_status_err_in),
    .csr_status_err_upd (csr_status_err_upd),
    .csr_status_cap_in (csr_status_cap_in),
    .csr_status_cap_upd (csr_status_cap_upd),
    // Local Bus
    .lb_waddr   (lb_waddr),
    .lb_wdata   (lb_wdata),
    .lb_wen     (lb_wen),
    .lb_wstrb   (lb_wstrb),
    .lb_wready  (lb_wready),
    .lb_raddr   (lb_raddr),
    .lb_ren     (lb_ren),
    .lb_rdata   (lb_rdata),
    .lb_rvalid  (lb_rvalid)
);

// Bridge to Local Bus
apb2lb apb2lb (
    // APB
    .psel    (apb_mst.psel),
    .paddr   (apb_mst.paddr),
    .penable (apb_mst.penable),
    .pwrite  (apb_mst.pwrite),
    .pwdata  (apb_mst.pwdata),
    .pstrb   (apb_mst.pstrb),
    .prdata  (apb_mst.prdata),
    .pready  (apb_mst.pready),
    .pslverr (apb_mst.pslverr),
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
) apb_mst (
    .pclk    (clk),
    .presetn (~rst)
);