// Created with Corsair vgit-latest
// Register map module v1.42

module regs #(
    parameter ADDR_W = 12,
    parameter DATA_W = 32,
    parameter STRB_W = DATA_W / 8
)(
    // System
    input clk,
    input rst,
    // CSR: LEN
    output [31:0] csr_len_len_out,
    // CSR: CNT
    output csr_cnt_rstrb,
    output csr_cnt_wstrb,
    input [15:0] csr_cnt_cnt_in,
    output [15:0] csr_cnt_cnt_out,
    input csr_cnt_cnt_upd,
    // CSR: START
    output  csr_start_sta_out,
    output  csr_start_stb_out,
    output  csr_start_stc_out,
    output [7:0] csr_start_key_out,
    // CSR: STAT
    input  csr_stat_dir_in,
    input [2:0] csr_stat_state_in,
    input csr_stat_state_upd,
    // CSR: CTL
    output  csr_ctl_ena_out,
    output [7:0] csr_ctl_initb_out,
    // CSR: FLAG
    input  csr_flag_eva_in,
    output  csr_flag_eva_out,
    input csr_flag_eva_upd,
    input  csr_flag_evb_in,
    input csr_flag_evb_upd,
    // CSR: VERSION
    // Local Bus
    input  [ADDR_W-1:0] lb_waddr,
    input  [DATA_W-1:0] lb_wdata,
    input               lb_wen,
    input  [STRB_W-1:0] lb_wstrb,
    output              lb_wready,
    input  [ADDR_W-1:0] lb_raddr,
    input               lb_ren,
    output [DATA_W-1:0] lb_rdata,
    output              lb_rvalid
);

//------------------------------------------------------------------------------
// CSR:
// [0x0] - LEN - Length of pulse
//------------------------------------------------------------------------------
wire [31:0] csr_len_rdata;


wire csr_len_wen;
assign csr_len_wen = lb_wen && (lb_waddr == 12'h0);
wire csr_len_ren;
assign csr_len_ren = lb_ren && (lb_raddr == 12'h0);

//---------------------
// Bit field:
// LEN[31:0] - LEN - Length of pulse
// rw
//---------------------
reg [31:0] csr_len_len_out_ff;
assign csr_len_rdata[31:0] = csr_len_len_out_ff;
assign csr_len_len_out = csr_len_len_out_ff;

always @(posedge clk) begin
    if (rst) begin
        csr_len_len_out_ff <= 32'h0;
    end else if (csr_len_wen) begin
        if (lb_wstrb[0])
            csr_len_len_out_ff[7:0] <= lb_wdata[7:0];
        if (lb_wstrb[1])
            csr_len_len_out_ff[15:8] <= lb_wdata[15:8];
        if (lb_wstrb[2])
            csr_len_len_out_ff[23:16] <= lb_wdata[23:16];
        if (lb_wstrb[3])
            csr_len_len_out_ff[31:24] <= lb_wdata[31:24];
    end
end

//------------------------------------------------------------------------------
// CSR:
// [0x4] - CNT - Counter value
//------------------------------------------------------------------------------
wire [31:0] csr_cnt_rdata;

assign csr_cnt_rdata[31:16] = 16'h0;

wire csr_cnt_wen;
assign csr_cnt_wen = lb_wen && (lb_waddr == 12'h4);
wire csr_cnt_ren;
assign csr_cnt_ren = lb_ren && (lb_raddr == 12'h4);
assign csr_cnt_wstrb = lb_wready && csr_cnt_wen;
assign csr_cnt_rstrb = lb_rvalid && csr_cnt_ren;

//---------------------
// Bit field:
// CNT[15:0] - CNT - Counter value
// rw, hwu
//---------------------
reg [15:0] csr_cnt_cnt_out_ff;
assign csr_cnt_rdata[15:0] = csr_cnt_cnt_out_ff;
assign csr_cnt_cnt_out = csr_cnt_cnt_out_ff;

always @(posedge clk) begin
    if (rst) begin
        csr_cnt_cnt_out_ff <= 16'h0;
    end else if (csr_cnt_wen) begin
        if (lb_wstrb[0])
            csr_cnt_cnt_out_ff[7:0] <= lb_wdata[7:0];
        if (lb_wstrb[1])
            csr_cnt_cnt_out_ff[15:8] <= lb_wdata[15:8];
    end else if (csr_cnt_cnt_upd) begin
        csr_cnt_cnt_out_ff <= csr_cnt_cnt_in;
    end
end

//------------------------------------------------------------------------------
// CSR:
// [0x8] - START - Start processes
//------------------------------------------------------------------------------
wire [31:0] csr_start_rdata;

assign csr_start_rdata[7:1] = 7'h0;
assign csr_start_rdata[15:9] = 7'h0;
assign csr_start_rdata[23:17] = 7'h0;

wire csr_start_wen;
assign csr_start_wen = lb_wen && (lb_waddr == 12'h8);

//---------------------
// Bit field:
// START[0] - STA - Start process A
// wo, sc
//---------------------
reg  csr_start_sta_out_ff;
assign csr_start_rdata[0] = 1'b0;
assign csr_start_sta_out = csr_start_sta_out_ff;

always @(posedge clk) begin
    if (rst) begin
        csr_start_sta_out_ff <= 1'b0;
    end else if (csr_start_wen) begin
        if (lb_wstrb[0])
            csr_start_sta_out_ff <= lb_wdata[0];
    end else begin
        csr_start_sta_out_ff <= 1'b0;
    end
end
//---------------------
// Bit field:
// START[8] - STB - Start process B
// wo, sc
//---------------------
reg  csr_start_stb_out_ff;
assign csr_start_rdata[8] = 1'b0;
assign csr_start_stb_out = csr_start_stb_out_ff;

always @(posedge clk) begin
    if (rst) begin
        csr_start_stb_out_ff <= 1'b0;
    end else if (csr_start_wen) begin
        if (lb_wstrb[1])
            csr_start_stb_out_ff <= lb_wdata[8];
    end else begin
        csr_start_stb_out_ff <= 1'b0;
    end
end
//---------------------
// Bit field:
// START[16] - STC - Start process C
// wo, sc
//---------------------
reg  csr_start_stc_out_ff;
assign csr_start_rdata[16] = 1'b0;
assign csr_start_stc_out = csr_start_stc_out_ff;

always @(posedge clk) begin
    if (rst) begin
        csr_start_stc_out_ff <= 1'b0;
    end else if (csr_start_wen) begin
        if (lb_wstrb[2])
            csr_start_stc_out_ff <= lb_wdata[16];
    end else begin
        csr_start_stc_out_ff <= 1'b0;
    end
end
//---------------------
// Bit field:
// START[31:24] - KEY - Secret key to start process
// wo
//---------------------
reg [7:0] csr_start_key_out_ff;
assign csr_start_rdata[31:24] = 8'h0;
assign csr_start_key_out = csr_start_key_out_ff;

always @(posedge clk) begin
    if (rst) begin
        csr_start_key_out_ff <= 8'h0;
    end else if (csr_start_wen) begin
        if (lb_wstrb[3])
            csr_start_key_out_ff[7:0] <= lb_wdata[31:24];
    end
end

//------------------------------------------------------------------------------
// CSR:
// [0x10] - STAT - Status
//------------------------------------------------------------------------------
wire [31:0] csr_stat_rdata;

assign csr_stat_rdata[2:1] = 2'h0;
assign csr_stat_rdata[31:6] = 26'h0;

wire csr_stat_ren;
assign csr_stat_ren = lb_ren && (lb_raddr == 12'h10);

//---------------------
// Bit field:
// STAT[0] - DIR - Current direction
// ro
//---------------------
assign csr_stat_rdata[0] = csr_stat_dir_in;

//---------------------
// Bit field:
// STAT[5:3] - STATE - Current state
// ro, hwu
//---------------------
reg [2:0] csr_stat_state_in_ff;
assign csr_stat_rdata[5:3] = csr_stat_state_in_ff;

always @(posedge clk) begin
    if (rst) begin
        csr_stat_state_in_ff <= 3'h0;
    end else if (csr_stat_state_upd) begin
        csr_stat_state_in_ff <= csr_stat_state_in;
    end
end

//------------------------------------------------------------------------------
// CSR:
// [0x20] - CTL - Control
//------------------------------------------------------------------------------
wire [31:0] csr_ctl_rdata;

assign csr_ctl_rdata[0] = 1'b0;
assign csr_ctl_rdata[7:2] = 6'h0;
assign csr_ctl_rdata[31:16] = 16'h0;

wire csr_ctl_wen;
assign csr_ctl_wen = lb_wen && (lb_waddr == 12'h20);
wire csr_ctl_ren;
assign csr_ctl_ren = lb_ren && (lb_raddr == 12'h20);

//---------------------
// Bit field:
// CTL[1] - ENA - Enable A
// rw
//---------------------
reg  csr_ctl_ena_out_ff;
assign csr_ctl_rdata[1] = csr_ctl_ena_out_ff;
assign csr_ctl_ena_out = csr_ctl_ena_out_ff;

always @(posedge clk) begin
    if (rst) begin
        csr_ctl_ena_out_ff <= 1'b0;
    end else if (csr_ctl_wen) begin
        if (lb_wstrb[0])
            csr_ctl_ena_out_ff <= lb_wdata[1];
    end
end
//---------------------
// Bit field:
// CTL[15:8] - INITB - Initial value for B
// rw
//---------------------
reg [7:0] csr_ctl_initb_out_ff;
assign csr_ctl_rdata[15:8] = csr_ctl_initb_out_ff;
assign csr_ctl_initb_out = csr_ctl_initb_out_ff;

always @(posedge clk) begin
    if (rst) begin
        csr_ctl_initb_out_ff <= 8'h0;
    end else if (csr_ctl_wen) begin
        if (lb_wstrb[1])
            csr_ctl_initb_out_ff[7:0] <= lb_wdata[15:8];
    end
end

//------------------------------------------------------------------------------
// CSR:
// [0x24] - FLAG - Flags
//------------------------------------------------------------------------------
wire [31:0] csr_flag_rdata;

assign csr_flag_rdata[1] = 1'b0;
assign csr_flag_rdata[31:3] = 29'h0;

wire csr_flag_wen;
assign csr_flag_wen = lb_wen && (lb_waddr == 12'h24);
wire csr_flag_ren;
assign csr_flag_ren = lb_ren && (lb_raddr == 12'h24);

//---------------------
// Bit field:
// FLAG[0] - EVA - Event A
// rw, hwu, w1tc
//---------------------
reg  csr_flag_eva_out_ff;
assign csr_flag_rdata[0] = csr_flag_eva_out_ff;
assign csr_flag_eva_out = csr_flag_eva_out_ff;

always @(posedge clk) begin
    if (rst) begin
        csr_flag_eva_out_ff <= 1'b0;
    end else if (csr_flag_wen) begin
        if (lb_wstrb[0] && lb_wdata[0])
            csr_flag_eva_out_ff <= 1'b0;
    end else if (csr_flag_eva_upd) begin
        csr_flag_eva_out_ff <= csr_flag_eva_in;
    end
end
//---------------------
// Bit field:
// FLAG[2] - EVB - Event B
// ro, hwu, rtc
//---------------------
reg  csr_flag_evb_in_ff;
assign csr_flag_rdata[2] = csr_flag_evb_in_ff;

always @(posedge clk) begin
    if (rst) begin
        csr_flag_evb_in_ff <= 1'b0;
    end else if (csr_flag_evb_upd) begin
        csr_flag_evb_in_ff <= csr_flag_evb_in;
    end if (csr_flag_ren) begin
        csr_flag_evb_in_ff <= 1'b0;
    end
end

//------------------------------------------------------------------------------
// CSR:
// [0x40] - VERSION - Current version
//------------------------------------------------------------------------------
wire [31:0] csr_version_rdata;

assign csr_version_rdata[15:8] = 8'h0;
assign csr_version_rdata[31:24] = 8'h0;

wire csr_version_ren;
assign csr_version_ren = lb_ren && (lb_raddr == 12'h40);

//---------------------
// Bit field:
// VERSION[7:0] - MINOR - Minor version
// ro, const
//---------------------
assign csr_version_rdata[7:0] = 8'h23;

//---------------------
// Bit field:
// VERSION[23:16] - MAJOR - Major version
// ro, const
//---------------------
assign csr_version_rdata[23:16] = 8'h2;


//------------------------------------------------------------------------------
// Write ready
//------------------------------------------------------------------------------
assign lb_wready = 1'b1;

//------------------------------------------------------------------------------
// Read address decoder
//------------------------------------------------------------------------------
reg [31:0] lb_rdata_ff;
always @(posedge clk) begin
    if (rst) begin
        lb_rdata_ff <= 32'hdeadbeef;
    end else if (lb_ren) begin
        case (lb_raddr)
            12'h0: lb_rdata_ff <= csr_len_rdata;
            12'h4: lb_rdata_ff <= csr_cnt_rdata;
            12'h8: lb_rdata_ff <= csr_start_rdata;
            12'h10: lb_rdata_ff <= csr_stat_rdata;
            12'h20: lb_rdata_ff <= csr_ctl_rdata;
            12'h24: lb_rdata_ff <= csr_flag_rdata;
            12'h40: lb_rdata_ff <= csr_version_rdata;
            default: lb_rdata_ff <= 32'hdeadbeef;
        endcase
    end else begin
        lb_rdata_ff <= 32'hdeadbeef;
    end
end
assign lb_rdata = lb_rdata_ff;

//------------------------------------------------------------------------------
// Read data valid
//------------------------------------------------------------------------------
reg lb_rvalid_ff;
always @(posedge clk) begin
    if (rst) begin
        lb_rvalid_ff <= 1'b0;
    end else if (lb_ren && lb_rvalid) begin
        lb_rvalid_ff <= 1'b0;
    end else if (lb_ren) begin
        lb_rvalid_ff <= 1'b1;
    end
end

assign lb_rvalid = lb_rvalid_ff;

endmodule