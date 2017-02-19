PYTHON ?= python
PREFIX ?= $(HOME)/.local/share/cura

PLATFORM = discoeasy200

O ?= output
I ?= input/$(PLATFORM)

all: definitions materials meshes qualities

O_DEFINITIONS = $(O)/definitions
O_MATERIALS   = $(O)/materials
O_MESHES      = $(O)/meshes
O_QUALITIES   = $(O)/quality/dagoma_$(PLATFORM)

DAGOMA_XML = $(I)/xml_config.xml

DEFINITION = $(O_DEFINITIONS)/dagoma_$(PLATFORM).def.json
definitions: $(O_DEFINITIONS)
	$(PYTHON) definition.py $(DAGOMA_XML) $(DEFINITION)

materials: $(O_MATERIALS)
	$(PYTHON) materials.py $(DAGOMA_XML) $<

qualities: $(O_QUALITIES)
	$(PYTHON) qualities.py $(DAGOMA_XML) $<

IMESH = $(I)/platform.stl
OMESH = $(O_MESHES)/dagoma_$(PLATFORM)_platform.stl
meshes: $(IMESH) $(O_MESHES)
	admesh --x-rotate 90 --z-rotate 180 --translate -105,-110,-57 -b $(OMESH) $(IMESH)

$(O):
	mkdir -p $@
$(O_DEFINITIONS) $(O_MATERIALS) $(O_MESHES) $(O_QUALITIES): $(O)
	mkdir -p $@

install: all
	cp -r $(O)/. $(PREFIX)

clean:
	$(RM) -r output
