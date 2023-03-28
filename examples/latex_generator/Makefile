SUBDIRS := $(wildcard */.)

export PYTHONPATH := ../../.:$(PYTHONPATH)

all: generate

generate:
	python -m corsair

clean:
	@rm -rf *.tex *.vhd

.PHONY: all generate clean