// Created with Corsair vgit-latest

`ifndef __REGS_VH
`define __REGS_VH

`define CSR_BASE_ADDR 0
`define CSR_DATA_WIDTH 32
`define CSR_ADDR_WIDTH 16

// DATA - Data register
`define CSR_DATA_ADDR 16'h0
`define CSR_DATA_RESET 32'h0

// DATA.val - Value of the register
`define CSR_DATA_VAL_WIDTH 32
`define CSR_DATA_VAL_LSB 0
`define CSR_DATA_VAL_MASK 32'h0
`define CSR_DATA_VAL_RESET 32'h0


// CTRL - Control register
`define CSR_CTRL_ADDR 16'h4
`define CSR_CTRL_RESET 32'h100

// CTRL.val - Value of the register
`define CSR_CTRL_VAL_WIDTH 16
`define CSR_CTRL_VAL_LSB 0
`define CSR_CTRL_VAL_MASK 32'h4
`define CSR_CTRL_VAL_RESET 16'h100


// STATUS - Status register
`define CSR_STATUS_ADDR 16'h8
`define CSR_STATUS_RESET 32'h0

// STATUS.val - Value of the register
`define CSR_STATUS_VAL_WIDTH 8
`define CSR_STATUS_VAL_LSB 0
`define CSR_STATUS_VAL_MASK 32'h8
`define CSR_STATUS_VAL_RESET 8'h0


// START - Start register
`define CSR_START_ADDR 16'h100
`define CSR_START_RESET 32'h0

// START.val - Value of the register
`define CSR_START_VAL_WIDTH 1
`define CSR_START_VAL_LSB 0
`define CSR_START_VAL_MASK 32'h100
`define CSR_START_VAL_RESET 1'h0


`endif // __REGS_VH