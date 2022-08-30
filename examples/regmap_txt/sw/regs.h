// Created with Corsair vgit-latest
#ifndef __REGS_H
#define __REGS_H

#define __I  volatile const // 'read only' permissions
#define __O  volatile       // 'write only' permissions
#define __IO volatile       // 'read / write' permissions


#ifdef __cplusplus
#include <cstdint>
extern "C" {
#else
#include <stdint.h>
#endif

#define CSR_BASE_ADDR 0x0

// DATA - Data register
#define CSR_DATA_ADDR 0x0
#define CSR_DATA_RESET 0x0
typedef struct {
    uint32_t VAL : 32; // Value of the register
} csr_data_t;

// DATA.val - Value of the register
#define CSR_DATA_VAL_WIDTH 32
#define CSR_DATA_VAL_LSB 0
#define CSR_DATA_VAL_MASK 0x0
#define CSR_DATA_VAL_RESET 0x0

// CTRL - Control register
#define CSR_CTRL_ADDR 0x4
#define CSR_CTRL_RESET 0x100
typedef struct {
    uint32_t VAL : 16; // Value of the register
    uint32_t : 16; // reserved
} csr_ctrl_t;

// CTRL.val - Value of the register
#define CSR_CTRL_VAL_WIDTH 16
#define CSR_CTRL_VAL_LSB 0
#define CSR_CTRL_VAL_MASK 0x4
#define CSR_CTRL_VAL_RESET 0x100

// STATUS - Status register
#define CSR_STATUS_ADDR 0x8
#define CSR_STATUS_RESET 0x0
typedef struct {
    uint32_t VAL : 8; // Value of the register
    uint32_t : 24; // reserved
} csr_status_t;

// STATUS.val - Value of the register
#define CSR_STATUS_VAL_WIDTH 8
#define CSR_STATUS_VAL_LSB 0
#define CSR_STATUS_VAL_MASK 0x8
#define CSR_STATUS_VAL_RESET 0x0

// START - Start register
#define CSR_START_ADDR 0x100
#define CSR_START_RESET 0x0
typedef struct {
    uint32_t VAL : 1; // Value of the register
    uint32_t : 31; // reserved
} csr_start_t;

// START.val - Value of the register
#define CSR_START_VAL_WIDTH 1
#define CSR_START_VAL_LSB 0
#define CSR_START_VAL_MASK 0x100
#define CSR_START_VAL_RESET 0x0


// Register map structure
typedef struct {
    union {
        __IO uint32_t DATA; // Data register
        __IO csr_data_t DATA_bf; // Bit access for DATA register
    };
    union {
        __IO uint32_t CTRL; // Control register
        __IO csr_ctrl_t CTRL_bf; // Bit access for CTRL register
    };
    union {
        __I uint32_t STATUS; // Status register
        __I csr_status_t STATUS_bf; // Bit access for STATUS register
    };
    __IO uint32_t RESERVED0[61];
    union {
        __O uint32_t START; // Start register
        __O csr_start_t START_bf; // Bit access for START register
    };
} csr_t;

#define CSR ((csr_t*)(CSR_BASE_ADDR))

#ifdef __cplusplus
}
#endif

#endif /* __REGS_H */