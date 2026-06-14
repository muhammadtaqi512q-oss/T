const fs = require('fs');
const path = require('path');

// Aapka strictly secured target link jo ab chhup chuka hai
const targetIDLink = "https://muhammadtaqi512q-oss.github.io/puzzle/web-builder";

// template.html ko read karna
const templatePath = path.join(__dirname, 'template.html');
let htmlContent = fs.readFileSync(templatePath, 'utf8');

// Success hone par inject hone wala text aur security scripts
const injectionPayload = `
    <div id="status" class="king-text">MUHAMMAD TAQI KING</div>
    <script>
        if (window.parent !== window) {
            window.parent.postMessage({ status: 'success', url: '${targetIDLink}' }, '*');
        }
    </script>
`;

// Marker dynamic content se replace hoga
htmlContent = htmlContent.replace('<!-- SECURITY_INJECTION_POINT -->', injectionPayload);

// Built page ko 'dist' directory me save karna GitHub Pages ke liye
const distDir = path.join(__dirname, 'dist');
if (!fs.existsSync(distDir)){
    fs.mkdirSync(distDir);
}
fs.writeFileSync(path.join(distDir, 'index.html'), htmlContent);
console.log("Backend verification output generated successfully.");
