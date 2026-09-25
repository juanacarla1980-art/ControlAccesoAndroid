[app]

title = Control de Acceso
package.name = controlacceso
package.domain = cl.controlacceso

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas

version = 1.0

requirements = python3,kivy,reportlab

orientation = portrait
fullscreen = 0

android.api = 35
android.minapi = 24
android.archs = arm64-v8a,armeabi-v7a

android.permissions = CAMERA

[buildozer]

log_level = 2
warn_on_root = 1
