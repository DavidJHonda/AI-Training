#!/usr/bin/env swift

import AppKit
import CoreText
import Foundation

let repoRoot = URL(fileURLWithPath: FileManager.default.currentDirectoryPath)
let outputPaths = [
    "board-review-first-four/alternatives/understand-ai/vector-space-city-closest-alternative.jpg",
    "illustrations/vector-space-cities.jpg",
    "lessons/vector-space-1-cities.jpg"
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

let lavender = color("#eeeaff")
let navy = color("#08072b")
let muted = color("#655f7c")
let purple = color("#6f52ff")
let teal = color("#14968f")
let blue = color("#3976d4")
let red = color("#e34a5f")
let gold = color("#ffe9ab")
let rule = color("#e3def2")
let pale = color("#f8f6ff")

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

func drawText(_ value: String, in rect: NSRect, font: NSFont, color: NSColor, alignment: NSTextAlignment = .left, lineHeight: CGFloat? = nil) {
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

func line(from start: NSPoint, to end: NSPoint, color: NSColor, width: CGFloat = 2, dash: [CGFloat] = []) {
    let path = NSBezierPath()
    path.move(to: start)
    path.line(to: end)
    path.lineWidth = width
    path.lineCapStyle = .round
    if !dash.isEmpty { path.setLineDash(dash, count: dash.count, phase: 0) }
    color.setStroke()
    path.stroke()
}

func drawArrow(from start: NSPoint, to end: NSPoint, color: NSColor) {
    line(from: start, to: end, color: color, width: 3)
    let angle = atan2(end.y - start.y, end.x - start.x)
    for offset in [CGFloat.pi * 0.82, -CGFloat.pi * 0.82] {
        let point = NSPoint(x: end.x + 11 * cos(angle + offset), y: end.y + 11 * sin(angle + offset))
        line(from: end, to: point, color: color, width: 3)
    }
}

let mapRect = NSRect(x: 116, y: 232, width: 850, height: 430)
func mapPoint(lon: CGFloat, lat: CGFloat) -> NSPoint {
    NSPoint(
        x: mapRect.minX + (lon + 127) / 63 * mapRect.width,
        y: mapRect.minY + (51 - lat) / 28 * mapRect.height
    )
}

let outline: [(CGFloat, CGFloat)] = [
    (-124.7,48.4),(-124.0,46.3),(-124.1,43.3),(-124.4,40.4),(-122.5,37.8),(-120.6,34.6),
    (-118.4,33.7),(-117.1,32.5),(-114.7,32.7),(-111.0,31.3),(-108.2,31.3),(-106.5,31.8),
    (-104.0,29.3),(-102.3,29.9),(-101.4,29.8),(-99.1,26.4),(-97.4,25.9),(-97.2,28.0),
    (-95.0,29.2),(-93.8,29.7),(-91.0,29.2),(-89.2,29.1),(-88.0,30.3),(-86.5,30.4),
    (-84.3,29.9),(-82.8,27.8),(-81.1,25.2),(-80.1,25.8),(-80.5,28.5),(-81.4,30.7),
    (-80.9,32.0),(-79.0,33.5),(-77.9,34.2),(-75.5,35.2),(-76.3,37.0),(-75.0,38.5),
    (-74.0,40.5),(-71.9,41.3),(-70.0,41.7),(-70.8,43.1),(-67.0,44.8),(-69.2,47.5),
    (-71.5,45.0),(-74.7,45.0),(-76.5,44.0),(-79.0,43.3),(-82.4,41.7),(-83.1,42.3),
    (-82.5,45.3),(-84.8,46.5),(-87.6,46.0),(-90.0,46.7),(-92.3,46.7),(-95.2,49.0),
    (-104.0,49.0),(-117.0,49.0),(-122.8,49.0)
]

func drawCity(name: String, coordinates: String, lon: CGFloat, lat: CGFloat, accent: NSColor, labelX: CGFloat, labelY: CGFloat, labelWidth: CGFloat) {
    let point = mapPoint(lon: lon, lat: lat)
    roundedRect(NSRect(x: point.x - 13, y: point.y - 13, width: 26, height: 26), radius: 13, fill: accent)
    roundedRect(NSRect(x: labelX, y: labelY, width: labelWidth, height: 70), radius: 12, fill: .white, stroke: accent, lineWidth: 2)
    drawText(name, in: NSRect(x: labelX + 12, y: labelY + 10, width: labelWidth - 24, height: 28), font: demi(23), color: navy, alignment: .center)
    drawText(coordinates, in: NSRect(x: labelX + 12, y: labelY + 39, width: labelWidth - 24, height: 24), font: demi(20), color: accent, alignment: .center)
}

func drawMatch(y: CGFloat, coordinates: String, answer: String, accent: NSColor) {
    roundedRect(NSRect(x: 1010, y: y, width: 446, height: 150), radius: 14, fill: pale, stroke: rule, lineWidth: 1.5)
    drawText(coordinates, in: NSRect(x: 1034, y: y + 18, width: 170, height: 42), font: demi(27), color: navy, alignment: .center)
    drawArrow(from: NSPoint(x: 1214, y: y + 49), to: NSPoint(x: 1260, y: y + 49), color: purple)
    drawText(answer, in: NSRect(x: 1272, y: y + 15, width: 162, height: 70), font: demi(25), color: accent, alignment: .center, lineHeight: 29)
    drawText("Closest known city", in: NSRect(x: 1034, y: y + 98, width: 398, height: 32), font: medium(23), color: muted, alignment: .center)
}

let image = NSImage(size: NSSize(width: width, height: height))
image.lockFocusFlipped(true)
lavender.setFill()
NSRect(x: 0, y: 0, width: width, height: height).fill()

drawText("No exact match? Find the closest point.", in: NSRect(x: 80, y: 57, width: 1440, height: 58), font: heavy(44), color: navy, alignment: .center)
roundedRect(NSRect(x: 80, y: 172, width: 1440, height: 564), radius: 16, fill: .white)
drawText("KNOWN COORDINATES", in: NSRect(x: 116, y: 196, width: 850, height: 32), font: demi(24), color: muted, alignment: .center)
drawText("NEW COORDINATES", in: NSRect(x: 1010, y: 196, width: 446, height: 32), font: demi(24), color: muted, alignment: .center)

let outlinePath = NSBezierPath()
for (index, pair) in outline.enumerated() {
    let point = mapPoint(lon: pair.0, lat: pair.1)
    index == 0 ? outlinePath.move(to: point) : outlinePath.line(to: point)
}
outlinePath.close()
color("#faf9ff").setFill()
outlinePath.fill()
color("#b7a9f7").setStroke()
outlinePath.lineWidth = 4
outlinePath.lineJoinStyle = .round
outlinePath.stroke()

let dallas = mapPoint(lon: -96.8, lat: 32.78)
line(from: NSPoint(x: mapRect.minX + 20, y: dallas.y), to: dallas, color: red.withAlphaComponent(0.65), width: 3, dash: [10, 10])
line(from: NSPoint(x: dallas.x, y: dallas.y), to: NSPoint(x: dallas.x, y: mapRect.maxY - 12), color: red.withAlphaComponent(0.65), width: 3, dash: [10, 10])

drawCity(name: "Mountain View, CA", coordinates: "37 N, 122 W", lon: -122.08, lat: 37.39, accent: teal, labelX: 168, labelY: 332, labelWidth: 244)
drawCity(name: "Dallas, Texas", coordinates: "33 N, 97 W", lon: -96.8, lat: 32.78, accent: red, labelX: 550, labelY: 420, labelWidth: 210)
drawCity(name: "New York City", coordinates: "41 N, 74 W", lon: -74.01, lat: 40.71, accent: blue, labelX: 714, labelY: 274, labelWidth: 210)

drawMatch(y: 268, coordinates: "38 N, 120 W", answer: "MOUNTAIN\nVIEW", accent: teal)
drawMatch(y: 452, coordinates: "39 N, 70 W", answer: "NEW YORK\nCITY", accent: blue)

roundedRect(NSRect(x: 80, y: 776, width: 1440, height: 84), radius: 16, fill: gold)
let takeaway = "When nothing matches exactly, distance finds the closest one."
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
    fputs("Could not encode city board.\n", stderr)
    exit(1)
}

for relativePath in outputPaths {
    let outputURL = repoRoot.appendingPathComponent(relativePath)
    try FileManager.default.createDirectory(at: outputURL.deletingLastPathComponent(), withIntermediateDirectories: true)
    try jpeg.write(to: outputURL)
    print("Built \(outputURL.path)")
}
