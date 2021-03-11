PROJNAME = spi

SOURCES += rmap.v
SOURCES += spi2lb_rmap.v
SOURCES += top.sv

all: clean $(PROJNAME).bin sta

# synthesis
$(PROJNAME).json:
	yosys -l syn.rpt -p "synth_ice40 -top top -json $(PROJNAME).json" $(SOURCES)

# place and route
$(PROJNAME).asc: $(PROJNAME).json pinout.pcf sdc.py
	nextpnr-ice40 --seed 424242 -l pr.rpt --pre-pack sdc.py --pcf pinout.pcf --u4k --package sg48 --json $(PROJNAME).json --asc $(PROJNAME).asc

# generate bitmap
$(PROJNAME).bin: $(PROJNAME).asc
	icepack $(PROJNAME).asc $(PROJNAME).bin

# timing analysis
.PHONY: sta
sta: $(PROJNAME).asc
	icetime -d u4k $(PROJNAME).asc -c 48 -t -i | tee sta.rpt

# load bitmap to flash
.PHONY: flash
flash:
	iceprog -d i:0x0403:0x6010 $(PROJNAME).bin

# clean temp files
.PHONY: clean
clean:
	@rm -f *.bin *.rpt $(PROJNAME).json *.asc