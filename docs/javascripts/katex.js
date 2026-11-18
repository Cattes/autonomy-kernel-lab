// Render the TeX that pymdownx.arithmatex leaves in the page, on every page load
// (document$ also fires on Zensical's instant navigation). Arithmatex rewrites
// $...$ and $$...$$ in Markdown to \(...\) and \[...\], so only those are used
// here; a stray "$5 to $10" in prose is never treated as math.
document$.subscribe(({ body }) => {
  renderMathInElement(body, {
    delimiters: [
      { left: "\\(", right: "\\)", display: false },
      { left: "\\[", right: "\\]", display: true },
    ],
  });
});
