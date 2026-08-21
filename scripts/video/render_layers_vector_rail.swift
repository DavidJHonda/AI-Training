#!/usr/bin/env swift

import AppKit
import CoreText
import Foundation

let repoRoot = URL(fileURLWithPath: FileManager.default.currentDirectoryPath)
let inputURL = repoRoot.appendingPathComponent("board-review-first-four/.pre-board-spec/understand-ai/layers-2-inside-alternative.jpg")
let outputURLs = [
    repoRoot.appendingPathComponent("board-review-first-four/alternatives/understand-ai/layers-2-inside-alternative.jpg"),
    repoRoot.appendingPathComponent("board-review-first-four/alternatives/understand-ai/layers-2-inside-vector-rail-alternative.jpg"),
    repoRoot.appendingPathComponent("lessons/layers-2-inside.jpg"),
    repoRoot.appendingPathComponent("illustrations/layers-inside.jpg")
]

let width: CGFloat = 1600
let height: CGFloat = 900

func color(_ hex: String, alpha: CGFloat = 1) -> NSColor {
    let clean = hex.replacingOccurrences(of: "#", with: "")
    var value: UInt64 = 0
    Scanner(string: clean).scanHexInt64(&value)
    return NSColor(
        calibratedRed: CGFloat((value >> 16) & 0xff) / 255,
        green: CGFloat((value >> 8) & 0xff) / 255,
        blue: CGFloat(value & 0xff) / 255,
        alpha: alpha
    )
}

let navy = color("#08072b")
let muted = color("#655f7c")
let purple = color("#6f52ff")
let lavender = color("#eeeaff")
let paleLavender = color("#f6f3ff")
let gold = color("#ffe9ab")
let rule = color("#ddd8ef")

func loadFont(path: String, size: CGFloat) -> NSFont {
    let url = URL(fileURLWithPath: path)
    CTFontManagerRegisterFontsForURL(url as CFURL, .process, nil)
    if let descriptors = CTFontManagerCreateFontDescriptorsFromURL(url as CFURL) as? [CTFontDescriptor],
       let descriptor = descriptors.first,
       let postscriptName = CTFontDescriptorCopyAttribute(descriptor, kCTFontNameAttribute) as? String,
       let font = NSFont(name: postscriptName, size: size) {
        return font
    }
    return NSFont.systemFont(ofSize: size)
}

let fontRoot = "/Users/davidobrien/Library/Fonts"
func heavy(_ size: CGFloat) -> NSFont { loadFont(path: "\(fontRoot)/AvenirNextforINTUIT-Heavy.otf", size: size) }
func demi(_ size: CGFloat) -> NSFont { loadFont(path: "\(fontRoot)/AvenirNextforINTUIT-Demi.otf", size: size) }
func medium(_ size: CGFloat) -> NSFont { loadFont(path: "\(fontRoot)/AvenirNextforINTUIT-Medium.otf", size: size) }

func roundedRect(_ rect: NSRect, radius: CGFloat, fill: NSColor, stroke: NSColor? = nil, lineWidth: CGFloat = 1) {
    let path = NSBezierPath(roundedRect: rect, xRadius: radius, yRadius: radius)
    fill.setFill()
    path.fill()
    if let stroke {
        stroke.setStroke()
        path.lineWidth = lineWidth
        path.stroke()
    }
}

func drawText(_ value: String, in rect: NSRect, font: NSFont, color: NSColor, alignment: NSTextAlignment = .left) {
    let paragraph = NSMutableParagraphStyle()
    paragraph.alignment = alignment
    (value as NSString).draw(
        in: rect,
        withAttributes: [
            .font: font,
            .foregroundColor: color,
            .paragraphStyle: paragraph
        ]
    )
}

func textSize(_ value: String, font: NSFont) -> NSSize {
    (value as NSString).size(withAttributes: [.font: font])
}

guard let source = NSImage(contentsOf: inputURL) else {
    fputs("Could not open \(inputURL.path)\n", stderr)
    exit(1)
}

let image = NSImage(size: NSSize(width: width, height: height))
image.lockFocusFlipped(true)
source.draw(
    in: NSRect(x: 0, y: 0, width: width, height: height),
    from: .zero,
    operation: .copy,
    fraction: 1,
    respectFlipped: true,
    hints: nil
)

// Use the full lower board area for the changing values. The optional takeaway
// band is omitted so the numbers can meet the board readability floor.
roundedRect(NSRect(x: 80, y: 620, width: 1440, height: 240), radius: 16, fill: .white)
roundedRect(NSRect(x: 100, y: 640, width: 1400, height: 194), radius: 14, fill: .white, stroke: rule, lineWidth: 1.5)

let stages: [(String, String)] = [
    ("STARTING VECTOR", "[.42, −1.15, …]"),
    ("AFTER LAYER 1", "[.51, −.87, …]"),
    ("AFTER LAYER 2", "[.27, −1.21, …]"),
    ("RICHER VECTOR", "[.19, −1.12, …]")
]

let cellWidth: CGFloat = 316
let cellHeight: CGFloat = 174
let gap: CGFloat = 38
let startX: CGFloat = 111

for (index, stage) in stages.enumerated() {
    let x = startX + CGFloat(index) * (cellWidth + gap)
    let isFinal = index == stages.count - 1
    roundedRect(
        NSRect(x: x, y: 650, width: cellWidth, height: cellHeight),
        radius: 12,
        fill: isFinal ? gold.withAlphaComponent(0.58) : paleLavender,
        stroke: isFinal ? color("#e4bf59") : rule,
        lineWidth: isFinal ? 1.5 : 1
    )
    drawText(stage.0, in: NSRect(x: x + 8, y: 672, width: cellWidth - 16, height: 44), font: heavy(28), color: isFinal ? navy : muted, alignment: .center)
    drawText(stage.1, in: NSRect(x: x + 5, y: 735, width: cellWidth - 10, height: 54), font: demi(38), color: isFinal ? navy : purple, alignment: .center)

    if index < stages.count - 1 {
        drawText("→", in: NSRect(x: x + cellWidth, y: 719, width: gap, height: 52), font: demi(38), color: purple, alignment: .center)
    }
}

image.unlockFocus()

guard let tiff = image.tiffRepresentation,
      let bitmap = NSBitmapImageRep(data: tiff),
      let jpeg = bitmap.representation(using: .jpeg, properties: [.compressionFactor: 0.94]) else {
    fputs("Could not encode output image.\n", stderr)
    exit(1)
}

for outputURL in outputURLs {
    try jpeg.write(to: outputURL)
    print("Built \(outputURL.path)")
}
