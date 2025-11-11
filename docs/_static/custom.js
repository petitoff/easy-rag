/* Custom JavaScript for Easy RAG Documentation */

document.addEventListener('DOMContentLoaded', function() {
    // Add copy button to code blocks
    const codeBlocks = document.querySelectorAll('pre code');
    
    codeBlocks.forEach(function(codeBlock) {
        // Skip if already has copy button
        if (codeBlock.parentElement.querySelector('.copy-button')) {
            return;
        }
        
        const copyButton = document.createElement('button');
        copyButton.className = 'copy-button';
        copyButton.textContent = 'Copy';
        copyButton.style.cssText = `
            position: absolute;
            top: 5px;
            right: 5px;
            background: #007bff;
            color: white;
            border: none;
            padding: 5px 10px;
            border-radius: 3px;
            cursor: pointer;
            font-size: 12px;
        `;
        
        const pre = codeBlock.parentElement;
        pre.style.position = 'relative';
        pre.appendChild(copyButton);
        
        copyButton.addEventListener('click', function() {
            const text = codeBlock.textContent;
            navigator.clipboard.writeText(text).then(function() {
                copyButton.textContent = 'Copied!';
                setTimeout(function() {
                    copyButton.textContent = 'Copy';
                }, 2000);
            });
        });
    });
    
    // Add smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
        anchor.addEventListener('click', function(e) {
            const href = anchor.getAttribute('href');
            if (href !== '#' && document.querySelector(href)) {
                e.preventDefault();
                document.querySelector(href).scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Add search functionality enhancement
    const searchInput = document.querySelector('input[type="search"]');
    if (searchInput) {
        searchInput.placeholder = 'Search documentation...';
    }
    
    // Highlight current section in sidebar
    const currentPath = window.location.pathname;
    const sidebarLinks = document.querySelectorAll('.wy-menu-vertical a');
    sidebarLinks.forEach(function(link) {
        if (link.getAttribute('href') === currentPath.split('/').pop()) {
            link.style.fontWeight = 'bold';
            link.style.color = '#007bff';
        }
    });
});

// Add API endpoint testing functionality
function testEndpoint(endpoint, method, body) {
    console.log(`Testing ${method} ${endpoint}`);
    // This would integrate with your API for testing
    // For documentation purposes only
}

