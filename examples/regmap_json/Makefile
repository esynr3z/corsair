SUBDIRS := $(wildcard */.)

export PYTHONPATH := ../../.:$(PYTHONPATH)

all: generate

generate:
	python3 -m corsair -t json
	python3 -m corsair

clean:
	@rm -rf csrconfig *.json hw doc sw

.PHONY: all generate clean