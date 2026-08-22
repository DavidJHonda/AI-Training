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

func strokePath(_ path: NSBezierPath, color: NSColor, lineWidth: CGFloat = 4) {
    color.setStroke()
    path.lineWidth = lineWidth
    path.lineCapStyle = .round
    path.lineJoinStyle = .round
    path.stroke()
}

func drawDetector(center: NSPoint, accent: NSColor) {
    let outer = NSBezierPath(ovalIn: NSRect(x: center.x - 49, y: center.y - 49, width: 98, height: 98))
    strokePath(outer, color: accent, lineWidth: 5)
    let inner = NSBezierPath(ovalIn: NSRect(x: center.x - 27, y: center.y - 27, width: 54, height: 54))
    strokePath(inner, color: accent.withAlphaComponent(0.45), lineWidth: 4)
    let dot = NSBezierPath(ovalIn: NSRect(x: center.x - 8, y: center.y - 8, width: 16, height: 16))
    accent.setFill()
    dot.fill()
    for radius: CGFloat in [66, 82] {
        let arc = NSBezierPath()
        arc.appendArc(withCenter: center, radius: radius, startAngle: 205, endAngle: 335)
        strokePath(arc, color: accent.withAlphaComponent(radius == 66 ? 0.48 : 0.24), lineWidth: 4)
    }
}

func drawToast(center: NSPoint, accent: NSColor) {
    let toast = NSBezierPath()
    toast.move(to: NSPoint(x: center.x - 52, y: center.y + 43))
    toast.line(to: NSPoint(x: center.x - 43, y: center.y - 23))
    toast.curve(to: NSPoint(x: center.x, y: center.y - 43), controlPoint1: NSPoint(x: center.x - 39, y: center.y - 47), controlPoint2: NSPoint(x: center.x - 13, y: center.y - 50))
    toast.curve(to: NSPoint(x: center.x + 43, y: center.y - 23), controlPoint1: NSPoint(x: center.x + 13, y: center.y - 50), controlPoint2: NSPoint(x: center.x + 39, y: center.y - 47))
    toast.line(to: NSPoint(x: center.x + 52, y: center.y + 43))
    toast.close()
    color("#fff1c7").setFill()
    toast.fill()
    strokePath(toast, color: accent, lineWidth: 4)
    for x in [center.x - 19, center.x + 19] {
        let eye = NSBezierPath(ovalIn: NSRect(x: x - 5, y: center.y - 7, width: 10, height: 10))
        accent.setFill()
        eye.fill()
    }
    let smile = NSBezierPath()
    smile.appendArc(withCenter: NSPoint(x: center.x, y: center.y + 8), radius: 18, startAngle: 15, endAngle: 165)
    strokePath(smile, color: accent, lineWidth: 4)
}

func drawCar(center: NSPoint, accent: NSColor) {
    roundedRect(NSRect(x: center.x - 62, y: center.y - 22, width: 124, height: 64), radius: 18, fill: color("#e9f6f5"), stroke: accent, lineWidth: 4)
    let roof = NSBezierPath()
    roof.move(to: NSPoint(x: center.x - 43, y: center.y - 22))
    roof.line(to: NSPoint(x: center.x - 25, y: center.y - 47))
    roof.line(to: NSPoint(x: center.x + 25, y: center.y - 47))
    roof.line(to: NSPoint(x: center.x + 43, y: center.y - 22))
    strokePath(roof, color: accent, lineWidth: 4)
    for x in [center.x - 36, center.x + 36] {
        let light = NSBezierPath(ovalIn: NSRect(x: x - 8, y: center.y - 1, width: 16, height: 16))
        accent.setFill()
        light.fill()
    }
    let grille = NSBezierPath()
    grille.move(to: NSPoint(x: center.x - 23, y: center.y + 24))
    grille.curve(to: NSPoint(x: center.x + 23, y: center.y + 24), controlPoint1: NSPoint(x: center.x - 10, y: center.y + 37), controlPoint2: NSPoint(x: center.x + 10, y: center.y + 37))
    strokePath(grille, color: accent, lineWidth: 4)
}

func drawSpeechBubble(_ value: String, rect: NSRect, accent: NSColor) {
    roundedRect(rect, radius: 20, fill: .white, stroke: accent, lineWidth: 3)
    let tail = NSBezierPath()
    tail.move(to: NSPoint(x: rect.minX + 30, y: rect.maxY))
    tail.line(to: NSPoint(x: rect.minX + 44, y: rect.maxY + 16))
    tail.line(to: NSPoint(x: rect.minX + 60, y: rect.maxY))
    tail.close()
    NSColor.white.setFill()
    tail.fill()
    strokePath(tail, color: accent, lineWidth: 3)
    drawText(value, in: NSRect(x: rect.minX + 14, y: rect.minY + 13, width: rect.width - 28, height: 38), font: demi(23), color: navy, alignment: .center)
}

func drawSequenceArrow(center: NSPoint) {
    let line = NSBezierPath()
    line.move(to: NSPoint(x: center.x - 17, y: center.y))
    line.line(to: NSPoint(x: center.x + 13, y: center.y))
    strokePath(line, color: purple, lineWidth: 5)
    let head = NSBezierPath()
    head.move(to: NSPoint(x: center.x + 3, y: center.y - 12))
    head.line(to: NSPoint(x: center.x + 16, y: center.y))
    head.line(to: NSPoint(x: center.x + 3, y: center.y + 12))
    strokePath(head, color: purple, lineWidth: 5)
}

func drawMindCard(rect: NSRect, title: String, body: String, accent: NSColor, graphic: String) {
    roundedRect(rect, radius: 16, fill: pale, stroke: rule, lineWidth: 1.5)
    drawText(title, in: NSRect(x: rect.minX + 34, y: rect.minY + 38, width: rect.width - 68, height: 48), font: demi(31), color: cardTitle, alignment: .center)
    drawText(body, in: NSRect(x: rect.minX + 48, y: rect.minY + 112, width: rect.width - 96, height: 110), font: medium(28), color: navy, alignment: .center, lineHeight: 35)

    let divider = NSBezierPath()
    divider.move(to: NSPoint(x: rect.minX + 54, y: rect.minY + 246))
    divider.line(to: NSPoint(x: rect.maxX - 54, y: rect.minY + 246))
    strokePath(divider, color: rule, lineWidth: 2)

    if graphic == "everywhere" {
        drawDetector(center: NSPoint(x: rect.midX, y: rect.minY + 340), accent: accent)
        drawToast(center: NSPoint(x: rect.midX - 172, y: rect.minY + 405), accent: accent)
        drawCar(center: NSPoint(x: rect.midX + 172, y: rect.minY + 405), accent: accent)
    } else {
        drawDetector(center: NSPoint(x: rect.midX + 120, y: rect.minY + 376), accent: accent)
        drawSpeechBubble("“I think”", rect: NSRect(x: rect.minX + 52, y: rect.minY + 292, width: 190, height: 62), accent: accent)
        drawSpeechBubble("“I feel”", rect: NSRect(x: rect.minX + 88, y: rect.minY + 388, width: 180, height: 62), accent: accent)
        let signal = NSBezierPath()
        signal.move(to: NSPoint(x: rect.minX + 265, y: rect.minY + 365))
        signal.line(to: NSPoint(x: rect.midX + 62, y: rect.minY + 376))
        signal.setLineDash([8, 7], count: 2, phase: 0)
        strokePath(signal, color: accent.withAlphaComponent(0.6), lineWidth: 4)
    }
}

func renderMindBoard() throws {
    let image = NSImage(size: NSSize(width: width, height: height))
    image.lockFocusFlipped(true)
    lavender.setFill()
    NSRect(x: 0, y: 0, width: width, height: height).fill()

    drawText("Why AI feels like somebody", in: NSRect(x: 80, y: 57, width: 1440, height: 58), font: heavy(44), color: navy, alignment: .center)
    roundedRect(NSRect(x: 80, y: 172, width: 1440, height: 564), radius: 16, fill: .white)
    drawMindCard(
        rect: NSRect(x: 112, y: 204, width: 658, height: 500),
        title: "YOUR BRAIN LOOKS FOR MINDS",
        body: "Your brain is built to detect minds. That’s why you see faces in toast and personalities in cars.",
        accent: teal,
        graphic: "everywhere"
    )
    drawSequenceArrow(center: NSPoint(x: 800, y: 454))
    drawMindCard(
        rect: NSRect(x: 830, y: 204, width: 658, height: 500),
        title: "AI SETS IT OFF HARDER",
        body: "AI says “I think” and “I feel.” Your brain hears a person, but those are generated words.",
        accent: purple,
        graphic: "ai"
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

if CommandLine.arguments.contains("--mind-only") {
    try renderMindBoard()
} else {
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
}
