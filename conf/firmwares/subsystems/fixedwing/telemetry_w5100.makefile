# Hey Emacs, this is a -*- makefile -*-

# W5100 ethernet chip.

ifeq ($(TARGET), ap)
include $(CFG_SHARED)/telemetry_w5100.makefile
endif

ap.srcs += $(SRC_FIRMWARE)/fixedwing_datalink.c $(SRC_FIRMWARE)/ap_downlink.c

# avoid fbw_telemetry_mode error
ap.srcs += $(SRC_FIRMWARE)/fbw_downlink.c

fbw.srcs += $(SRC_FIRMWARE)/fbw_downlink.c
