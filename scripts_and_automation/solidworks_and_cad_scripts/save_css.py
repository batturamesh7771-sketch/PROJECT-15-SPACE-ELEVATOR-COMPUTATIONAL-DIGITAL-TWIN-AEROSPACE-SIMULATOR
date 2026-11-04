import os

dash_js_path = r"C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\WebGL_Simulator\js\dashboard_ui.js"
with open(dash_js_path, "r", encoding="utf-8") as f:
    code = f.read()

# Find the CSS block
tag = "styleEl.textContent = `"
start = code.find(tag) + len(tag)
end = code.find("`;", start)
css_content = code[start:end]
print(f"Found CSS content: {len(css_content)} characters")

# Save directly to css/dashboard.css
css_dir = r"C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\WebGL_Simulator\css"
os.makedirs(css_dir, exist_ok=True)
with open(os.path.join(css_dir, "dashboard.css"), "w", encoding="utf-8") as f:
    f.write(css_content)

print("Saved WebGL_Simulator/css/dashboard.css successfully!")
