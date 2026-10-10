[app]
title = Fleet & Driver Manager
package.name = fleetmanager
package.domain = org.prakhar

# (str) Source files directory (relative to directory containing buildozer.spec)
source.dir = .

# (list) Source files to include (let it blank to include all files)
source.include_exts = py,png,jpg,kv,atlas

version = 0.1
requirements = python3,kivy

orientation = portrait
fullscreen = 0
android.permissions = INTERNET

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.min_api = 21

# (int) Android SDK version to use
android.sdk = 33

# (str) Version of the Android build tools to use
android.build_tools_version = 33.0.0

# (bool) Skip / Accept SDK license automatically
android.accept_sdk_license = True
