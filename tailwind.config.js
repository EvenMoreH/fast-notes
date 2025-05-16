/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./**/*.html",      // Scan all HTML files in the project
    "./app/**/*.py",    // Scan Python files (e.g., FastHTML components)
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}