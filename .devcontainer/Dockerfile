# ---- Verilator Builder -------------------------------------------------------
FROM ubuntu:24.04 as verilator_builder

# Avoid prompts from apt
ENV DEBIAN_FRONTEND=noninteractive

# Setup environment variables
ENV VERILATOR_VERSION=v5.034 \
    VERILATOR_INSTALL=/opt/verilator

# Install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ca-certificates git \
    help2man perl python3 make autoconf g++ mold flex bison ccache libfl2 libfl-dev

# Build Verilator
RUN git clone --branch ${VERILATOR_VERSION} --depth 1 https://github.com/verilator/verilator.git
RUN cd verilator && \
    autoconf && \
    ./configure --prefix ${VERILATOR_INSTALL} && \
    make -j$(nproc) && \
    make install


# ---- Modelsim Installer ------------------------------------------------------
FROM ubuntu:24.04 as modelsim_installer

# Avoid prompts from apt
ENV DEBIAN_FRONTEND=noninteractive

# Prepare environment variables
ENV MODELSIM_INSTALLER=ModelSimSetup-20.1.0.711-linux.run \
    MODELSIM_INSTALLER_URL=https://download.altera.com/akdlm/software/acdsinst/20.1std/711/ib_installers/ModelSimSetup-20.1.0.711-linux.run \
    MODELSIM_INSTALL=/opt/modelsim

# Install dependencies
RUN dpkg --add-architecture i386 && \
    echo "deb http://security.ubuntu.com/ubuntu focal-security main universe" > /etc/apt/sources.list.d/ubuntu-focal-sources.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
    ca-certificates wget \
    libc6:i386 libxtst6:i386 libncurses5:i386 libxft2:i386 libstdc++6:i386 libc6-dev-i386 lib32z1 libqt5xml5 liblzma-dev

# Download Modelsim
RUN wget ${MODELSIM_INSTALLER_URL} && \
    chmod +x ${MODELSIM_INSTALLER}

# Install Modelsim
RUN ./${MODELSIM_INSTALLER} --mode unattended --accept_eula 1 --installdir ${MODELSIM_INSTALL} --unattendedmodeui none


# ---- Main Image --------------------------------------------------------------
FROM ubuntu:24.04

# Install necessary system dependencies
RUN dpkg --add-architecture i386 && \
    echo "deb http://security.ubuntu.com/ubuntu focal-security main universe" > /etc/apt/sources.list.d/ubuntu-focal-sources.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
    ca-certificates curl git nano openssh-client \
    g++ mold ccache perl-doc z3 gtkwave \
    libc6:i386 libxtst6:i386 libncurses5:i386 libxft2:i386 libstdc++6:i386 libc6-dev-i386 lib32z1 libqt5xml5 liblzma-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Verilator
ENV VERILATOR_INSTALL=/opt/verilator
COPY --from=verilator_builder ${VERILATOR_INSTALL} ${VERILATOR_INSTALL}

# Install Modelsim
ENV MODELSIM_INSTALL=/opt/modelsim
COPY --from=modelsim_installer ${MODELSIM_INSTALL} ${MODELSIM_INSTALL}

# Install uv
ENV UV_VERSION=0.6.16
RUN curl -LsSf https://astral.sh/uv/${UV_VERSION}/install.sh | sh

# Update PATH
ENV PATH="/root/.local/bin:${MODELSIM_INSTALL}/modelsim_ase/bin:${VERILATOR_INSTALL}/bin:${PATH}"
