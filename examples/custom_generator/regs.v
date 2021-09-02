// Created with Corsair vgit-latest

module regs #(
    parameter ADDR_W = 16,
    parameter DATA_W = 32,
    parameter STRB_W = DATA_W / 8
)(
    // System
    input clk,
    input rst,
    // DATA.FIFO
    input csr_data_fifo_rvalid,
    output csr_data_fifo_ren,
    input [7:0] csr_data_fifo_in,
    output [7:0] csr_data_fifo_out,
    input csr_data_fifo_wready,
    output csr_data_fifo_wen,
    // DATA.FERR
    input  csr_data_ferr_in,
    // DATA.PERR
    input  csr_data_perr_in,

    // STAT.BUSY
    input csr_stat_busy_en,
    input  csr_stat_busy_in,
    // STAT.RXE
    input  csr_stat_rxe_in,
    // STAT.TXF
    input  csr_stat_txf_in,

    // CTRL.BAUD
    output [1:0] csr_ctrl_baud_out,
    // CTRL.TXEN
    input csr_ctrl_txen_en,
    input  csr_ctrl_txen_in,
    output  csr_ctrl_txen_out,
    // CTRL.RXEN
    input csr_ctrl_rxen_en,
    input  csr_ctrl_rxen_in,
    output  csr_ctrl_rxen_out,
    // CTRL.TXST
    output  csr_ctrl_txst_out,

    // LPMODE.DIV
    output [7:0] csr_lpmode_div_out,
    // LPMODE.EN
    output  csr_lpmode_en_out,

    // INTSTAT.TX
    input csr_intstat_tx_set,
    // INTSTAT.RX
    input csr_intstat_rx_set,

    // ID.UID

    // AXI
    input  [ADDR_W-1:0] axil_awaddr,
    input  [2:0]        axil_awprot,
    input               axil_awvalid,
    output              axil_awready,
    input  [DATA_W-1:0] axil_wdata,
    input  [STRB_W-1:0] axil_wstrb,
    input               axil_wvalid,
    output              axil_wready,
    output [1:0]        axil_bresp,
    output              axil_bvalid,
    input               axil_bready,

    input  [ADDR_W-1:0] axil_araddr,
    input  [2:0]        axil_arprot,
    input               axil_arvalid,
    output              axil_arready,
    output [DATA_W-1:0] axil_rdata,
    output [1:0]        axil_rresp,
    output              axil_rvalid,
    input               axil_rready
);
wire              wready;
wire [ADDR_W-1:0] waddr;
wire [DATA_W-1:0] wdata;
wire              wen;
wire [STRB_W-1:0] wstrb;
wire [DATA_W-1:0] rdata;
wire              rvalid;
wire [ADDR_W-1:0] raddr;
wire              ren;
    reg [ADDR_W-1:0] waddr_int;
    reg [ADDR_W-1:0] raddr_int;
    reg [DATA_W-1:0] wdata_int;
    reg [STRB_W-1:0] strb_int;
    reg              awflag;
    reg              wflag;
    reg              arflag;
    reg              rflag;

    reg              axil_bvalid_int;
    reg [DATA_W-1:0] axil_rdata_int;
    reg              axil_rvalid_int;

    assign axil_awready = ~awflag;
    assign axil_wready  = ~wflag;
    assign axil_bvalid  = axil_bvalid_int;
    assign waddr        = waddr_int;
    assign wdata        = wdata_int;
    assign wstrb        = strb_int;
    assign wen          = awflag && wflag;
    assign axil_bresp   = 'd0; // always okay

    always @(posedge clk) begin
        if (rst == 1'b1) begin
            waddr_int       <= 'd0;
            wdata_int       <= 'd0;
            strb_int        <= 'd0;
            awflag          <= 1'b0;
            wflag           <= 1'b0;
            axil_bvalid_int <= 1'b0;
        end else begin
            if (axil_awvalid == 1'b1 && awflag == 1'b0) begin
                awflag    <= 1'b1;
                waddr_int <= axil_awaddr;
            end else if (wen == 1'b1 && wready == 1'b1) begin
                awflag    <= 1'b0;
            end

            if (axil_wvalid == 1'b1 && wflag == 1'b0) begin
                wflag     <= 1'b1;
                wdata_int <= axil_wdata;
                strb_int  <= axil_wstrb;
            end else if (wen == 1'b1 && wready == 1'b1) begin
                wflag     <= 1'b0;
            end

            if (axil_bvalid_int == 1'b1 && axil_bready == 1'b1) begin
                axil_bvalid_int <= 1'b0;
            end else if ((axil_wvalid == 1'b1 && awflag == 1'b1) || (axil_awvalid == 1'b1 && wflag == 1'b1) || (wflag == 1'b1 && awflag == 1'b1)) begin
                axil_bvalid_int <= wready;
            end
        end
    end

    assign axil_arready = ~arflag;
    assign axil_rdata   = axil_rdata_int;
    assign axil_rvalid  = axil_rvalid_int;
    assign raddr        = raddr_int;
    assign ren          = arflag && ~rflag;
    assign axil_rresp   = 'd0; // always okay

    always @(posedge clk) begin
        if (rst == 1'b1) begin
            raddr_int       <= 'd0;
            arflag          <= 1'b0;
            rflag           <= 1'b0;
            axil_rdata_int  <= 'd0;
            axil_rvalid_int <= 1'b0;
        end else begin
            if (axil_arvalid == 1'b1 && arflag == 1'b0) begin
                arflag    <= 1'b1;
                raddr_int <= axil_araddr;
            end else if (axil_rvalid_int == 1'b1 && axil_rready == 1'b1) begin
                arflag    <= 1'b0;
            end

            if (rvalid == 1'b1 && ren == 1'b1 && rflag == 1'b0) begin
                rflag <= 1'b1;
            end else if (axil_rvalid_int == 1'b1 && axil_rready == 1'b1) begin
                rflag <= 1'b0;
            end

            if (rvalid == 1'b1 && axil_rvalid_int == 1'b0) begin
                axil_rdata_int  <= rdata;
                axil_rvalid_int <= 1'b1;
            end else if (axil_rvalid_int == 1'b1 && axil_rready == 1'b1) begin
                axil_rvalid_int <= 1'b0;
            end
        end
    end

//------------------------------------------------------------------------------
// CSR:
// [0x0] - DATA - Data register
//------------------------------------------------------------------------------
wire [31:0] csr_data_rdata;
assign csr_data_rdata[15:8] = 8'h0;
assign csr_data_rdata[31:18] = 14'h0;

wire csr_data_wen;
assign csr_data_wen = wen && (waddr == 16'h0);

wire csr_data_ren;
assign csr_data_ren = ren && (raddr == 16'h0);
reg csr_data_ren_ff;
always @(posedge clk) begin
    if (rst) begin
        csr_data_ren_ff <= 1'b0;
    end else begin
        csr_data_ren_ff <= csr_data_ren;
    end
end
//---------------------
// Bit field:
// DATA[7:0] - FIFO - Write to push value to TX FIFO, read to get data from RX FIFO
// access: rw, hardware: q
//---------------------
reg [7:0] csr_data_fifo_ff;

assign csr_data_rdata[7:0] = csr_data_fifo_in;

assign csr_data_fifo_out = wdata[7:0];
assign csr_data_fifo_ren = csr_data_ren & (~csr_data_ren_ff);
assign csr_data_fifo_wen = csr_data_wen;

always @(posedge clk) begin
    if (rst) begin
        csr_data_fifo_ff <= 8'h0;
    end else  begin
    if (csr_data_wen) begin
            if (wstrb[0]) begin
                csr_data_fifo_ff[7:0] <= wdata[7:0];
            end
        end else begin
            csr_data_fifo_ff <= csr_data_fifo_ff;
        end
    end
end

reg csr_data_fifo_rvalid_ff;
always @(posedge clk) begin
    if (rst) begin
        csr_data_fifo_rvalid_ff <= 1'b0;
    end else begin
        csr_data_fifo_rvalid_ff <= csr_data_fifo_rvalid;
    end
end

//---------------------
// Bit field:
// DATA[16] - FERR - Frame error flag. Read to clear.
// access: rolh, hardware: i
//---------------------
reg  csr_data_ferr_ff;

assign csr_data_rdata[16] = csr_data_ferr_ff;


always @(posedge clk) begin
    if (rst) begin
        csr_data_ferr_ff <= 1'b0;
    end else  begin
  if (csr_data_ren) begin
            csr_data_ferr_ff <= 1'b0;
        end else   if (csr_data_ferr_in == 1'b1) begin
            csr_data_ferr_ff <= csr_data_ferr_in;
        end
    end
end


//---------------------
// Bit field:
// DATA[17] - PERR - Parity error flag. Read to clear.
// access: rolh, hardware: i
//---------------------
reg  csr_data_perr_ff;

assign csr_data_rdata[17] = csr_data_perr_ff;


always @(posedge clk) begin
    if (rst) begin
        csr_data_perr_ff <= 1'b0;
    end else  begin
  if (csr_data_ren) begin
            csr_data_perr_ff <= 1'b0;
        end else   if (csr_data_perr_in == 1'b1) begin
            csr_data_perr_ff <= csr_data_perr_in;
        end
    end
end


//------------------------------------------------------------------------------
// CSR:
// [0x4] - STAT - Status register
//------------------------------------------------------------------------------
wire [31:0] csr_stat_rdata;
assign csr_stat_rdata[3:1] = 3'h0;
assign csr_stat_rdata[31:6] = 26'h0;


wire csr_stat_ren;
assign csr_stat_ren = ren && (raddr == 16'h4);
reg csr_stat_ren_ff;
always @(posedge clk) begin
    if (rst) begin
        csr_stat_ren_ff <= 1'b0;
    end else begin
        csr_stat_ren_ff <= csr_stat_ren;
    end
end
//---------------------
// Bit field:
// STAT[0] - BUSY - Transciever is busy
// access: ro, hardware: ie
//---------------------
reg  csr_stat_busy_ff;

assign csr_stat_rdata[0] = csr_stat_busy_ff;


always @(posedge clk) begin
    if (rst) begin
        csr_stat_busy_ff <= 1'b0;
    end else  begin
     if (csr_stat_busy_en) begin
            csr_stat_busy_ff <= csr_stat_busy_in;
        end
    end
end


//---------------------
// Bit field:
// STAT[4] - RXE - RX FIFO is empty
// access: ro, hardware: i
//---------------------
reg  csr_stat_rxe_ff;

assign csr_stat_rdata[4] = csr_stat_rxe_ff;


always @(posedge clk) begin
    if (rst) begin
        csr_stat_rxe_ff <= 1'b0;
    end else  begin
     begin            csr_stat_rxe_ff <= csr_stat_rxe_in;
        end
    end
end


//---------------------
// Bit field:
// STAT[5] - TXF - TX FIFO is full
// access: ro, hardware: i
//---------------------
reg  csr_stat_txf_ff;

assign csr_stat_rdata[5] = csr_stat_txf_ff;


always @(posedge clk) begin
    if (rst) begin
        csr_stat_txf_ff <= 1'b0;
    end else  begin
     begin            csr_stat_txf_ff <= csr_stat_txf_in;
        end
    end
end


//------------------------------------------------------------------------------
// CSR:
// [0x8] - CTRL - Control register
//------------------------------------------------------------------------------
wire [31:0] csr_ctrl_rdata;
assign csr_ctrl_rdata[3:2] = 2'h0;
assign csr_ctrl_rdata[31:7] = 25'h0;

wire csr_ctrl_wen;
assign csr_ctrl_wen = wen && (waddr == 16'h8);

wire csr_ctrl_ren;
assign csr_ctrl_ren = ren && (raddr == 16'h8);
reg csr_ctrl_ren_ff;
always @(posedge clk) begin
    if (rst) begin
        csr_ctrl_ren_ff <= 1'b0;
    end else begin
        csr_ctrl_ren_ff <= csr_ctrl_ren;
    end
end
//---------------------
// Bit field:
// CTRL[1:0] - BAUD - Baudrate value
// access: rw, hardware: o
//---------------------
reg [1:0] csr_ctrl_baud_ff;

assign csr_ctrl_rdata[1:0] = csr_ctrl_baud_ff;

assign csr_ctrl_baud_out = csr_ctrl_baud_ff;

always @(posedge clk) begin
    if (rst) begin
        csr_ctrl_baud_ff <= 2'h0;
    end else  begin
    if (csr_ctrl_wen) begin
            if (wstrb[0]) begin
                csr_ctrl_baud_ff[1:0] <= wdata[1:0];
            end
        end else begin
            csr_ctrl_baud_ff <= csr_ctrl_baud_ff;
        end
    end
end


//---------------------
// Bit field:
// CTRL[4] - TXEN - Transmitter enable. Can be disabled by hardware on error.
// access: rw, hardware: oie
//---------------------
reg  csr_ctrl_txen_ff;

assign csr_ctrl_rdata[4] = csr_ctrl_txen_ff;

assign csr_ctrl_txen_out = csr_ctrl_txen_ff;

always @(posedge clk) begin
    if (rst) begin
        csr_ctrl_txen_ff <= 1'b0;
    end else  begin
    if (csr_ctrl_wen) begin
            if (wstrb[0]) begin
                csr_ctrl_txen_ff <= wdata[4];
            end
        end else if (csr_ctrl_txen_en) begin
            csr_ctrl_txen_ff <= csr_ctrl_txen_in;
        end
    end
end


//---------------------
// Bit field:
// CTRL[5] - RXEN - Receiver enable. Can be disabled by hardware on error.
// access: rw, hardware: oie
//---------------------
reg  csr_ctrl_rxen_ff;

assign csr_ctrl_rdata[5] = csr_ctrl_rxen_ff;

assign csr_ctrl_rxen_out = csr_ctrl_rxen_ff;

always @(posedge clk) begin
    if (rst) begin
        csr_ctrl_rxen_ff <= 1'b0;
    end else  begin
    if (csr_ctrl_wen) begin
            if (wstrb[0]) begin
                csr_ctrl_rxen_ff <= wdata[5];
            end
        end else if (csr_ctrl_rxen_en) begin
            csr_ctrl_rxen_ff <= csr_ctrl_rxen_in;
        end
    end
end


//---------------------
// Bit field:
// CTRL[6] - TXST - Force transmission start
// access: wosc, hardware: o
//---------------------
reg  csr_ctrl_txst_ff;

assign csr_ctrl_rdata[6] = 1'b0;

assign csr_ctrl_txst_out = csr_ctrl_txst_ff;

always @(posedge clk) begin
    if (rst) begin
        csr_ctrl_txst_ff <= 1'b0;
    end else  begin
    if (csr_ctrl_wen) begin
            if (wstrb[0]) begin
                csr_ctrl_txst_ff <= wdata[6];
            end
        end else begin
            csr_ctrl_txst_ff <= 1'b0;
        end
    end
end


//------------------------------------------------------------------------------
// CSR:
// [0xc] - LPMODE - Low power mode control
//------------------------------------------------------------------------------
wire [31:0] csr_lpmode_rdata;
assign csr_lpmode_rdata[30:8] = 23'h0;

wire csr_lpmode_wen;
assign csr_lpmode_wen = wen && (waddr == 16'hc);

wire csr_lpmode_ren;
assign csr_lpmode_ren = ren && (raddr == 16'hc);
reg csr_lpmode_ren_ff;
always @(posedge clk) begin
    if (rst) begin
        csr_lpmode_ren_ff <= 1'b0;
    end else begin
        csr_lpmode_ren_ff <= csr_lpmode_ren;
    end
end
//---------------------
// Bit field:
// LPMODE[7:0] - DIV - Clock divider in low power mode
// access: rw, hardware: o
//---------------------
reg [7:0] csr_lpmode_div_ff;

assign csr_lpmode_rdata[7:0] = csr_lpmode_div_ff;

assign csr_lpmode_div_out = csr_lpmode_div_ff;

always @(posedge clk) begin
    if (rst) begin
        csr_lpmode_div_ff <= 8'h0;
    end else  begin
    if (csr_lpmode_wen) begin
            if (wstrb[0]) begin
                csr_lpmode_div_ff[7:0] <= wdata[7:0];
            end
        end else begin
            csr_lpmode_div_ff <= csr_lpmode_div_ff;
        end
    end
end


//---------------------
// Bit field:
// LPMODE[31] - EN - Low power mode enable
// access: rw, hardware: o
//---------------------
reg  csr_lpmode_en_ff;

assign csr_lpmode_rdata[31] = csr_lpmode_en_ff;

assign csr_lpmode_en_out = csr_lpmode_en_ff;

always @(posedge clk) begin
    if (rst) begin
        csr_lpmode_en_ff <= 1'b0;
    end else  begin
    if (csr_lpmode_wen) begin
            if (wstrb[3]) begin
                csr_lpmode_en_ff <= wdata[31];
            end
        end else begin
            csr_lpmode_en_ff <= csr_lpmode_en_ff;
        end
    end
end


//------------------------------------------------------------------------------
// CSR:
// [0x10] - INTSTAT - Interrupt status register
//------------------------------------------------------------------------------
wire [31:0] csr_intstat_rdata;
assign csr_intstat_rdata[31:2] = 30'h0;

wire csr_intstat_wen;
assign csr_intstat_wen = wen && (waddr == 16'h10);

wire csr_intstat_ren;
assign csr_intstat_ren = ren && (raddr == 16'h10);
reg csr_intstat_ren_ff;
always @(posedge clk) begin
    if (rst) begin
        csr_intstat_ren_ff <= 1'b0;
    end else begin
        csr_intstat_ren_ff <= csr_intstat_ren;
    end
end
//---------------------
// Bit field:
// INTSTAT[0] - TX - Transmitter interrupt flag. Write 1 to clear.
// access: rw1c, hardware: s
//---------------------
reg  csr_intstat_tx_ff;

assign csr_intstat_rdata[0] = csr_intstat_tx_ff;


always @(posedge clk) begin
    if (rst) begin
        csr_intstat_tx_ff <= 1'b0;
    end else  begin
        if (csr_intstat_tx_set) begin
            csr_intstat_tx_ff <= 1'b1;
        end else    if (csr_intstat_wen) begin
            if (wstrb[0] && wdata[0]) begin
                csr_intstat_tx_ff <= 1'b0;
            end
        end else begin
            csr_intstat_tx_ff <= csr_intstat_tx_ff;
        end
    end
end


//---------------------
// Bit field:
// INTSTAT[1] - RX - Receiver interrupt. Write 1 to clear.
// access: rw1c, hardware: s
//---------------------
reg  csr_intstat_rx_ff;

assign csr_intstat_rdata[1] = csr_intstat_rx_ff;


always @(posedge clk) begin
    if (rst) begin
        csr_intstat_rx_ff <= 1'b0;
    end else  begin
        if (csr_intstat_rx_set) begin
            csr_intstat_rx_ff <= 1'b1;
        end else    if (csr_intstat_wen) begin
            if (wstrb[0] && wdata[1]) begin
                csr_intstat_rx_ff <= 1'b0;
            end
        end else begin
            csr_intstat_rx_ff <= csr_intstat_rx_ff;
        end
    end
end


//------------------------------------------------------------------------------
// CSR:
// [0xffc] - ID - IP-core ID register
//------------------------------------------------------------------------------
wire [31:0] csr_id_rdata;


wire csr_id_ren;
assign csr_id_ren = ren && (raddr == 16'hffc);
reg csr_id_ren_ff;
always @(posedge clk) begin
    if (rst) begin
        csr_id_ren_ff <= 1'b0;
    end else begin
        csr_id_ren_ff <= csr_id_ren;
    end
end
//---------------------
// Bit field:
// ID[31:0] - UID - Unique ID
// access: ro, hardware: f
//---------------------
reg [31:0] csr_id_uid_ff;

assign csr_id_rdata[31:0] = csr_id_uid_ff;


always @(posedge clk) begin
    if (rst) begin
        csr_id_uid_ff <= 32'hcafe0666;
    end else  begin
     begin
            csr_id_uid_ff <= csr_id_uid_ff;
        end
    end
end


//------------------------------------------------------------------------------
// Write ready
//------------------------------------------------------------------------------
reg wready_drv;

always @(*) begin
    if (csr_data_wen)
        wready_drv = csr_data_fifo_wready;
    else
        wready_drv = 1'b1;
end

assign wready = wready_drv;

//------------------------------------------------------------------------------
// Read address decoder
//------------------------------------------------------------------------------
reg [31:0] rdata_ff;
always @(posedge clk) begin
    if (rst) begin
        rdata_ff <= 32'h0;
    end else if (ren) begin
        case (raddr)
            16'h0: rdata_ff <= csr_data_rdata;
            16'h4: rdata_ff <= csr_stat_rdata;
            16'h8: rdata_ff <= csr_ctrl_rdata;
            16'hc: rdata_ff <= csr_lpmode_rdata;
            16'h10: rdata_ff <= csr_intstat_rdata;
            16'hffc: rdata_ff <= csr_id_rdata;
            default: rdata_ff <= 32'h0;
        endcase
    end else begin
        rdata_ff <= 32'h0;
    end
end
assign rdata = rdata_ff;

//------------------------------------------------------------------------------
// Read data valid
//------------------------------------------------------------------------------
reg rvalid_ff;
always @(posedge clk) begin
    if (rst) begin
        rvalid_ff <= 1'b0;
    end else if (ren && rvalid) begin
        rvalid_ff <= 1'b0;
    end else if (ren) begin
        rvalid_ff <= 1'b1;
    end
end

reg rvalid_drv;
always @(*) begin
    if (csr_data_ren)
        rvalid_drv = csr_data_fifo_rvalid_ff;
    else
        rvalid_drv = rvalid_ff;
end

assign rvalid = rvalid_drv;

endmodule