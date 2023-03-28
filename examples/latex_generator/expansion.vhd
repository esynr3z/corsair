-------------------------------------------------------------------------------
-- COPYRIGHT (c) SOLECTRIX GmbH, Germany, 2023            All rights reserved
--
-- The copyright to the document(s) herein is the property of SOLECTRIX GmbH
-- The document(s) may be used and/or copied only with the written permission
-- from SOLECTRIX GmbH or in accordance with the terms/conditions stipulated
-- in the agreement/contract under which the document(s) have been supplied
-------------------------------------------------------------------------------
-- Project  : N/A
-- File     : expansion.vhd
-- Created  : 28.03.2023
-- Standard : VHDL'93/02
-------------------------------------------------------------------------------
--*
--* @short Register module (created with Corsair v.git-latest)
--*
--*   Needed Libraries and Packages:
--*   @li ieee.std_logic_1164 standard multi-value logic package
--*   @li ieee.numeric_std package
--*
--* @author malsheimer
--* @date 28.03.2023
--* @internal
--/
-------------------------------------------------------------------------------
-- Modification history :
-- Date        Author & Description
-- 28.03.2023  malsheimer: Created
-------------------------------------------------------------------------------

LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
USE ieee.numeric_std.ALL;

-------------------------------------------------------------------------------

ENTITY expansion IS
  GENERIC (
    g_addr_bits : INTEGER := 8);
  PORT (
    -- Clock & Reset
    clk                            : IN  STD_LOGIC;
    rst_n                          : IN  STD_LOGIC;
    -- Register Ports
    i_gpio0_value_gpio0_2          : IN  STD_LOGIC;
    o_gpio0_value_gpio0_2          : OUT STD_LOGIC;
    i_gpio0_value_gpio0_3          : IN  STD_LOGIC;
    o_gpio0_value_gpio0_3          : OUT STD_LOGIC;
    i_gpio0_value_gpio0_4          : IN  STD_LOGIC;
    o_gpio0_value_gpio0_4          : OUT STD_LOGIC;
    i_gpio0_value_gpio0_5          : IN  STD_LOGIC;
    o_gpio0_value_gpio0_5          : OUT STD_LOGIC;
    o_gpio0_dir_gpio0_2_dir        : OUT STD_LOGIC;
    o_gpio0_dir_gpio0_3_dir        : OUT STD_LOGIC;
    o_gpio0_dir_gpio0_4_dir        : OUT STD_LOGIC;
    o_gpio0_dir_gpio0_5_dir        : OUT STD_LOGIC;
    i_gpio1_value_gpio1_2          : IN  STD_LOGIC;
    o_gpio1_value_gpio1_2          : OUT STD_LOGIC;
    i_gpio1_value_gpio1_3          : IN  STD_LOGIC;
    o_gpio1_value_gpio1_3          : OUT STD_LOGIC;
    i_gpio1_value_gpio1_4          : IN  STD_LOGIC;
    o_gpio1_value_gpio1_4          : OUT STD_LOGIC;
    i_gpio1_value_gpio1_5          : IN  STD_LOGIC;
    o_gpio1_value_gpio1_5          : OUT STD_LOGIC;
    o_gpio1_dir_gpio1_2_dir        : OUT STD_LOGIC;
    o_gpio1_dir_gpio1_3_dir        : OUT STD_LOGIC;
    o_gpio1_dir_gpio1_4_dir        : OUT STD_LOGIC;
    o_gpio1_dir_gpio1_5_dir        : OUT STD_LOGIC;
    i_gpio2_value_gpio2_2          : IN  STD_LOGIC;
    o_gpio2_value_gpio2_2          : OUT STD_LOGIC;
    i_gpio2_value_gpio2_3          : IN  STD_LOGIC;
    o_gpio2_value_gpio2_3          : OUT STD_LOGIC;
    i_gpio2_value_gpio2_4          : IN  STD_LOGIC;
    o_gpio2_value_gpio2_4          : OUT STD_LOGIC;
    o_gpio2_dir_gpio2_2_dir        : OUT STD_LOGIC;
    o_gpio2_dir_gpio2_3_dir        : OUT STD_LOGIC;
    o_gpio2_dir_gpio2_4_dir        : OUT STD_LOGIC;
    i_gpio3_value_gpio3_2          : IN  STD_LOGIC;
    o_gpio3_value_gpio3_2          : OUT STD_LOGIC;
    i_gpio3_value_gpio3_3          : IN  STD_LOGIC;
    o_gpio3_value_gpio3_3          : OUT STD_LOGIC;
    i_gpio3_value_gpio3_4          : IN  STD_LOGIC;
    o_gpio3_value_gpio3_4          : OUT STD_LOGIC;
    o_gpio3_dir_gpio3_2_dir        : OUT STD_LOGIC;
    o_gpio3_dir_gpio3_3_dir        : OUT STD_LOGIC;
    o_gpio3_dir_gpio3_4_dir        : OUT STD_LOGIC;
    o_control_poc1_en              : OUT STD_LOGIC;
    i_control_poc1_err             : IN  STD_LOGIC;
    o_control_poc1_byp_en          : OUT STD_LOGIC;
    i_control_poc1_byp_err         : IN  STD_LOGIC;
    o_control_poc2_en              : OUT STD_LOGIC;
    i_control_poc2_err             : IN  STD_LOGIC;
    o_control_poc2_byp_en          : OUT STD_LOGIC;
    i_control_poc2_byp_err         : IN  STD_LOGIC;
    i_sm_fault_des0_ext_sm_fault   : IN  STD_LOGIC;
    i_sm_fault_des0_sm_fault       : IN  STD_LOGIC;
    i_sm_fault_des1_ext_sm_fault   : IN  STD_LOGIC;
    i_sm_fault_des1_sm_fault       : IN  STD_LOGIC;
    i_sm_fault_ser0_ext_sm_fault   : IN  STD_LOGIC;
    i_sm_fault_ser1_ext_sm_fault   : IN  STD_LOGIC;
    o_gpio_cnt_ctl_des0_gpio_sel   : OUT STD_LOGIC_VECTOR(3 DOWNTO 0);
    o_gpio_cnt_ctl_des1_gpio_sel   : OUT STD_LOGIC_VECTOR(3 DOWNTO 0);
    o_des0_gpio_re_cnt_edge_cnt_rd : OUT STD_LOGIC;
    i_des0_gpio_re_cnt_edge_cnt    : IN  STD_LOGIC_VECTOR(7 DOWNTO 0);
    o_des0_gpio_fe_cnt_edge_cnt_rd : OUT STD_LOGIC;
    i_des0_gpio_fe_cnt_edge_cnt    : IN  STD_LOGIC_VECTOR(7 DOWNTO 0);
    o_des1_gpio_re_cnt_edge_cnt_rd : OUT STD_LOGIC;
    i_des1_gpio_re_cnt_edge_cnt    : IN  STD_LOGIC_VECTOR(7 DOWNTO 0);
    o_des1_gpio_fe_cnt_edge_cnt_rd : OUT STD_LOGIC;
    i_des1_gpio_fe_cnt_edge_cnt    : IN  STD_LOGIC_VECTOR(7 DOWNTO 0);
    i_gpio4_value_gpio4_0          : IN  STD_LOGIC;
    o_gpio4_value_gpio4_0          : OUT STD_LOGIC;
    i_gpio4_value_gpio4_1          : IN  STD_LOGIC;
    o_gpio4_value_gpio4_1          : OUT STD_LOGIC;
    i_gpio4_value_gpio4_2          : IN  STD_LOGIC;
    o_gpio4_value_gpio4_2          : OUT STD_LOGIC;
    i_gpio4_value_gpio4_3          : IN  STD_LOGIC;
    o_gpio4_value_gpio4_3          : OUT STD_LOGIC;
    o_gpio4_dir_gpio4_2_dir        : OUT STD_LOGIC;
    o_gpio4_dir_gpio4_3_dir        : OUT STD_LOGIC;
    o_gpio4_dir_gpio4_4_dir        : OUT STD_LOGIC;
    o_gpio4_dir_gpio4_5_dir        : OUT STD_LOGIC;
    -- Expansion interface
    i_we                           : IN  STD_LOGIC;
    i_re                           : IN  STD_LOGIC;
    i_addr                         : IN  STD_LOGIC_VECTOR(g_addr_bits - 1 DOWNTO 0);
    i_data                         : IN  STD_LOGIC_VECTOR(7 DOWNTO 0);
    o_data                         : OUT STD_LOGIC_VECTOR(7 DOWNTO 0));
END ENTITY expansion;

-------------------------------------------------------------------------------

ARCHITECTURE rtl OF expansion IS

  -- signal declaration(s)
  SIGNAL s_gpio0_value_rdata            : STD_LOGIC_VECTOR(7 DOWNTO 0);
  SIGNAL s_gpio0_value_wen              : STD_LOGIC;
  SIGNAL s_gpio0_value_ren              : STD_LOGIC;
  SIGNAL s_gpio0_value_gpio0_2          : STD_LOGIC;
  SIGNAL s_gpio0_value_gpio0_3          : STD_LOGIC;
  SIGNAL s_gpio0_value_gpio0_4          : STD_LOGIC;
  SIGNAL s_gpio0_value_gpio0_5          : STD_LOGIC;
  SIGNAL s_gpio0_dir_rdata              : STD_LOGIC_VECTOR(7 DOWNTO 0);
  SIGNAL s_gpio0_dir_wen                : STD_LOGIC;
  SIGNAL s_gpio0_dir_ren                : STD_LOGIC;
  SIGNAL s_gpio0_dir_gpio0_2_dir        : STD_LOGIC;
  SIGNAL s_gpio0_dir_gpio0_3_dir        : STD_LOGIC;
  SIGNAL s_gpio0_dir_gpio0_4_dir        : STD_LOGIC;
  SIGNAL s_gpio0_dir_gpio0_5_dir        : STD_LOGIC;
  SIGNAL s_gpio1_value_rdata            : STD_LOGIC_VECTOR(7 DOWNTO 0);
  SIGNAL s_gpio1_value_wen              : STD_LOGIC;
  SIGNAL s_gpio1_value_ren              : STD_LOGIC;
  SIGNAL s_gpio1_value_gpio1_2          : STD_LOGIC;
  SIGNAL s_gpio1_value_gpio1_3          : STD_LOGIC;
  SIGNAL s_gpio1_value_gpio1_4          : STD_LOGIC;
  SIGNAL s_gpio1_value_gpio1_5          : STD_LOGIC;
  SIGNAL s_gpio1_dir_rdata              : STD_LOGIC_VECTOR(7 DOWNTO 0);
  SIGNAL s_gpio1_dir_wen                : STD_LOGIC;
  SIGNAL s_gpio1_dir_ren                : STD_LOGIC;
  SIGNAL s_gpio1_dir_gpio1_2_dir        : STD_LOGIC;
  SIGNAL s_gpio1_dir_gpio1_3_dir        : STD_LOGIC;
  SIGNAL s_gpio1_dir_gpio1_4_dir        : STD_LOGIC;
  SIGNAL s_gpio1_dir_gpio1_5_dir        : STD_LOGIC;
  SIGNAL s_gpio2_value_rdata            : STD_LOGIC_VECTOR(7 DOWNTO 0);
  SIGNAL s_gpio2_value_wen              : STD_LOGIC;
  SIGNAL s_gpio2_value_ren              : STD_LOGIC;
  SIGNAL s_gpio2_value_gpio2_2          : STD_LOGIC;
  SIGNAL s_gpio2_value_gpio2_3          : STD_LOGIC;
  SIGNAL s_gpio2_value_gpio2_4          : STD_LOGIC;
  SIGNAL s_gpio2_dir_rdata              : STD_LOGIC_VECTOR(7 DOWNTO 0);
  SIGNAL s_gpio2_dir_wen                : STD_LOGIC;
  SIGNAL s_gpio2_dir_ren                : STD_LOGIC;
  SIGNAL s_gpio2_dir_gpio2_2_dir        : STD_LOGIC;
  SIGNAL s_gpio2_dir_gpio2_3_dir        : STD_LOGIC;
  SIGNAL s_gpio2_dir_gpio2_4_dir        : STD_LOGIC;
  SIGNAL s_gpio3_value_rdata            : STD_LOGIC_VECTOR(7 DOWNTO 0);
  SIGNAL s_gpio3_value_wen              : STD_LOGIC;
  SIGNAL s_gpio3_value_ren              : STD_LOGIC;
  SIGNAL s_gpio3_value_gpio3_2          : STD_LOGIC;
  SIGNAL s_gpio3_value_gpio3_3          : STD_LOGIC;
  SIGNAL s_gpio3_value_gpio3_4          : STD_LOGIC;
  SIGNAL s_gpio3_dir_rdata              : STD_LOGIC_VECTOR(7 DOWNTO 0);
  SIGNAL s_gpio3_dir_wen                : STD_LOGIC;
  SIGNAL s_gpio3_dir_ren                : STD_LOGIC;
  SIGNAL s_gpio3_dir_gpio3_2_dir        : STD_LOGIC;
  SIGNAL s_gpio3_dir_gpio3_3_dir        : STD_LOGIC;
  SIGNAL s_gpio3_dir_gpio3_4_dir        : STD_LOGIC;
  SIGNAL s_control_rdata                : STD_LOGIC_VECTOR(7 DOWNTO 0);
  SIGNAL s_control_wen                  : STD_LOGIC;
  SIGNAL s_control_ren                  : STD_LOGIC;
  SIGNAL s_control_poc1_en              : STD_LOGIC;
  SIGNAL s_control_poc1_err             : STD_LOGIC;
  SIGNAL s_control_poc1_byp_en          : STD_LOGIC;
  SIGNAL s_control_poc1_byp_err         : STD_LOGIC;
  SIGNAL s_control_poc2_en              : STD_LOGIC;
  SIGNAL s_control_poc2_err             : STD_LOGIC;
  SIGNAL s_control_poc2_byp_en          : STD_LOGIC;
  SIGNAL s_control_poc2_byp_err         : STD_LOGIC;
  SIGNAL s_sm_fault_rdata               : STD_LOGIC_VECTOR(7 DOWNTO 0);
  SIGNAL s_sm_fault_ren                 : STD_LOGIC;
  SIGNAL s_sm_fault_des0_ext_sm_fault   : STD_LOGIC;
  SIGNAL s_sm_fault_des0_sm_fault       : STD_LOGIC;
  SIGNAL s_sm_fault_des1_ext_sm_fault   : STD_LOGIC;
  SIGNAL s_sm_fault_des1_sm_fault       : STD_LOGIC;
  SIGNAL s_sm_fault_ser0_ext_sm_fault   : STD_LOGIC;
  SIGNAL s_sm_fault_ser1_ext_sm_fault   : STD_LOGIC;
  SIGNAL s_gpio_cnt_ctl_rdata           : STD_LOGIC_VECTOR(7 DOWNTO 0);
  SIGNAL s_gpio_cnt_ctl_wen             : STD_LOGIC;
  SIGNAL s_gpio_cnt_ctl_ren             : STD_LOGIC;
  SIGNAL s_gpio_cnt_ctl_des0_gpio_sel   : STD_LOGIC_VECTOR(3 DOWNTO 0);
  SIGNAL s_gpio_cnt_ctl_des1_gpio_sel   : STD_LOGIC_VECTOR(3 DOWNTO 0);
  SIGNAL s_des0_gpio_re_cnt_rdata       : STD_LOGIC_VECTOR(7 DOWNTO 0);
  SIGNAL s_des0_gpio_re_cnt_ren         : STD_LOGIC;
  SIGNAL s_des0_gpio_re_cnt_edge_cnt    : STD_LOGIC_VECTOR(7 DOWNTO 0);
  SIGNAL s_des0_gpio_fe_cnt_rdata       : STD_LOGIC_VECTOR(7 DOWNTO 0);
  SIGNAL s_des0_gpio_fe_cnt_ren         : STD_LOGIC;
  SIGNAL s_des0_gpio_fe_cnt_edge_cnt    : STD_LOGIC_VECTOR(7 DOWNTO 0);
  SIGNAL s_des1_gpio_re_cnt_rdata       : STD_LOGIC_VECTOR(7 DOWNTO 0);
  SIGNAL s_des1_gpio_re_cnt_ren         : STD_LOGIC;
  SIGNAL s_des1_gpio_re_cnt_edge_cnt    : STD_LOGIC_VECTOR(7 DOWNTO 0);
  SIGNAL s_des1_gpio_fe_cnt_rdata       : STD_LOGIC_VECTOR(7 DOWNTO 0);
  SIGNAL s_des1_gpio_fe_cnt_ren         : STD_LOGIC;
  SIGNAL s_des1_gpio_fe_cnt_edge_cnt    : STD_LOGIC_VECTOR(7 DOWNTO 0);
  SIGNAL s_gpio4_value_rdata            : STD_LOGIC_VECTOR(7 DOWNTO 0);
  SIGNAL s_gpio4_value_wen              : STD_LOGIC;
  SIGNAL s_gpio4_value_ren              : STD_LOGIC;
  SIGNAL s_gpio4_value_gpio4_0          : STD_LOGIC;
  SIGNAL s_gpio4_value_gpio4_1          : STD_LOGIC;
  SIGNAL s_gpio4_value_gpio4_2          : STD_LOGIC;
  SIGNAL s_gpio4_value_gpio4_3          : STD_LOGIC;
  SIGNAL s_gpio4_dir_rdata              : STD_LOGIC_VECTOR(7 DOWNTO 0);
  SIGNAL s_gpio4_dir_wen                : STD_LOGIC;
  SIGNAL s_gpio4_dir_ren                : STD_LOGIC;
  SIGNAL s_gpio4_dir_gpio4_2_dir        : STD_LOGIC;
  SIGNAL s_gpio4_dir_gpio4_3_dir        : STD_LOGIC;
  SIGNAL s_gpio4_dir_gpio4_4_dir        : STD_LOGIC;
  SIGNAL s_gpio4_dir_gpio4_5_dir        : STD_LOGIC;

BEGIN

  --------------------------------------------------------------------------------
  -- [0x80] : GPIO0_VALUE - GPIO0 Value
  --------------------------------------------------------------------------------
  s_gpio0_value_rdata(1 DOWNTO 0) <= (OTHERS => '0');
  s_gpio0_value_rdata(7 DOWNTO 6) <= (OTHERS => '0');

  -- GPIO0_VALUE write access
  s_gpio0_value_wen <= i_we WHEN (i_addr = STD_LOGIC_VECTOR(to_unsigned(128, g_addr_bits))) ELSE '0';  -- 0x80
  -- GPIO0_VALUE read enable
  s_gpio0_value_ren <= i_re WHEN (i_addr = STD_LOGIC_VECTOR(to_unsigned(128, g_addr_bits))) ELSE '0';  -- 0x80

  -----------------------
  -- Bit field:
  -- GPIO0_VALUE(2) : GPIO0_2 - Deserializer #0 GENERAL_IO2 Value
  -- access: rw, hardware: io
  -----------------------
  -- readback
  s_gpio0_value_rdata(2) <= s_gpio0_value_gpio0_2;
  -- output
  o_gpio0_value_gpio0_2 <= s_gpio0_value_gpio0_2;

  --* purpose : GPIO0_2
  --* type    : sequential, rising edge, low active asynchronous reset
  p_gpio0_2 : PROCESS (clk, rst_n)
  BEGIN  -- PROCESS p_gpio0_2
    IF (rst_n = '0') THEN
      s_gpio0_value_gpio0_2 <= '0';  -- 0x0
    ELSIF rising_edge(clk) THEN
      IF (s_gpio0_value_wen = '1') THEN
        s_gpio0_value_gpio0_2 <= i_data(2);
      ELSE
        s_gpio0_value_gpio0_2 <= i_gpio0_value_gpio0_2;
      END IF;
    END IF;
  END PROCESS p_gpio0_2;

  -----------------------
  -- Bit field:
  -- GPIO0_VALUE(3) : GPIO0_3 - Deserializer #0 GENERAL_IO3 Value
  -- access: rw, hardware: io
  -----------------------
  -- readback
  s_gpio0_value_rdata(3) <= s_gpio0_value_gpio0_3;
  -- output
  o_gpio0_value_gpio0_3 <= s_gpio0_value_gpio0_3;

  --* purpose : GPIO0_3
  --* type    : sequential, rising edge, low active asynchronous reset
  p_gpio0_3 : PROCESS (clk, rst_n)
  BEGIN  -- PROCESS p_gpio0_3
    IF (rst_n = '0') THEN
      s_gpio0_value_gpio0_3 <= '0';  -- 0x0
    ELSIF rising_edge(clk) THEN
      IF (s_gpio0_value_wen = '1') THEN
        s_gpio0_value_gpio0_3 <= i_data(3);
      ELSE
        s_gpio0_value_gpio0_3 <= i_gpio0_value_gpio0_3;
      END IF;
    END IF;
  END PROCESS p_gpio0_3;

  -----------------------
  -- Bit field:
  -- GPIO0_VALUE(4) : GPIO0_4 - Deserializer #0 GENERAL_IO4 Value
  -- access: rw, hardware: io
  -----------------------
  -- readback
  s_gpio0_value_rdata(4) <= s_gpio0_value_gpio0_4;
  -- output
  o_gpio0_value_gpio0_4 <= s_gpio0_value_gpio0_4;

  --* purpose : GPIO0_4
  --* type    : sequential, rising edge, low active asynchronous reset
  p_gpio0_4 : PROCESS (clk, rst_n)
  BEGIN  -- PROCESS p_gpio0_4
    IF (rst_n = '0') THEN
      s_gpio0_value_gpio0_4 <= '0';  -- 0x0
    ELSIF rising_edge(clk) THEN
      IF (s_gpio0_value_wen = '1') THEN
        s_gpio0_value_gpio0_4 <= i_data(4);
      ELSE
        s_gpio0_value_gpio0_4 <= i_gpio0_value_gpio0_4;
      END IF;
    END IF;
  END PROCESS p_gpio0_4;

  -----------------------
  -- Bit field:
  -- GPIO0_VALUE(5) : GPIO0_5 - Deserializer #0 GENERAL_IO5 Value
  -- access: rw, hardware: io
  -----------------------
  -- readback
  s_gpio0_value_rdata(5) <= s_gpio0_value_gpio0_5;
  -- output
  o_gpio0_value_gpio0_5 <= s_gpio0_value_gpio0_5;

  --* purpose : GPIO0_5
  --* type    : sequential, rising edge, low active asynchronous reset
  p_gpio0_5 : PROCESS (clk, rst_n)
  BEGIN  -- PROCESS p_gpio0_5
    IF (rst_n = '0') THEN
      s_gpio0_value_gpio0_5 <= '0';  -- 0x0
    ELSIF rising_edge(clk) THEN
      IF (s_gpio0_value_wen = '1') THEN
        s_gpio0_value_gpio0_5 <= i_data(5);
      ELSE
        s_gpio0_value_gpio0_5 <= i_gpio0_value_gpio0_5;
      END IF;
    END IF;
  END PROCESS p_gpio0_5;


  --------------------------------------------------------------------------------
  -- [0x81] : GPIO0_DIR - GPIO0 Direction
  --------------------------------------------------------------------------------
  s_gpio0_dir_rdata(1 DOWNTO 0) <= (OTHERS => '0');
  s_gpio0_dir_rdata(7 DOWNTO 6) <= (OTHERS => '0');

  -- GPIO0_DIR write access
  s_gpio0_dir_wen <= i_we WHEN (i_addr = STD_LOGIC_VECTOR(to_unsigned(129, g_addr_bits))) ELSE '0';  -- 0x81
  -- GPIO0_DIR read enable
  s_gpio0_dir_ren <= i_re WHEN (i_addr = STD_LOGIC_VECTOR(to_unsigned(129, g_addr_bits))) ELSE '0';  -- 0x81

  -----------------------
  -- Bit field:
  -- GPIO0_DIR(2) : GPIO0_2_DIR - FPGA Pin to Deserializer #0 GENERAL_IO2 is Input (0) / Output (1)
  -- access: rw, hardware: o
  -----------------------
  -- readback
  s_gpio0_dir_rdata(2) <= s_gpio0_dir_gpio0_2_dir;
  -- output
  o_gpio0_dir_gpio0_2_dir <= s_gpio0_dir_gpio0_2_dir;

  --* purpose : GPIO0_2_DIR
  --* type    : sequential, rising edge, low active asynchronous reset
  p_gpio0_2_dir : PROCESS (clk, rst_n)
  BEGIN  -- PROCESS p_gpio0_2_dir
    IF (rst_n = '0') THEN
      s_gpio0_dir_gpio0_2_dir <= '0';  -- 0x0
    ELSIF rising_edge(clk) THEN
      IF (s_gpio0_dir_wen = '1') THEN
        s_gpio0_dir_gpio0_2_dir <= i_data(2);
      ELSE
        s_gpio0_dir_gpio0_2_dir <= s_gpio0_dir_gpio0_2_dir;
      END IF;
    END IF;
  END PROCESS p_gpio0_2_dir;

  -----------------------
  -- Bit field:
  -- GPIO0_DIR(3) : GPIO0_3_DIR - FPGA Pin to Deserializer #0 GENERAL_IO3 is Input (0) / Output (1)
  -- access: rw, hardware: o
  -----------------------
  -- readback
  s_gpio0_dir_rdata(3) <= s_gpio0_dir_gpio0_3_dir;
  -- output
  o_gpio0_dir_gpio0_3_dir <= s_gpio0_dir_gpio0_3_dir;

  --* purpose : GPIO0_3_DIR
  --* type    : sequential, rising edge, low active asynchronous reset
  p_gpio0_3_dir : PROCESS (clk, rst_n)
  BEGIN  -- PROCESS p_gpio0_3_dir
    IF (rst_n = '0') THEN
      s_gpio0_dir_gpio0_3_dir <= '0';  -- 0x0
    ELSIF rising_edge(clk) THEN
      IF (s_gpio0_dir_wen = '1') THEN
        s_gpio0_dir_gpio0_3_dir <= i_data(3);
      ELSE
        s_gpio0_dir_gpio0_3_dir <= s_gpio0_dir_gpio0_3_dir;
      END IF;
    END IF;
  END PROCESS p_gpio0_3_dir;

  -----------------------
  -- Bit field:
  -- GPIO0_DIR(4) : GPIO0_4_DIR - FPGA Pin to Deserializer #0 GENERAL_IO4 is Input (0) / Output (1)
  -- access: rw, hardware: o
  -----------------------
  -- readback
  s_gpio0_dir_rdata(4) <= s_gpio0_dir_gpio0_4_dir;
  -- output
  o_gpio0_dir_gpio0_4_dir <= s_gpio0_dir_gpio0_4_dir;

  --* purpose : GPIO0_4_DIR
  --* type    : sequential, rising edge, low active asynchronous reset
  p_gpio0_4_dir : PROCESS (clk, rst_n)
  BEGIN  -- PROCESS p_gpio0_4_dir
    IF (rst_n = '0') THEN
      s_gpio0_dir_gpio0_4_dir <= '0';  -- 0x0
    ELSIF rising_edge(clk) THEN
      IF (s_gpio0_dir_wen = '1') THEN
        s_gpio0_dir_gpio0_4_dir <= i_data(4);
      ELSE
        s_gpio0_dir_gpio0_4_dir <= s_gpio0_dir_gpio0_4_dir;
      END IF;
    END IF;
  END PROCESS p_gpio0_4_dir;

  -----------------------
  -- Bit field:
  -- GPIO0_DIR(5) : GPIO0_5_DIR - FPGA Pin to Deserializer #0 GENERAL_IO4 is Input (0) / Output (1)
  -- access: rw, hardware: o
  -----------------------
  -- readback
  s_gpio0_dir_rdata(5) <= s_gpio0_dir_gpio0_5_dir;
  -- output
  o_gpio0_dir_gpio0_5_dir <= s_gpio0_dir_gpio0_5_dir;

  --* purpose : GPIO0_5_DIR
  --* type    : sequential, rising edge, low active asynchronous reset
  p_gpio0_5_dir : PROCESS (clk, rst_n)
  BEGIN  -- PROCESS p_gpio0_5_dir
    IF (rst_n = '0') THEN
      s_gpio0_dir_gpio0_5_dir <= '0';  -- 0x0
    ELSIF rising_edge(clk) THEN
      IF (s_gpio0_dir_wen = '1') THEN
        s_gpio0_dir_gpio0_5_dir <= i_data(5);
      ELSE
        s_gpio0_dir_gpio0_5_dir <= s_gpio0_dir_gpio0_5_dir;
      END IF;
    END IF;
  END PROCESS p_gpio0_5_dir;


  --------------------------------------------------------------------------------
  -- [0x82] : GPIO1_VALUE - GPIO1 Value
  --------------------------------------------------------------------------------
  s_gpio1_value_rdata(1 DOWNTO 0) <= (OTHERS => '0');
  s_gpio1_value_rdata(7 DOWNTO 6) <= (OTHERS => '0');

  -- GPIO1_VALUE write access
  s_gpio1_value_wen <= i_we WHEN (i_addr = STD_LOGIC_VECTOR(to_unsigned(130, g_addr_bits))) ELSE '0';  -- 0x82
  -- GPIO1_VALUE read enable
  s_gpio1_value_ren <= i_re WHEN (i_addr = STD_LOGIC_VECTOR(to_unsigned(130, g_addr_bits))) ELSE '0';  -- 0x82

  -----------------------
  -- Bit field:
  -- GPIO1_VALUE(2) : GPIO1_2 - Deserializer #1 GENERAL_IO2 Value
  -- access: rw, hardware: io
  -----------------------
  -- readback
  s_gpio1_value_rdata(2) <= s_gpio1_value_gpio1_2;
  -- output
  o_gpio1_value_gpio1_2 <= s_gpio1_value_gpio1_2;

  --* purpose : GPIO1_2
  --* type    : sequential, rising edge, low active asynchronous reset
  p_gpio1_2 : PROCESS (clk, rst_n)
  BEGIN  -- PROCESS p_gpio1_2
    IF (rst_n = '0') THEN
      s_gpio1_value_gpio1_2 <= '0';  -- 0x0
    ELSIF rising_edge(clk) THEN
      IF (s_gpio1_value_wen = '1') THEN
        s_gpio1_value_gpio1_2 <= i_data(2);
      ELSE
        s_gpio1_value_gpio1_2 <= i_gpio1_value_gpio1_2;
      END IF;
    END IF;
  END PROCESS p_gpio1_2;

  -----------------------
  -- Bit field:
  -- GPIO1_VALUE(3) : GPIO1_3 - Deserializer #1 GENERAL_IO3 Value
  -- access: rw, hardware: io
  -----------------------
  -- readback
  s_gpio1_value_rdata(3) <= s_gpio1_value_gpio1_3;
  -- output
  o_gpio1_value_gpio1_3 <= s_gpio1_value_gpio1_3;

  --* purpose : GPIO1_3
  --* type    : sequential, rising edge, low active asynchronous reset
  p_gpio1_3 : PROCESS (clk, rst_n)
  BEGIN  -- PROCESS p_gpio1_3
    IF (rst_n = '0') THEN
      s_gpio1_value_gpio1_3 <= '0';  -- 0x0
    ELSIF rising_edge(clk) THEN
      IF (s_gpio1_value_wen = '1') THEN
        s_gpio1_value_gpio1_3 <= i_data(3);
      ELSE
        s_gpio1_value_gpio1_3 <= i_gpio1_value_gpio1_3;
      END IF;
    END IF;
  END PROCESS p_gpio1_3;

  -----------------------
  -- Bit field:
  -- GPIO1_VALUE(4) : GPIO1_4 - Deserializer #1 GENERAL_IO4 Value
  -- access: rw, hardware: io
  -----------------------
  -- readback
  s_gpio1_value_rdata(4) <= s_gpio1_value_gpio1_4;
  -- output
  o_gpio1_value_gpio1_4 <= s_gpio1_value_gpio1_4;

  --* purpose : GPIO1_4
  --* type    : sequential, rising edge, low active asynchronous reset
  p_gpio1_4 : PROCESS (clk, rst_n)
  BEGIN  -- PROCESS p_gpio1_4
    IF (rst_n = '0') THEN
      s_gpio1_value_gpio1_4 <= '0';  -- 0x0
    ELSIF rising_edge(clk) THEN
      IF (s_gpio1_value_wen = '1') THEN
        s_gpio1_value_gpio1_4 <= i_data(4);
      ELSE
        s_gpio1_value_gpio1_4 <= i_gpio1_value_gpio1_4;
      END IF;
    END IF;
  END PROCESS p_gpio1_4;

  -----------------------
  -- Bit field:
  -- GPIO1_VALUE(5) : GPIO1_5 - Deserializer #1 GENERAL_IO5 Value
  -- access: rw, hardware: io
  -----------------------
  -- readback
  s_gpio1_value_rdata(5) <= s_gpio1_value_gpio1_5;
  -- output
  o_gpio1_value_gpio1_5 <= s_gpio1_value_gpio1_5;

  --* purpose : GPIO1_5
  --* type    : sequential, rising edge, low active asynchronous reset
  p_gpio1_5 : PROCESS (clk, rst_n)
  BEGIN  -- PROCESS p_gpio1_5
    IF (rst_n = '0') THEN
      s_gpio1_value_gpio1_5 <= '0';  -- 0x0
    ELSIF rising_edge(clk) THEN
      IF (s_gpio1_value_wen = '1') THEN
        s_gpio1_value_gpio1_5 <= i_data(5);
      ELSE
        s_gpio1_value_gpio1_5 <= i_gpio1_value_gpio1_5;
      END IF;
    END IF;
  END PROCESS p_gpio1_5;


  --------------------------------------------------------------------------------
  -- [0x83] : GPIO1_DIR - GPIO1 Direction
  --------------------------------------------------------------------------------
  s_gpio1_dir_rdata(1 DOWNTO 0) <= (OTHERS => '0');
  s_gpio1_dir_rdata(7 DOWNTO 6) <= (OTHERS => '0');

  -- GPIO1_DIR write access
  s_gpio1_dir_wen <= i_we WHEN (i_addr = STD_LOGIC_VECTOR(to_unsigned(131, g_addr_bits))) ELSE '0';  -- 0x83
  -- GPIO1_DIR read enable
  s_gpio1_dir_ren <= i_re WHEN (i_addr = STD_LOGIC_VECTOR(to_unsigned(131, g_addr_bits))) ELSE '0';  -- 0x83

  -----------------------
  -- Bit field:
  -- GPIO1_DIR(2) : GPIO1_2_DIR - FPGA Pin to Deserializer #1 GENERAL_IO2 is Input (0) / Output (1)
  -- access: rw, hardware: o
  -----------------------
  -- readback
  s_gpio1_dir_rdata(2) <= s_gpio1_dir_gpio1_2_dir;
  -- output
  o_gpio1_dir_gpio1_2_dir <= s_gpio1_dir_gpio1_2_dir;

  --* purpose : GPIO1_2_DIR
  --* type    : sequential, rising edge, low active asynchronous reset
  p_gpio1_2_dir : PROCESS (clk, rst_n)
  BEGIN  -- PROCESS p_gpio1_2_dir
    IF (rst_n = '0') THEN
      s_gpio1_dir_gpio1_2_dir <= '0';  -- 0x0
    ELSIF rising_edge(clk) THEN
      IF (s_gpio1_dir_wen = '1') THEN
        s_gpio1_dir_gpio1_2_dir <= i_data(2);
      ELSE
        s_gpio1_dir_gpio1_2_dir <= s_gpio1_dir_gpio1_2_dir;
      END IF;
    END IF;
  END PROCESS p_gpio1_2_dir;

  -----------------------
  -- Bit field:
  -- GPIO1_DIR(3) : GPIO1_3_DIR - FPGA Pin to Deserializer #1 GENERAL_IO3 is Input (0) / Output (1)
  -- access: rw, hardware: o
  -----------------------
  -- readback
  s_gpio1_dir_rdata(3) <= s_gpio1_dir_gpio1_3_dir;
  -- output
  o_gpio1_dir_gpio1_3_dir <= s_gpio1_dir_gpio1_3_dir;

  --* purpose : GPIO1_3_DIR
  --* type    : sequential, rising edge, low active asynchronous reset
  p_gpio1_3_dir : PROCESS (clk, rst_n)
  BEGIN  -- PROCESS p_gpio1_3_dir
    IF (rst_n = '0') THEN
      s_gpio1_dir_gpio1_3_dir <= '0';  -- 0x0
    ELSIF rising_edge(clk) THEN
      IF (s_gpio1_dir_wen = '1') THEN
        s_gpio1_dir_gpio1_3_dir <= i_data(3);
      ELSE
        s_gpio1_dir_gpio1_3_dir <= s_gpio1_dir_gpio1_3_dir;
      END IF;
    END IF;
  END PROCESS p_gpio1_3_dir;

  -----------------------
  -- Bit field:
  -- GPIO1_DIR(4) : GPIO1_4_DIR - FPGA Pin to Deserializer #1 GENERAL_IO4 is Input (0) / Output (1)
  -- access: rw, hardware: o
  -----------------------
  -- readback
  s_gpio1_dir_rdata(4) <= s_gpio1_dir_gpio1_4_dir;
  -- output
  o_gpio1_dir_gpio1_4_dir <= s_gpio1_dir_gpio1_4_dir;

  --* purpose : GPIO1_4_DIR
  --* type    : sequential, rising edge, low active asynchronous reset
  p_gpio1_4_dir : PROCESS (clk, rst_n)
  BEGIN  -- PROCESS p_gpio1_4_dir
    IF (rst_n = '0') THEN
      s_gpio1_dir_gpio1_4_dir <= '0';  -- 0x0
    ELSIF rising_edge(clk) THEN
      IF (s_gpio1_dir_wen = '1') THEN
        s_gpio1_dir_gpio1_4_dir <= i_data(4);
      ELSE
        s_gpio1_dir_gpio1_4_dir <= s_gpio1_dir_gpio1_4_dir;
      END IF;
    END IF;
  END PROCESS p_gpio1_4_dir;

  -----------------------
  -- Bit field:
  -- GPIO1_DIR(5) : GPIO1_5_DIR - FPGA Pin to Deserializer #1 GENERAL_IO4 is Input (0) / Output (1)
  -- access: rw, hardware: o
  -----------------------
  -- readback
  s_gpio1_dir_rdata(5) <= s_gpio1_dir_gpio1_5_dir;
  -- output
  o_gpio1_dir_gpio1_5_dir <= s_gpio1_dir_gpio1_5_dir;

  --* purpose : GPIO1_5_DIR
  --* type    : sequential, rising edge, low active asynchronous reset
  p_gpio1_5_dir : PROCESS (clk, rst_n)
  BEGIN  -- PROCESS p_gpio1_5_dir
    IF (rst_n = '0') THEN
      s_gpio1_dir_gpio1_5_dir <= '0';  -- 0x0
    ELSIF rising_edge(clk) THEN
      IF (s_gpio1_dir_wen = '1') THEN
        s_gpio1_dir_gpio1_5_dir <= i_data(5);
      ELSE
        s_gpio1_dir_gpio1_5_dir <= s_gpio1_dir_gpio1_5_dir;
      END IF;
    END IF;
  END PROCESS p_gpio1_5_dir;


  --------------------------------------------------------------------------------
  -- [0x84] : GPIO2_VALUE - GPIO2 Value
  --------------------------------------------------------------------------------
  s_gpio2_value_rdata(1 DOWNTO 0) <= (OTHERS => '0');
  s_gpio2_value_rdata(7 DOWNTO 5) <= (OTHERS => '0');

  -- GPIO2_VALUE write access
  s_gpio2_value_wen <= i_we WHEN (i_addr = STD_LOGIC_VECTOR(to_unsigned(132, g_addr_bits))) ELSE '0';  -- 0x84
  -- GPIO2_VALUE read enable
  s_gpio2_value_ren <= i_re WHEN (i_addr = STD_LOGIC_VECTOR(to_unsigned(132, g_addr_bits))) ELSE '0';  -- 0x84

  -----------------------
  -- Bit field:
  -- GPIO2_VALUE(2) : GPIO2_2 - Serializer #0 GENERAL_IO2 Value
  -- access: rw, hardware: io
  -----------------------
  -- readback
  s_gpio2_value_rdata(2) <= s_gpio2_value_gpio2_2;
  -- output
  o_gpio2_value_gpio2_2 <= s_gpio2_value_gpio2_2;

  --* purpose : GPIO2_2
  --* type    : sequential, rising edge, low active asynchronous reset
  p_gpio2_2 : PROCESS (clk, rst_n)
  BEGIN  -- PROCESS p_gpio2_2
    IF (rst_n = '0') THEN
      s_gpio2_value_gpio2_2 <= '0';  -- 0x0
    ELSIF rising_edge(clk) THEN
      IF (s_gpio2_value_wen = '1') THEN
        s_gpio2_value_gpio2_2 <= i_data(2);
      ELSE
        s_gpio2_value_gpio2_2 <= i_gpio2_value_gpio2_2;
      END IF;
    END IF;
  END PROCESS p_gpio2_2;

  -----------------------
  -- Bit field:
  -- GPIO2_VALUE(3) : GPIO2_3 - Serializer #0 GENERAL_IO3 Value
  -- access: rw, hardware: io
  -----------------------
  -- readback
  s_gpio2_value_rdata(3) <= s_gpio2_value_gpio2_3;
  -- output
  o_gpio2_value_gpio2_3 <= s_gpio2_value_gpio2_3;

  --* purpose : GPIO2_3
  --* type    : sequential, rising edge, low active asynchronous reset
  p_gpio2_3 : PROCESS (clk, rst_n)
  BEGIN  -- PROCESS p_gpio2_3
    IF (rst_n = '0') THEN
      s_gpio2_value_gpio2_3 <= '0';  -- 0x0
    ELSIF rising_edge(clk) THEN
      IF (s_gpio2_value_wen = '1') THEN
        s_gpio2_value_gpio2_3 <= i_data(3);
      ELSE
        s_gpio2_value_gpio2_3 <= i_gpio2_value_gpio2_3;
      END IF;
    END IF;
  END PROCESS p_gpio2_3;

  -----------------------
  -- Bit field:
  -- GPIO2_VALUE(4) : GPIO2_4 - Serializer #0 GENERAL_IO4 Value
  -- access: rw, hardware: io
  -----------------------
  -- readback
  s_gpio2_value_rdata(4) <= s_gpio2_value_gpio2_4;
  -- output
  o_gpio2_value_gpio2_4 <= s_gpio2_value_gpio2_4;

  --* purpose : GPIO2_4
  --* type    : sequential, rising edge, low active asynchronous reset
  p_gpio2_4 : PROCESS (clk, rst_n)
  BEGIN  -- PROCESS p_gpio2_4
    IF (rst_n = '0') THEN
      s_gpio2_value_gpio2_4 <= '0';  -- 0x0
    ELSIF rising_edge(clk) THEN
      IF (s_gpio2_value_wen = '1') THEN
        s_gpio2_value_gpio2_4 <= i_data(4);
      ELSE
        s_gpio2_value_gpio2_4 <= i_gpio2_value_gpio2_4;
      END IF;
    END IF;
  END PROCESS p_gpio2_4;


  --------------------------------------------------------------------------------
  -- [0x85] : GPIO2_DIR - GPIO2 Direction
  --------------------------------------------------------------------------------
  s_gpio2_dir_rdata(1 DOWNTO 0) <= (OTHERS => '0');
  s_gpio2_dir_rdata(7 DOWNTO 5) <= (OTHERS => '0');

  -- GPIO2_DIR write access
  s_gpio2_dir_wen <= i_we WHEN (i_addr = STD_LOGIC_VECTOR(to_unsigned(133, g_addr_bits))) ELSE '0';  -- 0x85
  -- GPIO2_DIR read enable
  s_gpio2_dir_ren <= i_re WHEN (i_addr = STD_LOGIC_VECTOR(to_unsigned(133, g_addr_bits))) ELSE '0';  -- 0x85

  -----------------------
  -- Bit field:
  -- GPIO2_DIR(2) : GPIO2_2_DIR - FPGA Pin to Serializer #0 GENERAL_IO2 is Input (0) / Output (1)
  -- access: rw, hardware: o
  -----------------------
  -- readback
  s_gpio2_dir_rdata(2) <= s_gpio2_dir_gpio2_2_dir;
  -- output
  o_gpio2_dir_gpio2_2_dir <= s_gpio2_dir_gpio2_2_dir;

  --* purpose : GPIO2_2_DIR
  --* type    : sequential, rising edge, low active asynchronous reset
  p_gpio2_2_dir : PROCESS (clk, rst_n)
  BEGIN  -- PROCESS p_gpio2_2_dir
    IF (rst_n = '0') THEN
      s_gpio2_dir_gpio2_2_dir <= '0';  -- 0x0
    ELSIF rising_edge(clk) THEN
      IF (s_gpio2_dir_wen = '1') THEN
        s_gpio2_dir_gpio2_2_dir <= i_data(2);
      ELSE
        s_gpio2_dir_gpio2_2_dir <= s_gpio2_dir_gpio2_2_dir;
      END IF;
    END IF;
  END PROCESS p_gpio2_2_dir;

  -----------------------
  -- Bit field:
  -- GPIO2_DIR(3) : GPIO2_3_DIR - FPGA Pin to Serializer #0 GENERAL_IO3 is Input (0) / Output (1)
  -- access: rw, hardware: o
  -----------------------
  -- readback
  s_gpio2_dir_rdata(3) <= s_gpio2_dir_gpio2_3_dir;
  -- output
  o_gpio2_dir_gpio2_3_dir <= s_gpio2_dir_gpio2_3_dir;

  --* purpose : GPIO2_3_DIR
  --* type    : sequential, rising edge, low active asynchronous reset
  p_gpio2_3_dir : PROCESS (clk, rst_n)
  BEGIN  -- PROCESS p_gpio2_3_dir
    IF (rst_n = '0') THEN
      s_gpio2_dir_gpio2_3_dir <= '0';  -- 0x0
    ELSIF rising_edge(clk) THEN
      IF (s_gpio2_dir_wen = '1') THEN
        s_gpio2_dir_gpio2_3_dir <= i_data(3);
      ELSE
        s_gpio2_dir_gpio2_3_dir <= s_gpio2_dir_gpio2_3_dir;
      END IF;
    END IF;
  END PROCESS p_gpio2_3_dir;

  -----------------------
  -- Bit field:
  -- GPIO2_DIR(4) : GPIO2_4_DIR - FPGA Pin to Serializer #0 GENERAL_IO4 is Input (0) / Output (1)
  -- access: rw, hardware: o
  -----------------------
  -- readback
  s_gpio2_dir_rdata(4) <= s_gpio2_dir_gpio2_4_dir;
  -- output
  o_gpio2_dir_gpio2_4_dir <= s_gpio2_dir_gpio2_4_dir;

  --* purpose : GPIO2_4_DIR
  --* type    : sequential, rising edge, low active asynchronous reset
  p_gpio2_4_dir : PROCESS (clk, rst_n)
  BEGIN  -- PROCESS p_gpio2_4_dir
    IF (rst_n = '0') THEN
      s_gpio2_dir_gpio2_4_dir <= '0';  -- 0x0
    ELSIF rising_edge(clk) THEN
      IF (s_gpio2_dir_wen = '1') THEN
        s_gpio2_dir_gpio2_4_dir <= i_data(4);
      ELSE
        s_gpio2_dir_gpio2_4_dir <= s_gpio2_dir_gpio2_4_dir;
      END IF;
    END IF;
  END PROCESS p_gpio2_4_dir;


  --------------------------------------------------------------------------------
  -- [0x86] : GPIO3_VALUE - GPIO3 Value
  --------------------------------------------------------------------------------
  s_gpio3_value_rdata(1 DOWNTO 0) <= (OTHERS => '0');
  s_gpio3_value_rdata(7 DOWNTO 5) <= (OTHERS => '0');

  -- GPIO3_VALUE write access
  s_gpio3_value_wen <= i_we WHEN (i_addr = STD_LOGIC_VECTOR(to_unsigned(134, g_addr_bits))) ELSE '0';  -- 0x86
  -- GPIO3_VALUE read enable
  s_gpio3_value_ren <= i_re WHEN (i_addr = STD_LOGIC_VECTOR(to_unsigned(134, g_addr_bits))) ELSE '0';  -- 0x86

  -----------------------
  -- Bit field:
  -- GPIO3_VALUE(2) : GPIO3_2 - Serializer #1 GENERAL_IO2 Value
  -- access: rw, hardware: io
  -----------------------
  -- readback
  s_gpio3_value_rdata(2) <= s_gpio3_value_gpio3_2;
  -- output
  o_gpio3_value_gpio3_2 <= s_gpio3_value_gpio3_2;

  --* purpose : GPIO3_2
  --* type    : sequential, rising edge, low active asynchronous reset
  p_gpio3_2 : PROCESS (clk, rst_n)
  BEGIN  -- PROCESS p_gpio3_2
    IF (rst_n = '0') THEN
      s_gpio3_value_gpio3_2 <= '0';  -- 0x0
    ELSIF rising_edge(clk) THEN
      IF (s_gpio3_value_wen = '1') THEN
        s_gpio3_value_gpio3_2 <= i_data(2);
      ELSE
        s_gpio3_value_gpio3_2 <= i_gpio3_value_gpio3_2;
      END IF;
    END IF;
  END PROCESS p_gpio3_2;

  -----------------------
  -- Bit field:
  -- GPIO3_VALUE(3) : GPIO3_3 - Serializer #1 GENERAL_IO3 Value
  -- access: rw, hardware: io
  -----------------------
  -- readback
  s_gpio3_value_rdata(3) <= s_gpio3_value_gpio3_3;
  -- output
  o_gpio3_value_gpio3_3 <= s_gpio3_value_gpio3_3;

  --* purpose : GPIO3_3
  --* type    : sequential, rising edge, low active asynchronous reset
  p_gpio3_3 : PROCESS (clk, rst_n)
  BEGIN  -- PROCESS p_gpio3_3
    IF (rst_n = '0') THEN
      s_gpio3_value_gpio3_3 <= '0';  -- 0x0
    ELSIF rising_edge(clk) THEN
      IF (s_gpio3_value_wen = '1') THEN
        s_gpio3_value_gpio3_3 <= i_data(3);
      ELSE
        s_gpio3_value_gpio3_3 <= i_gpio3_value_gpio3_3;
      END IF;
    END IF;
  END PROCESS p_gpio3_3;

  -----------------------
  -- Bit field:
  -- GPIO3_VALUE(4) : GPIO3_4 - Serializer #1 GENERAL_IO4 Value
  -- access: rw, hardware: io
  -----------------------
  -- readback
  s_gpio3_value_rdata(4) <= s_gpio3_value_gpio3_4;
  -- output
  o_gpio3_value_gpio3_4 <= s_gpio3_value_gpio3_4;

  --* purpose : GPIO3_4
  --* type    : sequential, rising edge, low active asynchronous reset
  p_gpio3_4 : PROCESS (clk, rst_n)
  BEGIN  -- PROCESS p_gpio3_4
    IF (rst_n = '0') THEN
      s_gpio3_value_gpio3_4 <= '0';  -- 0x0
    ELSIF rising_edge(clk) THEN
      IF (s_gpio3_value_wen = '1') THEN
        s_gpio3_value_gpio3_4 <= i_data(4);
      ELSE
        s_gpio3_value_gpio3_4 <= i_gpio3_value_gpio3_4;
      END IF;
    END IF;
  END PROCESS p_gpio3_4;


  --------------------------------------------------------------------------------
  -- [0x87] : GPIO3_DIR - GPIO3 Direction
  --------------------------------------------------------------------------------
  s_gpio3_dir_rdata(1 DOWNTO 0) <= (OTHERS => '0');
  s_gpio3_dir_rdata(7 DOWNTO 5) <= (OTHERS => '0');

  -- GPIO3_DIR write access
  s_gpio3_dir_wen <= i_we WHEN (i_addr = STD_LOGIC_VECTOR(to_unsigned(135, g_addr_bits))) ELSE '0';  -- 0x87
  -- GPIO3_DIR read enable
  s_gpio3_dir_ren <= i_re WHEN (i_addr = STD_LOGIC_VECTOR(to_unsigned(135, g_addr_bits))) ELSE '0';  -- 0x87

  -----------------------
  -- Bit field:
  -- GPIO3_DIR(2) : GPIO3_2_DIR - FPGA Pin to Serializer #1 GENERAL_IO2 is Input (0) / Output (1)
  -- access: rw, hardware: o
  -----------------------
  -- readback
  s_gpio3_dir_rdata(2) <= s_gpio3_dir_gpio3_2_dir;
  -- output
  o_gpio3_dir_gpio3_2_dir <= s_gpio3_dir_gpio3_2_dir;

  --* purpose : GPIO3_2_DIR
  --* type    : sequential, rising edge, low active asynchronous reset
  p_gpio3_2_dir : PROCESS (clk, rst_n)
  BEGIN  -- PROCESS p_gpio3_2_dir
    IF (rst_n = '0') THEN
      s_gpio3_dir_gpio3_2_dir <= '0';  -- 0x0
    ELSIF rising_edge(clk) THEN
      IF (s_gpio3_dir_wen = '1') THEN
        s_gpio3_dir_gpio3_2_dir <= i_data(2);
      ELSE
        s_gpio3_dir_gpio3_2_dir <= s_gpio3_dir_gpio3_2_dir;
      END IF;
    END IF;
  END PROCESS p_gpio3_2_dir;

  -----------------------
  -- Bit field:
  -- GPIO3_DIR(3) : GPIO3_3_DIR - FPGA Pin to Serializer #1 GENERAL_IO3 is Input (0) / Output (1)
  -- access: rw, hardware: o
  -----------------------
  -- readback
  s_gpio3_dir_rdata(3) <= s_gpio3_dir_gpio3_3_dir;
  -- output
  o_gpio3_dir_gpio3_3_dir <= s_gpio3_dir_gpio3_3_dir;

  --* purpose : GPIO3_3_DIR
  --* type    : sequential, rising edge, low active asynchronous reset
  p_gpio3_3_dir : PROCESS (clk, rst_n)
  BEGIN  -- PROCESS p_gpio3_3_dir
    IF (rst_n = '0') THEN
      s_gpio3_dir_gpio3_3_dir <= '0';  -- 0x0
    ELSIF rising_edge(clk) THEN
      IF (s_gpio3_dir_wen = '1') THEN
        s_gpio3_dir_gpio3_3_dir <= i_data(3);
      ELSE
        s_gpio3_dir_gpio3_3_dir <= s_gpio3_dir_gpio3_3_dir;
      END IF;
    END IF;
  END PROCESS p_gpio3_3_dir;

  -----------------------
  -- Bit field:
  -- GPIO3_DIR(4) : GPIO3_4_DIR - FPGA Pin to Serializer #1 GENERAL_IO4 is Input (0) / Output (1)
  -- access: rw, hardware: o
  -----------------------
  -- readback
  s_gpio3_dir_rdata(4) <= s_gpio3_dir_gpio3_4_dir;
  -- output
  o_gpio3_dir_gpio3_4_dir <= s_gpio3_dir_gpio3_4_dir;

  --* purpose : GPIO3_4_DIR
  --* type    : sequential, rising edge, low active asynchronous reset
  p_gpio3_4_dir : PROCESS (clk, rst_n)
  BEGIN  -- PROCESS p_gpio3_4_dir
    IF (rst_n = '0') THEN
      s_gpio3_dir_gpio3_4_dir <= '0';  -- 0x0
    ELSIF rising_edge(clk) THEN
      IF (s_gpio3_dir_wen = '1') THEN
        s_gpio3_dir_gpio3_4_dir <= i_data(4);
      ELSE
        s_gpio3_dir_gpio3_4_dir <= s_gpio3_dir_gpio3_4_dir;
      END IF;
    END IF;
  END PROCESS p_gpio3_4_dir;


  --------------------------------------------------------------------------------
  -- [0x88] : CONTROL - Control Register
  --------------------------------------------------------------------------------

  -- CONTROL write access
  s_control_wen <= i_we WHEN (i_addr = STD_LOGIC_VECTOR(to_unsigned(136, g_addr_bits))) ELSE '0';  -- 0x88
  -- CONTROL read enable
  s_control_ren <= i_re WHEN (i_addr = STD_LOGIC_VECTOR(to_unsigned(136, g_addr_bits))) ELSE '0';  -- 0x88

  -----------------------
  -- Bit field:
  -- CONTROL(0) : POC1_EN - PoC 1 Enable
  -- access: rw, hardware: o
  -----------------------
  -- readback
  s_control_rdata(0) <= s_control_poc1_en;
  -- output
  o_control_poc1_en <= s_control_poc1_en;

  --* purpose : POC1_EN
  --* type    : sequential, rising edge, low active asynchronous reset
  p_poc1_en : PROCESS (clk, rst_n)
  BEGIN  -- PROCESS p_poc1_en
    IF (rst_n = '0') THEN
      s_control_poc1_en <= '0';  -- 0x0
    ELSIF rising_edge(clk) THEN
      IF (s_control_wen = '1') THEN
        s_control_poc1_en <= i_data(0);
      ELSE
        s_control_poc1_en <= s_control_poc1_en;
      END IF;
    END IF;
  END PROCESS p_poc1_en;

  -----------------------
  -- Bit field:
  -- CONTROL(1) : POC1_ERR - PoC 1 Error
  -- access: ro, hardware: i
  -----------------------
  -- readback
  s_control_rdata(1) <= s_control_poc1_err;

  --* purpose : POC1_ERR
  --* type    : sequential, rising edge, low active asynchronous reset
  p_poc1_err : PROCESS (clk, rst_n)
  BEGIN  -- PROCESS p_poc1_err
    IF (rst_n = '0') THEN
      s_control_poc1_err <= '0';  -- 0x0
    ELSIF rising_edge(clk) THEN
    
        s_control_poc1_err <= i_control_poc1_err;
    END IF;
  END PROCESS p_poc1_err;

  -----------------------
  -- Bit field:
  -- CONTROL(2) : POC1_BYP_EN - PoC 1 Bypass Enable
  -- access: rw, hardware: o
  -----------------------
  -- readback
  s_control_rdata(2) <= s_control_poc1_byp_en;
  -- output
  o_control_poc1_byp_en <= s_control_poc1_byp_en;

  --* purpose : POC1_BYP_EN
  --* type    : sequential, rising edge, low active asynchronous reset
  p_poc1_byp_en : PROCESS (clk, rst_n)
  BEGIN  -- PROCESS p_poc1_byp_en
    IF (rst_n = '0') THEN
      s_control_poc1_byp_en <= '0';  -- 0x0
    ELSIF rising_edge(clk) THEN
      IF (s_control_wen = '1') THEN
        s_control_poc1_byp_en <= i_data(2);
      ELSE
        s_control_poc1_byp_en <= s_control_poc1_byp_en;
      END IF;
    END IF;
  END PROCESS p_poc1_byp_en;

  -----------------------
  -- Bit field:
  -- CONTROL(3) : POC1_BYP_ERR - PoC 1 Bypass Error
  -- access: ro, hardware: i
  -----------------------
  -- readback
  s_control_rdata(3) <= s_control_poc1_byp_err;

  --* purpose : POC1_BYP_ERR
  --* type    : sequential, rising edge, low active asynchronous reset
  p_poc1_byp_err : PROCESS (clk, rst_n)
  BEGIN  -- PROCESS p_poc1_byp_err
    IF (rst_n = '0') THEN
      s_control_poc1_byp_err <= '0';  -- 0x0
    ELSIF rising_edge(clk) THEN
    
        s_control_poc1_byp_err <= i_control_poc1_byp_err;
    END IF;
  END PROCESS p_poc1_byp_err;

  -----------------------
  -- Bit field:
  -- CONTROL(4) : POC2_EN - PoC 2 Enable
  -- access: rw, hardware: o
  -----------------------
  -- readback
  s_control_rdata(4) <= s_control_poc2_en;
  -- output
  o_control_poc2_en <= s_control_poc2_en;

  --* purpose : POC2_EN
  --* type    : sequential, rising edge, low active asynchronous reset
  p_poc2_en : PROCESS (clk, rst_n)
  BEGIN  -- PROCESS p_poc2_en
    IF (rst_n = '0') THEN
      s_control_poc2_en <= '0';  -- 0x0
    ELSIF rising_edge(clk) THEN
      IF (s_control_wen = '1') THEN
        s_control_poc2_en <= i_data(4);
      ELSE
        s_control_poc2_en <= s_control_poc2_en;
      END IF;
    END IF;
  END PROCESS p_poc2_en;

  -----------------------
  -- Bit field:
  -- CONTROL(5) : POC2_ERR - PoC 2 Error
  -- access: ro, hardware: i
  -----------------------
  -- readback
  s_control_rdata(5) <= s_control_poc2_err;

  --* purpose : POC2_ERR
  --* type    : sequential, rising edge, low active asynchronous reset
  p_poc2_err : PROCESS (clk, rst_n)
  BEGIN  -- PROCESS p_poc2_err
    IF (rst_n = '0') THEN
      s_control_poc2_err <= '0';  -- 0x0
    ELSIF rising_edge(clk) THEN
    
        s_control_poc2_err <= i_control_poc2_err;
    END IF;
  END PROCESS p_poc2_err;

  -----------------------
  -- Bit field:
  -- CONTROL(6) : POC2_BYP_EN - PoC 2 Bypass Enable
  -- access: rw, hardware: o
  -----------------------
  -- readback
  s_control_rdata(6) <= s_control_poc2_byp_en;
  -- output
  o_control_poc2_byp_en <= s_control_poc2_byp_en;

  --* purpose : POC2_BYP_EN
  --* type    : sequential, rising edge, low active asynchronous reset
  p_poc2_byp_en : PROCESS (clk, rst_n)
  BEGIN  -- PROCESS p_poc2_byp_en
    IF (rst_n = '0') THEN
      s_control_poc2_byp_en <= '0';  -- 0x0
    ELSIF rising_edge(clk) THEN
      IF (s_control_wen = '1') THEN
        s_control_poc2_byp_en <= i_data(6);
      ELSE
        s_control_poc2_byp_en <= s_control_poc2_byp_en;
      END IF;
    END IF;
  END PROCESS p_poc2_byp_en;

  -----------------------
  -- Bit field:
  -- CONTROL(7) : POC2_BYP_ERR - PoC 2 Bypass Error
  -- access: ro, hardware: i
  -----------------------
  -- readback
  s_control_rdata(7) <= s_control_poc2_byp_err;

  --* purpose : POC2_BYP_ERR
  --* type    : sequential, rising edge, low active asynchronous reset
  p_poc2_byp_err : PROCESS (clk, rst_n)
  BEGIN  -- PROCESS p_poc2_byp_err
    IF (rst_n = '0') THEN
      s_control_poc2_byp_err <= '0';  -- 0x0
    ELSIF rising_edge(clk) THEN
    
        s_control_poc2_byp_err <= i_control_poc2_byp_err;
    END IF;
  END PROCESS p_poc2_byp_err;


  --------------------------------------------------------------------------------
  -- [0x89] : SM_FAULT - SM Fault Register
  --------------------------------------------------------------------------------
  s_sm_fault_rdata(5) <= '0';

  -- SM_FAULT read enable
  s_sm_fault_ren <= i_re WHEN (i_addr = STD_LOGIC_VECTOR(to_unsigned(137, g_addr_bits))) ELSE '0';  -- 0x89

  -----------------------
  -- Bit field:
  -- SM_FAULT(0) : DES0_EXT_SM_FAULT - Deserializer 0 EXT SM Fault
  -- access: ro, hardware: i
  -----------------------
  -- readback
  s_sm_fault_rdata(0) <= s_sm_fault_des0_ext_sm_fault;

  --* purpose : DES0_EXT_SM_FAULT
  --* type    : sequential, rising edge, low active asynchronous reset
  p_des0_ext_sm_fault : PROCESS (clk, rst_n)
  BEGIN  -- PROCESS p_des0_ext_sm_fault
    IF (rst_n = '0') THEN
      s_sm_fault_des0_ext_sm_fault <= '0';  -- 0x0
    ELSIF rising_edge(clk) THEN
    
        s_sm_fault_des0_ext_sm_fault <= i_sm_fault_des0_ext_sm_fault;
    END IF;
  END PROCESS p_des0_ext_sm_fault;

  -----------------------
  -- Bit field:
  -- SM_FAULT(1) : DES0_SM_FAULT - Deserializer 0 SM Fault
  -- access: ro, hardware: i
  -----------------------
  -- readback
  s_sm_fault_rdata(1) <= s_sm_fault_des0_sm_fault;

  --* purpose : DES0_SM_FAULT
  --* type    : sequential, rising edge, low active asynchronous reset
  p_des0_sm_fault : PROCESS (clk, rst_n)
  BEGIN  -- PROCESS p_des0_sm_fault
    IF (rst_n = '0') THEN
      s_sm_fault_des0_sm_fault <= '0';  -- 0x0
    ELSIF rising_edge(clk) THEN
    
        s_sm_fault_des0_sm_fault <= i_sm_fault_des0_sm_fault;
    END IF;
  END PROCESS p_des0_sm_fault;

  -----------------------
  -- Bit field:
  -- SM_FAULT(2) : DES1_EXT_SM_FAULT - Deserializer 1 EXT SM Fault
  -- access: ro, hardware: i
  -----------------------
  -- readback
  s_sm_fault_rdata(2) <= s_sm_fault_des1_ext_sm_fault;

  --* purpose : DES1_EXT_SM_FAULT
  --* type    : sequential, rising edge, low active asynchronous reset
  p_des1_ext_sm_fault : PROCESS (clk, rst_n)
  BEGIN  -- PROCESS p_des1_ext_sm_fault
    IF (rst_n = '0') THEN
      s_sm_fault_des1_ext_sm_fault <= '0';  -- 0x0
    ELSIF rising_edge(clk) THEN
    
        s_sm_fault_des1_ext_sm_fault <= i_sm_fault_des1_ext_sm_fault;
    END IF;
  END PROCESS p_des1_ext_sm_fault;

  -----------------------
  -- Bit field:
  -- SM_FAULT(3) : DES1_SM_FAULT - Deserializer 1 SM Fault
  -- access: ro, hardware: i
  -----------------------
  -- readback
  s_sm_fault_rdata(3) <= s_sm_fault_des1_sm_fault;

  --* purpose : DES1_SM_FAULT
  --* type    : sequential, rising edge, low active asynchronous reset
  p_des1_sm_fault : PROCESS (clk, rst_n)
  BEGIN  -- PROCESS p_des1_sm_fault
    IF (rst_n = '0') THEN
      s_sm_fault_des1_sm_fault <= '0';  -- 0x0
    ELSIF rising_edge(clk) THEN
    
        s_sm_fault_des1_sm_fault <= i_sm_fault_des1_sm_fault;
    END IF;
  END PROCESS p_des1_sm_fault;

  -----------------------
  -- Bit field:
  -- SM_FAULT(4) : SER0_EXT_SM_FAULT - Serializer 0 EXT SM Fault
  -- access: ro, hardware: i
  -----------------------
  -- readback
  s_sm_fault_rdata(4) <= s_sm_fault_ser0_ext_sm_fault;

  --* purpose : SER0_EXT_SM_FAULT
  --* type    : sequential, rising edge, low active asynchronous reset
  p_ser0_ext_sm_fault : PROCESS (clk, rst_n)
  BEGIN  -- PROCESS p_ser0_ext_sm_fault
    IF (rst_n = '0') THEN
      s_sm_fault_ser0_ext_sm_fault <= '0';  -- 0x0
    ELSIF rising_edge(clk) THEN
    
        s_sm_fault_ser0_ext_sm_fault <= i_sm_fault_ser0_ext_sm_fault;
    END IF;
  END PROCESS p_ser0_ext_sm_fault;

  -----------------------
  -- Bit field:
  -- SM_FAULT(6) : SER1_EXT_SM_FAULT - Serializer 1 EXT SM Fault
  -- access: ro, hardware: i
  -----------------------
  -- readback
  s_sm_fault_rdata(6) <= s_sm_fault_ser1_ext_sm_fault;

  --* purpose : SER1_EXT_SM_FAULT
  --* type    : sequential, rising edge, low active asynchronous reset
  p_ser1_ext_sm_fault : PROCESS (clk, rst_n)
  BEGIN  -- PROCESS p_ser1_ext_sm_fault
    IF (rst_n = '0') THEN
      s_sm_fault_ser1_ext_sm_fault <= '0';  -- 0x0
    ELSIF rising_edge(clk) THEN
    
        s_sm_fault_ser1_ext_sm_fault <= i_sm_fault_ser1_ext_sm_fault;
    END IF;
  END PROCESS p_ser1_ext_sm_fault;


  --------------------------------------------------------------------------------
  -- [0x8f] : GPIO_CNT_CTL - Deserializer GPIO Edge Counter Control
  --------------------------------------------------------------------------------

  -- GPIO_CNT_CTL write access
  s_gpio_cnt_ctl_wen <= i_we WHEN (i_addr = STD_LOGIC_VECTOR(to_unsigned(143, g_addr_bits))) ELSE '0';  -- 0x8f
  -- GPIO_CNT_CTL read enable
  s_gpio_cnt_ctl_ren <= i_re WHEN (i_addr = STD_LOGIC_VECTOR(to_unsigned(143, g_addr_bits))) ELSE '0';  -- 0x8f

  -----------------------
  -- Bit field:
  -- GPIO_CNT_CTL(3 DOWNTO 0) : DES0_GPIO_SEL - Deserializer #0 GPIO Select
  -- access: rw, hardware: o
  -----------------------
  -- readback
  s_gpio_cnt_ctl_rdata(3 DOWNTO 0) <= s_gpio_cnt_ctl_des0_gpio_sel;
  -- output
  o_gpio_cnt_ctl_des0_gpio_sel <= s_gpio_cnt_ctl_des0_gpio_sel;

  --* purpose : DES0_GPIO_SEL
  --* type    : sequential, rising edge, low active asynchronous reset
  p_des0_gpio_sel : PROCESS (clk, rst_n)
  BEGIN  -- PROCESS p_des0_gpio_sel
    IF (rst_n = '0') THEN
      s_gpio_cnt_ctl_des0_gpio_sel <= (OTHERS => '0');  -- 0x0
    ELSIF rising_edge(clk) THEN
      IF (s_gpio_cnt_ctl_wen = '1') THEN
        s_gpio_cnt_ctl_des0_gpio_sel(3 DOWNTO 0) <= i_data(3 DOWNTO 0);
      ELSE
        s_gpio_cnt_ctl_des0_gpio_sel <= s_gpio_cnt_ctl_des0_gpio_sel;
      END IF;
    END IF;
  END PROCESS p_des0_gpio_sel;

  -----------------------
  -- Bit field:
  -- GPIO_CNT_CTL(7 DOWNTO 4) : DES1_GPIO_SEL - Deserializer #1 GPIO Select
  -- access: rw, hardware: o
  -----------------------
  -- readback
  s_gpio_cnt_ctl_rdata(7 DOWNTO 4) <= s_gpio_cnt_ctl_des1_gpio_sel;
  -- output
  o_gpio_cnt_ctl_des1_gpio_sel <= s_gpio_cnt_ctl_des1_gpio_sel;

  --* purpose : DES1_GPIO_SEL
  --* type    : sequential, rising edge, low active asynchronous reset
  p_des1_gpio_sel : PROCESS (clk, rst_n)
  BEGIN  -- PROCESS p_des1_gpio_sel
    IF (rst_n = '0') THEN
      s_gpio_cnt_ctl_des1_gpio_sel <= (OTHERS => '0');  -- 0x0
    ELSIF rising_edge(clk) THEN
      IF (s_gpio_cnt_ctl_wen = '1') THEN
        s_gpio_cnt_ctl_des1_gpio_sel(3 DOWNTO 0) <= i_data(7 DOWNTO 4);
      ELSE
        s_gpio_cnt_ctl_des1_gpio_sel <= s_gpio_cnt_ctl_des1_gpio_sel;
      END IF;
    END IF;
  END PROCESS p_des1_gpio_sel;


  --------------------------------------------------------------------------------
  -- [0x90] : DES0_GPIO_RE_CNT - Deserializer #0 GPIO Rising Edge Counter
  --------------------------------------------------------------------------------

  -- DES0_GPIO_RE_CNT read enable
  s_des0_gpio_re_cnt_ren <= i_re WHEN (i_addr = STD_LOGIC_VECTOR(to_unsigned(144, g_addr_bits))) ELSE '0';  -- 0x90

  -----------------------
  -- Bit field:
  -- DES0_GPIO_RE_CNT(7 DOWNTO 0) : EDGE_CNT - Deserializer #0 Rising Edge Counter \newline Count the rising edges of the selected Deserializer #0 GENERAL_IO.
  -- access: roc, hardware: ia
  -----------------------
  -- access notification
  ---- read notify
  o_des0_gpio_re_cnt_edge_cnt_rd <= s_des0_gpio_re_cnt_ren;
  -- readback
  s_des0_gpio_re_cnt_rdata(7 DOWNTO 0) <= s_des0_gpio_re_cnt_edge_cnt;

  --* purpose : EDGE_CNT
  --* type    : sequential, rising edge, low active asynchronous reset
  p_edge_cnt : PROCESS (clk, rst_n)
  BEGIN  -- PROCESS p_edge_cnt
    IF (rst_n = '0') THEN
      s_des0_gpio_re_cnt_edge_cnt <= (OTHERS => '0');  -- 0x0
    ELSIF rising_edge(clk) THEN
      IF (s_des0_gpio_re_cnt_ren = '1' and s_des0_gpio_re_cnt_ren = '0') THEN
            s_des0_gpio_re_cnt_edge_cnt <= (OTHERS => '0');    
        s_des0_gpio_re_cnt_edge_cnt <= i_des0_gpio_re_cnt_edge_cnt;
    END IF;
  END PROCESS p_edge_cnt;


  --------------------------------------------------------------------------------
  -- [0x91] : DES0_GPIO_FE_CNT - Deserializer #0 GPIO Falling Edge Counter
  --------------------------------------------------------------------------------

  -- DES0_GPIO_FE_CNT read enable
  s_des0_gpio_fe_cnt_ren <= i_re WHEN (i_addr = STD_LOGIC_VECTOR(to_unsigned(145, g_addr_bits))) ELSE '0';  -- 0x91

  -----------------------
  -- Bit field:
  -- DES0_GPIO_FE_CNT(7 DOWNTO 0) : EDGE_CNT - Deserializer #0 Falling Edge Counter \newline Count the rising edges of the selected Deserializer #0 GENERAL_IO.
  -- access: roc, hardware: ia
  -----------------------
  -- access notification
  ---- read notify
  o_des0_gpio_fe_cnt_edge_cnt_rd <= s_des0_gpio_fe_cnt_ren;
  -- readback
  s_des0_gpio_fe_cnt_rdata(7 DOWNTO 0) <= s_des0_gpio_fe_cnt_edge_cnt;

  --* purpose : EDGE_CNT
  --* type    : sequential, rising edge, low active asynchronous reset
  p_edge_cnt : PROCESS (clk, rst_n)
  BEGIN  -- PROCESS p_edge_cnt
    IF (rst_n = '0') THEN
      s_des0_gpio_fe_cnt_edge_cnt <= (OTHERS => '0');  -- 0x0
    ELSIF rising_edge(clk) THEN
      IF (s_des0_gpio_fe_cnt_ren = '1' and s_des0_gpio_fe_cnt_ren = '0') THEN
            s_des0_gpio_fe_cnt_edge_cnt <= (OTHERS => '0');    
        s_des0_gpio_fe_cnt_edge_cnt <= i_des0_gpio_fe_cnt_edge_cnt;
    END IF;
  END PROCESS p_edge_cnt;


  --------------------------------------------------------------------------------
  -- [0x92] : DES1_GPIO_RE_CNT - Deserializer #1 GPIO Rising Edge Counter
  --------------------------------------------------------------------------------

  -- DES1_GPIO_RE_CNT read enable
  s_des1_gpio_re_cnt_ren <= i_re WHEN (i_addr = STD_LOGIC_VECTOR(to_unsigned(146, g_addr_bits))) ELSE '0';  -- 0x92

  -----------------------
  -- Bit field:
  -- DES1_GPIO_RE_CNT(7 DOWNTO 0) : EDGE_CNT - Deserializer #1 Rising Edge Counter \newline Count the rising edges of the selected Deserializer #1 GENERAL_IO.
  -- access: roc, hardware: ia
  -----------------------
  -- access notification
  ---- read notify
  o_des1_gpio_re_cnt_edge_cnt_rd <= s_des1_gpio_re_cnt_ren;
  -- readback
  s_des1_gpio_re_cnt_rdata(7 DOWNTO 0) <= s_des1_gpio_re_cnt_edge_cnt;

  --* purpose : EDGE_CNT
  --* type    : sequential, rising edge, low active asynchronous reset
  p_edge_cnt : PROCESS (clk, rst_n)
  BEGIN  -- PROCESS p_edge_cnt
    IF (rst_n = '0') THEN
      s_des1_gpio_re_cnt_edge_cnt <= (OTHERS => '0');  -- 0x0
    ELSIF rising_edge(clk) THEN
      IF (s_des1_gpio_re_cnt_ren = '1' and s_des1_gpio_re_cnt_ren = '0') THEN
            s_des1_gpio_re_cnt_edge_cnt <= (OTHERS => '0');    
        s_des1_gpio_re_cnt_edge_cnt <= i_des1_gpio_re_cnt_edge_cnt;
    END IF;
  END PROCESS p_edge_cnt;


  --------------------------------------------------------------------------------
  -- [0x93] : DES1_GPIO_FE_CNT - Deserializer #1 GPIO Falling Edge Counter
  --------------------------------------------------------------------------------

  -- DES1_GPIO_FE_CNT read enable
  s_des1_gpio_fe_cnt_ren <= i_re WHEN (i_addr = STD_LOGIC_VECTOR(to_unsigned(147, g_addr_bits))) ELSE '0';  -- 0x93

  -----------------------
  -- Bit field:
  -- DES1_GPIO_FE_CNT(7 DOWNTO 0) : EDGE_CNT - Deserializer #1 Falling Edge Counter \newline Count the falling edges of the selected Deserializer #1 GENERAL_IO.
  -- access: roc, hardware: ia
  -----------------------
  -- access notification
  ---- read notify
  o_des1_gpio_fe_cnt_edge_cnt_rd <= s_des1_gpio_fe_cnt_ren;
  -- readback
  s_des1_gpio_fe_cnt_rdata(7 DOWNTO 0) <= s_des1_gpio_fe_cnt_edge_cnt;

  --* purpose : EDGE_CNT
  --* type    : sequential, rising edge, low active asynchronous reset
  p_edge_cnt : PROCESS (clk, rst_n)
  BEGIN  -- PROCESS p_edge_cnt
    IF (rst_n = '0') THEN
      s_des1_gpio_fe_cnt_edge_cnt <= (OTHERS => '0');  -- 0x0
    ELSIF rising_edge(clk) THEN
      IF (s_des1_gpio_fe_cnt_ren = '1' and s_des1_gpio_fe_cnt_ren = '0') THEN
            s_des1_gpio_fe_cnt_edge_cnt <= (OTHERS => '0');    
        s_des1_gpio_fe_cnt_edge_cnt <= i_des1_gpio_fe_cnt_edge_cnt;
    END IF;
  END PROCESS p_edge_cnt;


  --------------------------------------------------------------------------------
  -- [0x9e] : GPIO4_VALUE - GPIO4 Value
  --------------------------------------------------------------------------------
  s_gpio4_value_rdata(7 DOWNTO 4) <= (OTHERS => '0');

  -- GPIO4_VALUE write access
  s_gpio4_value_wen <= i_we WHEN (i_addr = STD_LOGIC_VECTOR(to_unsigned(158, g_addr_bits))) ELSE '0';  -- 0x9e
  -- GPIO4_VALUE read enable
  s_gpio4_value_ren <= i_re WHEN (i_addr = STD_LOGIC_VECTOR(to_unsigned(158, g_addr_bits))) ELSE '0';  -- 0x9e

  -----------------------
  -- Bit field:
  -- GPIO4_VALUE(0) : GPIO4_0 - Net 'SPI_CLK Value'
  -- access: rw, hardware: io
  -----------------------
  -- readback
  s_gpio4_value_rdata(0) <= s_gpio4_value_gpio4_0;
  -- output
  o_gpio4_value_gpio4_0 <= s_gpio4_value_gpio4_0;

  --* purpose : GPIO4_0
  --* type    : sequential, rising edge, low active asynchronous reset
  p_gpio4_0 : PROCESS (clk, rst_n)
  BEGIN  -- PROCESS p_gpio4_0
    IF (rst_n = '0') THEN
      s_gpio4_value_gpio4_0 <= '0';  -- 0x0
    ELSIF rising_edge(clk) THEN
      IF (s_gpio4_value_wen = '1') THEN
        s_gpio4_value_gpio4_0 <= i_data(0);
      ELSE
        s_gpio4_value_gpio4_0 <= i_gpio4_value_gpio4_0;
      END IF;
    END IF;
  END PROCESS p_gpio4_0;

  -----------------------
  -- Bit field:
  -- GPIO4_VALUE(1) : GPIO4_1 - Net 'SPI_CS Value'
  -- access: rw, hardware: io
  -----------------------
  -- readback
  s_gpio4_value_rdata(1) <= s_gpio4_value_gpio4_1;
  -- output
  o_gpio4_value_gpio4_1 <= s_gpio4_value_gpio4_1;

  --* purpose : GPIO4_1
  --* type    : sequential, rising edge, low active asynchronous reset
  p_gpio4_1 : PROCESS (clk, rst_n)
  BEGIN  -- PROCESS p_gpio4_1
    IF (rst_n = '0') THEN
      s_gpio4_value_gpio4_1 <= '0';  -- 0x0
    ELSIF rising_edge(clk) THEN
      IF (s_gpio4_value_wen = '1') THEN
        s_gpio4_value_gpio4_1 <= i_data(1);
      ELSE
        s_gpio4_value_gpio4_1 <= i_gpio4_value_gpio4_1;
      END IF;
    END IF;
  END PROCESS p_gpio4_1;

  -----------------------
  -- Bit field:
  -- GPIO4_VALUE(2) : GPIO4_2 - Net 'SPI_MOSI Value'
  -- access: rw, hardware: io
  -----------------------
  -- readback
  s_gpio4_value_rdata(2) <= s_gpio4_value_gpio4_2;
  -- output
  o_gpio4_value_gpio4_2 <= s_gpio4_value_gpio4_2;

  --* purpose : GPIO4_2
  --* type    : sequential, rising edge, low active asynchronous reset
  p_gpio4_2 : PROCESS (clk, rst_n)
  BEGIN  -- PROCESS p_gpio4_2
    IF (rst_n = '0') THEN
      s_gpio4_value_gpio4_2 <= '0';  -- 0x0
    ELSIF rising_edge(clk) THEN
      IF (s_gpio4_value_wen = '1') THEN
        s_gpio4_value_gpio4_2 <= i_data(2);
      ELSE
        s_gpio4_value_gpio4_2 <= i_gpio4_value_gpio4_2;
      END IF;
    END IF;
  END PROCESS p_gpio4_2;

  -----------------------
  -- Bit field:
  -- GPIO4_VALUE(3) : GPIO4_3 - Net 'SPI_MISO Value'
  -- access: rw, hardware: io
  -----------------------
  -- readback
  s_gpio4_value_rdata(3) <= s_gpio4_value_gpio4_3;
  -- output
  o_gpio4_value_gpio4_3 <= s_gpio4_value_gpio4_3;

  --* purpose : GPIO4_3
  --* type    : sequential, rising edge, low active asynchronous reset
  p_gpio4_3 : PROCESS (clk, rst_n)
  BEGIN  -- PROCESS p_gpio4_3
    IF (rst_n = '0') THEN
      s_gpio4_value_gpio4_3 <= '0';  -- 0x0
    ELSIF rising_edge(clk) THEN
      IF (s_gpio4_value_wen = '1') THEN
        s_gpio4_value_gpio4_3 <= i_data(3);
      ELSE
        s_gpio4_value_gpio4_3 <= i_gpio4_value_gpio4_3;
      END IF;
    END IF;
  END PROCESS p_gpio4_3;


  --------------------------------------------------------------------------------
  -- [0x9f] : GPIO4_DIR - GPIO4 Direction
  --------------------------------------------------------------------------------
  s_gpio4_dir_rdata(7 DOWNTO 4) <= (OTHERS => '0');

  -- GPIO4_DIR write access
  s_gpio4_dir_wen <= i_we WHEN (i_addr = STD_LOGIC_VECTOR(to_unsigned(159, g_addr_bits))) ELSE '0';  -- 0x9f
  -- GPIO4_DIR read enable
  s_gpio4_dir_ren <= i_re WHEN (i_addr = STD_LOGIC_VECTOR(to_unsigned(159, g_addr_bits))) ELSE '0';  -- 0x9f

  -----------------------
  -- Bit field:
  -- GPIO4_DIR(0) : GPIO4_2_DIR - FPGA Pin to net 'SPI_CLK' is Input (0) / Output (1)
  -- access: rw, hardware: o
  -----------------------
  -- readback
  s_gpio4_dir_rdata(0) <= s_gpio4_dir_gpio4_2_dir;
  -- output
  o_gpio4_dir_gpio4_2_dir <= s_gpio4_dir_gpio4_2_dir;

  --* purpose : GPIO4_2_DIR
  --* type    : sequential, rising edge, low active asynchronous reset
  p_gpio4_2_dir : PROCESS (clk, rst_n)
  BEGIN  -- PROCESS p_gpio4_2_dir
    IF (rst_n = '0') THEN
      s_gpio4_dir_gpio4_2_dir <= '0';  -- 0x0
    ELSIF rising_edge(clk) THEN
      IF (s_gpio4_dir_wen = '1') THEN
        s_gpio4_dir_gpio4_2_dir <= i_data(0);
      ELSE
        s_gpio4_dir_gpio4_2_dir <= s_gpio4_dir_gpio4_2_dir;
      END IF;
    END IF;
  END PROCESS p_gpio4_2_dir;

  -----------------------
  -- Bit field:
  -- GPIO4_DIR(1) : GPIO4_3_DIR - FPGA Pin to net 'SPI_CS' is Input (0) / Output (1)
  -- access: rw, hardware: o
  -----------------------
  -- readback
  s_gpio4_dir_rdata(1) <= s_gpio4_dir_gpio4_3_dir;
  -- output
  o_gpio4_dir_gpio4_3_dir <= s_gpio4_dir_gpio4_3_dir;

  --* purpose : GPIO4_3_DIR
  --* type    : sequential, rising edge, low active asynchronous reset
  p_gpio4_3_dir : PROCESS (clk, rst_n)
  BEGIN  -- PROCESS p_gpio4_3_dir
    IF (rst_n = '0') THEN
      s_gpio4_dir_gpio4_3_dir <= '0';  -- 0x0
    ELSIF rising_edge(clk) THEN
      IF (s_gpio4_dir_wen = '1') THEN
        s_gpio4_dir_gpio4_3_dir <= i_data(1);
      ELSE
        s_gpio4_dir_gpio4_3_dir <= s_gpio4_dir_gpio4_3_dir;
      END IF;
    END IF;
  END PROCESS p_gpio4_3_dir;

  -----------------------
  -- Bit field:
  -- GPIO4_DIR(2) : GPIO4_4_DIR - FPGA Pin to net 'SPI_MOSI' is Input (0) / Output (1)
  -- access: rw, hardware: o
  -----------------------
  -- readback
  s_gpio4_dir_rdata(2) <= s_gpio4_dir_gpio4_4_dir;
  -- output
  o_gpio4_dir_gpio4_4_dir <= s_gpio4_dir_gpio4_4_dir;

  --* purpose : GPIO4_4_DIR
  --* type    : sequential, rising edge, low active asynchronous reset
  p_gpio4_4_dir : PROCESS (clk, rst_n)
  BEGIN  -- PROCESS p_gpio4_4_dir
    IF (rst_n = '0') THEN
      s_gpio4_dir_gpio4_4_dir <= '0';  -- 0x0
    ELSIF rising_edge(clk) THEN
      IF (s_gpio4_dir_wen = '1') THEN
        s_gpio4_dir_gpio4_4_dir <= i_data(2);
      ELSE
        s_gpio4_dir_gpio4_4_dir <= s_gpio4_dir_gpio4_4_dir;
      END IF;
    END IF;
  END PROCESS p_gpio4_4_dir;

  -----------------------
  -- Bit field:
  -- GPIO4_DIR(3) : GPIO4_5_DIR - FPGA Pin to net 'SPI_MISO' is Input (0) / Output (1)
  -- access: rw, hardware: o
  -----------------------
  -- readback
  s_gpio4_dir_rdata(3) <= s_gpio4_dir_gpio4_5_dir;
  -- output
  o_gpio4_dir_gpio4_5_dir <= s_gpio4_dir_gpio4_5_dir;

  --* purpose : GPIO4_5_DIR
  --* type    : sequential, rising edge, low active asynchronous reset
  p_gpio4_5_dir : PROCESS (clk, rst_n)
  BEGIN  -- PROCESS p_gpio4_5_dir
    IF (rst_n = '0') THEN
      s_gpio4_dir_gpio4_5_dir <= '0';  -- 0x0
    ELSIF rising_edge(clk) THEN
      IF (s_gpio4_dir_wen = '1') THEN
        s_gpio4_dir_gpio4_5_dir <= i_data(3);
      ELSE
        s_gpio4_dir_gpio4_5_dir <= s_gpio4_dir_gpio4_5_dir;
      END IF;
    END IF;
  END PROCESS p_gpio4_5_dir;



  --------------------------------------------------------------------------------
  -- Address decoder
  --------------------------------------------------------------------------------
  --* purpose : Register address decoder
  --* type    : sequential, rising edge, low active asynchronous reset
  p_addr_decode : PROCESS (clk, rst_n)
  BEGIN  -- PROCESS p_addr_decode
    IF (rst_n = '0') THEN
      o_data <= (OTHERS => '0');  -- 0x0
    ELSIF rising_edge(clk) THEN
      IF (i_addr = STD_LOGIC_VECTOR(to_unsigned(128, g_addr_bits))) THEN  -- 0x80
        o_data <= s_gpio0_value_rdata;
      ELSIF (i_addr = STD_LOGIC_VECTOR(to_unsigned(129, g_addr_bits))) THEN  -- 0x81
        o_data <= s_gpio0_dir_rdata;
      ELSIF (i_addr = STD_LOGIC_VECTOR(to_unsigned(130, g_addr_bits))) THEN  -- 0x82
        o_data <= s_gpio1_value_rdata;
      ELSIF (i_addr = STD_LOGIC_VECTOR(to_unsigned(131, g_addr_bits))) THEN  -- 0x83
        o_data <= s_gpio1_dir_rdata;
      ELSIF (i_addr = STD_LOGIC_VECTOR(to_unsigned(132, g_addr_bits))) THEN  -- 0x84
        o_data <= s_gpio2_value_rdata;
      ELSIF (i_addr = STD_LOGIC_VECTOR(to_unsigned(133, g_addr_bits))) THEN  -- 0x85
        o_data <= s_gpio2_dir_rdata;
      ELSIF (i_addr = STD_LOGIC_VECTOR(to_unsigned(134, g_addr_bits))) THEN  -- 0x86
        o_data <= s_gpio3_value_rdata;
      ELSIF (i_addr = STD_LOGIC_VECTOR(to_unsigned(135, g_addr_bits))) THEN  -- 0x87
        o_data <= s_gpio3_dir_rdata;
      ELSIF (i_addr = STD_LOGIC_VECTOR(to_unsigned(136, g_addr_bits))) THEN  -- 0x88
        o_data <= s_control_rdata;
      ELSIF (i_addr = STD_LOGIC_VECTOR(to_unsigned(137, g_addr_bits))) THEN  -- 0x89
        o_data <= s_sm_fault_rdata;
      ELSIF (i_addr = STD_LOGIC_VECTOR(to_unsigned(143, g_addr_bits))) THEN  -- 0x8f
        o_data <= s_gpio_cnt_ctl_rdata;
      ELSIF (i_addr = STD_LOGIC_VECTOR(to_unsigned(144, g_addr_bits))) THEN  -- 0x90
        o_data <= s_des0_gpio_re_cnt_rdata;
      ELSIF (i_addr = STD_LOGIC_VECTOR(to_unsigned(145, g_addr_bits))) THEN  -- 0x91
        o_data <= s_des0_gpio_fe_cnt_rdata;
      ELSIF (i_addr = STD_LOGIC_VECTOR(to_unsigned(146, g_addr_bits))) THEN  -- 0x92
        o_data <= s_des1_gpio_re_cnt_rdata;
      ELSIF (i_addr = STD_LOGIC_VECTOR(to_unsigned(147, g_addr_bits))) THEN  -- 0x93
        o_data <= s_des1_gpio_fe_cnt_rdata;
      ELSIF (i_addr = STD_LOGIC_VECTOR(to_unsigned(158, g_addr_bits))) THEN  -- 0x9e
        o_data <= s_gpio4_value_rdata;
      ELSIF (i_addr = STD_LOGIC_VECTOR(to_unsigned(159, g_addr_bits))) THEN  -- 0x9f
        o_data <= s_gpio4_dir_rdata;
      ELSE 
        o_data <= (OTHERS => '0');  -- 0x0
      END IF;
    END IF;
  END PROCESS p_addr_decode;

END ARCHITECTURE rtl;