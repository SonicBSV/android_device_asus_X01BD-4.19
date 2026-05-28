#
# Copyright (C) 2020 The LineageOS Project
#
# SPDX-License-Identifier: Apache-2.0
#

# Inherit from sdm660-common
$(call inherit-product, device/asus/sdm660-common/sdm660.mk)

# Boot animation
TARGET_SCREEN_HEIGHT := 2280
TARGET_SCREEN_WIDTH := 1080

# Overlays
DEVICE_PACKAGE_OVERLAYS += \
    $(LOCAL_PATH)/overlay \
    $(LOCAL_PATH)/overlay-lineage

PRODUCT_ENFORCE_RRO_EXCLUDED_OVERLAYS += \
    $(LOCAL_PATH)/overlay-lineage/lineage-sdk

PRODUCT_PACKAGES += \
    NoCutoutOverlay

# PowerHal
PRODUCT_COPY_FILES += \
    $(LOCAL_PATH)/configs/powerhint-sdm660.json:$(TARGET_COPY_OUT_VENDOR)/etc/powerhint.json

# Ramdisk
PRODUCT_PACKAGES += \
    init.device.rc \
    init.focaltech.sh

# Wifi
PRODUCT_PACKAGES += \
    X01BDWifiOverlay

# Inherit the proprietary files
$(call inherit-product, vendor/asus/X01BD/X01BD-vendor.mk)
