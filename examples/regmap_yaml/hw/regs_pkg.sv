// Created with Corsair vgit-latest
package regs_pkg;

parameter CSR_BASE_ADDR = 0;
parameter CSR_DATA_WIDTH = 32;
parameter CSR_ADDR_WIDTH = 16;

// DATA
parameter CSR_DATA_ADDR = 16'h4;
parameter CSR_DATA_RESET = 32'h0;

// DATA.FIFO
parameter CSR_DATA_FIFO_WIDTH = 8;
parameter CSR_DATA_FIFO_LSB = 0;
parameter CSR_DATA_FIFO_MASK = 32'hff;
parameter CSR_DATA_FIFO_RESET = 8'h0;

// DATA.FERR
parameter CSR_DATA_FERR_WIDTH = 1;
parameter CSR_DATA_FERR_LSB = 16;
parameter CSR_DATA_FERR_MASK = 32'h10000;
parameter CSR_DATA_FERR_RESET = 1'h0;

// DATA.PERR
parameter CSR_DATA_PERR_WIDTH = 1;
parameter CSR_DATA_PERR_LSB = 17;
parameter CSR_DATA_PERR_MASK = 32'h20000;
parameter CSR_DATA_PERR_RESET = 1'h0;


// STAT
parameter CSR_STAT_ADDR = 16'hc;
parameter CSR_STAT_RESET = 32'h0;

// STAT.BUSY
parameter CSR_STAT_BUSY_WIDTH = 1;
parameter CSR_STAT_BUSY_LSB = 2;
parameter CSR_STAT_BUSY_MASK = 32'h4;
parameter CSR_STAT_BUSY_RESET = 1'h0;

// STAT.RXE
parameter CSR_STAT_RXE_WIDTH = 1;
parameter CSR_STAT_RXE_LSB = 4;
parameter CSR_STAT_RXE_MASK = 32'h10;
parameter CSR_STAT_RXE_RESET = 1'h0;

// STAT.TXF
parameter CSR_STAT_TXF_WIDTH = 1;
parameter CSR_STAT_TXF_LSB = 8;
parameter CSR_STAT_TXF_MASK = 32'h100;
parameter CSR_STAT_TXF_RESET = 1'h0;


// CTRL
parameter CSR_CTRL_ADDR = 16'h10;
parameter CSR_CTRL_RESET = 32'h0;

// CTRL.BAUD
parameter CSR_CTRL_BAUD_WIDTH = 2;
parameter CSR_CTRL_BAUD_LSB = 0;
parameter CSR_CTRL_BAUD_MASK = 32'h3;
parameter CSR_CTRL_BAUD_RESET = 2'h0;
typedef enum {
    CSR_CTRL_BAUD_B9600 = 2'h0, //9600 baud
    CSR_CTRL_BAUD_B38400 = 2'h1, //38400 baud
    CSR_CTRL_BAUD_B115200 = 2'h2 //115200 baud
} csrctrl_baud_t;

// CTRL.TXEN
parameter CSR_CTRL_TXEN_WIDTH = 1;
parameter CSR_CTRL_TXEN_LSB = 4;
parameter CSR_CTRL_TXEN_MASK = 32'h10;
parameter CSR_CTRL_TXEN_RESET = 1'h0;

// CTRL.RXEN
parameter CSR_CTRL_RXEN_WIDTH = 1;
parameter CSR_CTRL_RXEN_LSB = 5;
parameter CSR_CTRL_RXEN_MASK = 32'h20;
parameter CSR_CTRL_RXEN_RESET = 1'h0;

// CTRL.TXST
parameter CSR_CTRL_TXST_WIDTH = 1;
parameter CSR_CTRL_TXST_LSB = 6;
parameter CSR_CTRL_TXST_MASK = 32'h40;
parameter CSR_CTRL_TXST_RESET = 1'h0;


// LPMODE
parameter CSR_LPMODE_ADDR = 16'h14;
parameter CSR_LPMODE_RESET = 32'h0;

// LPMODE.DIV
parameter CSR_LPMODE_DIV_WIDTH = 8;
parameter CSR_LPMODE_DIV_LSB = 0;
parameter CSR_LPMODE_DIV_MASK = 32'hff;
parameter CSR_LPMODE_DIV_RESET = 8'h0;

// LPMODE.EN
parameter CSR_LPMODE_EN_WIDTH = 1;
parameter CSR_LPMODE_EN_LSB = 31;
parameter CSR_LPMODE_EN_MASK = 32'h80000000;
parameter CSR_LPMODE_EN_RESET = 1'h0;


// INTSTAT
parameter CSR_INTSTAT_ADDR = 16'h20;
parameter CSR_INTSTAT_RESET = 32'h0;

// INTSTAT.TX
parameter CSR_INTSTAT_TX_WIDTH = 1;
parameter CSR_INTSTAT_TX_LSB = 0;
parameter CSR_INTSTAT_TX_MASK = 32'h1;
parameter CSR_INTSTAT_TX_RESET = 1'h0;

// INTSTAT.RX
parameter CSR_INTSTAT_RX_WIDTH = 1;
parameter CSR_INTSTAT_RX_LSB = 1;
parameter CSR_INTSTAT_RX_MASK = 32'h2;
parameter CSR_INTSTAT_RX_RESET = 1'h0;


// ID
parameter CSR_ID_ADDR = 16'h40;
parameter CSR_ID_RESET = 32'hcafe0666;

// ID.UID
parameter CSR_ID_UID_WIDTH = 32;
parameter CSR_ID_UID_LSB = 0;
parameter CSR_ID_UID_MASK = 32'hffffffff;
parameter CSR_ID_UID_RESET = 32'hcafe0666;


endpackage