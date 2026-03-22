#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'hardware/qcom-caf/sdm660',
    'vendor/asus/sdm660-common',
    'vendor/qcom/opensource/display',
]

# Define the blob fixups
blob_fixups: blob_fixups_user_type = {
    # Camera - uneeded
    'vendor/lib/libmmcamera_tuning.so': blob_fixup()
        .remove_needed('libmm-qcamera.so'),
    # Fingerprint - liblog dep.
    'vendor/lib64/hw/cdfinger.fingerprint.default.so': blob_fixup()
        .add_needed('liblog.so'),
    # Fingerprint - so name fixups
    'vendor/lib64/hw/cdfinger.fingerprint.default.so': blob_fixup()
        .fix_soname(),        
}  # fmt: skip

# Define the module
module = ExtractUtilsModule(
    'X01BD',
    'asus',
    blob_fixups=blob_fixups,
    namespace_imports=namespace_imports,
)

if __name__ == '__main__':
    utils = ExtractUtils.device_with_common(module, 'sdm660-common', module.vendor)
    utils.run()
