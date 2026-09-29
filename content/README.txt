CONTENT PACK - ARCore Mine Safety Training App
================================================
models/  (.glb, glTF 2.0, Y-up, units = metres, origin at base/centre)
  extinguisher_water.glb / _co2.glb / _powder.glb   ~0.58 m tall
  fire_flames.glb        ~0.8 m, emissive layered cones (animate scale/rotation in code for flicker)
  exit_sign.glb          0.5 x 0.19 m, textured (EXIT + running-man arrow), emissive
  gas_monitor.glb        handheld, 7 x 18 cm, screen texture shows CH4/O2/CO readout
  gas_cloud.glb          semi-transparent green blobs, ~1.5 m; alphaMode BLEND
  ppe_hard_hat.glb, ppe_safety_boots.glb, ppe_hivis_vest.glb
images/
  app_icon_1024.png, app_icon_512_playstore.png
  appicon/mipmap-*/ic_launcher.png + ic_launcher_round.png   (copy into android res/)
  appicon/ic_launcher_foreground_432.png + _background_432.png (adaptive icon layers)
  logo_govt_jharkhand_PLACEHOLDER.png, logo_dgms_PLACEHOLDER.png
audio/   (empty - optional Hindi/Santali voiceovers; TTS fallback is used otherwise)

NOTES
- The two logos are PLACEHOLDERS, not the official emblems. Replace them with the
  official Government of Jharkhand and DGMS files (keep the same filenames without
  "_PLACEHOLDER" if the code references them).
- Models are simple low-poly procedural shapes (10-60 KB each): light for mobile AR,
  but stylised. Swap in Sketchfab/Polycam models later for realism; names can stay the same.
