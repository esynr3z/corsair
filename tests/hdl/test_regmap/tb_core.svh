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

logic [31:0] csr_lena_val;
logic [15:0] csr_lenb_val;

logic [11:0] csr_cnt_eva;
logic [11:0] csr_cnt_eva_new = 0;
logic csr_cnt_eva_upd = 0;
logic [11:0] csr_cnt_evb;
logic [11:0] csr_cnt_evb_new = 0;
logic csr_cnt_evb_upd = 0;

logic csr_ctl_done;
logic csr_ctl_done_new = 0;
logic csr_ctl_done_upd = 0;
logic csr_ctl_gen;
logic csr_ctl_gen_new = 0;
logic csr_ctl_gen_upd = 0;
logic csr_ctl_mode;
logic csr_ctl_mode_new = 0;
logic csr_ctl_mode_upd = 0;

logic csr_start_en;
logic [15:0] csr_start_key;

logic csr_status_dir = 0;
logic csr_status_err_new = 0;
logic csr_status_err_upd = 0;
logic [11:0] csr_status_cap_new = 0;
logic csr_status_cap_upd = 0;

regs dut (
    // System
    .clk (clk),
    .rst (rst),
    // CSR: LENA
    .csr_lena_val (csr_lena_val),
    // CSR: LENB
    .csr_lenb_val (csr_lenb_val),
    // CSR: CNT
    .csr_cnt_eva     (csr_cnt_eva),
    .csr_cnt_eva_new (csr_cnt_eva_new),
    .csr_cnt_eva_upd (csr_cnt_eva_upd),
    .csr_cnt_evb     (csr_cnt_evb),
    .csr_cnt_evb_new (csr_cnt_evb_new),
    .csr_cnt_evb_upd (csr_cnt_evb_upd),
    // CSR: CTL
    .csr_ctl_done     (csr_ctl_done),
    .csr_ctl_done_new (csr_ctl_done_new),
    .csr_ctl_done_upd (csr_ctl_done_upd),
    .csr_ctl_gen      (csr_ctl_gen),
    .csr_ctl_gen_new  (csr_ctl_gen_new),
    .csr_ctl_gen_upd  (csr_ctl_gen_upd),
    .csr_ctl_mode     (csr_ctl_mode),
    .csr_ctl_mode_new (csr_ctl_mode_new),
    .csr_ctl_mode_upd (csr_ctl_mode_upd),
    // CSR: START
    .csr_start_en   (csr_start_en),
    .csr_start_key  (csr_start_key),
    // CSR: STATUS
    .csr_status_dir     (csr_status_dir),
    .csr_status_err_new (csr_status_err_new),
    .csr_status_err_upd (csr_status_err_upd),
    .csr_status_cap_new (csr_status_cap_new),
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