function render() {
  const md = markdownit();

  const content = document.getElementById("content");
  const mdSrc = document.getElementById("md-src");

  const mdRendered = md.render(mdSrc.innerText);
  content.innerHTML = mdRendered;
  content.style = "";
}


window.onload = render;
