SUBDIRS := $(wildcard */.)

export PYTHONPATH := ../../.:$(PYTHONPATH)

all: generate build

generate:
	python3 -m corsair -t yaml

build:
	python3 -m corsair

clean:
	@rm -rf csrconfig *.yaml hw doc sw

.PHONY: all generate clean