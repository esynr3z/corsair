// Created with Corsair vgit-latest

`ifndef __REGS_VH
`define __REGS_VH

`define CSR_BASE_ADDR 0
`define CSR_DATA_WIDTH 32
`define CSR_ADDR_WIDTH 16

// DATA - Data register
`define CSR_DATA_ADDR 16'h4
`define CSR_DATA_RESET 32'h0

// DATA.FIFO - Write to push value to TX FIFO, read to get data from RX FIFO
`define CSR_DATA_FIFO_WIDTH 8
`define CSR_DATA_FIFO_LSB 0
`define CSR_DATA_FIFO_MASK 32'h4
`define CSR_DATA_FIFO_RESET 8'h0

// DATA.FERR - Frame error flag. Read to clear.
`define CSR_DATA_FERR_WIDTH 1
`define CSR_DATA_FERR_LSB 16
`define CSR_DATA_FERR_MASK 32'h4
`define CSR_DATA_FERR_RESET 1'h0

// DATA.PERR - Parity error flag. Read to clear.
`define CSR_DATA_PERR_WIDTH 1
`define CSR_DATA_PERR_LSB 17
`define CSR_DATA_PERR_MASK 32'h4
`define CSR_DATA_PERR_RESET 1'h0


// STAT - Status register
`define CSR_STAT_ADDR 16'hc
`define CSR_STAT_RESET 32'h0

// STAT.BUSY - Transciever is busy
`define CSR_STAT_BUSY_WIDTH 1
`define CSR_STAT_BUSY_LSB 2
`define CSR_STAT_BUSY_MASK 32'hc
`define CSR_STAT_BUSY_RESET 1'h0

// STAT.RXE - RX FIFO is empty
`define CSR_STAT_RXE_WIDTH 1
`define CSR_STAT_RXE_LSB 4
`define CSR_STAT_RXE_MASK 32'hc
`define CSR_STAT_RXE_RESET 1'h0

// STAT.TXF - TX FIFO is full
`define CSR_STAT_TXF_WIDTH 1
`define CSR_STAT_TXF_LSB 8
`define CSR_STAT_TXF_MASK 32'hc
`define CSR_STAT_TXF_RESET 1'h0


// CTRL - Control register
`define CSR_CTRL_ADDR 16'h10
`define CSR_CTRL_RESET 32'h0

// CTRL.BAUD - Baudrate value
`define CSR_CTRL_BAUD_WIDTH 2
`define CSR_CTRL_BAUD_LSB 0
`define CSR_CTRL_BAUD_MASK 32'h10
`define CSR_CTRL_BAUD_RESET 2'h0
`define CSR_CTRL_BAUD_B9600 2'h0 //9600 baud
`define CSR_CTRL_BAUD_B38400 2'h1 //38400 baud
`define CSR_CTRL_BAUD_B115200 2'h2 //115200 baud

// CTRL.TXEN - Transmitter enable. Can be disabled by hardware on error.
`define CSR_CTRL_TXEN_WIDTH 1
`define CSR_CTRL_TXEN_LSB 4
`define CSR_CTRL_TXEN_MASK 32'h10
`define CSR_CTRL_TXEN_RESET 1'h0

// CTRL.RXEN - Receiver enable. Can be disabled by hardware on error.
`define CSR_CTRL_RXEN_WIDTH 1
`define CSR_CTRL_RXEN_LSB 5
`define CSR_CTRL_RXEN_MASK 32'h10
`define CSR_CTRL_RXEN_RESET 1'h0

// CTRL.TXST - Force transmission start
`define CSR_CTRL_TXST_WIDTH 1
`define CSR_CTRL_TXST_LSB 6
`define CSR_CTRL_TXST_MASK 32'h10
`define CSR_CTRL_TXST_RESET 1'h0


// LPMODE - Low power mode control
`define CSR_LPMODE_ADDR 16'h14
`define CSR_LPMODE_RESET 32'h0

// LPMODE.DIV - Clock divider in low power mode
`define CSR_LPMODE_DIV_WIDTH 8
`define CSR_LPMODE_DIV_LSB 0
`define CSR_LPMODE_DIV_MASK 32'h14
`define CSR_LPMODE_DIV_RESET 8'h0

// LPMODE.EN - Low power mode enable
`define CSR_LPMODE_EN_WIDTH 1
`define CSR_LPMODE_EN_LSB 31
`define CSR_LPMODE_EN_MASK 32'h14
`define CSR_LPMODE_EN_RESET 1'h0


// INTSTAT - Interrupt status register
`define CSR_INTSTAT_ADDR 16'h20
`define CSR_INTSTAT_RESET 32'h0

// INTSTAT.TX - Transmitter interrupt flag. Write 1 to clear.
`define CSR_INTSTAT_TX_WIDTH 1
`define CSR_INTSTAT_TX_LSB 0
`define CSR_INTSTAT_TX_MASK 32'h20
`define CSR_INTSTAT_TX_RESET 1'h0

// INTSTAT.RX - Receiver interrupt. Write 1 to clear.
`define CSR_INTSTAT_RX_WIDTH 1
`define CSR_INTSTAT_RX_LSB 1
`define CSR_INTSTAT_RX_MASK 32'h20
`define CSR_INTSTAT_RX_RESET 1'h0


// ID - IP-core ID register
`define CSR_ID_ADDR 16'h40
`define CSR_ID_RESET 32'hcafe0666

// ID.UID - Unique ID
`define CSR_ID_UID_WIDTH 32
`define CSR_ID_UID_LSB 0
`define CSR_ID_UID_MASK 32'h40
`define CSR_ID_UID_RESET 32'hcafe0666


`endif // __REGS_VH