

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
    -- DATA.val
    csr_data_val_en : in std_logic;
    csr_data_val_in : in std_logic_vector(31 downto 0);
    csr_data_val_out : out std_logic_vector(31 downto 0);

    -- CTRL.val
    csr_ctrl_val_out : out std_logic_vector(15 downto 0);

    -- STATUS.val
    csr_status_val_in : in std_logic_vector(7 downto 0);

    -- START.val
    csr_start_val_out : out std_logic;

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
signal csr_data_val_ff : std_logic_vector(31 downto 0);

signal csr_ctrl_rdata : std_logic_vector(31 downto 0);
signal csr_ctrl_wen : std_logic;
signal csr_ctrl_ren : std_logic;
signal csr_ctrl_ren_ff : std_logic;
signal csr_ctrl_val_ff : std_logic_vector(15 downto 0);

signal csr_status_rdata : std_logic_vector(31 downto 0);
signal csr_status_ren : std_logic;
signal csr_status_ren_ff : std_logic;
signal csr_status_val_ff : std_logic_vector(7 downto 0);

signal csr_start_rdata : std_logic_vector(31 downto 0);
signal csr_start_wen : std_logic;
signal csr_start_val_ff : std_logic;

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
-- [0x0] - DATA - Data register
--------------------------------------------------------------------------------

csr_data_wen <= wen when (waddr = "0000000000000000") else '0'; -- 0x0

csr_data_ren <= ren when (raddr = "0000000000000000") else '0'; -- 0x0
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
-- DATA(31 downto 0) - val - Value of the register
-- access: rw, hardware: ioe
-----------------------

csr_data_rdata(31 downto 0) <= csr_data_val_ff;

csr_data_val_out <= csr_data_val_ff;

process (clk) begin
if rising_edge(clk) then
if (rst = '1') then
    csr_data_val_ff <= "00000000000000000000000000000000"; -- 0x0
else
        if (csr_data_wen = '1') then
            if (wstrb(0) = '1') then
                csr_data_val_ff(7 downto 0) <= wdata(7 downto 0);
            end if;
            if (wstrb(1) = '1') then
                csr_data_val_ff(15 downto 8) <= wdata(15 downto 8);
            end if;
            if (wstrb(2) = '1') then
                csr_data_val_ff(23 downto 16) <= wdata(23 downto 16);
            end if;
            if (wstrb(3) = '1') then
                csr_data_val_ff(31 downto 24) <= wdata(31 downto 24);
            end if;
        elsif (csr_data_val_en = '1') then
            csr_data_val_ff <= csr_data_val_in;
        end if;
end if;
end if;
end process;



--------------------------------------------------------------------------------
-- CSR:
-- [0x4] - CTRL - Control register
--------------------------------------------------------------------------------
csr_ctrl_rdata(31 downto 16) <= (others => '0');

csr_ctrl_wen <= wen when (waddr = "0000000000000100") else '0'; -- 0x4

csr_ctrl_ren <= ren when (raddr = "0000000000000100") else '0'; -- 0x4
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
-- CTRL(15 downto 0) - val - Value of the register
-- access: rw, hardware: o
-----------------------

csr_ctrl_rdata(15 downto 0) <= csr_ctrl_val_ff;

csr_ctrl_val_out <= csr_ctrl_val_ff;

process (clk) begin
if rising_edge(clk) then
if (rst = '1') then
    csr_ctrl_val_ff <= "0000000100000000"; -- 0x100
else
        if (csr_ctrl_wen = '1') then
            if (wstrb(0) = '1') then
                csr_ctrl_val_ff(7 downto 0) <= wdata(7 downto 0);
            end if;
            if (wstrb(1) = '1') then
                csr_ctrl_val_ff(15 downto 8) <= wdata(15 downto 8);
            end if;
        else
            csr_ctrl_val_ff <= csr_ctrl_val_ff;
        end if;
end if;
end if;
end process;



--------------------------------------------------------------------------------
-- CSR:
-- [0x8] - STATUS - Status register
--------------------------------------------------------------------------------
csr_status_rdata(31 downto 8) <= (others => '0');


csr_status_ren <= ren when (raddr = "0000000000001000") else '0'; -- 0x8
process (clk) begin
if rising_edge(clk) then
if (rst = '1') then
    csr_status_ren_ff <= '0'; -- 0x0
else
        csr_status_ren_ff <= csr_status_ren;
end if;
end if;
end process;

-----------------------
-- Bit field:
-- STATUS(7 downto 0) - val - Value of the register
-- access: ro, hardware: i
-----------------------

csr_status_rdata(7 downto 0) <= csr_status_val_ff;


process (clk) begin
if rising_edge(clk) then
if (rst = '1') then
    csr_status_val_ff <= "00000000"; -- 0x0
else
            csr_status_val_ff <= csr_status_val_in;
end if;
end if;
end process;



--------------------------------------------------------------------------------
-- CSR:
-- [0x100] - START - Start register
--------------------------------------------------------------------------------
csr_start_rdata(31 downto 1) <= (others => '0');

csr_start_wen <= wen when (waddr = "0000000100000000") else '0'; -- 0x100

-----------------------
-- Bit field:
-- START(0) - val - Value of the register
-- access: wosc, hardware: o
-----------------------

csr_start_rdata(0) <= '0';

csr_start_val_out <= csr_start_val_ff;

process (clk) begin
if rising_edge(clk) then
if (rst = '1') then
    csr_start_val_ff <= '0'; -- 0x0
else
        if (csr_start_wen = '1') then
            if (wstrb(0) = '1') then
                csr_start_val_ff <= wdata(0);
            end if;
        else
            csr_start_val_ff <= '0';
        end if;
end if;
end if;
end process;



--------------------------------------------------------------------------------
-- Write ready
--------------------------------------------------------------------------------
wready <= '1';

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
            when "0000000000000000" => rdata_ff <= csr_data_rdata; -- 0x0
            when "0000000000000100" => rdata_ff <= csr_ctrl_rdata; -- 0x4
            when "0000000000001000" => rdata_ff <= csr_status_rdata; -- 0x8
            when "0000000100000000" => rdata_ff <= csr_start_rdata; -- 0x100
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


rvalid <= rvalid_ff;

end architecture;