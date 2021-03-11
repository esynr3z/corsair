
// Created with Corsair vgit-latest
//
// SPI to Local Bus bridge
//
// SPI parameters:
//   - slave;
//   - mode 0 only;
//   - most significant bit transmitted first;
//   - byte order from high to low;
//   - SCK frequency must at least 8 lower than system frequency.
//

module spi2lb_rmap #(
    parameter ADDR_W = 8,
    parameter DATA_W = 16,
    parameter STRB_W = DATA_W / 8
)(
    // System
    input                   clk,
    input                   rst,
    // SPI
    input                   spi_sck,
    input                   spi_cs_n,
    input                   spi_mosi,
    output reg              spi_miso,
    // Local Bus
    input                   lb_wready,
    output reg [ADDR_W-1:0] lb_waddr,
    output reg [DATA_W-1:0] lb_wdata,
    output reg              lb_wen,
    output reg [STRB_W-1:0] lb_wstrb,
    input      [DATA_W-1:0] lb_rdata,
    input                   lb_rvalid,
    output     [ADDR_W-1:0] lb_raddr,
    output reg              lb_ren
);

//------------------------------------------------------------------------------
// Inputs syncronization
//------------------------------------------------------------------------------
reg [1:0] cs_n_ff;
wire      cs;
reg [1:0] mosi_ff;
wire      mo;
reg [2:0] sck_ff;
wire      sck_rise, sck_fall;

// MOSI syncronization chain
always @(posedge clk) begin
    if (rst) begin
        mosi_ff <= 0;
    end else begin
        mosi_ff <= {mosi_ff[0], spi_mosi};
    end
end

assign mo = mosi_ff[1];

// CSn syncronization chain
always @(posedge clk) begin
    if (rst) begin
        cs_n_ff <= 0;
    end else begin
        cs_n_ff <= {cs_n_ff[0], spi_cs_n};
    end
end

assign cs = ~cs_n_ff[1];

// SCK syncronization and edge extraction
always @(posedge clk) begin
    if (rst) begin
        sck_ff <= 0;
    end else begin
        sck_ff <= {sck_ff[1:0], spi_sck};
    end
end

assign sck_rise = (~sck_ff[2]) & ( sck_ff[1]);
assign sck_fall = ( sck_ff[2]) & (~sck_ff[1]);

//------------------------------------------------------------------------------
// SPI slave FSM
//------------------------------------------------------------------------------
localparam BIT_CNT_W = ($clog2(DATA_W) > $clog2(ADDR_W)) ? $clog2(DATA_W) : $clog2(ADDR_W);
localparam CTRL_W    = 8;

// FSM states
localparam IDLE_S        = 0;
localparam RECV_MODE_S   = 1;
localparam RECV_STRB_S   = 2;
localparam RECV_ADDR_S   = 3;
localparam WAIT_TA_S     = 4;
localparam RECV_DATA_S   = 5;
localparam TRAN_DATA_S   = 6;
localparam WAIT_FINISH_S = 7;

reg [2:0] fsm_state;
reg [2:0] fsm_next;

reg [ADDR_W-1:0] lb_waddr_next;
reg [DATA_W-1:0] lb_wdata_next;
reg [STRB_W-1:0] lb_wstrb_next;
reg              lb_wen_next;
reg              lb_ren_next;

reg spi_miso_next;

reg [DATA_W-1:0]   dout_shifter, dout_shifter_next;
reg                mode_wr, mode_wr_next;
reg [BIT_CNT_W:0]  bit_cnt, bit_cnt_next;
reg                force_tran, force_tran_next;

always @(posedge clk) begin
    if (rst) begin
        fsm_state <= IDLE_S;
    end else begin
        fsm_state <= fsm_next;
    end
end

always @(*) begin
    fsm_next          = fsm_state;
    mode_wr_next      = mode_wr;
    dout_shifter_next = dout_shifter;
    bit_cnt_next      = bit_cnt;
    force_tran_next   = force_tran;
    spi_miso_next     = spi_miso;
    lb_waddr_next     = lb_waddr;
    lb_wdata_next     = lb_wdata;
    lb_wstrb_next     = lb_wstrb;
    lb_wen_next       = lb_wen;
    lb_ren_next       = lb_ren;
    case (fsm_state)
        IDLE_S : begin
            // wait cs_n assertion
            spi_miso_next = 1'b0;
            bit_cnt_next  = ADDR_W - 1;
            if (cs)
                fsm_next = RECV_ADDR_S;
        end

        RECV_ADDR_S : begin
            // receive address
            if (sck_rise) begin
                lb_waddr_next = {lb_waddr[ADDR_W-2:0], mo};
                if (bit_cnt == 0) begin
                    bit_cnt_next = 0;
                    fsm_next     = RECV_MODE_S;
                end else begin
                    bit_cnt_next = bit_cnt - 1;
                end
            end else if (!cs) // or finish packet
                fsm_next = WAIT_FINISH_S;
        end

        RECV_MODE_S : begin
            // receive transaction mode: write (1) or read (0)
            if (sck_rise) begin
                mode_wr_next = mo;
                lb_ren_next  = ~mo;
                bit_cnt_next = CTRL_W - 2;
                fsm_next     = RECV_STRB_S;
            end else if (!cs) // or finish packet
                fsm_next = WAIT_FINISH_S;
        end

        RECV_STRB_S : begin
            // receive byte strobe bits for write
            if (sck_rise) begin
                lb_wstrb_next = {lb_wstrb[STRB_W-2:0], mo};
                if (bit_cnt == 0) begin
                    bit_cnt_next = DATA_W - 1;
                    fsm_next     = mode_wr ? RECV_DATA_S : WAIT_TA_S;
                end else begin
                    bit_cnt_next = bit_cnt - 1;
                end
            end  else if (!cs) // or finish packet
                fsm_next = WAIT_FINISH_S;

            // and prepare data for reading at the same time
            if (lb_rvalid && lb_ren) begin
                dout_shifter_next = lb_rdata;
                lb_ren_next       = 1'b0;
            end
        end

        WAIT_TA_S : begin
            // wait turnaround to start
            if (sck_fall) begin
                force_tran_next = 1'b1;
                fsm_next        = TRAN_DATA_S;
            end else if (!cs) // or finish packet
                fsm_next = WAIT_FINISH_S;
        end

        RECV_DATA_S : begin
            // receive data bit by bit at every sck posedge
            if (sck_rise) begin
                lb_wdata_next = {lb_wdata[DATA_W-2:0], mo};
                if (bit_cnt == 0) begin
                    lb_wen_next  = 1'b1;
                    fsm_next     = WAIT_FINISH_S;
                end else begin
                    bit_cnt_next = bit_cnt - 1;
                end
            end else if (!cs) // or finish packet
                fsm_next = WAIT_FINISH_S;
        end

        TRAN_DATA_S : begin
            force_tran_next   = 1'b0;
            // transmit data bit by bit at every sck negedge
            if (sck_fall || force_tran) begin
                spi_miso_next     = dout_shifter[DATA_W-1];
                dout_shifter_next = {dout_shifter[DATA_W-2:0], 1'b0};
                if (bit_cnt == 0) begin
                    fsm_next = WAIT_FINISH_S;
                end else begin
                    bit_cnt_next = bit_cnt - 1;
                end
            end else if (!cs) // or finish packet
                fsm_next = WAIT_FINISH_S;
        end

        WAIT_FINISH_S : begin
            // finish write transaction if any
            if (lb_wready && lb_wen) begin
                lb_wen_next = 1'b0;
            end
            // finish read transaction if any
            if (lb_rvalid && lb_ren) begin
                lb_ren_next = 1'b0;
            end
            // and then just wait when it will be safe to go to idle
            if ((!lb_wen) && (!lb_ren) && (!cs)) begin
                fsm_next = IDLE_S;
            end
        end
    endcase
end

always @(posedge clk) begin
    if (rst) begin
        mode_wr      <= 1'b0;
        dout_shifter <= 0;
        bit_cnt      <= 0;
        force_tran   <= 1'b0;
        spi_miso     <= 1'b0;
        lb_waddr     <= 0;
        lb_wdata     <= 0;
        lb_wstrb     <= 0;
        lb_wen       <= 1'b0;
        lb_ren       <= 1'b0;
    end else begin
        mode_wr      <= mode_wr_next;
        dout_shifter <= dout_shifter_next;
        bit_cnt      <= bit_cnt_next;
        force_tran   <= force_tran_next;
        spi_miso     <= spi_miso_next;
        lb_waddr     <= lb_waddr_next;
        lb_wdata     <= lb_wdata_next;
        lb_wstrb     <= lb_wstrb_next;
        lb_wen       <= lb_wen_next;
        lb_ren       <= lb_ren_next;
    end
end

assign lb_raddr = lb_waddr;

endmodule