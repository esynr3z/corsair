SUBDIRS := $(wildcard */.)

export PYTHONPATH := ../../../.:$(PYTHONPATH)

all: run

run:
	python3 csrconfig.py

clean:
	@rm -rf new.csrconfig

.PHONY: all run clean