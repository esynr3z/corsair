

-- Created with Corsair vgit-latest
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity regs is
generic(
    ADDR_W : integer := 16;
    DATA_W : integer := 32;
    STRB_W : integer := 4
);
port(
    clk    : in std_logic;
    rst    : in std_logic;
    -- DATA.FIFO
    csr_data_fifo_rvalid : in std_logic;
    csr_data_fifo_ren : out std_logic;
    csr_data_fifo_in : in std_logic_vector(7 downto 0);
    csr_data_fifo_out : out std_logic_vector(7 downto 0);
    csr_data_fifo_wready : in std_logic;
    csr_data_fifo_wen : out std_logic;
    -- DATA.FERR
    csr_data_ferr_in : in std_logic;
    -- DATA.PERR
    csr_data_perr_in : in std_logic;

    -- STAT.BUSY
    csr_stat_busy_en : in std_logic;
    csr_stat_busy_in : in std_logic;
    -- STAT.RXE
    csr_stat_rxe_in : in std_logic;
    -- STAT.TXF
    csr_stat_txf_in : in std_logic;

    -- CTRL.BAUD
    csr_ctrl_baud_out : out std_logic_vector(1 downto 0);
    -- CTRL.TXEN
    csr_ctrl_txen_en : in std_logic;
    csr_ctrl_txen_in : in std_logic;
    csr_ctrl_txen_out : out std_logic;
    -- CTRL.RXEN
    csr_ctrl_rxen_en : in std_logic;
    csr_ctrl_rxen_in : in std_logic;
    csr_ctrl_rxen_out : out std_logic;
    -- CTRL.TXST
    csr_ctrl_txst_out : out std_logic;

    -- LPMODE.DIV
    csr_lpmode_div_out : out std_logic_vector(7 downto 0);
    -- LPMODE.EN
    csr_lpmode_en_out : out std_logic;

    -- INTSTAT.TX
    csr_intstat_tx_set : in std_logic;
    -- INTSTAT.RX
    csr_intstat_rx_set : in std_logic;

    -- ID.UID

    -- AXI-Lite
    axil_awaddr   : in  std_logic_vector(ADDR_W-1 downto 0);
    axil_awprot   : in  std_logic_vector(2 downto 0);
    axil_awvalid  : in  std_logic;
    axil_awready  : out std_logic;
    axil_wdata    : in  std_logic_vector(DATA_W-1 downto 0);
    axil_wstrb    : in  std_logic_vector(STRB_W-1 downto 0);
    axil_wvalid   : in  std_logic;
    axil_wready   : out std_logic;
    axil_bresp    : out std_logic_vector(1 downto 0);
    axil_bvalid   : out std_logic;
    axil_bready   : in  std_logic;
    axil_araddr   : in  std_logic_vector(ADDR_W-1 downto 0);
    axil_arprot   : in  std_logic_vector(2 downto 0);
    axil_arvalid  : in  std_logic;
    axil_arready  : out std_logic;
    axil_rdata    : out std_logic_vector(DATA_W-1 downto 0);
    axil_rresp    : out std_logic_vector(1 downto 0);
    axil_rvalid   : out std_logic;
    axil_rready   : in  std_logic

);
end entity;

architecture rtl of regs is
subtype ADDR_T is std_logic_vector(15 downto 0);

signal wready : std_logic;
signal waddr  : std_logic_vector(ADDR_W-1 downto 0);
signal wdata  : std_logic_vector(DATA_W-1 downto 0);
signal wen    : std_logic;
signal wstrb  : std_logic_vector(STRB_W-1 downto 0);
signal rdata  : std_logic_vector(DATA_W-1 downto 0);
signal rvalid : std_logic;
signal raddr  : std_logic_vector(ADDR_W-1 downto 0);
signal ren    : std_logic;
signal waddr_int       : std_logic_vector(ADDR_W-1 downto 0);
signal raddr_int       : std_logic_vector(ADDR_W-1 downto 0);
signal wdata_int       : std_logic_vector(DATA_W-1 downto 0);
signal strb_int        : std_logic_vector(STRB_W-1 downto 0);
signal awflag          : std_logic;
signal wflag           : std_logic;
signal arflag          : std_logic;
signal rflag           : std_logic;
signal wen_int         : std_logic;
signal ren_int         : std_logic;
signal axil_bvalid_int : std_logic;
signal axil_rdata_int  : std_logic_vector(DATA_W-1 downto 0);
signal axil_rvalid_int : std_logic;

signal csr_data_rdata : std_logic_vector(31 downto 0);
signal csr_data_wen : std_logic;
signal csr_data_ren : std_logic;
signal csr_data_ren_ff : std_logic;
signal csr_data_fifo_ff : std_logic_vector(7 downto 0);
signal csr_data_fifo_rvalid_ff : std_logic;
signal csr_data_ferr_ff : std_logic;
signal csr_data_perr_ff : std_logic;

signal csr_stat_rdata : std_logic_vector(31 downto 0);
signal csr_stat_ren : std_logic;
signal csr_stat_ren_ff : std_logic;
signal csr_stat_busy_ff : std_logic;
signal csr_stat_rxe_ff : std_logic;
signal csr_stat_txf_ff : std_logic;

signal csr_ctrl_rdata : std_logic_vector(31 downto 0);
signal csr_ctrl_wen : std_logic;
signal csr_ctrl_ren : std_logic;
signal csr_ctrl_ren_ff : std_logic;
signal csr_ctrl_baud_ff : std_logic_vector(1 downto 0);
signal csr_ctrl_txen_ff : std_logic;
signal csr_ctrl_rxen_ff : std_logic;
signal csr_ctrl_txst_ff : std_logic;

signal csr_lpmode_rdata : std_logic_vector(31 downto 0);
signal csr_lpmode_wen : std_logic;
signal csr_lpmode_ren : std_logic;
signal csr_lpmode_ren_ff : std_logic;
signal csr_lpmode_div_ff : std_logic_vector(7 downto 0);
signal csr_lpmode_en_ff : std_logic;

signal csr_intstat_rdata : std_logic_vector(31 downto 0);
signal csr_intstat_wen : std_logic;
signal csr_intstat_ren : std_logic;
signal csr_intstat_ren_ff : std_logic;
signal csr_intstat_tx_ff : std_logic;
signal csr_intstat_rx_ff : std_logic;

signal csr_id_rdata : std_logic_vector(31 downto 0);
signal csr_id_ren : std_logic;
signal csr_id_ren_ff : std_logic;
signal csr_id_uid_ff : std_logic_vector(31 downto 0);

signal wready_drv : std_logic;
signal rvalid_drv : std_logic;
signal rdata_ff : std_logic_vector(31 downto 0);
signal rvalid_ff : std_logic;
begin

axil_awready <= not awflag;
axil_wready  <= not wflag;
axil_bvalid  <= axil_bvalid_int;
waddr        <= waddr_int;
wdata        <= wdata_int;
wstrb        <= strb_int;
wen_int      <= awflag and wflag;
wen          <= wen_int;
axil_bresp   <= b"00";

process (clk) begin
if rising_edge(clk) then
if (rst = '1') then
    waddr_int <= (others => '0');
    wdata_int <= (others => '0');
    strb_int <= (others => '0');
    awflag <= '0';
    wflag <= '0';
    axil_bvalid_int <= '0';
else
    if (axil_awvalid = '1' and awflag = '0') then
        awflag    <= '1';
        waddr_int <= axil_awaddr;
    elsif (wen_int = '1' and wready = '1') then
        awflag    <= '0';
    end if;
    if (axil_wvalid = '1' and wflag = '0') then
        wflag     <= '1';
        wdata_int <= axil_wdata;
        strb_int  <= axil_wstrb;
    elsif (wen_int = '1' and wready = '1') then
        wflag     <= '0';
    end if;
    if (axil_bvalid_int = '1' and axil_bready = '1') then
        axil_bvalid_int <= '0';
    elsif ((axil_wvalid = '1' and awflag = '1') or (axil_awvalid = '1' and wflag = '1') or (wflag = '1' and awflag = '1')) then
        axil_bvalid_int <= wready;
    end if;
end if;
end if;
end process;


axil_arready <= not arflag;
axil_rdata   <= axil_rdata_int;
axil_rvalid  <= axil_rvalid_int;
raddr        <= raddr_int;
ren_int      <= arflag and (not rflag);
ren          <= ren_int;
axil_rresp   <= b"00";

process (clk) begin
if rising_edge(clk) then
if (rst = '1') then
    raddr_int <= (others => '0');
    arflag <= '0';
    rflag <= '0';
    axil_rdata_int <= (others => '0');
    axil_rvalid_int <= '0';
else
    if (axil_arvalid = '1' and arflag = '0') then
        arflag    <= '1';
        raddr_int <= axil_araddr;
    elsif (axil_rvalid_int = '1' and axil_rready = '1') then
        arflag    <= '0';
    end if;
    if (rvalid = '1' and ren_int = '1' and rflag = '0') then
        rflag <= '1';
    elsif (axil_rvalid_int = '1' and axil_rready = '1') then
        rflag <= '0';
    end if;
    if (rvalid = '1' and axil_rvalid_int = '0') then
        axil_rdata_int  <= rdata;
        axil_rvalid_int <= '1';
    elsif (axil_rvalid_int = '1' and axil_rready = '1') then
        axil_rvalid_int <= '0';
    end if;
end if;
end if;
end process;


--------------------------------------------------------------------------------
-- CSR:
-- [0x4] - DATA - Data register
--------------------------------------------------------------------------------
csr_data_rdata(15 downto 8) <= (others => '0');
csr_data_rdata(31 downto 18) <= (others => '0');

csr_data_wen <= wen when (waddr = "0000000000000100") else '0'; -- 0x4

csr_data_ren <= ren when (raddr = "0000000000000100") else '0'; -- 0x4
process (clk) begin
if rising_edge(clk) then
if (rst = '1') then
    csr_data_ren_ff <= '0'; -- 0x0
else
        csr_data_ren_ff <= csr_data_ren;
end if;
end if;
end process;

-----------------------
-- Bit field:
-- DATA(7 downto 0) - FIFO - Write to push value to TX FIFO, read to get data from RX FIFO
-- access: rw, hardware: q
-----------------------

csr_data_rdata(7 downto 0) <= csr_data_fifo_in;

csr_data_fifo_out <= wdata(7 downto 0);
csr_data_fifo_ren <= csr_data_ren and (not csr_data_ren_ff);
csr_data_fifo_wen <= csr_data_wen;

process (clk) begin
if rising_edge(clk) then
if (rst = '1') then
    csr_data_fifo_ff <= "00000000"; -- 0x0
else
        if (csr_data_wen = '1') then
            if (wstrb(0) = '1') then
                csr_data_fifo_ff(7 downto 0) <= wdata(7 downto 0);
            end if;
        else
            csr_data_fifo_ff <= csr_data_fifo_ff;
        end if;
end if;
end if;
end process;


process (clk) begin
if rising_edge(clk) then
if (rst = '1') then
    csr_data_fifo_rvalid_ff <= '0'; -- 0x0
else
        csr_data_fifo_rvalid_ff <= csr_data_fifo_rvalid;
end if;
end if;
end process;


-----------------------
-- Bit field:
-- DATA(16) - FERR - Frame error flag. Read to clear.
-- access: rolh, hardware: i
-----------------------

csr_data_rdata(16) <= csr_data_ferr_ff;


process (clk) begin
if rising_edge(clk) then
if (rst = '1') then
    csr_data_ferr_ff <= '0'; -- 0x0
else
        if (csr_data_ren = '1') then
            csr_data_ferr_ff <= '0';
         elsif (csr_data_ferr_in = '1') then
            csr_data_ferr_ff <= csr_data_ferr_in;
        end if;
end if;
end if;
end process;



-----------------------
-- Bit field:
-- DATA(17) - PERR - Parity error flag. Read to clear.
-- access: rolh, hardware: i
-----------------------

csr_data_rdata(17) <= csr_data_perr_ff;


process (clk) begin
if rising_edge(clk) then
if (rst = '1') then
    csr_data_perr_ff <= '0'; -- 0x0
else
        if (csr_data_ren = '1') then
            csr_data_perr_ff <= '0';
         elsif (csr_data_perr_in = '1') then
            csr_data_perr_ff <= csr_data_perr_in;
        end if;
end if;
end if;
end process;



--------------------------------------------------------------------------------
-- CSR:
-- [0xc] - STAT - Status register
--------------------------------------------------------------------------------
csr_stat_rdata(1 downto 0) <= (others => '0');
csr_stat_rdata(3) <= '0';
csr_stat_rdata(7 downto 5) <= (others => '0');
csr_stat_rdata(31 downto 9) <= (others => '0');


csr_stat_ren <= ren when (raddr = "0000000000001100") else '0'; -- 0xc
process (clk) begin
if rising_edge(clk) then
if (rst = '1') then
    csr_stat_ren_ff <= '0'; -- 0x0
else
        csr_stat_ren_ff <= csr_stat_ren;
end if;
end if;
end process;

-----------------------
-- Bit field:
-- STAT(2) - BUSY - Transciever is busy
-- access: ro, hardware: ie
-----------------------

csr_stat_rdata(2) <= csr_stat_busy_ff;


process (clk) begin
if rising_edge(clk) then
if (rst = '1') then
    csr_stat_busy_ff <= '0'; -- 0x0
else
        if (csr_stat_busy_en = '1') then
            csr_stat_busy_ff <= csr_stat_busy_in;
        end if;
end if;
end if;
end process;



-----------------------
-- Bit field:
-- STAT(4) - RXE - RX FIFO is empty
-- access: ro, hardware: i
-----------------------

csr_stat_rdata(4) <= csr_stat_rxe_ff;


process (clk) begin
if rising_edge(clk) then
if (rst = '1') then
    csr_stat_rxe_ff <= '0'; -- 0x0
else
            csr_stat_rxe_ff <= csr_stat_rxe_in;
end if;
end if;
end process;



-----------------------
-- Bit field:
-- STAT(8) - TXF - TX FIFO is full
-- access: ro, hardware: i
-----------------------

csr_stat_rdata(8) <= csr_stat_txf_ff;


process (clk) begin
if rising_edge(clk) then
if (rst = '1') then
    csr_stat_txf_ff <= '0'; -- 0x0
else
            csr_stat_txf_ff <= csr_stat_txf_in;
end if;
end if;
end process;



--------------------------------------------------------------------------------
-- CSR:
-- [0x10] - CTRL - Control register
--------------------------------------------------------------------------------
csr_ctrl_rdata(3 downto 2) <= (others => '0');
csr_ctrl_rdata(31 downto 7) <= (others => '0');

csr_ctrl_wen <= wen when (waddr = "0000000000010000") else '0'; -- 0x10

csr_ctrl_ren <= ren when (raddr = "0000000000010000") else '0'; -- 0x10
process (clk) begin
if rising_edge(clk) then
if (rst = '1') then
    csr_ctrl_ren_ff <= '0'; -- 0x0
else
        csr_ctrl_ren_ff <= csr_ctrl_ren;
end if;
end if;
end process;

-----------------------
-- Bit field:
-- CTRL(1 downto 0) - BAUD - Baudrate value
-- access: rw, hardware: o
-----------------------

csr_ctrl_rdata(1 downto 0) <= csr_ctrl_baud_ff;

csr_ctrl_baud_out <= csr_ctrl_baud_ff;

process (clk) begin
if rising_edge(clk) then
if (rst = '1') then
    csr_ctrl_baud_ff <= "00"; -- 0x0
else
        if (csr_ctrl_wen = '1') then
            if (wstrb(0) = '1') then
                csr_ctrl_baud_ff(1 downto 0) <= wdata(1 downto 0);
            end if;
        else
            csr_ctrl_baud_ff <= csr_ctrl_baud_ff;
        end if;
end if;
end if;
end process;



-----------------------
-- Bit field:
-- CTRL(4) - TXEN - Transmitter enable. Can be disabled by hardware on error.
-- access: rw, hardware: oie
-----------------------

csr_ctrl_rdata(4) <= csr_ctrl_txen_ff;

csr_ctrl_txen_out <= csr_ctrl_txen_ff;

process (clk) begin
if rising_edge(clk) then
if (rst = '1') then
    csr_ctrl_txen_ff <= '0'; -- 0x0
else
        if (csr_ctrl_wen = '1') then
            if (wstrb(0) = '1') then
                csr_ctrl_txen_ff <= wdata(4);
            end if;
        elsif (csr_ctrl_txen_en = '1') then
            csr_ctrl_txen_ff <= csr_ctrl_txen_in;
        end if;
end if;
end if;
end process;



-----------------------
-- Bit field:
-- CTRL(5) - RXEN - Receiver enable. Can be disabled by hardware on error.
-- access: rw, hardware: oie
-----------------------

csr_ctrl_rdata(5) <= csr_ctrl_rxen_ff;

csr_ctrl_rxen_out <= csr_ctrl_rxen_ff;

process (clk) begin
if rising_edge(clk) then
if (rst = '1') then
    csr_ctrl_rxen_ff <= '0'; -- 0x0
else
        if (csr_ctrl_wen = '1') then
            if (wstrb(0) = '1') then
                csr_ctrl_rxen_ff <= wdata(5);
            end if;
        elsif (csr_ctrl_rxen_en = '1') then
            csr_ctrl_rxen_ff <= csr_ctrl_rxen_in;
        end if;
end if;
end if;
end process;



-----------------------
-- Bit field:
-- CTRL(6) - TXST - Force transmission start
-- access: wosc, hardware: o
-----------------------

csr_ctrl_rdata(6) <= '0';

csr_ctrl_txst_out <= csr_ctrl_txst_ff;

process (clk) begin
if rising_edge(clk) then
if (rst = '1') then
    csr_ctrl_txst_ff <= '0'; -- 0x0
else
        if (csr_ctrl_wen = '1') then
            if (wstrb(0) = '1') then
                csr_ctrl_txst_ff <= wdata(6);
            end if;
        else
            csr_ctrl_txst_ff <= '0';
        end if;
end if;
end if;
end process;



--------------------------------------------------------------------------------
-- CSR:
-- [0x14] - LPMODE - Low power mode control
--------------------------------------------------------------------------------
csr_lpmode_rdata(30 downto 8) <= (others => '0');

csr_lpmode_wen <= wen when (waddr = "0000000000010100") else '0'; -- 0x14

csr_lpmode_ren <= ren when (raddr = "0000000000010100") else '0'; -- 0x14
process (clk) begin
if rising_edge(clk) then
if (rst = '1') then
    csr_lpmode_ren_ff <= '0'; -- 0x0
else
        csr_lpmode_ren_ff <= csr_lpmode_ren;
end if;
end if;
end process;

-----------------------
-- Bit field:
-- LPMODE(7 downto 0) - DIV - Clock divider in low power mode
-- access: rw, hardware: o
-----------------------

csr_lpmode_rdata(7 downto 0) <= csr_lpmode_div_ff;

csr_lpmode_div_out <= csr_lpmode_div_ff;

process (clk) begin
if rising_edge(clk) then
if (rst = '1') then
    csr_lpmode_div_ff <= "00000000"; -- 0x0
else
        if (csr_lpmode_wen = '1') then
            if (wstrb(0) = '1') then
                csr_lpmode_div_ff(7 downto 0) <= wdata(7 downto 0);
            end if;
        else
            csr_lpmode_div_ff <= csr_lpmode_div_ff;
        end if;
end if;
end if;
end process;



-----------------------
-- Bit field:
-- LPMODE(31) - EN - Low power mode enable
-- access: rw, hardware: o
-----------------------

csr_lpmode_rdata(31) <= csr_lpmode_en_ff;

csr_lpmode_en_out <= csr_lpmode_en_ff;

process (clk) begin
if rising_edge(clk) then
if (rst = '1') then
    csr_lpmode_en_ff <= '0'; -- 0x0
else
        if (csr_lpmode_wen = '1') then
            if (wstrb(3) = '1') then
                csr_lpmode_en_ff <= wdata(31);
            end if;
        else
            csr_lpmode_en_ff <= csr_lpmode_en_ff;
        end if;
end if;
end if;
end process;



--------------------------------------------------------------------------------
-- CSR:
-- [0x20] - INTSTAT - Interrupt status register
--------------------------------------------------------------------------------
csr_intstat_rdata(31 downto 2) <= (others => '0');

csr_intstat_wen <= wen when (waddr = "0000000000100000") else '0'; -- 0x20

csr_intstat_ren <= ren when (raddr = "0000000000100000") else '0'; -- 0x20
process (clk) begin
if rising_edge(clk) then
if (rst = '1') then
    csr_intstat_ren_ff <= '0'; -- 0x0
else
        csr_intstat_ren_ff <= csr_intstat_ren;
end if;
end if;
end process;

-----------------------
-- Bit field:
-- INTSTAT(0) - TX - Transmitter interrupt flag. Write 1 to clear.
-- access: rw1c, hardware: s
-----------------------

csr_intstat_rdata(0) <= csr_intstat_tx_ff;


process (clk) begin
if rising_edge(clk) then
if (rst = '1') then
    csr_intstat_tx_ff <= '0'; -- 0x0
else
        if (csr_intstat_tx_set = '1') then
            csr_intstat_tx_ff <= '1';
        elsif (csr_intstat_wen = '1') then
            if ((wstrb(0) = '1') and (wdata(0) = '1')) then
                csr_intstat_tx_ff <= '0';
            end if;
        else
            csr_intstat_tx_ff <= csr_intstat_tx_ff;
        end if;
end if;
end if;
end process;



-----------------------
-- Bit field:
-- INTSTAT(1) - RX - Receiver interrupt. Write 1 to clear.
-- access: rw1c, hardware: s
-----------------------

csr_intstat_rdata(1) <= csr_intstat_rx_ff;


process (clk) begin
if rising_edge(clk) then
if (rst = '1') then
    csr_intstat_rx_ff <= '0'; -- 0x0
else
        if (csr_intstat_rx_set = '1') then
            csr_intstat_rx_ff <= '1';
        elsif (csr_intstat_wen = '1') then
            if ((wstrb(0) = '1') and (wdata(1) = '1')) then
                csr_intstat_rx_ff <= '0';
            end if;
        else
            csr_intstat_rx_ff <= csr_intstat_rx_ff;
        end if;
end if;
end if;
end process;



--------------------------------------------------------------------------------
-- CSR:
-- [0x40] - ID - IP-core ID register
--------------------------------------------------------------------------------


csr_id_ren <= ren when (raddr = "0000000001000000") else '0'; -- 0x40
process (clk) begin
if rising_edge(clk) then
if (rst = '1') then
    csr_id_ren_ff <= '0'; -- 0x0
else
        csr_id_ren_ff <= csr_id_ren;
end if;
end if;
end process;

-----------------------
-- Bit field:
-- ID(31 downto 0) - UID - Unique ID
-- access: ro, hardware: f
-----------------------

csr_id_rdata(31 downto 0) <= csr_id_uid_ff;


process (clk) begin
if rising_edge(clk) then
if (rst = '1') then
    csr_id_uid_ff <= "11001010111111100000011001100110"; -- 0xcafe0666
else
        
            csr_id_uid_ff <= csr_id_uid_ff;
end if;
end if;
end process;



--------------------------------------------------------------------------------
-- Write ready
--------------------------------------------------------------------------------
wready_drv <=
    csr_data_fifo_wready when (csr_data_wen = '1') else
    '1';

wready <= wready_drv;

--------------------------------------------------------------------------------
-- Read address decoder
--------------------------------------------------------------------------------
process (clk) begin
if rising_edge(clk) then
if (rst = '1') then
    rdata_ff <= "00000000000000000000000000000000"; -- 0x0
else
    if (ren = '1') then
        case ADDR_T'(raddr) is
            when "0000000000000100" => rdata_ff <= csr_data_rdata; -- 0x4
            when "0000000000001100" => rdata_ff <= csr_stat_rdata; -- 0xc
            when "0000000000010000" => rdata_ff <= csr_ctrl_rdata; -- 0x10
            when "0000000000010100" => rdata_ff <= csr_lpmode_rdata; -- 0x14
            when "0000000000100000" => rdata_ff <= csr_intstat_rdata; -- 0x20
            when "0000000001000000" => rdata_ff <= csr_id_rdata; -- 0x40
            when others => rdata_ff <= "00000000000000000000000000000000"; -- 0x0
        end case;
    else
        rdata_ff <= "00000000000000000000000000000000"; -- 0x0
    end if;
end if;
end if;
end process;

rdata <= rdata_ff;

--------------------------------------------------------------------------------
-- Read data valid
--------------------------------------------------------------------------------
process (clk) begin
if rising_edge(clk) then
if (rst = '1') then
    rvalid_ff <= '0'; -- 0x0
else
    if ((ren = '1') and (rvalid = '1')) then
        rvalid_ff <= '0';
    elsif (ren = '1') then
        rvalid_ff <= '1';
    end if;
end if;
end if;
end process;


rvalid_drv <=
    csr_data_fifo_rvalid_ff when (csr_data_ren = '1') else
    rvalid_ff;

rvalid <= rvalid_drv;

end architecture;