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

struct Move {
    let title: String
    let prompt: String
    let accent: NSColor
    let icon: String
}

func drawLine(_ from: NSPoint, _ to: NSPoint, color: NSColor, width: CGFloat = 4) {
    let path = NSBezierPath()
    path.move(to: from)
    path.line(to: to)
    path.lineWidth = width
    path.lineCapStyle = .round
    color.setStroke()
    path.stroke()
}

func drawCenteredMultiline(
    _ value: String,
    in rect: NSRect,
    font: NSFont,
    color: NSColor,
    lineHeight: CGFloat
) {
    let paragraph = NSMutableParagraphStyle()
    paragraph.alignment = .center
    paragraph.minimumLineHeight = lineHeight
    paragraph.maximumLineHeight = lineHeight
    let attributes: [NSAttributedString.Key: Any] = [
        .font: font,
        .foregroundColor: color,
        .paragraphStyle: paragraph
    ]
    let bounds = (value as NSString).boundingRect(
        with: NSSize(width: rect.width, height: 1000),
        options: [.usesLineFragmentOrigin, .usesFontLeading],
        attributes: attributes
    )
    (value as NSString).draw(
        in: NSRect(x: rect.minX, y: rect.midY - ceil(bounds.height) / 2, width: rect.width, height: ceil(bounds.height) + 4),
        withAttributes: attributes
    )
}

func drawMagnifier(center: NSPoint, accent: NSColor, scale: CGFloat = 1) {
    let lens = NSBezierPath(ovalIn: NSRect(x: center.x - 30 * scale, y: center.y - 30 * scale, width: 60 * scale, height: 60 * scale))
    lens.lineWidth = 6 * scale
    accent.setStroke()
    lens.stroke()
    drawLine(
        NSPoint(x: center.x + 21 * scale, y: center.y + 21 * scale),
        NSPoint(x: center.x + 62 * scale, y: center.y + 62 * scale),
        color: accent,
        width: 7 * scale
    )
}

func drawArrow(from: NSPoint, to: NSPoint, accent: NSColor) {
    drawLine(from, to, color: accent, width: 5)
    let angle = atan2(to.y - from.y, to.x - from.x)
    let head: CGFloat = 15
    let left = NSPoint(x: to.x - head * cos(angle - .pi / 6), y: to.y - head * sin(angle - .pi / 6))
    let right = NSPoint(x: to.x - head * cos(angle + .pi / 6), y: to.y - head * sin(angle + .pi / 6))
    let path = NSBezierPath()
    path.move(to: left)
    path.line(to: to)
    path.line(to: right)
    path.lineWidth = 5
    path.lineCapStyle = .round
    path.lineJoinStyle = .round
    accent.setStroke()
    path.stroke()
}

func drawIcon(_ kind: String, center: NSPoint, accent: NSColor) {
    let stage = NSBezierPath(ovalIn: NSRect(x: center.x - 112, y: center.y - 82, width: 224, height: 164))
    accent.withAlphaComponent(0.10).setFill()
    stage.fill()

    if kind == "missing" {
        let tile: CGFloat = 42
        for row in 0..<2 {
            for column in 0..<3 where !(row == 1 && column == 2) {
                let x = center.x - 82 + CGFloat(column) * 52
                let y = center.y - 49 + CGFloat(row) * 52
                roundedRect(NSRect(x: x, y: y, width: tile, height: tile), radius: 8, fill: .white, stroke: accent, lineWidth: 3)
            }
        }
        let missingRect = NSRect(x: center.x + 22, y: center.y + 3, width: tile, height: tile)
        let missing = NSBezierPath(roundedRect: missingRect, xRadius: 8, yRadius: 8)
        missing.setLineDash([7, 6], count: 2, phase: 0)
        missing.lineWidth = 3
        accent.withAlphaComponent(0.55).setStroke()
        missing.stroke()
        drawMagnifier(center: NSPoint(x: center.x + 55, y: center.y + 32), accent: accent, scale: 0.72)
    } else if kind == "exceptions" {
        for index in 0..<4 {
            roundedRect(
                NSRect(x: center.x - 94 + CGFloat(index) * 48, y: center.y + 18, width: 34, height: 34),
                radius: 9,
                fill: accent.withAlphaComponent(0.20),
                stroke: accent,
                lineWidth: 3
            )
        }
        roundedRect(NSRect(x: center.x + 50, y: center.y - 55, width: 38, height: 38), radius: 10, fill: .white, stroke: accent, lineWidth: 4)
        drawArrow(
            from: NSPoint(x: center.x + 40, y: center.y + 15),
            to: NSPoint(x: center.x + 62, y: center.y - 32),
            accent: accent
        )
    } else {
        let cone = NSBezierPath()
        cone.move(to: NSPoint(x: center.x - 88, y: center.y - 70))
        cone.line(to: NSPoint(x: center.x - 18, y: center.y + 52))
        cone.line(to: NSPoint(x: center.x - 134, y: center.y + 52))
        cone.close()
        accent.withAlphaComponent(0.16).setFill()
        cone.fill()
        roundedRect(NSRect(x: center.x - 102, y: center.y + 5, width: 52, height: 52), radius: 26, fill: accent)
        centeredText("★", center: NSPoint(x: center.x - 76, y: center.y + 31), font: demi(25), color: .white)
        drawArrow(
            from: NSPoint(x: center.x - 35, y: center.y + 28),
            to: NSPoint(x: center.x + 8, y: center.y + 28),
            accent: accent
        )
        for (dx, dy) in [(38.0, -22.0), (82.0, -22.0), (60.0, 26.0)] {
            roundedRect(NSRect(x: center.x + dx - 18, y: center.y + dy - 18, width: 36, height: 36), radius: 18, fill: .white, stroke: accent, lineWidth: 3)
        }
    }
}

func drawMove(_ move: Move, rect: NSRect) {
    drawCenteredMultiline(move.title, in: NSRect(x: rect.minX + 24, y: rect.minY + 24, width: rect.width - 48, height: 52), font: demi(34), color: cardTitle, lineHeight: 40)
    drawCenteredMultiline(move.prompt, in: NSRect(x: rect.minX + 28, y: rect.minY + 92, width: rect.width - 56, height: 132), font: medium(30), color: navy, lineHeight: 38)
    drawIcon(move.icon, center: NSPoint(x: rect.midX, y: rect.minY + 350), accent: move.accent)
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

func promoteMechanismsBoard() throws {
    let source = repoRoot.appendingPathComponent("board-review-first-four/alternatives/avoid-traps/training-bias-1-mechanisms-alternative.jpg")
    let data = try Data(contentsOf: source)
    for relativePath in ["illustrations/training-bias-mechanisms.jpg", "lessons/training-bias-1-mechanisms-board.jpg"] {
        let output = repoRoot.appendingPathComponent(relativePath)
        try FileManager.default.createDirectory(at: output.deletingLastPathComponent(), withIntermediateDirectories: true)
        try data.write(to: output)
        print("Built \(output.path)")
    }
}

func renderQuestionsBoard() throws {
    let image = NSImage(size: NSSize(width: width, height: height))
    image.lockFocusFlipped(true)
    lavender.setFill()
    NSRect(x: 0, y: 0, width: width, height: height).fill()

    drawText("Three questions that crack the picture open", in: NSRect(x: 80, y: 45, width: 1440, height: 58), font: heavy(44), color: navy, alignment: .center)
    roundedRect(NSRect(x: 80, y: 132, width: 1440, height: 604), radius: 16, fill: .white)

    let moves = [
        Move(title: "ASK WHAT’S MISSING", prompt: "“What’s missing from this answer?”", accent: purple, icon: "missing"),
        Move(title: "ASK FOR EXCEPTIONS", prompt: "“Show me examples that don’t fit the pattern you just gave.”", accent: blue, icon: "exceptions"),
        Move(title: "REMOVE THE FAMOUS", prompt: "“Answer again, leaving out the most famous examples.”", accent: orange, icon: "famous")
    ]

    drawLine(NSPoint(x: 560, y: 160), NSPoint(x: 560, y: 708), color: rule, width: 2)
    drawLine(NSPoint(x: 1040, y: 160), NSPoint(x: 1040, y: 708), color: rule, width: 2)

    let cardWidth: CGFloat = 480
    let cardHeight: CGFloat = 548
    let xs: [CGFloat] = [80, 560, 1040]
    for (index, move) in moves.enumerated() {
        drawMove(move, rect: NSRect(x: xs[index], y: 160, width: cardWidth, height: cardHeight))
    }

    drawCheckBand("The model usually has the rest of the picture.")
    try save(image, relativePaths: [
        "board-review-first-four/alternatives/avoid-traps/training-bias-2-questions-alternative.jpg",
        "board-review-first-four/current-selected/avoid-traps/training-bias-2-questions.jpg",
        "illustrations/training-bias-questions.jpg",
        "lessons/training-bias-2-questions.jpg",
        "lessons/training-bias-2-questions-board.jpg"
    ])
}

try promoteMechanismsBoard()
try renderQuestionsBoard()
