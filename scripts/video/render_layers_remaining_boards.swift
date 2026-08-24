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
let bodyInk = color("#302c42")
let muted = color("#655f7c")
let purple = color("#6f52ff")
let orange = color("#ed8708")
let teal = color("#14968f")
let gold = color("#ffe9ab")
let rule = color("#e3def2")
let rowFill = color("#fbfaff")

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
func bold(_ size: CGFloat) -> NSFont { loadFont(path: "\(fontRoot)/AvenirNextforINTUIT-Bold.otf", size: size) }
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

func line(from start: NSPoint, to end: NSPoint, color: NSColor, width: CGFloat = 2) {
    let path = NSBezierPath()
    path.move(to: start)
    path.line(to: end)
    path.lineWidth = width
    path.lineCapStyle = .round
    color.setStroke()
    path.stroke()
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

func centeredText(_ value: String, center: NSPoint, font: NSFont, color: NSColor) {
    let size = textSize(value, font: font)
    drawText(
        value,
        in: NSRect(x: center.x - size.width / 2, y: center.y - size.height / 2 - 1, width: size.width + 2, height: size.height + 4),
        font: font,
        color: color,
        alignment: .center
    )
}

func drawArrow(from start: NSPoint, to end: NSPoint, color: NSColor, width: CGFloat = 3) {
    line(from: start, to: end, color: color, width: width)
    let angle = atan2(end.y - start.y, end.x - start.x)
    let head: CGFloat = 10
    for offset in [CGFloat.pi * 0.82, -CGFloat.pi * 0.82] {
        let tip = NSPoint(x: end.x + head * cos(angle + offset), y: end.y + head * sin(angle + offset))
        line(from: end, to: tip, color: color, width: width)
    }
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

func drawNumber(_ number: String, center: NSPoint) {
    roundedRect(NSRect(x: center.x - 26, y: center.y - 26, width: 52, height: 52), radius: 26, fill: purple)
    centeredText(number, center: center, font: heavy(24), color: .white)
}

func drawWordPill(_ value: String, center: NSPoint, fill: NSColor, textColor: NSColor = navy) {
    let pillWidth: CGFloat = 120
    roundedRect(NSRect(x: center.x - pillWidth / 2, y: center.y - 25, width: pillWidth, height: 50), radius: 12, fill: fill, stroke: rule)
    centeredText(value, center: center, font: medium(24), color: textColor)
}

func drawThreeReadsPicture(cardIndex: Int, rect: NSRect) {
    let centers = [
        NSPoint(x: rect.minX + 84, y: rect.midY),
        NSPoint(x: rect.midX, y: rect.midY),
        NSPoint(x: rect.maxX - 84, y: rect.midY)
    ]

    if cardIndex == 0 {
        drawWordPill("HORSE", center: NSPoint(x: centers[0].x, y: centers[0].y - 24), fill: color("#f3efff"))
        drawWordPill("BARN", center: NSPoint(x: centers[1].x, y: centers[1].y + 26), fill: color("#fff1dc"))
        drawWordPill("FELL", center: NSPoint(x: centers[2].x, y: centers[2].y - 14), fill: color("#e7f7f4"))
        centeredText("?", center: NSPoint(x: rect.midX, y: rect.maxY + 4), font: heavy(34), color: purple)
    } else if cardIndex == 1 {
        drawWordPill("HORSE", center: centers[0], fill: color("#f3efff"))
        drawWordPill("BARN", center: centers[1], fill: color("#fff1dc"))
        drawWordPill("FELL", center: centers[2], fill: color("#e7f7f4"))
        drawArrow(from: NSPoint(x: centers[0].x + 54, y: centers[0].y - 18), to: NSPoint(x: centers[1].x - 54, y: centers[1].y - 18), color: purple, width: 2.5)
        drawArrow(from: NSPoint(x: centers[1].x + 54, y: centers[1].y + 18), to: NSPoint(x: centers[2].x - 54, y: centers[2].y + 18), color: orange, width: 2.5)
        centeredText("?", center: NSPoint(x: rect.midX, y: rect.maxY + 4), font: heavy(30), color: purple)
    } else {
        line(from: NSPoint(x: centers[0].x, y: rect.maxY - 24), to: NSPoint(x: centers[2].x, y: rect.maxY - 24), color: teal, width: 4)
        drawWordPill("HORSE", center: centers[0], fill: color("#f3efff"))
        drawWordPill("BARN", center: centers[1], fill: color("#fff1dc"))
        drawWordPill("FELL", center: centers[2], fill: color("#e7f7f4"))
        roundedRect(NSRect(x: rect.midX - 19, y: rect.maxY - 15, width: 38, height: 38), radius: 19, fill: teal)
        centeredText("✓", center: NSPoint(x: rect.midX, y: rect.maxY + 4), font: demi(24), color: .white)
    }
}

func drawLayerStack(centerX: CGFloat, bottomY: CGFloat, count: Int, accent: NSColor) {
    let stackWidth: CGFloat = 244
    let layerHeight: CGFloat = 24
    let spacing: CGFloat = count > 5 ? 17 : 30
    for index in 0..<count {
        let y = bottomY - CGFloat(index) * spacing - layerHeight
        let inset = CGFloat(index) * 2.2
        roundedRect(
            NSRect(x: centerX - stackWidth / 2 + inset, y: y, width: stackWidth - inset * 2, height: layerHeight),
            radius: 8,
            fill: accent.withAlphaComponent(0.12 + CGFloat(index) * 0.035),
            stroke: accent.withAlphaComponent(0.55),
            lineWidth: 1.5
        )
    }
    drawArrow(from: NSPoint(x: centerX, y: bottomY + 5), to: NSPoint(x: centerX, y: bottomY - CGFloat(count) * spacing - 18), color: accent, width: 3)
}

func drawDiminishingReturns(rect: NSRect) {
    let origin = NSPoint(x: rect.minX + 48, y: rect.maxY - 32)
    let topRight = NSPoint(x: rect.maxX - 28, y: rect.minY + 24)
    line(from: origin, to: NSPoint(x: origin.x, y: topRight.y), color: muted, width: 2)
    line(from: origin, to: NSPoint(x: topRight.x, y: origin.y), color: muted, width: 2)

    let meaning = NSBezierPath()
    meaning.move(to: origin)
    meaning.curve(
        to: NSPoint(x: topRight.x, y: topRight.y + 26),
        controlPoint1: NSPoint(x: origin.x + 88, y: origin.y - 118),
        controlPoint2: NSPoint(x: topRight.x - 95, y: topRight.y + 28)
    )
    meaning.lineWidth = 5
    meaning.lineCapStyle = .round
    purple.setStroke()
    meaning.stroke()

    drawArrow(from: NSPoint(x: origin.x + 12, y: origin.y - 8), to: NSPoint(x: topRight.x - 14, y: topRight.y + 4), color: orange, width: 4)
    drawText("MEANING", in: NSRect(x: topRight.x - 150, y: topRight.y + 26, width: 145, height: 34), font: medium(24), color: purple, alignment: .right)
    drawText("COST", in: NSRect(x: topRight.x - 100, y: topRight.y - 20, width: 100, height: 34), font: medium(24), color: orange, alignment: .right)
}

func drawMeaningDot(_ label: String, center: NSPoint, fill: NSColor, radius: CGFloat = 32) {
    roundedRect(
        NSRect(x: center.x - radius, y: center.y - radius, width: radius * 2, height: radius * 2),
        radius: radius,
        fill: fill
    )
    centeredText(label, center: center, font: bold(22), color: .white)
}

func drawVectorAxes(in rect: NSRect) {
    line(
        from: NSPoint(x: rect.minX, y: rect.maxY),
        to: NSPoint(x: rect.minX, y: rect.minY),
        color: rule,
        width: 2
    )
    line(
        from: NSPoint(x: rect.minX, y: rect.maxY),
        to: NSPoint(x: rect.maxX, y: rect.maxY),
        color: rule,
        width: 2
    )
}

func drawAmbiguousVector(in rect: NSRect) {
    drawVectorAxes(in: rect)
    drawMeaningDot("CAT", center: NSPoint(x: rect.minX + 78, y: rect.minY + 54), fill: teal)
    drawMeaningDot("TIRED", center: NSPoint(x: rect.maxX - 66, y: rect.minY + 106), fill: orange, radius: 37)

    let itCenter = NSPoint(x: rect.midX + 12, y: rect.maxY - 48)
    roundedRect(
        NSRect(x: itCenter.x - 49, y: itCenter.y - 49, width: 98, height: 98),
        radius: 49,
        fill: color("#f1edff"),
        stroke: purple,
        lineWidth: 3
    )
    centeredText("?", center: NSPoint(x: itCenter.x, y: itCenter.y - 18), font: heavy(27), color: purple)
    centeredText("IT", center: NSPoint(x: itCenter.x, y: itCenter.y + 18), font: heavy(27), color: purple)
}

func drawLayerResolution(in rect: NSRect) {
    let catCenter = NSPoint(x: rect.minX + 58, y: rect.minY + 34)
    let tiredCenter = NSPoint(x: rect.maxX - 58, y: rect.minY + 34)
    drawMeaningDot("CAT", center: catCenter, fill: teal)
    drawMeaningDot("TIRED", center: tiredCenter, fill: orange, radius: 37)

    let stackX = rect.midX
    let stackTop = rect.minY + 68
    let layerWidth: CGFloat = 260
    let layerHeight: CGFloat = 32
    let layerGap: CGFloat = 7
    for index in 0..<4 {
        let y = stackTop + CGFloat(index) * (layerHeight + layerGap)
        roundedRect(
            NSRect(x: stackX - layerWidth / 2, y: y, width: layerWidth, height: layerHeight),
            radius: 10,
            fill: purple.withAlphaComponent(0.10 + CGFloat(index) * 0.07),
            stroke: purple.withAlphaComponent(0.52 + CGFloat(index) * 0.10),
            lineWidth: 2
        )
        drawText(
            "LAYER \(index + 1)",
            in: NSRect(x: stackX - layerWidth / 2 + 20, y: y + 4, width: 112, height: 24),
            font: demi(21),
            color: cardTitle,
            alignment: .left
        )
    }

    drawArrow(from: NSPoint(x: catCenter.x + 35, y: catCenter.y + 18), to: NSPoint(x: stackX - 78, y: stackTop + 8), color: teal, width: 3)
    drawArrow(from: NSPoint(x: tiredCenter.x - 40, y: tiredCenter.y + 18), to: NSPoint(x: stackX + 78, y: stackTop + 8), color: orange, width: 3)

    let itStart = NSPoint(x: stackX + 20, y: stackTop + 16)
    let itEnd = NSPoint(x: stackX + 92, y: stackTop + 3 * (layerHeight + layerGap) + 16)
    let path = NSBezierPath()
    path.move(to: itStart)
    path.curve(
        to: itEnd,
        controlPoint1: NSPoint(x: stackX + 34, y: stackTop + 48),
        controlPoint2: NSPoint(x: stackX + 70, y: stackTop + 90)
    )
    path.lineWidth = 5
    path.lineCapStyle = .round
    purple.setStroke()
    path.stroke()
    for point in [itStart, NSPoint(x: stackX + 42, y: stackTop + 50), NSPoint(x: stackX + 66, y: stackTop + 88), itEnd] {
        roundedRect(NSRect(x: point.x - 9, y: point.y - 9, width: 18, height: 18), radius: 9, fill: purple)
    }
    roundedRect(NSRect(x: itEnd.x - 27, y: itEnd.y - 27, width: 54, height: 54), radius: 27, fill: purple)
    centeredText("IT", center: itEnd, font: bold(20), color: .white)
}

func drawResolvedVector(in rect: NSRect) {
    drawVectorAxes(in: rect)
    let catCenter = NSPoint(x: rect.minX + 104, y: rect.minY + 70)
    let itCenter = NSPoint(x: catCenter.x + 82, y: catCenter.y + 20)
    let tiredCenter = NSPoint(x: rect.maxX - 52, y: rect.maxY - 52)

    roundedRect(
        NSRect(x: catCenter.x - 66, y: catCenter.y - 58, width: 174, height: 128),
        radius: 64,
        fill: teal.withAlphaComponent(0.10)
    )
    drawMeaningDot("CAT", center: catCenter, fill: teal)
    drawMeaningDot("IT", center: itCenter, fill: purple)
    drawMeaningDot("TIRED", center: tiredCenter, fill: orange, radius: 37)
    line(from: catCenter, to: itCenter, color: purple.withAlphaComponent(0.65), width: 3)
    drawText("closest", in: NSRect(x: catCenter.x + 24, y: catCenter.y - 39, width: 90, height: 30), font: demi(20), color: teal, alignment: .center)
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

func makeCanvas(title: String, subtitle: String?) -> NSImage {
    let image = NSImage(size: NSSize(width: width, height: height))
    image.lockFocusFlipped(true)
    lavender.setFill()
    NSRect(x: 0, y: 0, width: width, height: height).fill()

    if let subtitle {
        drawText(title, in: NSRect(x: 80, y: 40, width: 1440, height: 58), font: heavy(44), color: navy, alignment: .center)
        drawText(subtitle, in: NSRect(x: 80, y: 100, width: 1440, height: 38), font: medium(26), color: muted, alignment: .center)
    } else if title.contains("\n") {
        drawText(title, in: NSRect(x: 80, y: 31, width: 1440, height: 112), font: heavy(40), color: navy, alignment: .center, lineHeight: 48)
    } else {
        drawText(title, in: NSRect(x: 80, y: 57, width: 1440, height: 58), font: heavy(44), color: navy, alignment: .center)
    }
    roundedRect(NSRect(x: 80, y: 172, width: 1440, height: 564), radius: 16, fill: .white)
    return image
}

func renderThreeReads() throws {
    let image = makeCanvas(
        title: "“The horse raced past the barn fell.”",
        subtitle: nil
    )

    let markers = ["1", "…", "✓"]
    let titles = ["FIRST PASS", "MORE PASSES", "MEANING CLICKS"]
    let bodies = [
        "It doesn’t make sense.\nDid someone forget\na word?",
        "Wait, did a barn fall?\nDid the horse race past\nthe barn afterward?",
        "Got it. A horse ran past\na barn. After running past\nthe barn, the horse fell."
    ]

    let innerX: CGFloat = 112
    let innerWidth: CGFloat = 1376
    let gap: CGFloat = 24
    let cardWidth = (innerWidth - gap * 2) / 3

    for index in 0..<3 {
        let x = innerX + CGFloat(index) * (cardWidth + gap)
        roundedRect(NSRect(x: x, y: 204, width: cardWidth, height: 500), radius: 16, fill: rowFill, stroke: rule, lineWidth: 1.25)
        drawNumber(markers[index], center: NSPoint(x: x + cardWidth / 2, y: 246))
        drawText(titles[index], in: NSRect(x: x + 22, y: 288, width: cardWidth - 44, height: 42), font: bold(32), color: cardTitle, alignment: .center)
        drawText(bodies[index], in: NSRect(x: x + 28, y: 342, width: cardWidth - 56, height: 132), font: medium(30), color: bodyInk, alignment: .center, lineHeight: 38)
        drawThreeReadsPicture(cardIndex: index, rect: NSRect(x: x + 24, y: 510, width: cardWidth - 48, height: 162))
    }

    drawCheckBand("Each pass updates the meaning until it clicks.")
    try save(image, relativePaths: [
        "board-review-first-four/alternatives/understand-ai/layers-1-three-reads-alternative.jpg",
        "lessons/layers-1-three-reads.jpg",
        "illustrations/layers-three-reads.jpg"
    ])
}

func renderWhyDozens() throws {
    let image = makeCanvas(title: "Why are there dozens of layers?", subtitle: nil)
    let titles = ["A FEW PASSES", "DOZENS OF PASSES", "WHY NOT HUNDREDS?"]
    let bodies = [
        "Plain meaning settles early\nin only a handful of layers.",
        "Sarcasm, story twists, and\ncomplicated reasoning need\nmore depth.",
        "Past a point, extra depth\nadds cost without adding\nmuch meaning."
    ]

    let innerX: CGFloat = 112
    let innerWidth: CGFloat = 1376
    let gap: CGFloat = 24
    let cardWidth = (innerWidth - gap * 2) / 3

    for index in 0..<3 {
        let x = innerX + CGFloat(index) * (cardWidth + gap)
        roundedRect(NSRect(x: x, y: 204, width: cardWidth, height: 500), radius: 16, fill: rowFill, stroke: rule, lineWidth: 1.25)
        drawNumber("\(index + 1)", center: NSPoint(x: x + cardWidth / 2, y: 246))
        drawText(titles[index], in: NSRect(x: x + 22, y: 286, width: cardWidth - 44, height: 76), font: bold(32), color: cardTitle, alignment: .center, lineHeight: 37)
        drawText(bodies[index], in: NSRect(x: x + 28, y: 366, width: cardWidth - 56, height: 132), font: medium(30), color: bodyInk, alignment: .center, lineHeight: 38)

        if index == 0 {
            drawLayerStack(centerX: x + cardWidth / 2, bottomY: 665, count: 3, accent: teal)
        } else if index == 1 {
            drawLayerStack(centerX: x + cardWidth / 2, bottomY: 675, count: 8, accent: purple)
        } else {
            drawDiminishingReturns(rect: NSRect(x: x + 55, y: 500, width: cardWidth - 110, height: 170))
        }
    }

    drawCheckBand("More depth leaves room for deeper meaning.")
    try save(image, relativePaths: [
        "board-review-first-four/alternatives/understand-ai/layers-3-why-dozens-alternative.jpg",
        "lessons/layers-3-why-dozens.jpg",
        "illustrations/layers-why-dozens.jpg"
    ])
}

func renderLayerResolution() throws {
    let image = makeCanvas(
        title: "“The cat sat on the mat during the May rainstorm\nbecause it was tired.”",
        subtitle: nil
    )
    let titles = ["AMBIGUOUS “IT”", "THROUGH THE LAYERS", "LANDS NEAR “CAT”"]
    let bodies = [
        "At first, IT is only a pronoun.\nIts numbers do not identify\nCAT.",
        "Attention links IT to CAT\nand TIRED. Transformation\nshifts its vector.",
        "After many layers, IT’s final\nvector lands closest to CAT."
    ]

    let innerX: CGFloat = 112
    let innerWidth: CGFloat = 1376
    let columnWidth = innerWidth / 3

    for index in 0..<3 {
        let x = innerX + CGFloat(index) * columnWidth
        if index > 0 {
            line(from: NSPoint(x: x, y: 214), to: NSPoint(x: x, y: 700), color: rule, width: 2)
        }
        drawNumber("\(index + 1)", center: NSPoint(x: x + columnWidth / 2, y: 246))
        drawText(titles[index], in: NSRect(x: x + 22, y: 288, width: columnWidth - 44, height: 44), font: bold(32), color: cardTitle, alignment: .center)
        drawText(bodies[index], in: NSRect(x: x + 34, y: 346, width: columnWidth - 68, height: 122), font: medium(30), color: bodyInk, alignment: .center, lineHeight: 38)

        let graphicRect = NSRect(x: x + 58, y: 492, width: columnWidth - 116, height: 196)
        if index == 0 {
            drawAmbiguousVector(in: graphicRect)
        } else if index == 1 {
            drawLayerResolution(in: graphicRect)
        } else {
            drawResolvedVector(in: graphicRect)
        }
    }

    drawCheckBand("Each layer moves IT closer to what it means.")
    try save(image, relativePaths: [
        "board-review-first-four/alternatives/understand-ai/layers-3-resolves-it-alternative.jpg",
        "lessons/layers-3-resolves-it.jpg",
        "illustrations/layers-resolves-it.jpg"
    ])
}

if CommandLine.arguments.dropFirst().first == "resolution" {
    try renderLayerResolution()
} else {
    try renderThreeReads()
    try renderLayerResolution()
    try renderWhyDozens()
}
