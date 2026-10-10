[app]
title = Fleet & Driver Manager
package.name = fleetmanager
package.domain = org.prakhar

# Source files directory
source.dir = .

# Source files to include
source.include_exts = py,png,jpg,kv,atlas

version = 0.1
requirements = python3,kivy

orientation = portrait
fullscreen = 0
android.permissions = INTERNET

# Target Android API & SDK
android.api = 33
android.min_api = 21
android.sdk = 33

# Explicitly fix build tools version to avoid missing aidl error
android.build_tools_version = 33.0.2

# Automatically accept SDK licenses
android.accept_sdk_license = True

log_level = 2
