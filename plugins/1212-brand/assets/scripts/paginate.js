// The continuous flow of the 1212 A4 documents (Noah, 1 Oct 2026): after the cover, which stays alone, the parts
// follow one another and a page turns only when it is full. The builders write the parts once, in a
// <section class="flow">; this script, run by the page itself once its fonts are ready, lays them into .page
// sections the browser measures, then the PDF prints one .page per sheet as before (render_pdf.py waits for it).
//
// The rules, the same as the app's PDFs (packages/documents, kit/flow.tsx):
// - a part marked data-flow="keep" is never cut: it moves whole to the next page when it does not fit;
// - data-flow="table": its table breaks between rows only, its header repeated on the next page; the title keeps
//   the header and the first row on its page, and the note under the table keeps the last row;
// - data-flow="blocks": its blocks (paragraphs) are never cut; the title keeps the first block on its page.
(function () {
  "use strict";

  function paginate() {
    var flow = document.querySelector("section.flow");
    if (!flow) return done();
    var head = flow.querySelector("template.flow__head").innerHTML;
    var foot = flow.querySelector("template.flow__foot").innerHTML;
    var contentClass = flow.getAttribute("data-content") || "page__content";
    var parts = Array.prototype.slice.call(flow.querySelectorAll(":scope > .flow__parts > .flow__part"));
    var content = newPage();

    function newPage() {
      var page = document.createElement("section");
      page.className = "page";
      var box = document.createElement("div");
      box.className = contentClass;
      box.innerHTML = head;
      page.appendChild(box);
      page.insertAdjacentHTML("beforeend", foot);
      flow.parentNode.insertBefore(page, flow);
      return box;
    }
    function fits(box) {
      return box.scrollHeight <= box.clientHeight + 0.5;
    }
    /** Append `node`; true when it fits, otherwise it is taken out again. */
    function tryAppend(node) {
      content.appendChild(node);
      if (fits(content)) return true;
      content.removeChild(node);
      return false;
    }
    function onNextPage(node) {
      content = newPage();
      content.appendChild(node);
    }

    parts.forEach(function (part) {
      var kind = part.getAttribute("data-flow") || "keep";
      var node = part.firstElementChild;
      if (tryAppend(node)) return;
      if (kind === "table") return placeTable(node);
      if (kind === "blocks") return placeBlocks(node);
      onNextPage(node); // kept whole
    });

    function placeTable(section) {
      var table = section.querySelector(".table");
      var header = table.firstElementChild;
      var rows = Array.prototype.slice.call(table.children, 1);
      var after = [];
      for (var n = table.nextElementSibling; n; n = n.nextElementSibling) after.push(n);
      after.forEach(function (n) { section.removeChild(n); });
      rows.forEach(function (r) { table.removeChild(r); });

      // The title keeps the header and the first row: otherwise the whole part starts on the next page.
      var shell = section;
      if (rows.length) table.appendChild(rows[0]);
      if (!tryAppend(shell)) onNextPage(shell);
      var current = table;
      for (var i = 1; i < rows.length; i++) {
        current.appendChild(rows[i]);
        if (fits(content)) continue;
        current.removeChild(rows[i]);
        current = continuation(header);
        current.appendChild(rows[i]);
      }
      // The note keeps the last row: if it does not fit, the last row goes with it, under a repeated header.
      after.forEach(function (n) {
        var holder = current.parentNode;
        holder.appendChild(n);
        if (fits(content)) return;
        holder.removeChild(n);
        var last = current.lastElementChild;
        if (current.children.length > 2) {
          current.removeChild(last);
          current = continuation(header);
          current.appendChild(last);
          current.parentNode.appendChild(n);
        } else {
          onNextPage(n);
        }
      });
    }
    /** A new page holding the same table, its header repeated, no title. */
    function continuation(header) {
      var section = document.createElement("div");
      section.className = "section";
      var table = document.createElement("div");
      table.className = "table";
      table.appendChild(header.cloneNode(true));
      section.appendChild(table);
      onNextPage(section);
      return table;
    }

    function placeBlocks(section) {
      var title = section.firstElementChild;
      var blocks = Array.prototype.slice.call(section.children, 1);
      blocks.forEach(function (b) { section.removeChild(b); });
      // The title keeps the first block.
      if (blocks.length) section.appendChild(blocks[0]);
      if (!tryAppend(section)) onNextPage(section);
      var holder = section;
      for (var i = 1; i < blocks.length; i++) {
        holder.appendChild(blocks[i]);
        if (fits(content)) continue;
        holder.removeChild(blocks[i]);
        holder = section.cloneNode(false);
        onNextPage(holder);
        holder.appendChild(blocks[i]);
      }
      void title;
    }

    // "n / N" in every foot, the cover not counted, as the builders always did.
    var pages = document.querySelectorAll("section.page");
    Array.prototype.forEach.call(pages, function (page, i) {
      var number = page.querySelector(".pagefoot__page");
      if (number) number.textContent = i + 1 + " / " + pages.length;
    });
    flow.parentNode.removeChild(flow);
    done();
  }

  function done() {
    document.documentElement.setAttribute("data-paginated", "true");
  }

  if (document.fonts && document.fonts.ready) document.fonts.ready.then(paginate);
  else window.addEventListener("load", paginate);
})();
