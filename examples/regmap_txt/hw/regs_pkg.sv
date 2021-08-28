// Created with Corsair vgit-latest
package regs_pkg;

parameter CSR_BASE_ADDR = 0;
parameter CSR_DATA_WIDTH = 32;
parameter CSR_ADDR_WIDTH = 16;

// DATA
parameter CSR_DATA_ADDR = 16'h0;
parameter CSR_DATA_RESET = 32'h0;

// DATA.val
parameter CSR_DATA_VAL_WIDTH = 32;
parameter CSR_DATA_VAL_LSB = 0;
parameter CSR_DATA_VAL_MASK = 32'hffffffff;
parameter CSR_DATA_VAL_RESET = 32'h0;


// CTRL
parameter CSR_CTRL_ADDR = 16'h4;
parameter CSR_CTRL_RESET = 32'h100;

// CTRL.val
parameter CSR_CTRL_VAL_WIDTH = 16;
parameter CSR_CTRL_VAL_LSB = 0;
parameter CSR_CTRL_VAL_MASK = 32'hffff;
parameter CSR_CTRL_VAL_RESET = 16'h100;


// STATUS
parameter CSR_STATUS_ADDR = 16'h8;
parameter CSR_STATUS_RESET = 32'h0;

// STATUS.val
parameter CSR_STATUS_VAL_WIDTH = 8;
parameter CSR_STATUS_VAL_LSB = 0;
parameter CSR_STATUS_VAL_MASK = 32'hff;
parameter CSR_STATUS_VAL_RESET = 8'h0;


// START
parameter CSR_START_ADDR = 16'h100;
parameter CSR_START_RESET = 32'h0;

// START.val
parameter CSR_START_VAL_WIDTH = 1;
parameter CSR_START_VAL_LSB = 0;
parameter CSR_START_VAL_MASK = 32'h1;
parameter CSR_START_VAL_RESET = 1'h0;


endpackage