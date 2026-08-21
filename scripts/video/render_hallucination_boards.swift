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
    let number: String
    let title: String
    let body: String
    let accent: NSColor
}

func drawTypeCard(_ item: HallucinationType, rect: NSRect) {
    roundedRect(rect, radius: 16, fill: pale, stroke: rule, lineWidth: 1.5)
    roundedRect(NSRect(x: rect.minX + 28, y: rect.minY + 26, width: 58, height: 58), radius: 29, fill: item.accent)
    centeredText(item.number, center: NSPoint(x: rect.minX + 57, y: rect.minY + 55), font: heavy(25), color: .white)
    drawText(item.title, in: NSRect(x: rect.minX + 108, y: rect.minY + 28, width: rect.width - 138, height: 48), font: demi(31), color: navy)
    drawText(item.body, in: NSRect(x: rect.minX + 28, y: rect.minY + 104, width: rect.width - 56, height: 92), font: medium(27), color: muted, lineHeight: 33)
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

    drawText("What counts as a hallucination?", in: NSRect(x: 80, y: 57, width: 1440, height: 58), font: heavy(44), color: navy, alignment: .center)
    roundedRect(NSRect(x: 80, y: 172, width: 1440, height: 564), radius: 16, fill: .white)

    let items = [
        HallucinationType(number: "1", title: "Fake source", body: "A study, article, author, journal, or citation that does not exist.", accent: purple),
        HallucinationType(number: "2", title: "Fake detail", body: "A real person, place, event, or idea with invented dates, numbers, quotes, or specifics.", accent: blue),
        HallucinationType(number: "3", title: "Blended fact", body: "Real facts combined in a way that creates a conclusion that is false.", accent: orange),
        HallucinationType(number: "4", title: "Misread source", body: "The source is real, but the model read it wrong.", accent: teal)
    ]

    let cardWidth: CGFloat = 658
    let cardHeight: CGFloat = 236
    let xs: [CGFloat] = [112, 830]
    let ys: [CGFloat] = [202, 466]
    drawTypeCard(items[0], rect: NSRect(x: xs[0], y: ys[0], width: cardWidth, height: cardHeight))
    drawTypeCard(items[1], rect: NSRect(x: xs[1], y: ys[0], width: cardWidth, height: cardHeight))
    drawTypeCard(items[2], rect: NSRect(x: xs[0], y: ys[1], width: cardWidth, height: cardHeight))
    drawTypeCard(items[3], rect: NSRect(x: xs[1], y: ys[1], width: cardWidth, height: cardHeight))

    drawCheckBand("Not every wrong answer is a hallucination.")
    try save(image, relativePaths: [
        "board-review-first-four/alternatives/avoid-traps/hallucination-2-types-alternative.jpg",
        "illustrations/hallucination-types.jpg",
        "lessons/hallucination-2-types.jpg"
    ])
}

try promoteWhyBoard()
try renderTypesBoard()
