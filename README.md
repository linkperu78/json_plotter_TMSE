# Project Name

*Summary:* This project is designed to demonstrate [briefly explain what your project does, e.g., "a GUI interface for dragging and dropping files and visualizing 2D graphs."].

## Author

- **Diego Quispe**
- **Email: diegoar.quispec@gmail.com**

## Prerequisites

To run this project, you'll need the following Python packages. You can install them using `pip` ["pip install"]:  
tkinter  
tkinterdnd2  
matplotlib

## Summary

[This project provides a GUI interface allowing users to drag and drop files, select items from a combobox, and visualize a 2D graph. It was created as an exercise in using `tkinter` with Python and integrating drag-and-drop functionality along with data visualization using `matplotlib`.]


# Testing copy to clipboard
<!DOCTYPE html>
<html>
<head>
  <script type="module">
    import 'https://cdn.jsdelivr.net/npm/@github/clipboard-copy-element@1.0.8/dist/clipboard-copy.js';

    document.addEventListener('DOMContentLoaded', () => {
      const clipboardButton = document.querySelector('.clipboard-button');
      const codeBlock = document.querySelector('.code-block');

      clipboardButton.addEventListener('clipboard-copy', () => {
        console.log('Text copied to clipboard!');
      });

      clipboardButton.addEventListener('clipboard-error', () => {
        console.error('Failed to copy text to clipboard.');
      });

      clipboardButton.addEventListener('click', () => {
        clipboardButton.copy(codeBlock);
      });
    });
  </script>
</head>
<body>
  <div>
    <pre class="code-block">This is the text you want to copy.</pre>
    <button class="clipboard-button">Copy</button>
  </div>
</body>
</html>
