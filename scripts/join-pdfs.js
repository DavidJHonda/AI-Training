// Merge PDFs using the macOS built-in PDFKit — zero dependencies.
// Usage: osascript -l JavaScript scripts/join-pdfs.js out.pdf in1.pdf in2.pdf ...
ObjC.import("Quartz");
function run(argv) {
  var out = $.PDFDocument.alloc.init;
  for (var i = 1; i < argv.length; i++) {
    var doc = $.PDFDocument.alloc.initWithURL($.NSURL.fileURLWithPath(argv[i]));
    if (doc.isNil()) throw new Error("Could not read " + argv[i]);
    for (var p = 0; p < doc.pageCount; p++) out.insertPageAtIndex(doc.pageAtIndex(p), out.pageCount);
  }
  if (!out.writeToFile(argv[0])) throw new Error("Could not write " + argv[0]);
  return out.pageCount + " pages";
}
