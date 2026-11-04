import os
import shutil

src_html = r"C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\WebGL_Simulator\index.html"
dst_html = r"E:\Downloads\index.html"

with open(src_html, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Fix loader overlay CSS so it NEVER intercepts clicks
content = content.replace(
    "#loader-overlay {",
    "#loader-overlay {\n      pointer-events: none !important;",
    1
)

# 2. Fix dismissLoader function to immediately remove the overlay from the DOM
old_dismiss = """    function dismissLoader() {
      const overlay = document.getElementById('loader-overlay');
      if (overlay) {
        overlay.style.opacity = '0';
        setTimeout(() => { if (overlay) overlay.style.display = 'none'; }, 400);
      }
    }"""

new_dismiss = """    function dismissLoader() {
      const overlay = document.getElementById('loader-overlay');
      if (overlay) {
        overlay.style.pointerEvents = 'none';
        overlay.style.opacity = '0';
        overlay.style.display = 'none';
        try { overlay.remove(); } catch (e) {}
      }
    }"""

content = content.replace(old_dismiss, new_dismiss, 1)

# Also trigger dismissLoader immediately on startup
content = content.replace(
    "setTimeout(dismissLoader, 2500);",
    "dismissLoader(); setTimeout(dismissLoader, 100);",
    1
)

# 3. FIX lastTime declaration and safe animate loop
old_animate = """    function animate(currentTime) {

      requestAnimationFrame(animate);



      const dt = Math.min((currentTime - lastTime) / 1000.0, 0.1);

      lastTime = currentTime;"""

new_animate = """    let lastTime = performance.now();

    function animate(currentTime) {
      requestAnimationFrame(animate);

      if (!currentTime) currentTime = performance.now();
      if (!lastTime) lastTime = currentTime;
      const dt = Math.min(Math.max((currentTime - lastTime) / 1000.0, 0.0001), 0.1);
      lastTime = currentTime;"""

if old_animate in content:
    content = content.replace(old_animate, new_animate, 1)
    print("Replaced animate with safe lastTime")
else:
    # Use regex
    import re
    content = re.sub(
        r'function animate\(currentTime\)\s*\{\s*requestAnimationFrame\(animate\);\s*const dt = Math\.min\(\(currentTime - lastTime\) / 1000\.0, 0\.1\);\s*lastTime = currentTime;',
        """let lastTime = performance.now();

    function animate(currentTime) {
      requestAnimationFrame(animate);

      if (!currentTime) currentTime = performance.now();
      if (!lastTime) lastTime = currentTime;
      const dt = Math.min(Math.max((currentTime - lastTime) / 1000.0, 0.0001), 0.1);
      lastTime = currentTime;""",
        content
    )
    print("Replaced animate via regex")

with open(src_html, "w", encoding="utf-8") as f:
    f.write(content)
print("Saved fixed", src_html)

if os.path.exists(os.path.dirname(dst_html)):
    shutil.copyfile(src_html, dst_html)
    print("Synchronized to", dst_html)
