
logic [31:0] csr_lena_val_out;
logic [15:0] csr_lenb_val_out;

logic csr_cnt_rstrb;
logic csr_cnt_wstrb;
logic csr_cnt_wlock = 0;
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

logic csr_start_wlock = 0;
logic csr_start_en_out;
logic [15:0] csr_start_key_out;

logic csr_status_dir_in = 0;
logic csr_status_err_in = 0;
logic csr_status_err_upd = 0;
logic [11:0] csr_status_cap_in = 0;
logic csr_status_cap_upd = 0;

logic csr_intstat_ch0_in = 0;
logic csr_intstat_ch1_in = 0;
logic csr_intclr_ch0_out;
logic csr_intclr_ch1_out;

regs dut (
    // System
    .clk (clk),
    .rst (rst),
    // CSR: LENA
    .csr_lena_val_out (csr_lena_val_out),
    // CSR: LENB
    .csr_lenb_val_out (csr_lenb_val_out),
    // CSR: CNT
    .csr_cnt_rstrb (csr_cnt_rstrb),
    .csr_cnt_wstrb (csr_cnt_wstrb),
    .csr_cnt_wlock (csr_cnt_wlock),
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
    .csr_start_wlock    (csr_start_wlock),
    .csr_start_en_out   (csr_start_en_out),
    .csr_start_key_out  (csr_start_key_out),
    // CSR: STATUS
    .csr_status_dir_in     (csr_status_dir_in),
    .csr_status_err_in (csr_status_err_in),
    .csr_status_err_upd (csr_status_err_upd),
    .csr_status_cap_in (csr_status_cap_in),
    .csr_status_cap_upd (csr_status_cap_upd),
    // CSR: INTSTAT
    .csr_intstat_ch0_in (csr_intstat_ch0_in),
    .csr_intstat_ch1_in (csr_intstat_ch1_in),
    // CSR: INTCLR
    .csr_intclr_ch0_out (csr_intclr_ch0_out),
    .csr_intclr_ch1_out (csr_intclr_ch1_out),
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