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
let cardTitle = color("#152b7a")
let muted = color("#655f7c")
let purple = color("#6f52ff")
let blue = color("#3976d4")
let orange = color("#ed8708")
let teal = color("#14968f")
let red = color("#dd4b68")
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

func promote(_ sourcePath: String, to relativePaths: [String]) throws {
    let source = repoRoot.appendingPathComponent(sourcePath)
    let data = try Data(contentsOf: source)
    for relativePath in relativePaths {
        let output = repoRoot.appendingPathComponent(relativePath)
        try FileManager.default.createDirectory(at: output.deletingLastPathComponent(), withIntermediateDirectories: true)
        try data.write(to: output)
        print("Built \(output.path)")
    }
}

func drawTwoCard(
    rect: NSRect,
    marker: String,
    title: String,
    body: String,
    footer: String,
    accent: NSColor
) {
    roundedRect(rect, radius: 16, fill: pale, stroke: rule, lineWidth: 1.5)
    roundedRect(NSRect(x: rect.midX - 30, y: rect.minY + 30, width: 60, height: 60), radius: 30, fill: accent)
    centeredText(marker, center: NSPoint(x: rect.midX, y: rect.minY + 60), font: heavy(26), color: .white)
    drawText(title, in: NSRect(x: rect.minX + 30, y: rect.minY + 116, width: rect.width - 60, height: 48), font: demi(31), color: cardTitle, alignment: .center)
    drawText(body, in: NSRect(x: rect.minX + 42, y: rect.minY + 206, width: rect.width - 84, height: 150), font: medium(29), color: muted, alignment: .center, lineHeight: 36)
    roundedRect(NSRect(x: rect.minX + 42, y: rect.maxY - 82, width: rect.width - 84, height: 52), radius: 10, fill: .white)
    drawText(footer, in: NSRect(x: rect.minX + 52, y: rect.maxY - 70, width: rect.width - 104, height: 34), font: demi(24), color: accent, alignment: .center)
}

func renderMindBoard() throws {
    let image = NSImage(size: NSSize(width: width, height: height))
    image.lockFocusFlipped(true)
    lavender.setFill()
    NSRect(x: 0, y: 0, width: width, height: height).fill()

    drawText("Why AI feels like somebody", in: NSRect(x: 80, y: 57, width: 1440, height: 58), font: heavy(44), color: navy, alignment: .center)
    roundedRect(NSRect(x: 80, y: 172, width: 1440, height: 564), radius: 16, fill: .white)
    drawTwoCard(
        rect: NSRect(x: 112, y: 204, width: 658, height: 500),
        marker: "1",
        title: "YOUR BRAIN LOOKS FOR MINDS",
        body: "Detecting minds kept your ancestors alive, so the detector fires constantly. You see faces in toast and personalities in cars.",
        footer: "THE DETECTOR FIRES",
        accent: teal
    )
    drawTwoCard(
        rect: NSRect(x: 830, y: 204, width: 658, height: 500),
        marker: "2",
        title: "AI SETS IT OFF HARDER",
        body: "It says “I think” and “I feel.” Your brain hears a person. They are tokens a probability process landed on.",
        footer: "WORDS, NOT A MIND",
        accent: purple
    )
    drawCheckBand("Human-sounding is not a mind.")
    try save(image, relativePaths: [
        "board-review-first-four/alternatives/avoid-traps/mind-trap-eliza-effect-alternative.jpg",
        "board-review-first-four/current-selected/avoid-traps/mind-trap-1-eliza-effect.jpg",
        "illustrations/mind-trap-eliza-effect.jpg",
        "lessons/mind-trap-1-eliza-effect.jpg"
    ])
}

struct Reason {
    let number: String
    let title: String
    let body: String
    let accent: NSColor
}

func drawReason(_ reason: Reason, rect: NSRect) {
    roundedRect(rect, radius: 16, fill: pale, stroke: rule, lineWidth: 1.5)
    roundedRect(NSRect(x: rect.minX + 28, y: rect.minY + 26, width: 58, height: 58), radius: 29, fill: reason.accent)
    centeredText(reason.number, center: NSPoint(x: rect.minX + 57, y: rect.minY + 55), font: heavy(25), color: .white)
    drawText(reason.title, in: NSRect(x: rect.minX + 108, y: rect.minY + 28, width: rect.width - 138, height: 48), font: demi(31), color: navy)
    drawText(reason.body, in: NSRect(x: rect.minX + 28, y: rect.minY + 104, width: rect.width - 56, height: 92), font: medium(27), color: muted, lineHeight: 33)
}

func renderFakeReasonsBoard() throws {
    let image = NSImage(size: NSSize(width: width, height: height))
    image.lockFocusFlipped(true)
    lavender.setFill()
    NSRect(x: 0, y: 0, width: width, height: height).fill()

    drawText("Why some fakes aren’t friendly", in: NSRect(x: 80, y: 57, width: 1440, height: 58), font: heavy(44), color: navy, alignment: .center)
    roundedRect(NSRect(x: 80, y: 172, width: 1440, height: 564), radius: 16, fill: .white)

    let reasons = [
        Reason(number: "1", title: "Money", body: "Outrage gets clicks, and clicks pay.", accent: purple),
        Reason(number: "2", title: "Power", body: "Change what people believe and you change how they vote, protest, and spend.", accent: blue),
        Reason(number: "3", title: "Fame", body: "A viral clip means followers, and it doesn’t have to be true to travel.", accent: orange),
        Reason(number: "4", title: "Cruelty", body: "Some fakes exist to humiliate one person, especially at school.", accent: red)
    ]
    let cardWidth: CGFloat = 658
    let cardHeight: CGFloat = 236
    let xs: [CGFloat] = [112, 830]
    let ys: [CGFloat] = [202, 466]
    drawReason(reasons[0], rect: NSRect(x: xs[0], y: ys[0], width: cardWidth, height: cardHeight))
    drawReason(reasons[1], rect: NSRect(x: xs[1], y: ys[0], width: cardWidth, height: cardHeight))
    drawReason(reasons[2], rect: NSRect(x: xs[0], y: ys[1], width: cardWidth, height: cardHeight))
    drawReason(reasons[3], rect: NSRect(x: xs[1], y: ys[1], width: cardWidth, height: cardHeight))
    drawCheckBand("A fake is built to get something back.")
    try save(image, relativePaths: [
        "board-review-first-four/alternatives/avoid-traps/fake-trap-four-reasons-alternative.jpg",
        "board-review-first-four/current-selected/avoid-traps/fake-trap-2-four-reasons.jpg",
        "illustrations/fake-trap-four-reasons.jpg",
        "lessons/fake-trap-2-four-reasons-board.jpg"
    ])
}

try renderMindBoard()
try renderFakeReasonsBoard()
try promote(
    "board-review-first-four/alternatives/avoid-traps/flattery-trap-praise-loop-alternative.jpg",
    to: ["board-review-first-four/current-selected/avoid-traps/flattery-trap-2-praise-loop.jpg", "illustrations/flattery-trap-praise-loop.jpg", "lessons/flattery-trap-2-praise-loop.jpg"]
)
try promote(
    "board-review-first-four/alternatives/avoid-traps/support-trap-real-vs-missing-alternative.jpg",
    to: ["board-review-first-four/current-selected/avoid-traps/support-trap-2-real-vs-missing.jpg", "illustrations/support-trap-real-vs-missing.jpg", "lessons/support-trap-2-real-vs-missing.jpg"]
)
try promote(
    "board-review-first-four/alternatives/avoid-traps/fake-trap-three-checks-alternative.jpg",
    to: ["board-review-first-four/current-selected/avoid-traps/fake-trap-3-three-checks.jpg", "illustrations/fake-trap-three-checks.jpg", "lessons/fake-trap-3-three-checks-board.jpg"]
)
