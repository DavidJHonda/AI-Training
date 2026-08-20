#!/usr/bin/env swift

import AppKit
import CoreText
import Foundation

let repoRoot = URL(fileURLWithPath: FileManager.default.currentDirectoryPath)
let firstBoard = CommandLine.arguments.contains("--first")
let outputPaths = firstBoard
    ? [
        "board-review-first-four/alternatives/understand-ai/embeddings-taste-profile-two-vector-alternative.jpg",
        "illustrations/embeddings-taste-two.jpg",
        "lessons/embeddings-1-taste-two.jpg"
    ]
    : [
        "board-review-first-four/alternatives/understand-ai/embeddings-taste-profile-vector-alternative.jpg",
        "board-review-first-four/alternatives/understand-ai/vector-space-taste-profile-alternative.jpg",
        "illustrations/embeddings-taste-three.jpg",
        "illustrations/vector-space-taste-profile.jpg",
        "lessons/embeddings-2-taste-three.jpg",
        "lessons/vector-space-2-taste.jpg"
    ]
let outputURLs = outputPaths.map { repoRoot.appendingPathComponent($0) }

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
let gold = color("#ffe9ab")
let paleGold = color("#fff8e4")
let panelLine = color("#e4e0f3")
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
    return NSFont.systemFont(ofSize: size, weight: .regular)
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

func centeredText(_ value: String, centerX: CGFloat, y: CGFloat, font: NSFont, color: NSColor, width: CGFloat = 220, height: CGFloat = 40) {
    drawText(value, in: NSRect(x: centerX - width / 2, y: y, width: width, height: height), font: font, color: color, alignment: .center)
}

struct Dimension {
    let name: String
    let color: NSColor
}

struct Drink {
    let name: String
    let tokenID: String
    let values: [Int]
    let color: NSColor
    let kind: Int
}

let dimensions = [
    Dimension(name: "SWEET", color: color("#c755d6")),
    Dimension(name: "BITTER", color: color("#15968f")),
    Dimension(name: "FIZZ", color: color("#4c78e5")),
    Dimension(name: "HEAT", color: color("#ef8739")),
    Dimension(name: "CAFFEINE", color: color("#7856db")),
    Dimension(name: "DARK", color: color("#3b4969")),
    Dimension(name: "CITRUS", color: color("#d99b00"))
]

let drinks = [
    Drink(name: "COKE", tokenID: "24317", values: [9, 1, 10, 2, 3, 8, 1], color: color("#e0434f"), kind: 0),
    Drink(name: "PEPSI", tokenID: "38106", values: [9, 1, 10, 2, 3, 8, 10], color: color("#3d6ed2"), kind: 1),
    Drink(name: "COFFEE", tokenID: "51820", values: [1, 9, 0, 9, 8, 10, 0], color: color("#9a623d"), kind: 2)
]

let boardDimensions = firstBoard ? Array(dimensions.prefix(6)) : dimensions
let boardDrinks = firstBoard ? [drinks[0], drinks[2]] : drinks

func drawDrinkIcon(_ drink: Drink, center: NSPoint) {
    let circleRect = NSRect(x: center.x - 26, y: center.y - 26, width: 52, height: 52)
    roundedRect(circleRect, radius: 26, fill: drink.color.withAlphaComponent(0.13))
    drink.color.setStroke()

    if drink.kind < 2 {
        let cup = NSBezierPath(roundedRect: NSRect(x: center.x - 10, y: center.y - 13, width: 20, height: 27), xRadius: 4, yRadius: 4)
        cup.lineWidth = 3
        cup.stroke()
        line(from: NSPoint(x: center.x + 4, y: center.y - 13), to: NSPoint(x: center.x + 12, y: center.y - 22), color: drink.color, width: 3)
        line(from: NSPoint(x: center.x - 7, y: center.y - 5), to: NSPoint(x: center.x + 7, y: center.y - 5), color: drink.color, width: 2)
    } else {
        let cup = NSBezierPath(roundedRect: NSRect(x: center.x - 13, y: center.y - 10, width: 24, height: 19), xRadius: 5, yRadius: 5)
        cup.lineWidth = 3
        cup.stroke()
        let handle = NSBezierPath(ovalIn: NSRect(x: center.x + 7, y: center.y - 6, width: 13, height: 12))
        handle.lineWidth = 3
        handle.stroke()
        line(from: NSPoint(x: center.x - 17, y: center.y + 14), to: NSPoint(x: center.x + 18, y: center.y + 14), color: drink.color, width: 3)
        line(from: NSPoint(x: center.x - 7, y: center.y - 19), to: NSPoint(x: center.x - 5, y: center.y - 25), color: drink.color, width: 2)
        line(from: NSPoint(x: center.x + 2, y: center.y - 19), to: NSPoint(x: center.x + 4, y: center.y - 25), color: drink.color, width: 2)
    }
}

let image = NSImage(size: NSSize(width: width, height: height))
image.lockFocusFlipped(true)

lavender.setFill()
NSRect(x: 0, y: 0, width: width, height: height).fill()

drawText(
    firstBoard
        ? "Meaning becomes an ordered row of numbers"
        : "One new dimension separates similar meanings",
    in: NSRect(x: 80, y: 57, width: 1440, height: 58),
    font: heavy(44),
    color: navy,
    alignment: .center
)

// Dense-board variant: omit the optional takeaway band and give its space to the
// teaching content. The 688 px panel is 124 px taller than the standard panel.
roundedRect(NSRect(x: 80, y: 172, width: 1440, height: 688), radius: 16, fill: .white)

let contentLeft: CGFloat = 112
let labelDividerX: CGFloat = 500
let dimensionStart: CGFloat = 520
let dimensionWidth: CGFloat = 960 / CGFloat(boardDimensions.count)
let dimensionCenters = (0..<boardDimensions.count).map { dimensionStart + dimensionWidth * (CGFloat($0) + 0.5) }
let citrusLeft = dimensionStart + dimensionWidth * 6

if !firstBoard {
    roundedRect(NSRect(x: citrusLeft + 5, y: 188, width: dimensionWidth - 10, height: 532), radius: 12, fill: paleGold, stroke: gold, lineWidth: 1.5)
}

drawText("TOKEN", in: NSRect(x: contentLeft + 62, y: 205, width: 250, height: 32), font: heavy(22), color: muted)
drawText("ID identifies the token", in: NSRect(x: contentLeft + 62, y: 238, width: 250, height: 28), font: medium(20), color: muted)
line(from: NSPoint(x: labelDividerX, y: 194), to: NSPoint(x: labelDividerX, y: 838), color: panelLine, width: 2)

for index in 0..<boardDimensions.count {
    if index == 6 { continue }
    // CAFFEINE is the longest heading. Keep the 28 pt readability floor, but
    // use the slightly narrower demi face so the final letter stays visible.
    let dimensionFont = dimensions[index].name == "CAFFEINE" ? demi(28) : heavy(28)
    centeredText(dimensions[index].name, centerX: dimensionCenters[index], y: 207, font: dimensionFont, color: dimensions[index].color, width: dimensionWidth, height: 36)
}
if !firstBoard {
    roundedRect(NSRect(x: dimensionCenters[6] - 45, y: 187, width: 90, height: 26), radius: 13, fill: gold)
    centeredText("NEW", centerX: dimensionCenters[6], y: 190, font: heavy(18), color: navy, width: 90, height: 23)
    centeredText(dimensions[6].name, centerX: dimensionCenters[6], y: 218, font: heavy(28), color: dimensions[6].color, width: dimensionWidth, height: 36)
}
drawText("0 = low    10 = high", in: NSRect(x: dimensionStart, y: 248, width: 960, height: 28), font: medium(20), color: muted, alignment: .center)

let rowYs: [CGFloat] = firstBoard ? [288, 552] : [278, 466, 654]
let rowHeight: CGFloat = firstBoard ? 236 : 176
let sliderOffset: CGFloat = firstBoard ? 87 : 68
let valueOffset: CGFloat = firstBoard ? 119 : 98

for (rowIndex, drink) in boardDrinks.enumerated() {
    let y = rowYs[rowIndex]
    roundedRect(NSRect(x: contentLeft, y: y, width: 1376, height: rowHeight), radius: 14, fill: rowFill, stroke: panelLine, lineWidth: 1.25)

    // Treat the icon, drink name, and token ID as one 80 px identity block and
    // center that complete block vertically within the drink row.
    let identityTop = y + (rowHeight - 80) / 2
    drawDrinkIcon(drink, center: NSPoint(x: 150, y: identityTop + 38))
    drawText(drink.name, in: NSRect(x: 186, y: identityTop, width: 220, height: 42), font: heavy(30), color: navy)
    drawText("TOKEN ID  \(drink.tokenID)", in: NSRect(x: 186, y: identityTop + 46, width: 250, height: 32), font: medium(21), color: muted)

    for dimensionIndex in 0..<boardDimensions.count {
        let centerX = dimensionCenters[dimensionIndex]
        let sliderY = y + sliderOffset
        let sliderStart = centerX - 50
        let sliderEnd = centerX + 50
        let activeEnd = sliderStart + 100 * CGFloat(drink.values[dimensionIndex]) / 10

        line(from: NSPoint(x: sliderStart, y: sliderY), to: NSPoint(x: sliderEnd, y: sliderY), color: color("#ddd9ea"), width: 7)
        line(from: NSPoint(x: sliderStart, y: sliderY), to: NSPoint(x: activeEnd, y: sliderY), color: dimensions[dimensionIndex].color, width: 7)
        roundedRect(NSRect(x: activeEnd - 8, y: sliderY - 8, width: 16, height: 16), radius: 8, fill: dimensions[dimensionIndex].color)

        let valueText = "\(drink.values[dimensionIndex])"
        let pillWidth: CGFloat = valueText.count == 2 ? 60 : 50
        roundedRect(NSRect(x: centerX - pillWidth / 2, y: y + valueOffset, width: pillWidth, height: 48), radius: 14, fill: dimensions[dimensionIndex].color.withAlphaComponent(0.12))
        centeredText(valueText, centerX: centerX, y: y + valueOffset + 3, font: demi(36), color: dimensions[dimensionIndex].color, width: pillWidth, height: 43)
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
    try FileManager.default.createDirectory(at: outputURL.deletingLastPathComponent(), withIntermediateDirectories: true)
    try jpeg.write(to: outputURL)
    print("Built \(outputURL.path)")
}
