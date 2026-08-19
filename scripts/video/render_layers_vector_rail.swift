#!/usr/bin/env swift

import AppKit
import CoreText
import Foundation

let repoRoot = URL(fileURLWithPath: FileManager.default.currentDirectoryPath)
let inputURL = repoRoot.appendingPathComponent("board-review-first-four/.pre-board-spec/understand-ai/layers-2-inside-alternative.jpg")
let outputURLs = [
    repoRoot.appendingPathComponent("board-review-first-four/alternatives/understand-ai/layers-2-inside-alternative.jpg"),
    repoRoot.appendingPathComponent("board-review-first-four/alternatives/understand-ai/layers-2-inside-vector-rail-alternative.jpg"),
    repoRoot.appendingPathComponent("lessons/layers-2-inside.jpg")
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

// The rail covers only the unused lower portion of the transparent layer stack.
roundedRect(NSRect(x: 100, y: 592, width: 1400, height: 132), radius: 14, fill: .white, stroke: rule, lineWidth: 1.5)

let stages: [(String, String)] = [
    ("STARTING VECTOR", "[.42, −1.15, …]"),
    ("AFTER LAYER 1", "[.51, −.87, …]"),
    ("AFTER LAYER 2", "[.27, −1.21, …]"),
    ("AFTER LAYER 3", "[.31, −.92, …]"),
    ("RICHER VECTOR", "[.19, −1.12, …]")
]

let cellWidth: CGFloat = 250
let cellHeight: CGFloat = 110
let gap: CGFloat = 32
let startX: CGFloat = 111

for (index, stage) in stages.enumerated() {
    let x = startX + CGFloat(index) * (cellWidth + gap)
    let isFinal = index == stages.count - 1
    roundedRect(
        NSRect(x: x, y: 603, width: cellWidth, height: cellHeight),
        radius: 12,
        fill: isFinal ? gold.withAlphaComponent(0.58) : paleLavender,
        stroke: isFinal ? color("#e4bf59") : rule,
        lineWidth: isFinal ? 1.5 : 1
    )
    drawText(stage.0, in: NSRect(x: x + 8, y: 614, width: cellWidth - 16, height: 32), font: heavy(24), color: isFinal ? navy : muted, alignment: .center)
    drawText(stage.1, in: NSRect(x: x + 5, y: 658, width: cellWidth - 10, height: 38), font: demi(28), color: isFinal ? navy : purple, alignment: .center)

    if index < stages.count - 1 {
        drawText("→", in: NSRect(x: x + cellWidth, y: 638, width: gap, height: 38), font: demi(28), color: purple, alignment: .center)
    }
}

// Rebuild the standardized takeaway band with the revised message.
roundedRect(NSRect(x: 80, y: 776, width: 1440, height: 84), radius: 16, fill: gold)
let takeaway = "Same two moves. A different vector after every pass."
let takeawayFont = demi(32)
let takeawaySize = textSize(takeaway, font: takeawayFont)
let lockupWidth: CGFloat = 52 + 16 + takeawaySize.width
let lockupX = (width - lockupWidth) / 2
roundedRect(NSRect(x: lockupX, y: 792, width: 52, height: 52), radius: 26, fill: purple)

let check = NSBezierPath()
check.move(to: NSPoint(x: lockupX + 14, y: 818))
check.line(to: NSPoint(x: lockupX + 23, y: 827))
check.line(to: NSPoint(x: lockupX + 39, y: 807))
check.lineWidth = 5
check.lineCapStyle = .round
check.lineJoinStyle = .round
NSColor.white.setStroke()
check.stroke()
drawText(takeaway, in: NSRect(x: lockupX + 68, y: 800, width: takeawaySize.width + 4, height: 46), font: takeawayFont, color: navy)

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
