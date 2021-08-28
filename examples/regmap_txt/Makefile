SUBDIRS := $(wildcard */.)

export PYTHONPATH := ../../.:$(PYTHONPATH)

all: generate

generate:
	python3 -m corsair -t txt
	python3 -m corsair

clean:
	@rm -rf csrconfig *.txt hw doc sw

.PHONY: all generate clean