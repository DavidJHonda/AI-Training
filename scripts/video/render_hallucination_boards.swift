#!/usr/bin/env swift

import AppKit
import CoreText
import Foundation

let repoRoot = URL(fileURLWithPath: FileManager.default.currentDirectoryPath)
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

let lavender = color("#eeeaff")
let navy = color("#08072b")
let muted = color("#655f7c")
let purple = color("#6f52ff")
let blue = color("#3976d4")
let orange = color("#ed8708")
let teal = color("#14968f")
let gold = color("#ffe9ab")
let rule = color("#e3def2")
let pale = color("#fbfaff")

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

func drawText(
    _ value: String,
    in rect: NSRect,
    font: NSFont,
    color: NSColor,
    alignment: NSTextAlignment = .left,
    lineHeight: CGFloat? = nil
) {
    let paragraph = NSMutableParagraphStyle()
    paragraph.alignment = alignment
    if let lineHeight {
        paragraph.minimumLineHeight = lineHeight
        paragraph.maximumLineHeight = lineHeight
    }
    (value as NSString).draw(in: rect, withAttributes: [
        .font: font,
        .foregroundColor: color,
        .paragraphStyle: paragraph
    ])
}

func textSize(_ value: String, font: NSFont) -> NSSize {
    (value as NSString).size(withAttributes: [.font: font])
}

func centeredText(_ value: String, center: NSPoint, font: NSFont, color: NSColor) {
    let size = textSize(value, font: font)
    drawText(
        value,
        in: NSRect(x: center.x - size.width / 2, y: center.y - size.height / 2 - 1, width: size.width + 4, height: size.height + 6),
        font: font,
        color: color,
        alignment: .center
    )
}

func drawCheckBand(_ takeaway: String) {
    roundedRect(NSRect(x: 80, y: 776, width: 1440, height: 84), radius: 16, fill: gold)
    let font = demi(32)
    let size = textSize(takeaway, font: font)
    let lockupWidth: CGFloat = 52 + 16 + size.width
    let x = (width - lockupWidth) / 2
    roundedRect(NSRect(x: x, y: 792, width: 52, height: 52), radius: 26, fill: purple)

    let check = NSBezierPath()
    check.move(to: NSPoint(x: x + 14, y: 818))
    check.line(to: NSPoint(x: x + 23, y: 827))
    check.line(to: NSPoint(x: x + 39, y: 807))
    check.lineWidth = 5
    check.lineCapStyle = .round
    check.lineJoinStyle = .round
    NSColor.white.setStroke()
    check.stroke()
    drawText(takeaway, in: NSRect(x: x + 68, y: 800, width: size.width + 4, height: 46), font: font, color: navy)
}

struct HallucinationType {
    let title: String
    let body: String
    let accent: NSColor
    let icon: String
}

func strokeLine(from: NSPoint, to: NSPoint, color: NSColor, width: CGFloat = 4) {
    let path = NSBezierPath()
    path.move(to: from)
    path.line(to: to)
    path.lineWidth = width
    path.lineCapStyle = .round
    color.setStroke()
    path.stroke()
}

func drawCheck(center: NSPoint, color: NSColor) {
    let path = NSBezierPath()
    path.move(to: NSPoint(x: center.x - 12, y: center.y))
    path.line(to: NSPoint(x: center.x - 3, y: center.y + 9))
    path.line(to: NSPoint(x: center.x + 15, y: center.y - 12))
    path.lineWidth = 5
    path.lineCapStyle = .round
    path.lineJoinStyle = .round
    color.setStroke()
    path.stroke()
}

func drawTypeIcon(_ kind: String, center: NSPoint, accent: NSColor) {
    roundedRect(NSRect(x: center.x - 78, y: center.y - 58, width: 156, height: 116), radius: 58, fill: accent.withAlphaComponent(0.10))

    if kind == "source" {
        let document = NSRect(x: center.x - 50, y: center.y - 44, width: 72, height: 88)
        roundedRect(document, radius: 9, fill: .white, stroke: accent, lineWidth: 3)
        strokeLine(from: NSPoint(x: document.minX + 15, y: document.minY + 24), to: NSPoint(x: document.maxX - 14, y: document.minY + 24), color: accent.withAlphaComponent(0.55), width: 3)
        strokeLine(from: NSPoint(x: document.minX + 15, y: document.minY + 41), to: NSPoint(x: document.maxX - 25, y: document.minY + 41), color: accent.withAlphaComponent(0.55), width: 3)
        drawText("?", in: NSRect(x: center.x + 17, y: center.y - 34, width: 48, height: 68), font: heavy(50), color: accent, alignment: .center)
    } else if kind == "detail" {
        let card = NSRect(x: center.x - 65, y: center.y - 42, width: 130, height: 84)
        roundedRect(card, radius: 12, fill: .white, stroke: accent, lineWidth: 3)
        let head = NSBezierPath(ovalIn: NSRect(x: card.minX + 18, y: card.minY + 16, width: 28, height: 28))
        accent.withAlphaComponent(0.75).setFill(); head.fill()
        let shoulders = NSBezierPath(ovalIn: NSRect(x: card.minX + 10, y: card.minY + 43, width: 44, height: 25))
        accent.withAlphaComponent(0.35).setFill(); shoulders.fill()
        roundedRect(NSRect(x: card.minX + 69, y: card.minY + 15, width: 44, height: 20), radius: 6, fill: accent.withAlphaComponent(0.15))
        roundedRect(NSRect(x: card.minX + 69, y: card.minY + 45, width: 44, height: 20), radius: 6, fill: accent.withAlphaComponent(0.15))
        centeredText("12", center: NSPoint(x: card.minX + 91, y: card.minY + 25), font: demi(16), color: accent)
        centeredText("99", center: NSPoint(x: card.minX + 91, y: card.minY + 55), font: demi(16), color: accent)
    } else if kind == "blend" {
        for offset in [-39.0, 8.0] {
            roundedRect(NSRect(x: center.x + offset, y: center.y - 35, width: 50, height: 50), radius: 12, fill: .white, stroke: accent, lineWidth: 3)
            drawCheck(center: NSPoint(x: center.x + offset + 25, y: center.y - 10), color: accent)
        }
        strokeLine(from: NSPoint(x: center.x - 2, y: center.y + 30), to: NSPoint(x: center.x + 42, y: center.y + 30), color: accent, width: 4)
        let arrow = NSBezierPath()
        arrow.move(to: NSPoint(x: center.x + 42, y: center.y + 30))
        arrow.line(to: NSPoint(x: center.x + 31, y: center.y + 21))
        arrow.move(to: NSPoint(x: center.x + 42, y: center.y + 30))
        arrow.line(to: NSPoint(x: center.x + 31, y: center.y + 39))
        arrow.lineWidth = 4; arrow.lineCapStyle = .round; accent.setStroke(); arrow.stroke()
        roundedRect(NSRect(x: center.x + 47, y: center.y + 8, width: 44, height: 44), radius: 22, fill: accent)
        strokeLine(from: NSPoint(x: center.x + 60, y: center.y + 21), to: NSPoint(x: center.x + 78, y: center.y + 39), color: .white, width: 4)
        strokeLine(from: NSPoint(x: center.x + 78, y: center.y + 21), to: NSPoint(x: center.x + 60, y: center.y + 39), color: .white, width: 4)
    } else {
        let document = NSRect(x: center.x - 57, y: center.y - 43, width: 88, height: 88)
        roundedRect(document, radius: 10, fill: .white, stroke: accent, lineWidth: 3)
        for y in [document.minY + 23, document.minY + 42, document.minY + 61] {
            strokeLine(from: NSPoint(x: document.minX + 15, y: y), to: NSPoint(x: document.maxX - 14, y: y), color: accent.withAlphaComponent(0.42), width: 3)
        }
        let lens = NSBezierPath(ovalIn: NSRect(x: center.x + 4, y: center.y - 23, width: 48, height: 48))
        accent.withAlphaComponent(0.10).setFill(); lens.fill(); accent.setStroke(); lens.lineWidth = 4; lens.stroke()
        strokeLine(from: NSPoint(x: center.x + 41, y: center.y + 15), to: NSPoint(x: center.x + 68, y: center.y + 42), color: accent, width: 6)
        strokeLine(from: NSPoint(x: center.x + 10, y: center.y + 2), to: NSPoint(x: center.x + 43, y: center.y + 2), color: accent, width: 4)
    }
}

func drawTypeQuadrant(_ item: HallucinationType, rect: NSRect) {
    drawText(item.title, in: NSRect(x: rect.minX + 40, y: rect.minY + 35, width: 500, height: 50), font: demi(34), color: navy)
    drawText(item.body, in: NSRect(x: rect.minX + 40, y: rect.minY + 91, width: 480, height: 124), font: medium(30), color: navy, lineHeight: 37)
    drawTypeIcon(item.icon, center: NSPoint(x: rect.maxX - 112, y: rect.midY + 13), accent: item.accent)
}

func save(_ image: NSImage, relativePaths: [String]) throws {
    image.unlockFocus()
    guard let tiff = image.tiffRepresentation,
          let bitmap = NSBitmapImageRep(data: tiff),
          let jpeg = bitmap.representation(using: .jpeg, properties: [.compressionFactor: 0.94]) else {
        throw NSError(domain: "render", code: 1)
    }
    for relativePath in relativePaths {
        let url = repoRoot.appendingPathComponent(relativePath)
        try FileManager.default.createDirectory(at: url.deletingLastPathComponent(), withIntermediateDirectories: true)
        try jpeg.write(to: url)
        print("Built \(url.path)")
    }
}

func promoteWhyBoard() throws {
    let source = repoRoot.appendingPathComponent("board-review-first-four/alternatives/avoid-traps/hallucination-1-why-alternative.jpg")
    let data = try Data(contentsOf: source)
    for relativePath in ["illustrations/hallucination-why.jpg", "lessons/hallucination-1-why.jpg"] {
        let output = repoRoot.appendingPathComponent(relativePath)
        try FileManager.default.createDirectory(at: output.deletingLastPathComponent(), withIntermediateDirectories: true)
        try data.write(to: output)
        print("Built \(output.path)")
    }
}

func renderTypesBoard() throws {
    let image = NSImage(size: NSSize(width: width, height: height))
    image.lockFocusFlipped(true)
    lavender.setFill()
    NSRect(x: 0, y: 0, width: width, height: height).fill()

    drawText("What counts as a hallucination?", in: NSRect(x: 80, y: 45, width: 1440, height: 64), font: heavy(46), color: navy, alignment: .center)
    roundedRect(NSRect(x: 80, y: 132, width: 1440, height: 604), radius: 18, fill: .white)

    let items = [
        HallucinationType(title: "Fake source", body: "A study, article, author, journal, or citation that does not exist.", accent: purple, icon: "source"),
        HallucinationType(title: "Fake detail", body: "A real person, place, event, or idea with invented dates, numbers, quotes, or specifics.", accent: blue, icon: "detail"),
        HallucinationType(title: "Blended fact", body: "Real facts combined in a way that creates a conclusion that is false.", accent: orange, icon: "blend"),
        HallucinationType(title: "Misread source", body: "The source is real, but the model read it wrong.", accent: teal, icon: "misread")
    ]

    rule.setStroke()
    let vertical = NSBezierPath(); vertical.move(to: NSPoint(x: 800, y: 160)); vertical.line(to: NSPoint(x: 800, y: 708)); vertical.lineWidth = 2; vertical.stroke()
    let horizontal = NSBezierPath(); horizontal.move(to: NSPoint(x: 108, y: 434)); horizontal.line(to: NSPoint(x: 1492, y: 434)); horizontal.lineWidth = 2; horizontal.stroke()

    drawTypeQuadrant(items[0], rect: NSRect(x: 80, y: 132, width: 720, height: 302))
    drawTypeQuadrant(items[1], rect: NSRect(x: 800, y: 132, width: 720, height: 302))
    drawTypeQuadrant(items[2], rect: NSRect(x: 80, y: 434, width: 720, height: 302))
    drawTypeQuadrant(items[3], rect: NSRect(x: 800, y: 434, width: 720, height: 302))

    drawCheckBand("Not every wrong answer is a hallucination.")
    try save(image, relativePaths: [
        "board-review-first-four/alternatives/avoid-traps/hallucination-2-types-alternative.jpg",
        "illustrations/hallucination-types.jpg",
        "lessons/hallucination-2-types.jpg"
    ])
}

try promoteWhyBoard()
try renderTypesBoard()
